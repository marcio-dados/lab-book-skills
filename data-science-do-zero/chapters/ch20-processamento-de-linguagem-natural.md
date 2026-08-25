# Capítulo 20 — Processamento de Linguagem Natural (NLP)

## Nuvens de Palavras (e por que desconfiar delas)
Visualização popular (tamanho da palavra ∝ frequência), mas **cientistas de dados geralmente não gostam** — a posição das palavras na nuvem não carrega significado, é só "onde coube". Alternativa melhor sugerida: se há **duas métricas** por palavra (ex.: popularidade em vagas de emprego × popularidade em currículos), usar um **gráfico de dispersão de texto** (`plt.text` posicionado pelas duas métricas, tamanho de fonte proporcional à soma) — os eixos passam a carregar informação real, ao contrário da nuvem decorativa.

## Modelos n-gramas
Objetivo lúdico: gerar texto artificial "parecido com data science" a partir de um corpus real (ensaio de Mike Loukides, raspado com `requests`+`BeautifulSoup`, Capítulo 9). Pré-processamento: corrigir apóstrofo unicode (`fix_unicode`), tokenizar em palavras/pontuação via `re.findall(r"[\w']+|[\.]", texto)`.

- **Modelo bigrama**: para cada palavra, olha-se todas as palavras que a seguiram no corpus (`transitions = defaultdict(list)` populado a partir de `zip(document, document[1:])`), escolhendo aleatoriamente a próxima a cada passo (`generate_using_bigrams`) até sortear um ponto final. Produz frases gramaticalmente incoerentes.
- **Modelo trigrama**: condiciona a próxima palavra nas **duas** anteriores (`zip(document, document[1:], document[2:])`), rastreando também as palavras que legitimamente começam frase (`starts`, aquelas que seguem um ponto). Produz frases **mais coerentes**, mas pelo motivo errado: com menos opções de continuação a cada passo, o modelo frequentemente reproduz **trechos literais** do texto-fonte em vez de generalizar. Mais dados (múltiplos artigos) ajudariam a variar mais.

## Gramáticas
Abordagem alternativa e determinística por **regras de produção** (BNF-like): um dict onde chaves começando com `_` são não-terminais a expandir (ex.: `_S → _NP _VP`), e o resto são terminais (palavras concretas). **Recursão é permitida** (`_NP` pode conter `_NP`), permitindo gerar infinitas frases distintas de uma gramática finita.

`is_terminal(token)` — checa se não começa com `_`. `expand(grammar, tokens)` — encontra o primeiro token não-terminal, substitui por uma produção aleatória (recursivamente, até sobrar só terminais). `generate_sentence(grammar) = expand(grammar, ["_S"])`.

**Uso inverso mencionado (não implementado)**: gramáticas também servem para **fazer parsing** de sentenças reais (entender estrutura sintática), não só gerar — citado como "mais mágico" que gerar, remetido a bibliotecas especializadas.

## Amostragem de Gibbs (ferramenta preparatória para LDA)
Técnica para amostrar de distribuições multidimensionais conjuntas conhecendo **apenas as distribuições condicionais**, quando amostrar diretamente da conjunta é difícil. Exemplo didático com dois dados: `x` = valor do primeiro dado, `y` = soma dos dois. Amostrar diretamente é trivial (`direct_sample`), mas o exercício é mostrar que, conhecendo só `P(y|x)` (fácil) e `P(x|y)` (mais elaborada, ver `random_x_given_y`), alternar repetidamente entre sortear `x` dado `y` atual e `y` dado `x` atual (`gibbs_sample`, tipicamente ~100 iterações de "queima") converge para uma amostra da distribuição conjunta — validado comparando histogramas de `gibbs_sample` vs. `direct_sample`.

## Modelagem de Tópicos (LDA simplificado)
Generaliza a recomendação por "interesse em comum" do Capítulo 1: em vez de casar palavras exatas, identificar **tópicos latentes** que geram as palavras observadas. Modelo probabilístico assumido (análogo em espírito ao Naive Bayes do Cap. 13):
- `K` tópicos fixos, cada um com uma distribuição de probabilidade sobre palavras.
- Cada documento tem uma distribuição de probabilidade sobre tópicos (sua "mistura" de tópicos).
- Cada palavra do documento é gerada sorteando primeiro um tópico (da mistura do documento), depois uma palavra (da distribuição daquele tópico).

**O que se observa**: `documents` (listas de palavras/interesses por usuário) e nada mais — `document_topics` (a que tópico pertence cada palavra observada) é **latente**, inferido via **amostragem de Gibbs**.

### Estruturas de contagem mantidas
- `document_topic_counts[d]` — `Counter` de tópicos por documento.
- `topic_word_counts[k]` — `Counter` de palavras por tópico.
- `topic_counts[k]` — total de palavras atribuídas a cada tópico.
- `document_lengths[d]` — total de palavras por documento.

### Probabilidades condicionais suavizadas (mesmo padrão do Cap. 13)
```
p_topic_given_document(topic, d, alpha=0.1) = (contagem + alpha) / (tamanho_doc + K*alpha)
p_word_given_topic(word, topic, beta=0.1)   = (contagem + beta) / (total_topico + W*beta)
```
`topic_weight(d, word, k) = p_word_given_topic(word,k) * p_topic_given_document(k,d)` — combina "quão típica é esta palavra deste tópico" com "quão presente está este tópico neste documento". `sample_from(weights)` sorteia um índice proporcionalmente a pesos arbitrários (não precisam somar 1).

### Algoritmo (Gibbs Sampling aplicado)
1. Inicializa cada palavra de cada documento com um tópico **aleatório**, populando as contagens.
2. Repetidamente (1000 iterações no exemplo), para cada palavra de cada documento: **remove** sua contagem atual (para não influenciar seu próprio peso), recalcula os pesos por tópico via `topic_weight`, sorteia um **novo tópico** via `sample_from`, e **readiciona** a contagem sob o novo tópico.
3. Após convergência, `topic_word_counts` revela quais palavras dominam cada tópico — usados para **nomear** os tópicos manualmente (ex.: "Big Data e linguagens de programação", "Python e estatística", "bases de dados", "aprendizado de máquina").
4. `document_topic_counts` revela a mistura de tópicos de cada usuário/documento.

**Limitação reconhecida**: com poucos dados (o dataset de brinquedo tem ~15 documentos curtos), tópicos ficam um pouco confusos ("e" nos nomes sugere sobreposição) — mais tópicos provavelmente exigiriam mais dados para se resolverem bem.

## Por Que Isso Importa
Amostragem de Gibbs é a ferramenta que viabiliza LDA sem exigir cálculo de uma distribuição conjunta fechada — é o primeiro (e único) uso de MCMC no livro. O padrão de suavização com pseudo-contagem (`alpha`/`beta`) é idêntico ao `k` do Naive Bayes (Capítulo 13), reforçando o mesmo princípio: nunca deixar uma probabilidade estimada cair exatamente a zero por falta de dados.
