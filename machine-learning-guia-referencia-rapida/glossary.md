# Glossário — Machine Learning: Guia de Referência Rápida

**ADASYN** — variante de SMOTE que gera mais amostras sintéticas da minoria nas regiões mais difíceis de aprender (Ch 9).

**Atributo (feature)** — cada coluna de `X`; representa uma característica de uma amostra (Ch 3).

**AUC (Area Under Curve)** — área sob a curva ROC; resume o desempenho de um classificador em um único número entre 0 e 1 (Ch 3, Ch 12).

**Bagging** — combinar vários modelos treinados em subamostras independentes (bootstrap) dos dados para reduzir variância; base das florestas aleatórias (Ch 10).

**Biplot (gráfico duplo)** — scatter de componentes de PCA sobreposto com setas de carga dos atributos originais (Ch 17).

**Bootstrap (amostragem)** — amostragem com reposição usada para gerar subconjuntos de treino independentes (bagging) (Ch 10).

**Classes desbalanceadas** — quando uma classe domina o dataset, tornando accuracy uma métrica enganosa (Ch 9).

**Class_weight='balanced'** — parâmetro de vários modelos do sklearn que pondera o erro pela frequência inversa da classe (Ch 9, Ch 10).

**Coeficiente de determinação (R²)** — métrica padrão de regressão; fração da variância do alvo explicada pelo modelo (Ch 14, Ch 15).

**Colinearidade / multicolinearidade** — alta correlação entre atributos; não prejudica necessariamente a predição, mas compromete a interpretação de coeficientes/importância (Ch 6, Ch 8, Ch 14).

**`col_na`** — padrão de preservar uma coluna booleana indicando ausência, mesmo depois de imputar o valor (Ch 4, Ch 7).

**Curse of dimensionality (maldição da dimensionalidade)** — em altas dimensões, os dados ficam esparsos e métricas de distância perdem significado (Ch 8, Ch 10).

**Curva de aprendizagem (learning curve)** — pontuação de treino/validação em função do tamanho da amostra; diagnostica se mais dados ajudariam (Ch 3, Ch 11).

**Curva de precisão-recall** — alternativa à curva ROC, mais informativa sob classes desbalanceadas (Ch 12).

**Curva de validação (validation curve)** — pontuação de treino/validação em função de um hiperparâmetro (Ch 11).

**Curva ROC** — taxa de verdadeiro positivo vs. falso-positivo variando o limiar de decisão (Ch 3, Ch 12).

**Dendrograma** — árvore que registra a que distância cada fusão ocorreu no clustering hierárquico aglomerativo (Ch 18).

**Discrimination threshold (limiar de discriminação)** — valor de corte (padrão 50%) acima do qual `predict_proba` vira predição positiva; ajustável para trocar precisão por recall (Ch 12).

**DummyClassifier / DummyRegressor** — modelo de base ingênuo (ex. prever a classe majoritária ou a média); baseline mínimo antes de confiar em qualquer métrica (Ch 3, Ch 14).

**Downsampling** — reduzir a classe majoritária (sem reposição) para balancear classes (Ch 9).

**Elimin. Recursiva de Atributos (RFE/RFECV)** — remove iterativamente os atributos mais fracos e refaz o treino (Ch 8).

**Encoder bayesiano** (`TargetEncoder`, `WOEEncoder`, etc.) — codifica categoria de alta cardinalidade em uma única coluna combinando probabilidade posterior do alvo com a priori (Ch 7).

**Ensemble** — combinação de vários modelos-base (bagging, boosting, stacking) para melhorar generalização (Ch 3, Ch 10).

**Explicação global vs. local** — global explica o modelo como um todo (coeficientes, importância); local explica uma predição individual (LIME, SHAP, treeinterpreter) (Ch 13).

**Gradient boosting** — treina árvores sequenciais, cada uma corrigindo o erro residual da anterior (XGBoost, LightGBM) (Ch 10, Ch 14).

**Heterocedasticidade** — variância do erro/resíduo que muda sistematicamente com o valor previsto; testável via Breusch-Pagan (Ch 14, Ch 15).

