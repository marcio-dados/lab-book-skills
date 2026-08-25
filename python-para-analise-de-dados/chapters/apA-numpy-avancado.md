# Apêndice A: NumPy avançado

## Core Idea
Sob o `ndarray` existe um bloco de memória homogêneo interpretado via `dtype` + `shape` + `strides` — entender essa organização interna explica por que fatiamento é grátis (views), como broadcasting realmente decide compatibilidade, e como espremer desempenho quando as ferramentas de alto nível (pandas) não bastam.

## Frameworks Introduced
- **`ndarray` = ponteiro + dtype + shape + strides**: um array é uma "lente" sobre um bloco de memória; strides (bytes para pular por eixo) explicam por que fatias e transposições não copiam dados.
  - Quando usar: ao raciocinar sobre por que uma operação copia ou não, ou por que um layout de memória é mais rápido que outro.
- **Regra de broadcasting**: dois arrays são compatíveis se, comparando dimensões de trás para frente, cada par coincide ou um dos dois é 1; dimensões ausentes contam como 1.
  - Quando usar: sempre que uma operação envolve arrays de formatos diferentes; usar `np.newaxis`/`reshape` para forçar a dimensão "1" no eixo correto quando o broadcast automático não se aplica (ex. subtrair média por linha, não por coluna).
- **Métodos de instância de ufunc (`reduce`, `accumulate`, `outer`, `reduceat`)**: generalizam a redução/acumulação/produto-cruzado/"groupby local" para qualquer operação binária, não só as pré-definidas (`sum`, `cumsum`).
  - Quando usar: expressar uma agregação customizada sobre uma ufunc existente sem escrever um laço Python.

## Key Concepts
- **`strides`**: tupla de inteiros (bytes a pular por eixo); strides negativos permitem "andar para trás" na memória (ex. `arr[::-1]`).
- **Hierarquia de dtypes** (`np.integer`, `np.floating`, `np.number`...): `np.issubdtype(dtype, superclasse)` evita enumerar manualmente todos os subtipos numéricos; `dtype.mro()` mostra a cadeia completa.
- **`reshape`/`ravel`/`flatten`**: `reshape` e `ravel` não copiam quando os dados resultantes são contíguos; `flatten` sempre copia; uma dimensão `-1` em `reshape` é inferida automaticamente.
- **Ordem C (row-major) vs. Fortran (column-major)**: controla em que ordem os elementos são percorridos ao redefinir formato/linearizar (`order='C'`/`'F'`); afeta desempenho porque acesso contíguo aproveita melhor a cache da CPU.
- **`concatenate`/`vstack`/`hstack`/`split`**: funções gerais e atalhos para juntar/separar arrays ao longo de um eixo; `np.r_`/`np.c_` são atalhos ainda mais concisos (incluindo tradução de fatias em arrays).
- **`repeat`/`tile`**: replicam elementos individualmente (`repeat`) ou o array inteiro em bloco (`tile`); menos necessários em NumPy do que em outras linguagens porque broadcasting resolve boa parte desses casos.
- **`take`/`put`**: equivalentes a fancy indexing para leitura/escrita restritas a um único eixo; `put` sempre opera sobre a versão linearizada (ordem C), não aceita `axis`.
- **`np.newaxis`**: insere um eixo de tamanho 1 via indexação (`arr[:, np.newaxis]`), o idioma padrão para forçar compatibilidade de broadcasting num eixo específico.
- **Arrays estruturados (`dtype=[(nome, tipo), ...]`)**: representam registros heterogêneos (como uma struct C ou linha SQL) num único bloco de memória contíguo — ferramenta de baixo nível para I/O binário eficiente, não um substituto para `DataFrame`.
- **`argsort`/`lexsort`/`searchsorted`/`partition`**: `argsort` devolve índices que ordenam um array; `lexsort` ordena por múltiplas chaves (a última chave passada tem prioridade mais alta); `searchsorted` faz busca binária (posição de inserção); `partition`/`argpartition` separam os k menores elementos sem ordenar tudo (mais barato que sort completo).
- **`numba.jit`/`numba.vectorize`**: compila subconjunto de Python para código de máquina via LLVM — pode superar até a versão vetorizada do NumPy para laços explícitos, sem exigir reescrever em C.
- **`np.memmap`**: array cujo conteúdo vive em disco, lido/escrito em pedaços — permite trabalhar com dados maiores que a RAM disponível.

## Mental Models
- Pense em qualquer operação NumPy "sem cópia" (fatiamento, `reshape`, `ravel`, transposição) como apenas reinterpretar os mesmos bytes com strides diferentes — a cópia só acontece quando o layout de memória resultante não pode ser expresso como uma view.
- Ao errar em broadcasting, pense "comparando da direita para a esquerda, onde os tamanhos não coincidem e nenhum dos dois é 1?" — isso localiza exatamente o eixo problemático.
- Pense em memória contígua como "o que a cache da CPU consegue prefetch eficientemente" — operações ao longo do eixo contíguo (ordem C: linhas) são mais rápidas que ao longo do eixo não contíguo.

