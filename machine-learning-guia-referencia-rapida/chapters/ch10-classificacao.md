# Capítulo 10: Classificação

## Core Idea
Todo modelo de classificação do scikit-learn (e os compatíveis, como XGBoost/LightGBM/TPOT) compartilha a mesma interface (`.fit`, `.predict`, `.predict_proba`, `.score`) e pode ser avaliado pelas mesmas quatro perguntas — eficiência de execução, exigências de pré-processamento, como evitar superadequação, e como interpretar o resultado — o que torna trivial trocar de família de modelo sem reescrever o pipeline.

## Frameworks Introduced
- **As quatro perguntas por modelo**: eficiência (complexidade de treino/predição), pré-processamento exigido (escala? colinearidade? categóricas?), controle de superadequação (quais hiperparâmetros regularizam) e interpretabilidade (coeficientes? importância? vetores suporte?) — usar essa lista como checklist ao adotar qualquer modelo novo.
  - Como usar: ver Reference Tables abaixo, uma linha por modelo.
- **Interface uniforme do scikit-learn**: `modelo.fit(X_train, y_train)` → `.score(X_test, y_test)` → `.predict`/`.predict_proba`/`.predict_log_proba` — o mesmo padrão funciona para regressão logística, árvore, SVM, KNN, Naive Bayes, floresta, XGBoost, LightGBM e TPOT, permitindo testar famílias por substituição direta (ver o laço do Capítulo 3).

## Key Concepts
- **Regressão logística**: apesar do nome, é classificação; estima probabilidade via função logística. `.coef_` dá log-odds por atributo — aplicar `inv_logit` no coeficiente devolve a proporção associada; `.intercept_` é o log-odds da condição de base.
- **Naive Bayes** (`GaussianNB`/`MultinomialNB`/`BernoulliNB`): assume independência entre atributos; treina com poucos dados, mas não captura interações; sofre do "problema da probabilidade zero" (mitigado por suavização de Laplace, `alpha`).
- **SVM (`SVC`)**: maximiza a margem entre classes via hiperplano; kernel `'rbf'` (padrão) usa o "truque de kernel" para fronteiras não lineares sem mapear explicitamente para mais dimensões; exige padronização; `probability=True` deixa o treino mais lento.
- **KNN**: aprendizado baseado em instâncias (sem parâmetros aprendidos); `n_neighbors` (k) é o hiperparâmetro central; sofre da maldição da dimensionalidade (distâncias perdem significado com muitos atributos); `weights='distance'` favorece vizinhos mais próximos.
- **Árvore de decisão (CART)**: usa impureza de Gini (ou entropia) para escolher separações; não exige escala; interpretável ao percorrer os nós, mas instável (pequena mudança nos dados muda a árvore inteira); `max_depth` controla superadequação.
- **Floresta aleatória**: bagging de árvores (cada uma treinada em subamostra de linhas/colunas) — a lógica do "júri de Condorcet" (cada membro com >50% de acerto, independente, melhora o resultado agregado ao somar votos). Permite estimativa OOB (out-of-bag) sem conjunto de validação separado.
- **XGBoost**: gradient boosting — cada árvore nova corrige o erro residual da anterior; `early_stopping_rounds` + `eval_set` param o treino quando a métrica para de melhorar; `reg_alpha`/`reg_lambda` regularizam (L1/L2); importância pode ser por `weight`, `gain` ou `cover`.
- **LightGBM**: gradient boosting por folha (leaf-wise), não por nível — mais rápido e mais econômico em memória que XGBoost, mas controla superadequação por `num_leaves` (não `max_depth`).
- **TPOT**: busca automatizada (algoritmo genético) de pipeline completo (pré-processamento + modelo + hiperparâmetros); caro em tempo (horas/dias), mas exporta código Python pronto (`.export`) do melhor pipeline achado.

## Mental Models
- Pense em floresta aleatória e gradient boosting (XGBoost/LightGBM) como duas estratégias opostas de combinar árvores fracas: bagging reduz variância treinando árvores independentes em paralelo (o júri de Condorcet); boosting reduz bias treinando árvores sequenciais que corrigem o erro da anterior.
- A importância de atributos "ingênua" (`feature_importances_`) pode enganar quando há colinearidade ou atributos em escalas/cardinalidades diferentes — importância por permutação (`rfpimp.importances`) ou por remoção de coluna são mais confiáveis, ao custo de mais computação.

