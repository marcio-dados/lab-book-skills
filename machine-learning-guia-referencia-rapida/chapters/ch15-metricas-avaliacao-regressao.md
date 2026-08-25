# Capítulo 15: Métricas e avaliação de regressão

## Core Idea
Diferente da classificação (matriz de confusão), regressão avalia-se por distância entre valor previsto e real — R² resume "quanto da variância eu explico", enquanto MAE/MSE/log-erro traduzem o erro na unidade do próprio alvo (ou penalizando erros grandes/subpredição de formas diferentes); gráficos de resíduos e testes estatísticos (Breusch-Pagan, Kolmogorov-Smirnov) verificam se as suposições do modelo linear se sustentam.

## Frameworks Introduced
- **Escolher a métrica de erro pelo tipo de penalidade desejada**: MAE penaliza todo erro linearmente (bom quando outliers não devem dominar); MSE/RMSE penaliza erros grandes desproporcionalmente (bom quando "errar muito" é bem pior que "errar pouco"); erro logarítmico quadrático médio penaliza subpredição mais que superpredição (bom para alvos com crescimento exponencial, como população/preço de ações).
  - Como usar: nomear o custo do erro (linear? quadrático? assimétrico?) antes de escolher entre MAE/MSE/MSLE.
- **Diagnóstico de resíduos como checklist de suposições do modelo linear**: gráfico de resíduos (padrão aleatório = bom sinal), teste de Breusch-Pagan (heterocedasticidade), histograma/gráfico de probabilidade + teste de Kolmogorov-Smirnov (normalidade dos resíduos) — três checagens independentes da mesma pergunta: "os erros deste modelo se comportam como o modelo assume?".
  - Quando usar: sempre que usar um modelo que assume erros homocedásticos/normais (regressão linear e variantes), antes de confiar nos p-valores/intervalos de confiança.

## Key Concepts
- **R² (`.score` padrão)**: fração da variância do alvo explicada; não tem "valor bom" universal — 0,7 pode ser ótimo em um domínio e ruim em outro (ex. prever preço de ações do dia seguinte pode dar R²=0,99 e ainda ser inútil na prática).
- **MAE**: erro médio absoluto, na unidade do alvo, sem limite superior; robusto a outliers; só serve para comparar modelos entre si, não para dizer "o modelo é bom".
- **MSE/RMSE**: penaliza erros grandes mais que proporcionalmente (assume erro normalmente distribuído).
- **MSLE**: penaliza subpredição mais que superpredição — adequado a alvos que crescem exponencialmente.
- **Variância explicada**: igual a R² quando a média dos resíduos é 0 (verdade em OLS).
- **Homocedasticidade**: variância dos resíduos constante através dos valores previstos — suposição do modelo linear; testável visualmente (gráfico de resíduos) e estatisticamente (Breusch-Pagan, p < 0,05 rejeita homocedasticidade).
- **Normalidade dos resíduos**: outra suposição do modelo linear; testável via histograma, gráfico de probabilidade (quantis alinhados = normal) e teste de Kolmogorov-Smirnov (p < 0,05 rejeita normalidade).
- **Gráfico de erro de predição**: real vs. previsto; um modelo perfeito cairia na diagonal de 45°; desvios sistemáticos (ex. subestimar valores altos) revelam viés estrutural do modelo.

## Anti-patterns
- **Julgar um modelo de regressão só pelo valor absoluto de R²**: sempre contextualizar com o domínio (um R² alto pode ser inútil se o erro residual, em unidade real, ainda for inaceitável para a decisão de negócio).
- **Confiar em coeficientes/p-valores de um modelo linear sem checar homocedasticidade e normalidade dos resíduos**: as suposições por trás da inferência estatística clássica (OLS) quebram silenciosamente sem esse diagnóstico.
- **Usar MSE quando outliers não deveriam dominar a métrica**: MSE amplifica erros grandes; MAE é mais robusto nesse cenário.

## Code Examples
```python
from sklearn import metrics
metrics.r2_score(bos_y_test, bos_y_test_pred)
metrics.mean_absolute_error(bos_y_test, bos_y_test_pred)
metrics.mean_squared_error(bos_y_test, bos_y_test_pred)
metrics.mean_squared_log_error(bos_y_test, bos_y_test_pred)

# diagnóstico de heterocedasticidade (Breusch-Pagan)
import statsmodels.stats.api as sms
hb = sms.het_breuschpagan(resids, bos_X_test)  # p < 0.05 → heterocedástico

# diagnóstico de normalidade dos resíduos (Kolmogorov-Smirnov)
from scipy import stats
stats.kstest(resids, cdf="norm")  # p < 0.05 → não normal

# visualização (Yellowbrick)
from yellowbrick.regressor import ResidualsPlot, PredictionError
```
- **O que demonstra**: o par métrica-escalar + teste-estatístico-formal para a mesma pergunta (o modelo é adequado?), permitindo tanto uma leitura rápida quanto uma confirmação formal.

## Reference Tables
| Métrica | Direção | Quando preferir |
|---|---|---|
| R² | maximizar | resumo geral, comparação rápida entre modelos |
| MAE | minimizar | erro robusto a outliers, na unidade do alvo |
| MSE/RMSE | minimizar | penalizar erros grandes mais que proporcionalmente |
| MSLE | minimizar | alvo com crescimento exponencial, penaliza subpredição |
| Variância explicada | maximizar | equivalente a R² quando resíduos têm média 0 (OLS) |

## Key Takeaways
1. Não existe "bom R²" universal — sempre interpretar no contexto do domínio e do custo real do erro.
2. A escolha entre MAE/MSE/MSLE reflete o tipo de penalidade desejada para o erro (linear, quadrática, assimétrica).
3. Regressão linear carrega suposições (homocedasticidade, normalidade dos resíduos) que devem ser checadas visual e estatisticamente, não assumidas.
4. Gráfico de erro de predição revela viés sistemático (ex. subestimar valores altos) que R²/MAE sozinhos não mostram.

## Connects To
- **Ch 14**: modelos de regressão avaliados aqui (regressão linear, floresta) foram treinados lá.
- **Ch 12**: par direto do lado de classificação (matriz de confusão vs. resíduos).
- **Ch 16**: explicação de modelos de regressão (SHAP) complementa o diagnóstico de erro deste capítulo.
</content>
