# Capítulo 6 — Probabilidade

## Dependência e Independência
Dois eventos `E` e `F` são **independentes** se saber sobre um não dá informação sobre o outro — formalmente `P(E,F) = P(E)P(F)`. Exemplo: duas jogadas de moeda são independentes; "primeira jogada coroa" e "ambas cara" são dependentes (mutuamente exclusivos, na prática).

## Probabilidade Condicional
`P(E|F) = P(E,F)/P(F)` — probabilidade de `E` dado que `F` ocorreu. Quando independentes, `P(E|F) = P(E)`.

**Problema clássico das duas crianças** (contraintuitivo, resolvido por simulação com `random_kid()`):
- `P(ambas meninas | mais velha é menina) = 1/2` (intuitivo)
- `P(ambas meninas | pelo menos uma é menina) = 1/3` (surpreendente — condicionar em "pelo menos uma" é uma informação mais fraca que condicionar na posição específica "a mais velha").

## Teorema de Bayes
`P(E|F) = P(F|E)P(E) / P(F)` — "inverte" probabilidades condicionais quando só se conhece a direção oposta.

**Caso do teste médico** (o exemplo canônico do livro para "por que cientistas de dados são mais espertos que médicos"): doença com prevalência 1/10.000, teste com 99% de acerto em ambas as direções. Resultado contraintuitivo: `P(doença | teste positivo) ≈ 0,98%` — menos de 1%, porque a base de não-doentes é imensamente maior que a de doentes, então mesmo 1% de falso-positivo nela gera muito mais positivos que os 99% de verdadeiro-positivo entre os poucos doentes. Ilustrado com contagem intuitiva sobre população de 1 milhão: ~99 verdadeiros positivos vs. ~9.999 falsos positivos.

## Variáveis Aleatórias
Variável cujo valor tem uma distribuição de probabilidade associada (ex.: resultado de moeda: 0/1 com p=0,5 cada). **Valor esperado** = média ponderada pelas probabilidades. Variáveis aleatórias podem ser condicionadas a eventos, exatamente como no exemplo das duas crianças.

## Distribuições Contínuas
- **PDF** (função de densidade de probabilidade): para um resultado contínuo, a probabilidade de um ponto exato é 0; a densidade `f` dá `P(x ≤ X ≤ x+h) ≈ h·f(x)`.
- **Distribuição uniforme**: `uniform_pdf`/`uniform_cdf` — peso igual entre 0 e 1; `random.random()` do Python amostra dela.
- **CDF** (função de distribuição cumulativa): `P(X ≤ x)`.

## Distribuição Normal
`normal_pdf(x, mu, sigma)` — parametrizada por média `μ` e desvio padrão `σ`. **Normal padrão**: `μ=0, σ=1`. Transformação: se `Z` é normal padrão, `X = σZ + μ` é normal `(μ,σ)`, e o inverso `Z = (X-μ)/σ` padroniza qualquer normal.

`normal_cdf` é implementada via `math.erf` (não tem forma fechada elementar). Para o inverso (`inverse_normal_cdf`, dado `p` encontrar `x`), como não há fórmula fechada mas a CDF é contínua e crescente, usa-se **busca binária** — padrão geral do livro para "inverter" funções monótonas sem fórmula analítica.

## Teorema do Limite Central
A média (ou soma) de muitas variáveis aleatórias i.i.d. é aproximadamente normal, independente da distribuição original — desde que `n` seja grande. Demonstrado com a distribuição **Binomial(n,p)** (soma de `n` ensaios `Bernoulli(p)`): conforme `n` cresce, `Binomial(n,p)` se aproxima de `Normal(np, sqrt(np(1-p)))`, o que é visualizado sobrepondo um histograma de amostras binomiais com a curva normal correspondente (`make_hist`).

**Aplicação prática**: em vez de calcular a CDF binomial exata (difícil), aproxima-se por uma normal com mesma média/desvio — mecanismo central por trás do teste de hipótese do Capítulo 7 (teste da moeda).

## Por Que Isso Importa
`normal_cdf`, `inverse_normal_cdf` e a aproximação normal da binomial são usados diretamente no Capítulo 7 (teste de hipótese, p-values, intervalos de confiança) sem nova explicação.
