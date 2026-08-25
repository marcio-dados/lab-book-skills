# Padrões e Técnicas — Machine Learning: Guia de Referência Rápida

## Pipeline canônico de classificação/regressão
**Quando usar**: qualquer projeto supervisionado, do zero.
**Como**: coletar → limpar (remover vazamento) → criar atributos → **split treino/teste** → imputar/normalizar (fit só no treino) → baseline (`Dummy*`) → comparar famílias via k-fold → treinar → avaliar → otimizar (`GridSearchCV`) → implantar (`pickle`).
**Trade-offs**: pular o baseline economiza tempo mas impede saber se o modelo "bom" é realmente bom ou só reflexo do desbalanceamento; pular a comparação de famílias otimiza cedo demais em um modelo que pode não ser o melhor para o dataset.

## Fit só no treino, transform nos dois
**Quando usar**: toda vez que uma estatística é calculada a partir dos dados (imputação, escala, encoder de frequência/bayesiano, PCA) antes de treinar.
**Como**: `transformador.fit(X_train)` (ou `fit_transform`) seguido de `transformador.transform(X_test)` — nunca `fit`/`fit_transform` no teste.
**Trade-offs**: nenhum — é sempre a via correta; a única "vantagem" de pular esse cuidado é conveniência de código, ao custo de vazamento de informação e métricas infladas artificialmente.

## Detecção de vazamento de informação (leaky features)
**Quando usar**: antes de treinar qualquer modelo, ao revisar cada coluna do dataset.
**Como**: perguntar "esse atributo estaria disponível no momento real da predição?" para cada coluna; remover as que não estariam (ex. `boat`/`body` no Titanic entregam a sobrevivência).
**Trade-offs**: nenhum — manter um atributo vazado sempre infla a métrica de forma enganosa e inútil em produção.

## Baseline antes de qualquer modelo real
**Quando usar**: sempre, antes de confiar em qualquer métrica de um modelo treinado.
**Como**: `DummyClassifier`/`DummyRegressor` treinado nos mesmos dados; comparar a métrica do modelo real contra esse piso.
**Trade-offs**: custo desprezível (treino instantâneo); pular esse passo é a causa mais comum de conclusões erradas sob classes desbalanceadas.

## Comparação de famílias via k-fold antes de otimizar
**Quando usar**: fase de seleção de modelo, antes de investir em `GridSearchCV`.
**Como**: laço sobre uma lista de classes de modelo + `cross_val_score(cls, X, y, scoring=..., cv=kfold)`, comparando média e desvio-padrão da métrica.
**Trade-offs**: mais caro que treinar um único modelo, mas evita otimizar hiperparâmetros da família errada (teorema "No Free Lunch": nenhum algoritmo vence em todo dataset).

## Reamostragem para classes desbalanceadas
**Quando usar**: quando ajustar métrica/`class_weight` não é suficiente para lidar com desbalanceamento severo.
**Como**: upsampling da minoria (`resample(replace=True)` ou `RandomOverSampler`), downsampling da maioria (`resample(replace=False)`), ou geração sintética (`SMOTE`/`ADASYN`) — sempre só no conjunto de treino.
**Trade-offs**: upsampling com repetição arrisca overfitting; downsampling descarta dado real; SMOTE/ADASYN geram dados plausíveis mas não reais — escolher conforme quanto dado se pode perder/arriscar.

## Seleção de atributos combinando múltiplos métodos
**Quando usar**: reduzir dimensionalidade sem perder atributos relevantes.
**Como**: combinar correlação/dependência via floresta (colinearidade entre atributos) com RFE/informação mútua/`feature_importances_` (relevância em relação ao alvo).
**Trade-offs**: nenhum método sozinho é suficiente — correlação de Pearson só captura relações lineares; `feature_importances_` bruto pode enganar sob colinearidade.

## Checklist de quatro perguntas por família de modelo
**Quando usar**: ao adotar qualquer modelo novo (classificação ou regressão).
**Como**: perguntar eficiência (custo de treino/predição), pré-processamento exigido (escala? categóricas?), controle de superadequação (quais hiperparâmetros regularizam), e interpretação (coeficientes? importância? vetores suporte?).
**Trade-offs**: adiciona um passo de análise antes de codificar, mas evita erros comuns (ex. esquecer de padronizar antes de SVM/KNN).

## Escolha de métrica pelo custo relativo do erro
**Quando usar**: antes de escolher `scoring=` em qualquer busca/validação.
**Como**: nomear explicitamente o custo de um falso-positivo vs. falso-negativo (classificação) ou o tipo de penalidade desejada — linear/quadrática/assimétrica (regressão) — antes de escolher entre accuracy/precisão/recall/F1/AUC ou MAE/MSE/MSLE.
**Trade-offs**: métrica errada otimiza o modelo para o objetivo errado, mesmo com pipeline tecnicamente correto.

## Explicação em camadas (nativa → local → global agregado)
**Quando usar**: para justificar comportamento de um modelo, seja para debug ou para stakeholder.
**Como**: começar com explicação nativa (coeficientes/`feature_importances_`); se o modelo for opaco, usar modelo substituto ou LIME/SHAP local para uma amostra específica; usar SHAP `summary_plot`/PDP para visão global.
**Trade-offs**: técnicas nativas são gratuitas mas só existem para modelos simples; SHAP/LIME custam mais computação mas funcionam em qualquer modelo.

## Pipeline scikit-learn para eliminar duplicação treino/produção
**Quando usar**: sempre que a limpeza/pré-processamento precisa ser idêntica em treino e produção.
**Como**: encapsular limpeza customizada em `BaseEstimator`+`TransformerMixin`; encadear em `Pipeline` junto com imputação/escala/modelo; usar `GridSearchCV` com namespace `<etapa>__<parametro>`.
**Trade-offs**: mais boilerplate inicial (criar a classe transformadora), mas elimina risco de divergência entre código de treino e de produção.

## Decidir número de clusters por múltiplas métricas
**Quando usar**: K-means ou clustering hierárquico sem número de clusters conhecido a priori.
**Como**: rodar para uma faixa de k, plotar inércia (cotovelo) + silhueta + Calinski-Harabasz + Davies-Bouldin juntos; escolher onde a maioria concorda.
**Trade-offs**: mais caro que confiar só na inércia, mas evita escolher k por um cotovelo ambíguo/inexistente.

## Explicar cluster via agregação e modelo substituto
**Quando usar**: depois de qualquer clustering, antes de comunicar os grupos encontrados.
**Como**: `X.assign(cluster=labels).groupby("cluster").agg(["mean","var"])` + treinar árvore de decisão para prever o rótulo de cluster e inspecionar `feature_importances_`.
**Trade-offs**: nenhum — um cluster sem essa tradução de volta aos atributos originais não é acionável.
</content>
