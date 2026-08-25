# Capítulo 4: Básico sobre o NumPy: arrays e processamento vetorizado

## Core Idea
O `ndarray` do NumPy é o contêiner de dados homogêneos, contíguo em memória, que permite expressar operações em lote ("vetorização") sem laços `for` explícitos — 10 a 100x mais rápido que Python puro — e é a "língua franca" sobre a qual pandas e todo o ecossistema científico Python são construídos.

## Frameworks Introduced
- **Vetorização**: substituir laços `for` explícitos por expressões de array inteiras (`arr * 2`, `np.sqrt(arr)`, `np.where(cond, x, y)`).
  - Quando usar: qualquer transformação element-wise ou lógica condicional aplicada a um array inteiro.
  - Como: escrever a operação matemática/lógica diretamente sobre o array; usar `np.where` no lugar de list comprehensions com `if/else`.
- **Views vs. cópias**: fatias (`slices`) de um `ndarray` são visualizações da memória original (sem cópia); indexação booleana e indexação sofisticada (fancy indexing) sempre copiam.
  - Quando usar: entender isso é essencial antes de mutar uma fatia — mutação se propaga ao array original.
  - Como: usar `.copy()` explicitamente quando uma cópia independente é necessária.
- **Ufuncs (funções universais)**: wrappers vetorizados rápidos, unários (`sqrt`, `exp`) ou binários (`add`, `maximum`), que operam element-wise em `ndarray`s.
  - Quando usar: qualquer transformação matemática element-wise em vez de laço Python.
  - Como: chamar `np.<func>(arr)`; usar o argumento `out` para operar in-place e evitar alocação.

## Key Concepts
- **`shape`**: tupla com o tamanho de cada dimensão do array.
- **`dtype`**: metadado que descreve o tipo de dado armazenado (ex. `float64`, `int32`); `ndarray` é homogêneo — todos os elementos compartilham o mesmo `dtype`.
- **`astype`**: converte (faz cast d)o array para outro `dtype`, sempre criando uma cópia; truncar float→int descarta a parte decimal.
- **Broadcasting**: regras para operações aritméticas entre arrays de formatos diferentes (aprofundado no Apêndice A).
- **Indexação booleana**: usar um array de `True`/`False` (do mesmo tamanho do eixo) para selecionar/filtrar/atribuir; combine condições com `&`/`|` (nunca `and`/`or` — não funcionam com arrays).
- **Indexação sofisticada (fancy indexing)**: indexar com listas/arrays de inteiros; sempre copia os dados; resultado combinando múltiplas listas de índices é 1D (não retangular) — para região retangular, indexe em dois passos ou use `np.ix_`.
- **`np.where(cond, x, y)`**: versão vetorizada da expressão ternária `x if cond else y`; `x`/`y` podem ser escalares ou arrays.
- **Métodos de agregação (`sum`, `mean`, `std`, `cumsum`, `cumprod`, `any`, `all`)**: aceitam `axis` (0 = ao longo das linhas, 1 = ao longo das colunas); `any`/`all` são idiomáticos para arrays booleanos.
- **`np.unique`, `np.in1d`**: operações de conjunto em arrays 1D (equivalentes vetorizados de `sorted(set(...))` e teste de pertinência).
- **`numpy.random.RandomState`**: gerador de números aleatórios isolado (evita depender do estado global de `np.random.seed`).

## Mental Models
- Pense no `ndarray` como "um bloco contíguo de memória + metadados (`shape`, `dtype`)" — é isso que permite que algoritmos em C operem sem overhead de verificação de tipo.
- Ao indexar arrays multidimensionais, pense nos eixos como coordenadas: `arr[i, j]` é equivalente (mas mais eficiente) a `arr[i][j]`.
- Fatiamento = visualização (barato, compartilha memória); indexação booleana/sofisticada = cópia (mais caro, mas seguro para mutar sem afetar o original).

## Anti-patterns
- **Assumir que `np.empty` devolve zeros**: pode conter "lixo" de memória não inicializada — use `np.zeros` quando precisar de valores determinísticos.
- **Usar `and`/`or` Python em condições com arrays**: levanta erro ou comportamento incorreto; use `&`/`|` com parênteses em cada condição.
- **Confiar que a indexação booleana falha se o array de máscara tiver tamanho errado**: ela não falha — silenciosamente produz resultado incorreto. Verifique os tamanhos manualmente.
- **Reimplementar `x if c else y` com list comprehension sobre arrays grandes**: lento (interpretado) e não generaliza para multidimensional — use `np.where`.
- **Esperar que `arr[[i1,i2],[j1,j2]]` retorne uma submatriz retangular**: fancy indexing com múltiplas listas seleciona pares `(i,j)` específicos (resultado 1D), não o produto cartesiano — para retângulo, indexe em dois passos (`arr[[i1,i2]][:, [j1,j2]]`).

