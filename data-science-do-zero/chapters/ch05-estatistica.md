# Capítulo 5 — Estatística

## Descrevendo um Conjunto Único de Dados
Listar dados brutos não escala — a estatística existe para **destilar e comunicar** aspectos relevantes. Ferramentas básicas: `len`, `max`/`min`, valores em posições ordenadas (`sorted(x)[k]`).

## Tendências Centrais
- **Média** (`mean`): soma / contagem. Reage suavemente a mudanças — se um ponto cresce em `e`, a média cresce `e/n`. **Muito sensível a outliers** (exemplo citado: Michael Jordan distorcendo a média salarial da turma de Geografia da UNC).
- **Mediana** (`median`): valor central (ou média dos dois centrais, se `n` par); não depende da magnitude de cada ponto, só da ordem — não reage a outliers.
- **Quantil** (`quantile(x, p)`): generalização da mediana — valor abaixo do qual está a fração `p` dos dados.
- **Moda** (`mode`): valor(es) mais frequente(s), via `Counter`.

## Dispersão
- **Amplitude** (`data_range = max - min`): não depende de todo o dataset (mesma fraqueza da mediana).
- **Variância** (`variance`): soma dos quadrados dos desvios da média, dividida por `n-1` (não `n`) — correção de Bessel para estimar a variância populacional a partir de uma amostra.
- **Desvio padrão** (`standard_deviation = sqrt(variance)`): mesma unidade dos dados originais (variância está na unidade ao quadrado).
- **Amplitude interquartil** (`quantile(x,0.75) - quantile(x,0.25)`): alternativa robusta a outliers, ao contrário de amplitude e desvio padrão.

## Correlação
- **Covariância** (`covariance(x,y) = dot(de_mean(x), de_mean(y)) / (n-1)`): mede como duas variáveis variam juntas em torno de suas médias. Difícil de interpretar — unidade é o produto das unidades de entrada, e escala com a magnitude das variáveis.
- **Correlação** (`correlation = covariance / (stdev_x * stdev_y)`): adimensional, sempre entre -1 e 1.
- **Outliers distorcem correlação fortemente** — exemplo do livro: um único usuário-teste com 100 amigos e 1 minuto/dia reduz a correlação de 0,57 para 0,25; removê-lo (após confirmar que é lixo de dados, não sinal real) revela a correlação verdadeira.

## Paradoxo de Simpson
Agrupar dados sem controlar por uma variável de confusão (no exemplo: posse de PhD) pode inverter o sinal da correlação observada (Costa Oeste parece mais "amigável" que Costa Leste no agregado, mas o oposto é verdade dentro de cada subgrupo por PhD). Lição: correlação mede relação "tudo mais constante" — sem checar fatores de confusão, o agregado pode enganar.

## Limites da Correlação
- Correlação zero **não implica ausência de relação** — só ausência de relação *linear* (exemplo: `y = |x|` tem correlação zero com `x`, mas relação perfeita não-linear).
- Correlação não diz nada sobre o **tamanho** do efeito — duas variáveis podem ter correlação 1 com uma delas variando muito pouco em termos absolutos.

## Correlação e Causalidade
"Correlação não é causalidade": uma correlação forte entre X e Y é compatível com X→Y, Y→X, causa comum, ou coincidência. A forma mais confiável de estabelecer causalidade é o **experimento aleatorizado** (dividir usuários aleatoriamente em grupos com tratamentos diferentes e comparar resultados) — retomado no Capítulo 7 (teste A/B).

## Por Que Isso Importa
`mean`, `median`, `variance`, `standard_deviation`, `correlation`, `de_mean` (que reaparece como bloco de construção de regressão) são usados sem redefinição nos capítulos de hipótese/inferência (7), gradiente descendente (8) e regressão (14-16).
