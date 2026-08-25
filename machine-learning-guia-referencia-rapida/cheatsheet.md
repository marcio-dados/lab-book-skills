# Cheatsheet — Machine Learning: Guia de Referência Rápida

## Decisões rápidas

- **Classificação ou regressão?** Alvo é categoria/rótulo → classificação. Alvo é valor contínuo → regressão. Mesma API do sklearn (`.fit`/`.score`/`.predict`) nos dois casos.
- **Qual encoder categórico usar?** Baixa cardinalidade sem ordem → `get_dummies(drop_first=True)`. Alta cardinalidade + modelo de árvore → `LabelEncoder`. Ordem real conhecida → `OrdinalEncoder` com mapeamento explícito. Vocabulário desconhecido/streaming → `HashingEncoder`. Alta cardinalidade nominal, quer 1 coluna → encoder bayesiano (`TargetEncoder` etc.).
- **Accuracy é suficiente?** Só se as classes forem balanceadas. Caso contrário, usar precisão/recall/F1/AUC e sempre comparar contra `DummyClassifier`.
- **ROC ou precisão-recall?** Classes balanceadas → ROC/AUC. Classes desbalanceadas → curva de precisão-recall (ROC fica otimista demais).
- **Qual métrica de erro de regressão?** Robusto a outliers → MAE. Penalizar erros grandes mais que proporcionalmente → MSE/RMSE. Alvo com crescimento exponencial → MSLE.
- **Bagging ou boosting?** Reduzir variância (modelo já não enviesado, mas instável) → bagging (floresta aleatória). Reduzir bias (modelo simples demais) → boosting (XGBoost/LightGBM).
- **PCA, t-SNE, UMAP ou PHATE?** Quer estrutura global/linear interpretável → PCA. Só clusters locais, sem se importar com distância entre eles → t-SNE. Quer os dois, mais rápido → UMAP. Quer os dois, via difusão → PHATE.
- **K-means ou clustering hierárquico?** Sabe (ou pode estimar) o número de clusters de antemão e quer eficiência → K-means. Quer explorar visualmente quantos clusters fazem sentido (dendrograma) → hierárquico.
- **Explicação nativa, LIME/SHAP ou modelo substituto?** Modelo linear/árvore → nativa (`coef_`/`feature_importances_`). Modelo caixa-preta, quer explicação de uma amostra específica → LIME/SHAP local. Quer explicação global de modelo caixa-preta → SHAP `summary_plot` ou modelo substituto.
- **Upsampling, downsampling ou SMOTE?** Pode perder dado real sem prejuízo → downsampling. Não quer perder dado, aceita repetição → upsampling. Quer dado sintético plausível → SMOTE/ADASYN.

## Limiares e defaults a lembrar

| Situação | Regra prática |
|---|---|
| Split treino/teste | `train_test_split(..., stratify=y)` sempre que as classes forem desbalanceadas |
| Imputação/escala/encoder | `fit` só no treino, `transform` nos dois — nunca `fit_transform` no teste |
| `GridSearchCV` sobre pipeline | Prefixar parâmetro com `<nome_da_etapa>__` |
| Árvore/floresta sem `max_depth` | Tende a superadequar — sempre validar profundidade por validação cruzada |
| SVM/KNN sem padronização | Atributos de escala maior dominam artificialmente — sempre padronizar antes |
| Limiar de decisão em classificação | Padrão 50%, mas ajustável via `DiscriminationThreshold` conforme custo de FP/FN |
| `feature_importances_` sob colinearidade | Prefira importância por permutação (`rfpimp.importances`) |
| TPOT | Reservar para quando a busca manual já não é suficiente — é caro (horas/dias) |

## Tabela de decisão: métricas de classificação

| Pergunta | Métrica |
|---|---|
| % de acerto geral (só se balanceado) | `accuracy` |
| De todos os positivos reais, quantos achei? | `recall` |
| Das predições positivas, quantas estavam certas? | `precision` |
| Resumo do trade-off precisão/recall | `f1` |
| Ranking de qualidade em todos os limiares | `roc_auc` |
| Observando os X% melhores, que fração de positivos capturo? | ganhos cumulativos / lift |

## Tabela de decisão: hiperparâmetros de superadequação

| Modelo | Hiperparâmetro principal | Direção que reduz overfitting |
|---|---|---|
| Regressão logística/linear | `C` / regularização | ↓ `C` (mais regularização) |
| SVM | `C`, `gamma` | ↓ ambos |
| KNN | `n_neighbors` | ↑ |
| Árvore de decisão | `max_depth`, `min_impurity_decrease` | ↓ profundidade, ↑ impureza mínima |
| Floresta aleatória | `n_estimators`, `max_depth` | ↑ árvores, ↓ profundidade |
| XGBoost | `reg_alpha`/`reg_lambda`, `early_stopping_rounds` | ↑ regularização, ativar early stopping |
| LightGBM | `num_leaves`, `min_data_in_leaf` | ↓ folhas, ↑ amostras mínimas |

## Tells / cheiros de problema

- Accuracy alta (>95%) sem checar `DummyClassifier` → suspeitar de classes desbalanceadas mascarando o resultado.
- R² alto mas erro absoluto (MAE) ainda grande na unidade real → contextualizar sempre com o custo de negócio do erro.
- Coeficientes de regressão linear com sinais/magnitudes estranhos → checar multicolinearidade (`correlated_columns`) antes de confiar na interpretação.
- Duas colunas de `get_dummies` com correlação -1 (ex. `sex_male`/`sex_female`) → usar `drop_first=True` ou remover uma manualmente.
- `feature_importances_` dominado por uma única coluna de forma suspeita → checar vazamento de informação (leaky feature) antes de comemorar.
- Gráfico de resíduos em forma de leque/cone → heterocedasticidade; considerar transformação do alvo ou modelo não linear.
- Distância grande entre dois clusters em gráfico t-SNE sendo usada como argumento de dissimilaridade → t-SNE não preserva estrutura global, essa leitura é inválida.
- `GridSearchCV` não encontra o hiperparâmetro esperado dentro de um `Pipeline` → falta o prefixo `<etapa>__` no nome do parâmetro.
</content>