## Anti-patterns
- **Fazer broadcast sem ajustar a dimensão do array menor**: `arr - arr.mean(1)` falha porque `arr.mean(1)` tem shape `(4,)`, não `(4,1)` — sempre `reshape`/`np.newaxis` para alinhar a dimensão que deve ficar "1".
- **Usar `frompyfunc`/`vectorize` esperando desempenho de ufunc nativa**: ambas chamam uma função Python por elemento — ordens de magnitude mais lentas que ufuncs em C; usar apenas por conveniência de API, não por performance (Numba resolve isso).
- **Assumir que uma view de um array já ordenado/mutado é independente**: ordenar in-place (`arr.sort()`) ou mutar uma fatia se propaga ao array original — comportamento correto, mas fácil de esquecer.
- **Esperar ordem decrescente nativa em `sort`**: NumPy não tem argumento de ordem decrescente — usar fatiamento reverso (`arr[::-1]`) sobre o resultado ordenado (grátis, é view).

## Code Examples
```python
import numpy as np

# Broadcasting correto no eixo 1 (subtrair média de cada linha)
row_means = arr.mean(1)
demeaned = arr - row_means.reshape((-1, 1))  # ou row_means[:, np.newaxis]

# reduceat: "groupby de array" por fronteiras de bucket
np.add.reduceat(np.arange(10), [0, 5, 8])  # soma arr[0:5], arr[5:8], arr[8:]

# searchsorted + groupby: discretização vetorizada em buckets
bins = np.array([0, 100, 1000, 5000, 10000])
labels = bins.searchsorted(data)
pd.Series(data).groupby(labels).mean()
```
- **O que demonstra**: o idioma correto para broadcasting em eixo não-zero, e como `reduceat`/`searchsorted` resolvem "agregação por bucket" sem laço Python nem `pd.cut`.

## Reference Tables
| Método ufunc | Descrição |
|---|---|
| `reduce(x)` | Agrega valores por aplicações sucessivas da operação |
| `accumulate(x)` | Como `reduce`, mas preserva agregações parciais (equivalente a `cumsum` para `add`) |
| `outer(x, y)` | Produto cruzado par-a-par; shape resultante = `x.shape + y.shape` |
| `reduceat(x, bins)` | Redução local por fatias contíguas ("groupby" de array) |

| Algoritmo `sort` | Estável | Pior caso |
|---|---|---|
| `'quicksort'` (default) | Não | O(n²) |
| `'mergesort'` | Sim | O(n log n) |
| `'heapsort'` | Não | O(n log n) |

## Worked Example
Broadcasting em array 3D: dado `arr` com shape `(3,4,5)`, subtrair a média ao longo do eixo 2 (`depth_means = arr.mean(2)`, shape `(3,4)`) exige `arr - depth_means[:, :, np.newaxis]` para que o resultado tenha shape `(3,4,1)`, compatível por broadcasting com `(3,4,5)`. O autor generaliza isso numa função `demean_axis(arr, axis)` que constrói um indexador dinâmico (`[slice(None)]*arr.ndim` com `np.newaxis` no eixo alvo) — o padrão para "subtrair uma agregação ao longo de qualquer eixo, para arrays de qualquer dimensão", sem hardcode do número de dimensões.

## Key Takeaways
1. Fatiamento, `reshape`, `ravel` e transposição são views (sem cópia) sempre que o layout resultante for expressável via strides — economize cópia sabendo disso.
2. A regra de broadcasting compara dimensões da direita para a esquerda; use `np.newaxis`/`reshape` para forçar tamanho 1 no eixo que precisa de broadcast quando não é o eixo final.
3. Métodos de ufunc (`reduce`/`accumulate`/`outer`/`reduceat`) evitam laços Python para agregações customizadas sobre qualquer operação binária.
4. `argsort`/`lexsort`/`searchsorted`/`partition` são as ferramentas vetorizadas de ordenação indireta — preferíveis a laços manuais para ordenar por múltiplas chaves ou encontrar posição de inserção.
5. `numba.jit`/`vectorize` compilam Python puro para código de máquina — útil quando um laço explícito não pode ser vetorizado e o NumPy puro não basta.
6. Memória contígua (ordem C) importa para performance real em operações ao longo do eixo — verificável via `.flags`, ajustável via `.copy('C'/'F')`.

## Connects To
- **Ch 4**: pré-requisito direto — este apêndice aprofunda `ndarray`, broadcasting, ufuncs e ordenação já introduzidos ali.
- **Ch 7/10**: `cut`/`groupby` no pandas são construídos sobre os mesmos princípios de `searchsorted`/`reduceat` vistos aqui em versão NumPy pura.
</content>
