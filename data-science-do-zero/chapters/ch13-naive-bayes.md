# Capítulo 13 — Naive Bayes

## Filtro de Spam Muito Estúpido (uma palavra só)
Modelo com apenas o evento `V` = "mensagem contém 'viagra'". Via Teorema de Bayes, `P(S|V) = P(V|S) / (P(V|S) + P(V|¬S))` assumindo `P(S)=P(¬S)=0,5`. Exemplo numérico: se 50% dos spams e 1% dos não-spams contêm "viagra", `P(spam|viagra) = 0,5/(0,5+0,01) ≈ 98%`.

## Filtro Mais Sofisticado (vocabulário inteiro)
Generaliza para um vocabulário `w1...wn`, cada palavra `wi` gerando um evento `Xi` = "mensagem contém wi". **A suposição "naive" (ingênua)**: as presenças/ausências de cada palavra são **condicionalmente independentes** dado spam/não-spam — `P(X1=x1,...,Xn=xn|S) = ∏ P(Xi=xi|S)`. É uma suposição extrema e sabidamente falsa (palavras têm correlação real — "viagra" e "rolex" não são independentes), mas funciona bem na prática mesmo assim.

**Problema numérico (underflow)**: multiplicar muitas probabilidades pequenas gera números próximos de zero que o ponto flutuante não representa bem. Solução padrão: trabalhar em **espaço log** (`log(p1*...*pn) = log p1 + ... + log pn`) e depois `exp()` no final.

**Problema de contagem zero**: se uma palavra (ex.: "dado") só aparece em não-spam no treino, `P("dado"|S)=0` faz o classificador zerar a probabilidade de spam de qualquer mensagem que contenha essa palavra, não importa quão suspeita seja o resto. **Suavização (smoothing) com pseudo-contagem `k`**:
```
P(Xi|S) = (k + spams_com_wi) / (2k + total_spams)
```
Equivalente a fingir que já se viu `k` spams adicionais com a palavra e `k` sem.

## Implementação
- `tokenize(message)` — minúsculas, `re.findall("[a-z0-9']+", ...)`, `set()` (remove duplicatas — conta presença, não frequência).
- `count_words(training_set)` — `defaultdict(lambda: [0,0])`, incrementando `[spam_count, non_spam_count]` por palavra.
- `word_probabilities(counts, total_spams, total_non_spams, k=0.5)` — aplica a suavização, retorna triplas `(palavra, P(palavra|spam), P(palavra|¬spam))`.
- `spam_probability(word_probs, message)` — para **cada** palavra do vocabulário de treino (não só as da mensagem), soma `log(P)` se a palavra está presente na mensagem, ou `log(1-P)` se ausente — a ausência de uma palavra também é evidência. Combina via `exp` e normaliza no final.
- `NaiveBayesClassifier` — classe com `.train(training_set)` (calcula `word_probs`) e `.classify(message)` (chama `spam_probability`).

## Testando com o SpamAssassin Public Corpus
Extrai apenas a linha `Subject:` de cada e-mail (`glob.glob` + regex), rotula por pasta (`ham` no nome do arquivo = não-spam). `split_data` (75/25) para treino/teste. Resultado no experimento do livro: **75% de precisão (accuracy), 73% de sensibilidade (recall)** — "não são números ruins para um modelo tão simples", usando só a linha de assunto.

**Inspeção qualitativa dos erros**: hams classificados como mais "spammy" continham palavras como "precisa", "seguro", "importante" (fortemente associadas a spam no treino, mas usadas legitimamente); o spam mais "hammy" era curto demais para ter sinal ("Re: garotas"). `p_spam_given_word` permite rankear palavras por quão indicativas são de spam.

## Possíveis Melhorias (citadas, não implementadas)
- Usar o corpo da mensagem, não só o assunto.
- Filtrar palavras raras com um `min_count`.
- **Stemming** (reduzir palavras à raiz, ex.: `drop_final_s` como stemmer ingênuo, ou Porter Stemmer para algo sério) para unificar variações como "cheap"/"cheapest".
- Adicionar features sintéticas além de "contém a palavra wi" (ex.: token artificial `contains:number`).

## Por Que Isso Importa
É o primeiro classificador probabilístico completo do livro, e o único baseado inteiramente em contagem + Teorema de Bayes (Capítulo 6) sem gradiente descendente. Reaparece como contraponto conceitual quando o livro discute, no Capítulo 20, extração de tópicos/texto.