**Homocedasticidade** — suposição de variância constante dos resíduos, exigida pelo modelo de regressão linear clássico (Ch 15).

**Imputação indutiva vs. transdutiva** — indutiva aceita `fit` no treino e `transform` em dados novos; transdutiva só funciona no dataset com que foi ajustada (Ch 4).

**Informação mútua** — mede, via k-vizinhos, quanta informação um atributo fornece sobre o alvo, sem assumir relação linear (Ch 8).

**K-fold (validação cruzada)** — dividir os dados em k partes, treinar/testar k vezes, usado para comparar famílias de modelo de forma robusta (Ch 3, Ch 11).

**K-means** — algoritmo de clustering que escolhe k centroides e itera atribuição/recálculo até convergência (Ch 18).

**KNN (K-Nearest Neighbors)** — aprendizado baseado em instâncias; classifica/regride pela distância aos k vizinhos mais próximos (Ch 10, Ch 14).

**LIME** — explica uma predição individual perturbando a amostra e ajustando um modelo linear local (Ch 13).

**Modelo substituto (surrogate model)** — árvore de decisão treinada para prever as saídas de um modelo opaco (SVM, rede neural) ou o rótulo de um cluster, tornando-o interpretável (Ch 13, Ch 18).

**Naive Bayes** — classificador probabilístico que assume independência entre atributos (Ch 10).

**No Free Lunch (teorema)** — nenhum algoritmo é o melhor em todo dataset; sempre comparar famílias de modelo empiricamente (Ch 3, Ch 10).

**Overfitting/superadequação** — modelo ajusta ruído do treino em vez do padrão real, generalizando mal para dados novos (todos os capítulos de modelo).

**PCA (Principal Component Analysis)** — projeta atributos em componentes ortogonais ordenados por variância decrescente; preserva estrutura global, assume linearidade (Ch 8, Ch 17).

**PHATE** — técnica de redução de dimensionalidade via difusão que equilibra estrutura global e local (Ch 17).

**Pipeline (sklearn)** — encadeia transformadores e um estimador final em um único objeto com `.fit`/`.score`/`.predict` (Ch 19).

**Precisão (precision)** — `TP/(TP+FP)`; proporção de predições positivas corretas (Ch 12).

**Recall (revocação/sensibilidade)** — `TP/(TP+FN)`; proporção de positivos reais identificados (Ch 12).

**Reamostragem (resampling)** — upsampling, downsampling ou geração sintética (SMOTE/ADASYN) para balancear classes (Ch 9).

**RFE** — ver Eliminação Recursiva de Atributos.

**SHAP (SHapley Additive exPlanations)** — atribui contribuição aditiva de cada atributo, do valor de base até a predição, model-agnóstico (Ch 13, Ch 16).

**Silhueta (coeficiente de)** — mede separação/coesão de cada amostra em relação ao seu cluster (-1 a 1, maior é melhor) (Ch 18).

**SMOTE** — gera amostras sintéticas da minoria interpolando entre vizinhos mais próximos (Ch 9).

**Stacking** — combina saídas de vários modelos-base como entrada de um meta-classificador (Ch 3).

**t-SNE** — técnica de redução de dimensionalidade que preserva estrutura local, mas distorce distância entre clusters distantes (Ch 17).

**TPOT** — busca automatizada de pipeline (algoritmo genético) sobre modelos, pré-processamento e hiperparâmetros (Ch 10).

**Treeinterpreter** — decompõe a predição de um modelo de árvore em bias (média do treino) + contribuição de cada atributo (Ch 13).

**UMAP** — técnica de redução de dimensionalidade (manifold learning) que preserva estrutura global e local melhor que t-SNE (Ch 17).

**Vazamento de informação (leaky features)** — atributo que carrega informação do futuro/do próprio alvo, inflando artificialmente a métrica (Ch 3, Ch 8).

**X / y** — convenção universal: `X` é a matriz de atributos, `y` é o vetor de rótulos/alvo (Ch 3).
</content>
