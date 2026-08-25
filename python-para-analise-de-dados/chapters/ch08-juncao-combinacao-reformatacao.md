# Capítulo 8: Tratamento de dados: junção, combinação e reformatação

## Core Idea
Indexação hierárquica (`MultiIndex`), `merge`/`concat`/`combine_first` e `stack`/`unstack`/`pivot`/`melt` são as ferramentas com as quais o pandas expressa, respectivamente: dados de dimensão maior em formato tabular, junção estilo-SQL de tabelas, e conversão entre formato "longo" e "largo" — os três pilares de reorganizar dados que já foram limpos.

## Frameworks Introduced
- **MultiIndex (indexação hierárquica)**: múltiplos níveis de rótulo em um único eixo, permitindo representar dados N-dimensionais em uma estrutura 2D (`Series`/`DataFrame`).
  - Quando usar: quando os dados naturalmente têm 2+ chaves compostas (ex. estado+ano) e você quer indexação parcial (`data['b']`) e reshaping (`unstack`/`stack`) prontos.
  - Como: passar lista de arrays como `index=[[...],[...]]`; nomear níveis com `.index.names`; ordenar com `sort_index(level=)` para performance.
- **Merge estilo-SQL (`pd.merge`)**: junção de tabelas por uma ou mais chaves, com semântica `inner`/`left`/`right`/`outer` idêntica a bancos relacionais.
  - Quando usar: combinar duas tabelas por chave(s) compartilhada(s) (coluna ou índice).
  - Como: `pd.merge(df1, df2, on=..., how=...)`; usar `left_index=True`/`right_index=True` quando a chave está no índice; `suffixes=` para colunas homônimas.
- **Concatenação (`pd.concat`)**: empilhar objetos ao longo de um eixo, com controle explícito sobre união vs. interseção dos outros eixos e rastreabilidade da origem via `keys`.
  - Quando usar: juntar pedaços com a mesma estrutura (ex. mesmas colunas, linhas diferentes), não uma junção por chave.
- **Formato longo ↔ largo (`stack`/`unstack`, `pivot`/`melt`)**: dois pares de operações inversas para alternar entre "uma linha por observação" (longo, bom para bancos relacionais) e "uma coluna por variável" (largo, bom para leitura/análise).
  - Quando usar: `pivot` quando os dados vêm em formato longo (`date, item, value`) e você quer `item` como colunas; `melt` para o inverso (várias colunas de valor → duas colunas `variable`/`value`).

## Key Concepts
- **`data['b']` / `data.loc[:, 2]`**: indexação parcial em `MultiIndex` — seleciona por nível externo ou interno, respectivamente.
- **`swaplevel`/`sort_index(level=)`**: reordenam/ordenam níveis do `MultiIndex`; performance de seleção é muito melhor com o índice ordenado lexicograficamente pelo nível mais externo.
- **`set_index`/`reset_index`**: promovem coluna(s) a índice e vice-versa — operação inversa uma da outra.
- **`how=` em `merge`**: `'inner'` (interseção, default), `'left'`, `'right'`, `'outer'` (união) — junção muitos-para-muitos produz produto cartesiano das chaves repetidas.
- **`left_on`/`right_on` vs. `left_index`/`right_index`**: chave de junção pode vir de coluna(s) nomeadas diferentemente em cada tabela, ou do índice de uma ou ambas.
- **`DataFrame.join`**: atalho conveniente de `merge` orientado a índice, com junção `left` por padrão; aceita lista de DataFrames para combinar vários de uma vez.
- **`combine_first`**: "patch" de dados ausentes de um objeto com valores de outro, alinhado por rótulo — equivalente a `np.where(isnull(a), b, a)` mas com o alinhamento completo do pandas.
- **`pd.concat(objs, axis=, join=, keys=, ignore_index=)`**: `join='outer'` (default, união) vs `'inner'` (interseção); `keys=` cria um nível extra de índice identificando a origem de cada bloco; `ignore_index=True` descarta o índice original quando ele não carrega informação útil.
- **`stack`/`unstack(level=)`**: por padrão operam no nível mais interno; `unstack` pode introduzir `NaN` quando os subgrupos não têm o mesmo conjunto de rótulos no nível desempilhado; `stack(dropna=False)` preserva esses `NaN` em vez de filtrá-los.
- **`pivot(index, columns, values)`**: equivalente a `set_index([index, columns]).unstack(columns)`; omitir `values` produz colunas hierárquicas (uma por variável original).
- **`pd.melt(df, id_vars=, value_vars=)`**: operação inversa de `pivot` — funde várias colunas de valor em duas (`variable`, `value`), mantendo `id_vars` como identificador de grupo.

