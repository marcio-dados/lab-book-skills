# Capítulo 5: Introdução ao pandas

## Core Idea
`Series` e `DataFrame` são as duas estruturas de trabalho do pandas: combinam a velocidade vetorizada do NumPy com rótulos de eixo explícitos (índices), possibilitando alinhamento automático de dados heterogêneos — a diferença central em relação ao `ndarray`, que é homogêneo e sem rótulos.

## Frameworks Introduced
- **Alinhamento automático por índice**: operações aritméticas entre `Series`/`DataFrame` com índices diferentes produzem a união dos rótulos, preenchendo `NaN` onde não há correspondência (equivalente a um outer join automático).
  - Quando usar: sempre que combinar dados de fontes com identificadores parcialmente sobrepostos.
  - Como: usar operadores aritméticos diretamente, ou métodos como `.add(other, fill_value=0)` quando `NaN` no resultado não é desejado.
- **`loc` (rótulo) vs. `iloc` (posição)**: dois operadores de indexação explícitos e não ambíguos, em vez de sobrecarregar `[]`.
  - Quando usar: `loc` para selecionar por rótulo de linha/coluna; `iloc` para selecionar por posição inteira — nunca misturar semânticas dentro do mesmo `[]`.
  - Como: `df.loc[rótulo_linha, rótulo_coluna]`; `df.iloc[posição_linha, posição_coluna]`.
- **`apply`/`applymap`/`map`**: aplicar uma função em blocos de granularidade diferente — `apply` por coluna/linha (Series → escalar ou Series), `applymap` element-wise em todo o DataFrame, `map` element-wise em uma Series.
  - Quando usar: `apply` para agregações customizadas por eixo; `applymap`/`map` para transformação element-wise sem equivalente vetorizado direto.

## Key Concepts
- **`Series`**: array 1D rotulado (`index` + `values`); comporta-se como um "dicionário ordenado de tamanho fixo" — suporta `in`, seleção por rótulo, e é criável a partir de um `dict` (chaves viram índice, ordenadas).
- **`DataFrame`**: tabela retangular com índice de linha e coluna; internamente blocos 2D, não uma coleção de arrays 1D; pode ser pensado como "dicionário de Series compartilhando o índice".
- **`reindex`**: cria um novo objeto reorganizado segundo um novo índice, introduzindo `NaN` para rótulos ausentes; aceita `method='ffill'`/`'bfill'` para interpolação em dados ordenados.
- **`drop`**: remove entradas de um eixo (`axis=0` linhas, `axis=1`/`'columns'` colunas); `inplace=True` modifica e descarta os dados removidos (cuidado, é destrutivo).
- **Índices inteiros são ambíguos por design**: se o índice do eixo contém inteiros, `obj[-1]` levanta erro em vez de "adivinhar" rótulo vs. posição — use `loc`/`iloc` explicitamente.
- **`isnull`/`notnull`** (função top-level `pd.isnull` e método): forma padrão de detectar dados ausentes (`NaN`/`NA`).
- **Métodos de redução** (`sum`, `mean`, `describe`, `idxmax`, `cumsum`...): ignoram `NA` por padrão (`skipna=True`); aceitam `axis=0`(linhas)/`1`(colunas).
- **`corr`/`cov`/`corrwith`**: correlação e covariância par a par, alinhadas por índice, excluindo `NA`.
- **`unique`/`value_counts`/`isin`**: análise de valores distintos em uma `Series`; `value_counts` ordena por frequência decrescente por padrão.
- **Rótulos de índice duplicados**: permitidos (diferente de `set` Python); indexar um rótulo duplicado devolve uma `Series`/`DataFrame`, não um escalar — muda o tipo de retorno dependendo se há duplicata.

## Mental Models
- Pense em `Series` como "array + dicionário fundidos": suporta operações vetorizadas do NumPy e semântica de lookup por chave do dict, ao mesmo tempo.
- Pense na aritmética `DataFrame`/`Series` como um caso especial de broadcasting do NumPy, mas alinhado por rótulo em vez de por posição.
- `loc`/`iloc` existem porque `ix` (obsoleto) tentava adivinhar rótulo-vs-posição e falhava silenciosamente em índices inteiros — a lição de design é: torne a ambiguidade impossível de expressar, não tente resolvê-la automaticamente.

