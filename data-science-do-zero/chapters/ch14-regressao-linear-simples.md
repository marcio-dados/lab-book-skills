# Capítulo 14 — Regressão Linear Simples

## O Modelo
Hipótese: `y_i = β·x_i + α + ε_i` (`ε` = erro/ruído não capturado). `predict(alpha, beta, x_i) = beta*x_i + alpha`. Erro por ponto: `error = y_i - predict(...)`. Somar erros brutos cancelaria positivos e negativos, então minimiza-se a **soma dos erros ao quadrado** (`sum_of_squared_errors`).

## Solução Analítica (Mínimos Quadrados)
```
beta = correlation(x, y) * standard_deviation(y) / standard_deviation(x)
alpha = mean(y) - beta * mean(x)
```
Interpretação: `alpha` garante que, no valor médio de `x`, a previsão é a média de `y`. `beta` traduz "um desvio padrão a mais em x" em "correlation(x,y) desvios padrão a mais em y" — quando a correlação é zero, `beta=0` (x não afeta a previsão).

Aplicado aos dados de amigos/minutos (já sem o outlier do Cap. 5): `alpha≈22,95`, `beta≈0,903` — cada amigo adicional soma ~0,9 minuto/dia previsto; zero amigos ainda prevê ~23 minutos.

## R² (Coeficiente de Determinação)
`r_squared = 1 - sum_of_squared_errors/total_sum_of_squares(y)` — fração da variância de `y` capturada pelo modelo. Limite inferior 0 (modelo "sempre prevê a média", que é o caso `beta=0`), superior 1. No exemplo, `R²≈0,329` — relação real, mas fraca; outros fatores estão em jogo.

## Via Gradiente Descendente (alternativa)
`squared_error`/`squared_error_gradient(x_i, y_i, theta=[alpha,beta])` com derivadas parciais explícitas (`-2*error`, `-2*error*x_i`), alimentando `minimize_stochastic` do Capítulo 8. Resultado praticamente idêntico à fórmula fechada (`alpha≈22,93, beta≈0,905`) — serve para validar a solução analítica e generalizar o método para os casos em que não há fórmula fechada (regressão múltipla e logística, capítulos seguintes).

## Justificativa via Máxima Verossimilhança
Se os erros `ε_i` são assumidos normalmente distribuídos com média 0 e desvio padrão `σ` fixo, **minimizar a soma dos erros ao quadrado é matematicamente equivalente a maximizar a verossimilhança** (probabilidade) dos dados observados sob esse modelo. Justifica por que "mínimos quadrados" não é uma escolha arbitrária, mas decorre de uma suposição estatística específica sobre o ruído.

## Por Que Isso Importa
`predict`, `error`, `total_sum_of_squares` e a lógica de R² são estendidos diretamente (sem redefinição) no Capítulo 15 para múltiplas variáveis independentes, e o padrão "gradiente + `minimize_stochastic`" é reaplicado no Capítulo 16 (regressão logística).
