# Capítulo 7 — Hipótese e Inferência

## Teste Estatístico de Hipótese
Estrutura clássica: **hipótese nula H0** (posição padrão) vs. **hipótese alternativa H1**. A estatística observada, sob H0, é vista como amostra de uma distribuição conhecida — isso permite decidir se há evidência para rejeitar H0.

## Exemplo: Lançar uma Moeda
`H0: p=0,5` (moeda honesta). `X` = número de caras em `n` lançamentos ~ `Binomial(n,p)`, aproximada por Normal via `normal_approximation_to_binomial(n,p)` (Capítulo 6). Funções auxiliares constroem o vocabulário do teste:
- `normal_probability_below/above/between/outside(lo, hi, mu, sigma)`.
- `normal_upper_bound`/`normal_lower_bound`/`normal_two_sided_bounds(probability, mu, sigma)` — inversas: dado um nível de confiança, retornam os cortes.

**Erro Tipo 1** (falso positivo: rejeitar H0 verdadeira) — nível de significância convencional 5% ou 1%. **Erro Tipo 2** (falso negativo: não rejeitar H0 falsa) — seu complemento é o **poder do teste**, que depende de qual H1 específica se assume (ex.: `p=0,55`).

**Teste unilateral vs. bilateral**: se H0 é "moeda não é mais provável de dar cara" (`p≤0,5`), um teste unilateral (rejeita só se X for muito alto, não muito baixo) tem mais poder que o bilateral para essa alternativa específica — ilustra que a escolha do teste deve refletir a hipótese alternativa real de interesse.

## p-values
Abordagem equivalente: em vez de fixar limiares antes, calcula-se a probabilidade de observar algo **tão ou mais extremo** que o valor observado, assumindo H0 (`two_sided_p_value`). Usa **correção de continuidade** (529.5 em vez de 530) porque se aproxima uma distribuição discreta (binomial) por uma contínua (normal). Validado por simulação de Monte Carlo (100.000 experimentos de 1000 lançamentos).

**Alerta explícito**: p-values só são interpretáveis se a suposição de normalidade do dado for válida — "uma em um milhão" comumente significa "uma em um milhão *se os dados forem normalmente distribuídos*", o que pode não valer.

## Intervalos de Confiança
Terceira abordagem: em vez de testar uma hipótese específica, estimar `p_hat` (proporção observada) e construir um intervalo em torno dele via `normal_two_sided_bounds`, usando o desvio padrão estimado a partir de `p_hat` (não do `p` verdadeiro, desconhecido). Interpretação correta (frequentista): "se repetíssemos o experimento muitas vezes, 95% dos intervalos construídos assim conteriam o `p` verdadeiro" — não é uma afirmação de probabilidade sobre o `p` fixo em si.

## P-Hacking
Demonstração empírica: um teste com 5% de significância rejeita a hipótese nula (mesmo sendo verdadeira) em ~5% dos experimentos por puro acaso — simulação com 1000 experimentos de lançamento de moeda honesta resulta em 46 rejeições falsas. **Consequência prática**: testar hipóteses suficientes contra o mesmo dataset, ou remover outliers seletivamente após ver o resultado, quase garante achar "significância" espúria. Recomendação: decidir hipóteses **antes** de olhar os dados, limpar dados sem olhar para a hipótese, e não tratar p-value como substituto de bom senso.

## Exemplo: Teste A/B
Comparar duas propagandas (`N_A, n_A` visualizações/cliques do anúncio A; idem B) tratando cada uma como proporção estimada com seu próprio erro padrão (`estimated_parameters`). Sob H0 (`p_A = p_B`), a estatística `(p_B - p_A) / sqrt(sigma_A² + sigma_B²)` é aproximadamente normal padrão (`a_b_test_statistic`) — permite computar um p-value para a diferença entre as duas taxas de clique.

## Inferência Bayesiana
Abordagem alternativa: tratar o parâmetro desconhecido (ex.: `p` da moeda) como variável aleatória com uma **distribuição a priori**, atualizada via Teorema de Bayes para uma **distribuição a posteriori** dado os dados observados. Para probabilidades, a priori conveniente é a **distribuição Beta** (`beta_pdf(x, alpha, beta)`), pois é **conjugada** da Binomial — a posteriori após observar `h` caras e `t` coroas é simplesmente `Beta(alpha+h, beta+t)`. Quanto mais dados, menos a priori importa (posteriores convergem independente do ponto de partida). Diferença filosófica chave: permite afirmações diretas sobre a probabilidade do parâmetro ("há 5% de chance de p estar entre 49% e 51%"), ao contrário do p-value frequentista ("se H0 for verdade, veríamos dados tão extremos só 5% das vezes"). O livro não usa Bayesiano no resto do texto, mas registra a alternativa.

## Por Que Isso Importa
`normal_probability_*`, `normal_two_sided_bounds` e o vocabulário de p-value/intervalo de confiança reaparecem ao avaliar coeficientes de regressão (Capítulos 14-15, "Erros Padrões de Coeficientes de Regressão").