## Anti-patterns
- **Usar `frame.column_name` para criar uma nova coluna**: não funciona (só leitura); use `frame['nova_coluna'] = ...`.
- **Confiar em `obj[-1]` para "última posição" em Series com índice inteiro**: gera erro proposital, pois o pandas não arrisca adivinhar rótulo vs. posição — use `.iloc[-1]`.
- **`inplace=True` sem necessidade**: destrói os dados descartados permanentemente; usar a versão que retorna novo objeto por padrão, e reservar `inplace` para quando a economia de memória realmente importa.
- **Esquecer que uma coluna obtida por indexação (`frame['col']`) é uma view**: mutação in-place nela se reflete no DataFrame original; usar `.copy()` para independência.
- **Usar o operador `ix` (obsoleto)**: comportamento ambíguo entre rótulo e posição; o autor recomenda explicitamente não usá-lo — preferir `loc`/`iloc`.

## Code Examples
```python
import pandas as pd
import numpy as np

# Alinhamento automático: união dos índices, NaN onde não há correspondência
s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=['a', 'c', 'd', 'e'])
s2 = pd.Series([-2.1, 3.6, -1.5, 4, 3.1], index=['a', 'c', 'e', 'f', 'g'])
s1 + s2  # NaN em 'd', 'f', 'g' (sem correspondência em ambos)

# apply devolvendo múltiplos valores (Series) por coluna
def f(x):
    return pd.Series([x.min(), x.max()], index=['min', 'max'])
frame.apply(f)
```
- **O que demonstra**: alinhamento automático por rótulo (não por posição) e `apply` como ferramenta genérica de agregação por eixo, incluindo retorno multivalorado.

## Reference Tables
| Indexação DataFrame | O que faz |
|---|---|
| `df[val]` | Seleciona coluna(s); ou filtra linhas se `val` for array booleano/fatia |
| `df.loc[val]` / `df.loc[v1, v2]` | Seleciona linha(s) / linha(s)+coluna(s) por **rótulo** |
| `df.iloc[val]` / `df.iloc[i, j]` | Seleciona por **posição** inteira |
| `df.at[label, label]` / `df.iat[i, j]` | Escalar único, por rótulo / por posição |

| Método aritmético flexível | Operador |
|---|---|
| `add`/`radd` | `+` |
| `sub`/`rsub` | `-` |
| `div`/`rdiv` | `/` |
| `mul`/`rmul` | `*` |

| Método de desempate `rank` | Descrição |
|---|---|
| `'average'` (default) | Classificação média do grupo empatado |
| `'min'` / `'max'` | Usa o mínimo/máximo do grupo |
| `'first'` | Ordem de ocorrência nos dados |

## Worked Example
Construção de um `DataFrame` a partir de um dicionário de dicionários aninhados: `pop = {'Nevada': {2001: 2.4, 2002: 2.9}, 'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}`. O pandas interpreta as chaves externas (`'Nevada'`, `'Ohio'`) como colunas e as internas (anos) como índice de linha, unindo e ordenando os anos que aparecem em qualquer uma das séries — anos ausentes em uma chave viram `NaN` (ex. Nevada em 2000). Isso ilustra o princípio geral do capítulo: toda estrutura heterogênea de entrada (dict de dicts, dict de listas, dict de Series) é normalizada para a mesma tabela retangular indexada, com `NaN` explícito preenchendo o que não existe — nunca erro silencioso ou truncamento.

## Key Takeaways
1. `Series`/`DataFrame` alinham por rótulo automaticamente em operações aritméticas — entenda isso antes de somar objetos com índices diferentes (gera `NaN`, não erro).
2. Use `loc` para rótulo e `iloc` para posição, sempre — nunca dependa de indexação `[]` ambígua para seleção de linha por posição.
3. `reindex` + `fill_value`/`method='ffill'` é a ferramenta padrão para preencher lacunas ao realinhar dados.
4. `apply` (por eixo) e `applymap`/`map` (element-wise) cobrem a maioria das transformações que não têm um método vetorizado dedicado.
5. `value_counts`, `unique`, `isin` são o kit básico para explorar a distribuição de valores em uma coluna categórica.
6. Rótulos de índice podem ser duplicados — saiba que isso muda o tipo de retorno da indexação (escalar vs. Series/DataFrame).
7. Prefira os métodos aritméticos nomeados (`.add`, `.sub`, `.div` com `fill_value`) a operadores infixos quando dados ausentes não devem virar `NaN`.

## Connects To
- **Ch 4**: pandas herda o estilo vetorizado do NumPy; `ndarray` é a estrutura subjacente de `values`.
- **Ch 6**: carga de dados de arquivos para `DataFrame` (`read_csv` etc.) — esta seção assumiu os dados já em memória.
- **Ch 7**: tratamento mais profundo de dados ausentes (`fillna`, `dropna`) além do básico de `isnull`/`skipna` visto aqui.
- **Ch 8**: indexação hierárquica (`MultiIndex`), mencionada mas não desenvolvida neste capítulo.
</content>
