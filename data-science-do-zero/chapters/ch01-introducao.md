# Capítulo 1 — Introdução

## Ideia Central
O livro é construído em torno de uma narrativa fictícia: você foi contratado para liderar data science na "DataSciencester", uma rede social para cientistas de dados que nunca investiu em construir suas próprias ferramentas — então tudo será feito **do zero**, sem bibliotecas prontas, para entender os fundamentos antes de usar atalhos.

## O Que É Data Science?
Definição de trabalho adotada: um cientista de dados é alguém que **extrai conhecimento de dados desorganizados**. Exemplos citados de uso real: OkCupid (inferir compatibilidade a partir de respostas), Facebook (padrões de migração via localização), Target (modelo preditivo de gravidez a partir de compras), campanha Obama 2012 (segmentação de eleitores/doadores).

## Encontrando Conectores-Chave (grau de centralidade)
Dado `users` (lista de dicts com `id`/`name`) e `friendships` (lista de pares `(id, id)`), constrói-se a lista de amigos de cada usuário populando `user["friends"]`. A métrica mais simples de importância na rede é o **grau** (número de conexões), calculado ordenando `(user_id, number_of_friends(user))`.

**Limitação exposta desde já**: grau é fácil de calcular mas não corresponde sempre à intuição — no exemplo, "Thor" tem menos conexões que "Dunn" mas parece mais central na rede. Isso é adiado para o Capítulo 21 (medidas de centralidade mais ricas: intermediação, autovetor, PageRank).

## Cientistas de Dados Que Você Talvez Conheça (recomendação por amigos-de-amigos)
Primeira tentativa ingênua (`friends_of_friend_ids_bad`) itera amigos-de-amigos sem filtrar o próprio usuário nem amigos já existentes, gerando ruído. Versão corrigida usa `Counter` + funções auxiliares (`not_the_same`, `not_friends`) para contar amigos-em-comum excluindo o próprio usuário e amigos diretos.

Uma segunda dimensão de similaridade é o **interesse em comum**: dado `interests` (lista de pares `(user_id, interest)`), constroem-se dois índices invertidos com `defaultdict(list)` — `user_ids_by_interest` e `interests_by_user_id` — para achar rapidamente usuários com interesses sobrepostos (`most_common_interests_with`). Padrão: trocar busca linear repetida por **índice invertido** construído uma vez.

## Salários e Experiência
Ao agrupar salário por tempo de experiência (`tenure`) exato, o resultado é inútil (cada chave tem um único valor). Agrupar em **buckets** (`tenure_bucket`: menos de 2 / entre 2 e 5 / mais de 5 anos) produz uma média por grupo mais informativa, mas os cortes dos buckets foram escolhidos visualmente/à mão — o livro sinaliza que o correto é modelar o efeito de cada ano adicional de experiência sobre o salário (adiado para regressão linear, Capítulo 14).

## Contas Pagas
Observando que usuários com pouca OU muita experiência tendem a pagar, e os do meio não, o capítulo mostra um classificador manual por limiares (`if years_experience < 3.0 / < 8.5 / else`) — os cortes de novo vieram de inspeção visual, não de um modelo. Antecipa regressão logística (Capítulo 16).

## Tópicos de Interesse
Contagem de palavras simples (lowercase + split + `Counter`) sobre a lista de interesses para achar tópicos populares — falha em casos como "scikit-learn" (seria dividido em duas palavras). Antecipa técnicas melhores de extração de tópicos (Capítulo 20, NLP).

## Por Que Isso Importa
O capítulo estabelece o padrão do livro inteiro: cada problema de negócio simples aponta para um capítulo posterior mais rigoroso. Serve como mapa de motivação, não como referência técnica em si.