## Anti-patterns
- **Usar `feature_importances_` bruto para decidir remoção de atributos em presença de colinearidade**: prefira importância por permutação (`rfpimp`) quando a decisão importa.
- **Não padronizar dados antes de SVM ou KNN**: ambos dependem de distância/margem — sem padronização, atributos de escala maior dominam artificialmente.
- **Deixar árvores/florestas sem limite de profundidade**: os valores-padrão tendem a superadequar; sempre validar `max_depth`/`num_leaves` por validação cruzada.
- **Rodar TPOT como primeira tentativa em vez de último recurso**: é caro (horas/dias); vale mais explorar as famílias manualmente primeiro (Capítulo 3) e reservar busca automatizada para quando já se sabe que vale o investimento.

## Reference Tables
| Modelo | Eficiência | Pré-processamento | Superadequação | Interpretação |
|---|---|---|---|---|
| Regressão logística | rápida, paraleliza (exceto `liblinear`) | padronizar se solver `sag`/`saga` | `C` (menor = mais regularização), `penalty` l1/l2 | `.coef_` → log-odds via `inv_logit` |
| Naive Bayes | O(Nd) treino, O(cd) teste | assume independência; remover colinearidade | alto bias/baixa variância (ensemble não ajuda) | probabilidade por classe via priors |
| SVM (`SVC`) | O(n³–n⁴), custoso em escala | padronização obrigatória | `C`, `gamma` (kernel `rbf`) | vetores suporte; `.coef_` só em kernel linear |
| KNN | treino O(1), teste O(Nd) | padronização recomendada | ↑ `n_neighbors`, ajustar `p` (L1/L2) | inspecionar `.kneighbors` |
| Árvore de decisão | O(mn log n) treino, O(altura) predição | não exige escala; tratar ausentes | `max_depth` ↓, `min_impurity_decrease` ↑ | percorrer a árvore; `feature_importances_` |
| Floresta aleatória | paraleliza (`n_jobs`) | não exige escala | ↑ `n_estimators`, ↓ `max_depth` | `feature_importances_`, `oob_score_` |
| XGBoost | paraleliza, usa GPU | não exige escala; codificar categóricas | `early_stopping_rounds`, `reg_alpha`/`reg_lambda` | `feature_importances_` (weight/gain/cover) |
| LightGBM | mais rápido que XGBoost (binning) | idem XGBoost | ↓ `num_leaves`, ↑ `min_data_in_leaf` | `feature_importances_` (split/gain) |
| TPOT | horas/dias | remover NaN e categóricas antes | validação cruzada embutida | depende do pipeline encontrado; exporta código |

## Code Examples
```python
# a mesma interface para qualquer família (troca só a classe do modelo)
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(random_state=42)
lr.fit(X_train, y_train)
lr.score(X_test, y_test)
lr.predict_proba(X.iloc[[0]])

# XGBoost com early stopping (para de treinar quando a métrica estagna)
import xgboost as xgb
xgb_class = xgb.XGBClassifier(random_state=42)
xgb_class.fit(
    X_train, y_train,
    early_stopping_rounds=10,
    eval_set=[(X_test, y_test)],
)

# importância de atributos mais confiável que feature_importances_ bruto
import rfpimp
rfpimp.importances(rf, X_test, y_test).Importance
```
- **O que demonstra**: a intercambialidade de modelos via interface comum e a diferença entre importância nativa e importância por permutação.

## Key Takeaways
1. Toda família de modelo responde às mesmas quatro perguntas (eficiência, pré-processamento, superadequação, interpretação) — use isso como checklist ao escolher um modelo novo.
2. Bagging (floresta) reduz variância combinando árvores independentes; boosting (XGBoost/LightGBM) reduz bias combinando árvores sequenciais que corrigem erro residual.
3. SVM e KNN exigem padronização; árvores e seus ensembles não.
4. `feature_importances_` nativo pode enganar sob colinearidade — `rfpimp.importances` (permutação) é mais confiável.
5. TPOT automatiza a busca de pipeline inteiro, mas é caro — reservar para quando a busca manual já não é suficiente.

## Connects To
- **Ch 3**: já usou várias dessas famílias no fluxo de comparação por k-fold.
- **Ch 8**: seleção de atributos usa `.feature_importances_`/`.coef_` destes modelos.
- **Ch 9**: `class_weight`, `scale_pos_weight` (XGBoost) e `weights='distance'` (KNN) retomam o tratamento de classes desbalanceadas.
- **Ch 12**: métricas de avaliação além de `.score` (accuracy) para cada um destes modelos.
- **Ch 13**: SHAP e outras técnicas de explicação complementam a importância nativa de cada modelo.
- **Ch 14**: as versões de regressão dos mesmos modelos (regressão linear, SVR, árvore/floresta/XGBoost/LightGBM de regressão).
</content>