## Code Examples
```python
import numpy as np

# Vetorização vs. Python puro: mesma operação, 10-100x mais rápida
my_arr = np.arange(1_000_000)
my_arr2 = my_arr * 2  # sem laço for

# np.where: ternário vetorizado, substitui list comprehension com zip
result = np.where(cond, xarr, yarr)

# Indexação booleana combinada com seleção de colunas
data[names == 'Bob', 2:]

# Passeio aleatório vetorizado (5000 simulações de uma vez)
draws = np.random.randint(0, 2, size=(nwalks, nsteps))
steps = np.where(draws > 0, 1, -1)
walks = steps.cumsum(1)
hits30 = (np.abs(walks) >= 30).any(1)
crossing_times = (np.abs(walks[hits30]) >= 30).argmax(1)
```
- **O que demonstra**: como recursos vetorizados (`where`, `cumsum`, indexação booleana, `argmax`) compõem simulações inteiras sem nenhum laço `for` explícito em Python.

## Reference Tables
| Função de criação | Descrição |
|---|---|
| `array` | Converte sequência em `ndarray`, copiando por padrão |
| `asarray` | Como `array`, mas não copia se a entrada já é `ndarray` |
| `arange` | Como `range`, mas devolve `ndarray` |
| `zeros`/`ones`/`empty` (+ `_like`) | Arrays preenchidos com 0/1/não inicializado |
| `full`/`full_like` | Array preenchido com valor arbitrário |
| `eye`/`identity` | Matriz identidade N×N |

| Ufunc unária | Descrição |
|---|---|
| `sqrt`, `square`, `exp` | Raiz quadrada, quadrado, exponencial |
| `log`, `log10`, `log2`, `log1p` | Logaritmos |
| `sign`, `ceil`, `floor`, `rint` | Sinal, teto, piso, arredondamento |
| `modf` | Partes fracionária/inteira (2 arrays de saída) |
| `isnan`, `isfinite`, `isinf` | Testes de valor |

| Método `numpy.linalg` | Descrição |
|---|---|
| `dot` | Multiplicação de matrizes (também `x.dot(y)` ou `x @ y`) |
| `inv` | Inversa de matriz quadrada |
| `qr`, `svd` | Decomposição QR / SVD |
| `solve` | Resolve `Ax = b` |

## Worked Example
Simulação de passeio aleatório (random walk): a versão em Python puro usa um laço `for` de 1000 passos chamando `random.randint` a cada iteração e acumulando em uma lista. A versão vetorizada gera todos os 1000 sorteios de uma vez (`np.random.randint(0, 2, size=1000)`), converte para passos `+1`/`-1` com `np.where`, e obtém a trajetória inteira com `.cumsum()` — uma única chamada em vez de 1000 iterações Python. Estendendo para 5.000 passeios simultâneos, basta passar `size=(nwalks, nsteps)`: o mesmo padrão (`where` + `cumsum(axis=1)`) opera na matriz inteira, e perguntas como "quantos passeios cruzaram ±30" (`(np.abs(walks) >= 30).any(1)`) ou "em qual passo isso aconteceu" (`argmax(1)` sobre a máscara booleana, já que `True` é o valor máximo) tornam-se agregações de uma linha, sem laços.

## Key Takeaways
1. Vetorize: prefira expressões de array (`arr * 2`, `np.where`, ufuncs) a laços `for` — ganho de 10-100x é típico.
2. Fatias são views (mutação se propaga); indexação booleana/fancy indexing sempre copia — saiba qual está usando.
3. Use `&`/`|` (nunca `and`/`or`) para combinar condições booleanas em arrays.
4. `np.where(cond, x, y)` é o ternário vetorizado — funciona também em multidimensional, o que list comprehensions não fazem de forma eficiente.
5. Agregações (`sum`, `mean`, `cumsum`, `any`, `all`) aceitam `axis`; `axis=0` reduz ao longo das linhas, `axis=1` ao longo das colunas.
6. `np.unique`/`np.in1d` são os equivalentes vetorizados de operações de conjunto Python (`set`, `in`).
7. Prefira `numpy.random.RandomState` a `np.random.seed` global quando isolamento de estado importa (ex. testes, reprodutibilidade em paralelo).

## Connects To
- **Ch 5**: `Series`/`DataFrame` do pandas são construídos sobre `ndarray` e herdam grande parte dessa semântica de indexação/vetorização.
- **Ap. A**: aprofunda broadcasting, `reshape`, ordenação avançada e mais detalhes de NumPy deixados fora do fluxo principal.
- **Ch 9**: `matplotlib.pyplot.imshow`/`plot` usados aqui para visualizar arrays 2D são retomados em profundidade.
</content>
