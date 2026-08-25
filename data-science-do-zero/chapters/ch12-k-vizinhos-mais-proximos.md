# Capítulo 12 — K-Vizinhos Mais Próximos (k-NN)

## O Modelo
Premissa mínima: uma noção de **distância** + a ideia de que **pontos próximos são similares**. É o modelo preditivo mais simples do livro — não tenta explicar o fenômeno (prever meu voto pelos vizinhos não revela *por que* eu voto assim), só prever.

Algoritmo: dado `k` e um ponto novo, encontrar os `k` pontos rotulados mais próximos (usando `distance` do Capítulo 4) e deixá-los **votar** no rótulo.

- `raw_majority_vote(labels)` — voto majoritário simples via `Counter`, mas não trata empates.
- `majority_vote(labels)` — assume rótulos já ordenados do mais próximo ao mais distante; em caso de empate, **remove recursivamente o vizinho mais distante** (`labels[:-1]`) e tenta de novo até haver vencedor único. Sempre termina (na pior hipótese sobra 1 rótulo).
- `knn_classify(k, labeled_points, new_point)` — ordena todos os pontos rotulados por distância ao novo ponto, pega os `k` primeiros rótulos, aplica `majority_vote`.

## Exemplo: Linguagens de Programação Favoritas por Cidade
Dado `(localização, linguagem)` por cidade, testar k-NN via **leave-one-out**: para cada cidade, prever usando todas as outras como referência. `k=3` teve melhor acerto (59%) na comparação entre `k=1,3,5,7`. Visualização: classificar uma grade densa de pontos no mapa e colorir por linguagem prevista mostra que `k` pequeno gera fronteiras irregulares/ruidosas; `k` maior gera regiões mais suaves — mas nem sempre melhor acerto (k=7 teve pior desempenho que k=3 no experimento).

**Nota de pré-processamento**: se as dimensões não fossem comparáveis (como longitude/latitude aqui, que são), seria necessário redimensionar (Capítulo 10) antes de aplicar distância.

## A Maldição da Dimensionalidade
Em espaços de alta dimensão, pontos aleatórios tendem a ficar **longe uns dos outros** — demonstrado gerando pares de pontos aleatórios no hipercubo unitário para dimensões de 1 a 100 e medindo distância média e mínima (`random_point`, `random_distances`). Conforme a dimensão cresce:
- A distância média entre pontos cresce.
- A razão entre a distância mínima e a média **tende a 1** — ou seja, em alta dimensão o vizinho mais próximo não é muito mais próximo que a média, esvaziando o conceito de "vizinhança".

Intuição geométrica complementar: 50 pontos aleatórios cobrem bem o intervalo `[0,1]` em 1D, cobrem pior o quadrado unitário em 2D, e ainda pior o cubo em 3D — em dimensões mais altas restam grandes vazios sem pontos próximos de nada.

**Implicação prática**: k-NN degrada em problemas de alta dimensionalidade, a menos que haja estrutura real que efetivamente reduza a dimensão intrínseca dos dados — recomenda-se **redução de dimensionalidade** (PCA, Capítulo 10) antes de aplicar k-NN em dados com muitas features.

## Por Que Isso Importa
k-NN é o único modelo do livro que **não aprende parâmetros** — serve de contraponto conceitual aos modelos paramétricos dos capítulos seguintes (Naive Bayes, regressão, árvores, redes neurais), todos os quais tentam condensar o dataset em um conjunto fixo de parâmetros em vez de guardar (e comparar contra) todos os pontos.
