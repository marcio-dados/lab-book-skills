# Capítulo 22 — Sistemas Recomendadores

## O Problema
Recomendar novos interesses a um usuário dado seus interesses atuais (dataset `users_interests` reaproveitado do Cap. 1/20). Analogia histórica: o bibliotecário que recomendava livros — não escala e é limitado à imaginação de uma pessoa.

## Recomendando o que É Popular (baseline)
Abordagem mais simples: `Counter` sobre todos os interesses de todos os usuários → recomendar os mais populares que o usuário **ainda não tem** (`most_popular_new_interests`). Funciona como baseline razoável para usuário novo (sem dados), mas é genérico — "muita gente gosta de Python" não é uma recomendação personalizada.

## Filtragem Colaborativa Baseada no Usuário
Ideia: achar usuários **similares** e recomendar o que eles gostam.

**Similaridade do cosseno**: `cosine_similarity(v,w) = dot(v,w) / sqrt(dot(v,v)*dot(w,w))` — mede o ângulo entre vetores, resultado entre -1 e 1 (aqui, entre 0 e 1 porque os vetores são binários/não-negativos). Vetores idênticos → 1; sem sobreposição → 0.

**Pipeline**:
1. `unique_interests` — lista ordenada de todos os interesses distintos (via set + sorted), define os índices.
2. `make_user_interest_vector(user_interests)` — vetor binário (1/0) por usuário, indicando presença de cada interesse na posição correspondente.
3. `user_interest_matrix` — todos os vetores de usuário empilhados.
4. `user_similarities` — matriz de similaridade do cosseno **par a par** entre todos os usuários (viável só porque o dataset é pequeno).
5. `most_similar_users_to(user_id)` — ordena outros usuários por similaridade decrescente, excluindo o próprio e similaridade zero.
6. `user_based_suggestions(user_id)` — para cada usuário similar, soma sua similaridade em cada interesse que ele tem (`defaultdict(float)`); ordena as sugestões pelo peso acumulado; opcionalmente filtra interesses que o usuário já possui. **Os pesos não têm significado absoluto** — servem só para ordenar.

**Limitação explícita**: em espaços de muitos itens, a **maldição da dimensionalidade** (Capítulo 12) volta a valer — com muitas dimensões, "usuários mais similares" tendem a não ser realmente similares (analogia: em um site tipo Amazon com milhares de produtos possíveis, é improvável achar alguém genuinamente parecido com você em todo o histórico de compras).

## Filtragem Colaborativa Baseada em Itens
Abordagem alternativa: em vez de similaridade entre **usuários**, calcular similaridade entre **itens/interesses** diretamente, olhando quais usuários compartilham cada par de interesses.

1. `interest_user_matrix` — **transposta** de `user_interest_matrix` (linhas = interesses, colunas = usuários); cada linha é o vetor binário "quem tem interesse neste tópico".
2. `interest_similarities` — similaridade do cosseno entre pares de interesses (mesma função `cosine_similarity`, aplicada às linhas transpostas).
3. `most_similar_interests_to(interest_id)` — interesses mais próximos de um dado interesse (ex.: "Big Data" → Hadoop, Java, MapReduce, Spark, Storm...).
4. `item_based_suggestions(user_id)` — para cada interesse que o usuário já tem, soma a similaridade de todos os interesses relacionados a ele (`defaultdict(float)`), ordena, filtra os que já possui.

**Vantagem sobre a versão baseada em usuário**: mais estável/interpretável quando há muitos usuários mas relativamente poucos itens — a matriz de similaridade item-item costuma ser menor e mais estável que usuário-usuário.

## Comparação Prática
Ambas as abordagens (usuário e item) produzem recomendações "aparentemente razoáveis" para o usuário 0 (interessado em Big Data/Hadoop) — sugerem MapReduce, MongoDB, Postgres, NoSQL — mas com pesos e ordens ligeiramente diferentes, refletindo os dois ângulos distintos do mesmo problema (similaridade entre pessoas vs. similaridade entre coisas).

## Por Que Isso Importa
`cosine_similarity` é a única métrica de similaridade nova introduzida no livro (distinta de `distance` euclidiana usada em k-NN e clustering) — captura direção/padrão de interesse, não magnitude, o que a torna adequada para vetores binários esparsos. É o último capítulo técnico do livro; o Capítulo 25 (final) é uma retrospectiva/guia de próximos passos.