## Mental Models
- Pense em `MultiIndex` como uma forma de "esconder" dimensões extras num eixo 2D — `unstack` "abre" uma dimensão do índice para virar coluna; `stack` faz o inverso.
- Pense nas 4 opções de `how` do merge exatamente como junções SQL: a escolha determina que linhas *sem correspondência* sobrevivem no resultado, preenchidas com `NaN`.
- Formato longo é bom para armazenamento (schema fixo, fácil adicionar novos itens); formato largo é bom para leitura/plotagem humana — `pivot`/`melt` são a ponte entre os dois mundos.

## Anti-patterns
- **Não especificar `on=` em `merge` quando os nomes de coluna coincidentes não são intencionais**: `merge` sem `on` usa a interseção dos nomes de coluna — comportamento implícito arriscado; especificar `on=`/`left_on`/`right_on` explicitamente é mais seguro e mais legível.
- **Esperar que junção muitos-para-muitos preserve a contagem de linhas**: produz o produto cartesiano das chaves duplicadas — 3×2 linhas repetidas viram 6, não uma correspondência 1:1 "mágica".
- **Fazer merge/join com índice não ordenado em datasets grandes**: seleção em `MultiIndex` desordenado é significativamente mais lenta — ordenar com `sort_index(level=0)` antes de operações repetidas.
- **Usar `concat` para o que na verdade é uma junção por chave**: `concat` empilha; não alinha por valor de coluna — se a intenção é combinar por chave, o certo é `merge`.

## Code Examples
```python
import pandas as pd

# MultiIndex: reshape longo -> largo com pivot
pivoted = ldata.pivot('date', 'item', 'value')

# Equivalente explícito via set_index + unstack
unstacked = ldata.set_index(['date', 'item']).unstack('item')

# Operação inversa: largo -> longo
melted = pd.melt(df, id_vars=['key'], value_vars=['A', 'B'])
```
- **O que demonstra**: `pivot` e `melt` são operações inversas — o mesmo dado pode transitar entre formato longo (uma linha por observação, ótimo para storage) e largo (uma coluna por variável, ótimo para leitura) sem perda de informação.

## Reference Tables
| `how` em `merge` | Chaves no resultado |
|---|---|
| `'inner'` (default) | Interseção das chaves das duas tabelas |
| `'left'` / `'right'` | Todas as chaves da tabela à esquerda / direita |
| `'outer'` | União das chaves de ambas |

| Argumento `pd.concat` | Papel |
|---|---|
| `axis` | 0 = empilha linhas (default), 1 = empilha colunas |
| `join` | `'outer'` (união, default) / `'inner'` (interseção) nos outros eixos |
| `keys` | Cria nível extra de índice identificando a origem de cada bloco |
| `ignore_index` | Descarta índice original, gera `range(N)` novo |

## Worked Example
Conversão de macrodados econômicos (PIB, inflação, desemprego) do formato longo para largo: `ldata` tem colunas `date`, `item` (`'realgdp'`, `'infl'`, `'unemp'`), `value` — uma linha por combinação data×indicador. `ldata.pivot('date', 'item', 'value')` produz um `DataFrame` com uma linha por data e uma coluna por indicador — o formato "natural" para plotar séries temporais lado a lado. O autor mostra que isso é idêntico a `ldata.set_index(['date', 'item']).unstack('item')`, tornando explícito que `pivot` é açúcar sintático sobre `set_index` + `unstack`. Ao adicionar uma segunda coluna de valor (`value2`) e omitir o argumento `values` de `pivot`, o resultado ganha colunas hierárquicas (`value`/`value2` como nível externo, `item` como interno) — o mesmo padrão generalizado para múltiplas variáveis simultâneas.

## Key Takeaways
1. `MultiIndex` representa dados N-dimensionais em 2D; `stack`/`unstack` movem informação entre índice e colunas sem perdê-la.
2. `merge` é para combinar por **chave** (estilo SQL); `concat` é para **empilhar** blocos com a mesma estrutura; `combine_first` é para **fazer patch** de ausência entre dois objetos sobrepostos.
3. Sempre prefira especificar `on=`/`left_on`/`right_on` explicitamente em `merge` — não depender da inferência implícita de colunas em comum.
4. Junção muitos-para-muitos produz produto cartesiano das chaves repetidas — comportamento correto, mas fácil de subestimar o tamanho do resultado.
5. `pivot` (longo→largo) e `melt` (largo→longo) são inversas; `pivot` é equivalente a `set_index(...).unstack(...)`.
6. Ordene o `MultiIndex` (`sort_index(level=0)`) antes de operações de seleção repetidas em datasets grandes — impacta performance diretamente.

## Connects To
- **Ch 5**: pré-requisito — `reindex`, `loc`, alinhamento por rótulo já vistos ali no caso de índice simples.
- **Ch 7**: a limpeza (Ch 7) tipicamente precede a reorganização (Ch 8) num pipeline real.
- **Ch 10**: `groupby` usa `MultiIndex` extensivamente nos resultados de agregação.
- **Ch 11**: `PeriodIndex`, mencionado de passagem aqui (macrodados), é aprofundado no capítulo de séries temporais.
</content>
