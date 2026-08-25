# Capítulo 16 — Regressão Logística

## O Problema
Retoma o exemplo do Capítulo 1: prever se um usuário paga por conta premium (`y ∈ {0,1}`) a partir de experiência e salário.

## Por Que Não Usar Regressão Linear Direto
Aplicar `estimate_beta` (Cap. 15) direto sobre `y` binário produz dois problemas:
1. As saídas previstas não ficam confinadas a `[0,1]` — podem ser negativas ou muito grandes, difíceis de interpretar como probabilidade.
2. Viola a suposição de erros não-correlacionados com `x`: como o valor real é sempre 0 ou 1, prever valores fora desse intervalo para pessoas com muita experiência força os erros a se correlacionarem sistematicamente com `x`, **enviesando a estimativa de beta**.

## A Função Logística
```
logistic(x) = 1 / (1 + exp(-x))
```
Mapeia qualquer real para `(0,1)`: satura perto de 1 para entradas grandes/positivas, perto de 0 para grandes/negativas. Derivada conveniente: `logistic'(x) = logistic(x)*(1-logistic(x))` (usada na derivação do gradiente).

Modelo: `y_i` é Bernoulli com `P(y_i=1) = logistic(dot(x_i, beta))`.

## Ajuste via Máxima Verossimilhança
Diferente da regressão linear (onde minimizar soma de quadrados = maximizar verossimilhança sob erro normal), aqui **não há equivalência** — maximiza-se a log-verossimilhança diretamente:
- `logistic_log_likelihood_i(x_i, y_i, beta)` = `log(f(x_i·beta))` se `y_i=1`, `log(1-f(x_i·beta))` se `y_i=0`.
- Soma sobre todos os pontos (assumindo independência) = log-verossimilhança total.
- Gradiente analítico derivado via cálculo: `logistic_log_partial_ij = (y_i - logistic(dot(x_i,beta))) * x_i[j]` — tem a forma elegante "(real - previsto) × feature", análoga ao gradiente do erro quadrado em regressão linear.
- Otimização via `maximize_batch` ou `maximize_stochastic` (Capítulo 8) sobre essa log-verossimilhança.

## Aplicando o Modelo
Fluxo padrão: `rescale(x)` → `train_test_split` → `maximize_batch(logistic_log_likelihood, logistic_log_gradient, beta_0)`. Resultado nos dados redimensionados: `beta_hat = [-1.90, 4.05, -3.87]`, revertido para a escala original: `[7.61, 1.42, -0.000249]`.

**Interpretação é mais difícil que em regressão linear**: o efeito de aumentar uma variável em uma unidade depende de **onde** você já está na curva logística — se `dot(beta,x_i)` já é grande (perto da saturação), um aumento tem pouco efeito na probabilidade; se está perto de 0 (região mais "íngreme" da curva), o mesmo aumento tem efeito grande. Só é possível afirmar direção do efeito ("mais experiência → mais provável pagar; mais salário → menos provável pagar"), não magnitude direta em probabilidade.

## Avaliação no Conjunto de Teste
Aplicando limiar 0,5 sobre `logistic(dot(beta_hat, x_i))` nos dados de teste: **precision 93%, recall 82%** — "números bem respeitáveis". Gráfico de dispersão `previsto vs. real` confirma separação razoável entre as classes.

## Máquinas de Vetor de Suporte (SVM) — Introdução Conceitual
O conjunto de pontos onde `dot(beta_hat, x_i) = 0` é o **limite de decisão** (um hiperplano) que a regressão logística produz como efeito colateral de maximizar verossimilhança. **SVM ataca o problema de outro ângulo**: procura diretamente o hiperplano que **maximiza a margem** até o ponto mais próximo de cada classe — não é derivado de um modelo probabilístico.

**Limitações reconhecidas**:
- Encontrar esse hiperplano é um problema de otimização "avançado demais" para o tratamento do-zero do livro — não implementado.
- Pode não existir hiperplano separador nos dados originais (ex.: dataset 1D onde positivos ficam "entre" negativos).
- **Truque do kernel**: mapear os dados para um espaço de dimensão maior (ex.: `x → (x, x²)`) pode torná-los linearmente separáveis; em vez de fazer o mapeamento explícito (caro), usa-se uma função kernel para computar produtos escalares diretamente no espaço maior.
- Recomendação explícita do autor: usar biblioteca especializada (`libsvm`, via `scikit-learn`) em vez de implementar SVM do zero — o livro conscientemente não tenta.

## Por Que Isso Importa
É o último capítulo de "modelos lineares" do livro — fecha o arco iniciado no Capítulo 14 (linear → múltipla → logística) e faz a ponte explícita para SVM como técnica de classificação alternativa não-probabilística, preparando a comparação com árvores de decisão (Cap. 17) e redes neurais (Cap. 18) como outras formas de traçar fronteiras de decisão não-lineares.
