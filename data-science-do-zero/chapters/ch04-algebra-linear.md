# Capítulo 4 — Álgebra Linear

## Vetores como Listas
Vetores são representados como listas de números Python (ex.: `[altura, peso, idade]`). Como listas puras não suportam aritmética, o capítulo constrói do zero as operações necessárias:

- `vector_add(v, w)` / `vector_subtract(v, w)` — soma/subtração componente a componente via `zip` + compreensão de lista.
- `vector_sum(vectors)` — soma uma lista de vetores; pode ser reescrita como `reduce(vector_add, vectors)`.
- `scalar_multiply(c, v)` — multiplica cada componente por um escalar.
- `vector_mean(vectors)` — média componente a componente (`scalar_multiply(1/n, vector_sum(vectors))`).
- `dot(v, w)` — **produto escalar**: soma dos produtos componente a componente. Interpretação geométrica: o quanto `v` se estende na direção de `w` (projeção).
- `sum_of_squares(v) = dot(v, v)`, `magnitude(v) = sqrt(sum_of_squares(v))`.
- `distance(v, w) = magnitude(vector_subtract(v, w))` — distância euclidiana.

**Aviso explícito do autor**: usar listas Python como vetores é didaticamente claro mas ruim em desempenho — em produção, usar **NumPy**.

## Matrizes como Listas de Listas
`A[i][j]` = elemento da linha `i`, coluna `j` (indexação a partir de 0). `shape(A)` retorna `(num_rows, num_cols)`. `get_row`/`get_column` extraem vetores de uma matriz. `make_matrix(num_rows, num_cols, entry_fn)` constrói uma matriz aplicando uma função geradora a cada posição `(i,j)` — usada para gerar, por exemplo, a matriz identidade (`entry_fn = is_diagonal`).

## Três Usos de Matrizes no Livro
1. **Representar um dataset**: cada linha é um vetor/observação (ex.: matriz 1000×3 de altura/peso/idade de 1000 pessoas).
2. **Representar uma função linear** que mapeia vetores de dimensão `k` para dimensão `n` (revisitado em capítulos posteriores).
3. **Representar uma relação binária/grafo**: matriz de adjacência `A[i][j] = 1` se os nós `i,j` estão conectados. Comparado à lista de arestas do Capítulo 1, a matriz de adjacência troca economia de memória (esparsa) por velocidade de consulta O(1) (`friendships[i][j]`) em vez de busca linear.

## Por Que Isso Importa
As funções `dot`, `magnitude`, `distance`, `vector_mean` e `make_matrix` são reutilizadas literalmente (sem redefinição) em quase todos os capítulos de aprendizado de máquina que seguem (k-NN, gradiente descendente, PCA/redução de dimensionalidade, redes neurais).
