# Capítulo 14: Regressão

## Core Idea
Regressão reusa a mesma API e (em grande parte) os mesmos modelos da classificação (SVM, KNN, árvore, floresta, XGBoost, LightGBM) para prever um valor contínuo em vez de um rótulo — a diferença central está nas métricas de avaliação (R², erro quadrático) e em cuidados específicos de regressão linear (heterocedasticidade, multicolinearidade).

## Frameworks Introduced
- **Mesma família de modelos, API idêntica, alvo contínuo**: trocar `Classifier` por `Regressor` na mesma classe (`DecisionTreeRegressor`, `RandomForestRegressor`, `XGBRegressor`, `LGBMRegressor`, `KNeighborsRegressor`, `SVR`) preserva `.fit`/`.score`/`.predict`; `.score` passa a devolver R² em vez de accuracy.
  - Quando usar: sempre que migrar um pipeline de classificação para um problema de valor contínuo — a estrutura do código muda pouco.
- **R² como baseline universal de regressão**: mede a fração da variância do alvo explicada pelo modelo (1 = perfeito, pode ser negativo se pior que prever a média); `DummyRegressor` (prevê a média do treino) é o baseline mínimo, equivalente ao `DummyClassifier` do Capítulo 3.

## Key Concepts
- **Regressão linear**: ajusta `y = mx + b` generalizado para múltiplas dimensões, minimizando soma dos quadrados dos erros; `.coef_` — sinal indica direção, magnitude (após padronização) indica força relativa; `.intercept_` é o valor médio esperado quando os atributos padronizados são zero.
- **Heterocedasticidade**: quando o erro/resíduo varia sistematicamente com o valor de entrada (gráfico de resíduos em forma de leque/cone) — sintoma de que o modelo linear pode não ser adequado sem transformação.
- **Multicolinearidade em regressão linear**: não prejudica necessariamente a predição, mas compromete a interpretação dos coeficientes — mesmo cuidado do Capítulo 6/8.
- **`PolynomialFeatures`**: adiciona flexibilidade a um modelo linear via combinações polinomiais dos atributos; se causar superadequação, regularizar com ridge/lasso.
- **SVR**: versão de regressão da SVM; `epsilon` define uma margem de tolerância sem penalidade — `epsilon=0` tende a superadequar.
- **KNN regressor**: prediz a média dos alvos dos k vizinhos mais próximos (em vez de votação por classe).
- **Árvore/floresta/XGBoost/LightGBM de regressão**: mesmos hiperparâmetros e mesma lógica de controle de superadequação do capítulo de classificação (`max_depth`, `n_estimators`, `reg_alpha`/`reg_lambda`, `num_leaves`), só muda o critério de impureza (`criterion='mse'`/`'mae'` em vez de gini/entropy) e a interpretação de `objective` (`'reg:linear'` no XGBoost).

## Mental Models
- Pense em regressão e classificação como a mesma máquina (mesmos modelos, mesma API) com uma peça trocada: a função de perda/impureza (gini/entropy → MSE/MAE) e a métrica de avaliação (accuracy/AUC → R²/erro quadrático).
- Coeficientes de regressão linear só são diretamente comparáveis entre si depois de padronizar os atributos — sem padronização, a magnitude reflete a escala da unidade, não a importância real.

## Anti-patterns
- **Comparar coeficientes de regressão linear não padronizados para julgar importância relativa**: a escala de cada atributo distorce a magnitude do coeficiente; padronizar antes de comparar.
- **Ignorar heterocedasticidade**: um padrão em leque no gráfico de resíduos invalida a suposição de erro homogêneo do modelo linear — considerar transformação do alvo ou modelo não linear.

## Code Examples
```python
# baseline de regressão (equivalente ao DummyClassifier)
from sklearn.dummy import DummyRegressor
dr = DummyRegressor()
dr.fit(bos_X_train, bos_y_train)
dr.score(bos_X_test, bos_y_test)  # pode ser negativo

# regressão linear com coeficientes interpretáveis (dados padronizados)
from sklearn.linear_model import LinearRegression
lr2 = LinearRegression()
lr2.fit(bos_sX_train, bos_sy_train)
lr2.coef_        # comparável entre atributos porque X foi padronizado
lr2.intercept_   # valor médio esperado

# mesma API para qualquer família de regressão
from sklearn.ensemble import RandomForestRegressor
rfr = RandomForestRegressor(random_state=42, n_estimators=100)
rfr.fit(bos_X_train, bos_y_train)
rfr.score(bos_X_test, bos_y_test)  # R²
```
- **O que demonstra**: o mesmo padrão baseline→modelo→score do Capítulo 3, agora com R² no lugar de accuracy, e a importância de padronizar antes de comparar coeficientes.

## Reference Tables
| Modelo | Critério de impureza/perda | Hiperparâmetro-chave de regularização |
|---|---|---|
| Regressão linear | soma dos quadrados dos erros | nenhum nativo (usar ridge/lasso) |
| SVR | margem `epsilon` | `C`, `epsilon`, `gamma` |
| KNN regressor | média dos k vizinhos | `n_neighbors`, `p` (L1/L2) |
| Árvore de regressão | MSE (ou MAE/friedman_mse) | `max_depth`, `min_impurity_decrease` |
| Floresta de regressão | MSE por árvore, média do ensemble | `n_estimators`, `max_depth` |
| XGBoost regressor | `reg:linear`/`reg:squarederror` | `early_stopping_rounds`, `reg_alpha`/`reg_lambda` |
| LightGBM regressor | MSE por folha (leaf-wise) | `num_leaves`, `min_data_in_leaf` |

## Key Takeaways
1. Regressão reaproveita quase toda a infraestrutura de modelos e código da classificação — troque a classe (`*Regressor`) e a métrica (R² em vez de accuracy).
2. `DummyRegressor` (prevê a média) é o baseline mínimo, assim como `DummyClassifier` na classificação.
3. Coeficientes de regressão linear só são comparáveis entre atributos depois de padronizar os dados.
4. Heterocedasticidade e multicolinearidade são as duas armadilhas específicas de interpretação da regressão linear (ver Capítulo 15 para diagnóstico visual).
5. Todos os modelos baseados em árvore/boosting mantêm os mesmos hiperparâmetros de controle de superadequação já vistos na classificação.

## Connects To
- **Ch 10**: par direto — mesmos modelos, agora para alvo contínuo.
- **Ch 6/8**: multicolinearidade e seleção de atributos aplicam-se igualmente aqui.
- **Ch 13**: SHAP e demais técnicas de explicação funcionam também para regressão.
- **Ch 15**: métricas de avaliação de regressão (R², MSE, MAE) e diagnóstico visual de heterocedasticidade.
- **Ch 16**: explicação de modelos de regressão via SHAP.
</content>
