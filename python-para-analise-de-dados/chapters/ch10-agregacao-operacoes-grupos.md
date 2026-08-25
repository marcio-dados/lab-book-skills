# Capítulo 10: Agregação de dados e operações em grupos

## Core Idea
O padrão **separar-aplicar-combinar** (split-apply-combine, termo de Hadley Wickham) é o motor único por trás de `groupby`: separar os dados em grupos por uma ou mais chaves, aplicar uma função a cada grupo (agregação, transformação ou filtro), e combinar os resultados — mais expressivo que SQL porque a "função" pode ser qualquer código Python/pandas/NumPy.

## Frameworks Introduced
- **Split-apply-combine via `groupby`**: qualquer operação de grupo é uma instância desse padrão de 3 passos, independentemente de a "aplicação" ser uma agregação (`mean`), transformação (`fillna` por grupo) ou seleção (top-N por grupo).
  - Quando usar: sempre que a pergunta é "calcule/transforme X, mas separadamente para cada valor de Y".
  - Como: `df.groupby(chave).método()` para casos otimizados (Tabela 10.1); `.agg(func)` para agregação customizada; `.apply(func)` para o caso geral (função pode devolver escalar, Series ou DataFrame).
- **Chave de grupo como qualquer "coisa que produz um array de rótulos"**: array/lista, nome de coluna, dict/Series (mapeamento), ou função (chamada uma vez por rótulo de índice) — todos convergem para a mesma máquina interna.
  - Quando usar: escolher a forma mais direta para a informação de agrupamento disponível — não força os dados a uma coluna extra se um dict/função já expressa o mapeamento.
- **Tabela pivô / crosstab como `groupby` + reshape**: `pivot_table` é `groupby` + agregação + `unstack` empacotados; `crosstab` é `pivot_table` especializado em contagem/frequência.
  - Quando usar: `pivot_table` para resumir com uma função de agregação (default `mean`), com margens (subtotais) opcionais; `crosstab` para tabelas de frequência cruzada.

## Key Concepts
- **Objeto `GroupBy` é preguiçoso (lazy)**: `df.groupby(key)` não computa nada — só guarda o suficiente para aplicar operações depois.
- **Colunas "inconvenientes" (nuisance columns)**: colunas não-numéricas são automaticamente excluídas de agregações como `.mean()` sem aviso.
- **Iteração em `GroupBy`**: gera tuplas `(nome_grupo, porção_de_dados)`; com múltiplas chaves, o nome é uma tupla `(k1, k2)`. `dict(list(df.groupby(key)))` é uma receita útil para acessar grupos por nome.
- **`groupby(..., axis=1)`**: agrupa colunas em vez de linhas (ex. por `dtype`).
- **Seleção de subconjunto de colunas**: `df.groupby('k')['col']` é açúcar sintático para `df['col'].groupby(df['k'])` — evita agregar colunas desnecessárias em datasets grandes.
- **Agrupar por nível de índice hierárquico**: `df.groupby(level='nome_nivel', axis=)`.
- **`.agg(func|str|list|dict)`**: aceita nome de método como string (`'mean'`), função customizada, lista de funções/tuplas `(nome, func)` (evita nomes `<lambda>` no resultado), ou dict `{coluna: func(s)}` para aplicar funções diferentes por coluna.
- **Funções de agregação customizadas são mais lentas** que os métodos otimizados da Tabela 10.1 — overhead de reorganização de dados e chamadas de função por grupo.
- **`as_index=False`**: evita que as chaves de grupo virem índice hierárquico no resultado — mais barato que `reset_index()` posterior quando não se precisa do índice.
- **`group_keys=False`**: suprime o nível extra de índice que `apply` normalmente adiciona com o nome do grupo.
- **`grouped.apply(func, *args, **kwargs)`**: forma mais genérica; a função pode devolver DataFrame, Series ou escalar — pandas monta o resultado com `concat` internamente.
- **`cut`/`qcut` + `groupby`**: o objeto `Categorical` devolvido por `cut`/`qcut` é passável diretamente como chave de agrupamento — viabiliza análise de quantis/buckets.
- **`pivot_table(values, index, columns, aggfunc='mean', margins=, fill_value=)`**: `margins=True` adiciona subtotais `'All'`; `aggfunc=len`/`'count'` produz tabulação de frequência.
- **`pd.crosstab(a, b, margins=True)`**: atalho para `pivot_table` com `aggfunc='count'`.

## Mental Models
- Pense em `groupby` como uma "fábrica de sub-DataFrames": tudo que você faria manualmente com um laço `for` + filtro + concat, `groupby` faz internamente e de forma otimizada — só escreva a função que processa **um grupo**.
- Ao escolher entre `.agg`/`.apply`, pense na forma do retorno: um escalar por grupo → `.agg`; qualquer coisa mais elaborada (Series, DataFrame, top-N, regressão) → `.apply`.
- `groupby` sobre um `Categorical` de `cut`/`qcut` transforma "discretização" e "agregação por grupo" em uma única operação componível.

## Anti-patterns
- **Escrever uma função de agregação customizada quando existe equivalente otimizado (Tabela 10.1)**: `.agg(minha_func)` é sempre mais lento que `.sum()`/`.mean()`/`.std()` nativos — só personalize quando realmente não há equivalente.
- **Esperar que colunas não-numéricas sobrevivam a `.groupby(k).mean()`**: são descartadas silenciosamente ("nuisance columns") — se precisar delas, agregue-as separadamente com `first`/`last`.
- **Deixar `apply` devolver uma função lambda sem nome em uma lista de agregação**: gera coluna `'<lambda>'` difícil de identificar — usar tupla `(nome, func)`.
- **Usar `pivot_table`/`crosstab` sem `margins=True` quando subtotais são parte da pergunta de negócio**: força um segundo cálculo separado que já vem de graça com a flag.

## Code Examples
```python
import pandas as pd
import numpy as np

# split-apply-combine genérico: top-N por grupo, com args extras
def top(df, n=5, column='tip_pct'):
    return df.sort_values(by=column)[-n:]

tips.groupby(['smoker', 'day']).apply(top, n=1, column='total_bill')

# Preenchimento de NA com valor específico por grupo (closure sobre g.name)
fill_values = {'East': 0.5, 'West': -1}
fill_func = lambda g: g.fillna(fill_values[g.name])
data.groupby(group_key).apply(fill_func)

# Regressão OLS por grupo (statsmodels) — apply devolvendo uma Series por grupo
def regress(data, yvar, xvars):
    Y = data[yvar]
    X = data[xvars]
    X['intercept'] = 1.
    result = sm.OLS(Y, X).fit()
    return result.params

by_year.apply(regress, 'AAPL', ['SPX'])
```
- **O que demonstra**: `apply` é suficientemente genérico para expressar desde "top-N por grupo" até "regressão linear por grupo" — a única exigência é que a função devolva um objeto pandas ou escalar; tudo mais é responsabilidade do usuário.

## Reference Tables
| Método otimizado `GroupBy` | Descrição |
|---|---|
| `count`, `sum`, `mean`, `median` | Estatística sobre valores não-NA |
| `std`, `var` | Desvio-padrão/variância (n-1) |
| `min`, `max`, `first`, `last` | Extremos / primeiro-último não-NA |
| `prod` | Produto dos valores não-NA |

| Argumento `pivot_table` | Papel |
|---|---|
| `values` | Coluna(s) a agregar (default: todas numéricas) |
| `index` / `columns` | Chaves de agrupamento → linhas / colunas |
| `aggfunc` | Função de agregação (default `'mean'`) |
| `margins=True` | Adiciona subtotais/total geral (`'All'`) |
| `fill_value` | Substitui `NaN` no resultado |

## Worked Example
Preenchimento de valores ausentes com a média **do grupo**, não a média global: dado `data` (valores por estado dos EUA) e `group_key` (`'East'`/`'West'`), a receita é `data.groupby(group_key).apply(lambda g: g.fillna(g.mean()))`. Cada porção de dados (`g`) recebe sua própria `fillna(g.mean())` — Vermont (East, ausente) é preenchido com a média dos estados East, não com a média nacional. O autor generaliza isso para valores de preenchimento pré-definidos por grupo usando o atributo `g.name` (disponível automaticamente dentro do `apply`): `fill_func = lambda g: g.fillna(fill_values[g.name])`. Isso ilustra o padrão geral do capítulo — qualquer limpeza de dados "por grupo" (não só agregação) se expressa naturalmente com `groupby(...).apply(...)`.

## Key Takeaways
1. `groupby` é preguiçoso — nada é calculado até você chamar um método de agregação, `.agg`, ou `.apply`.
2. Escolha a chave de agrupamento pela forma mais direta disponível: coluna, array, dict/Series, ou função — todas são equivalentes internamente.
3. Prefira métodos otimizados (Tabela 10.1) a `.agg(func_customizada)` — a diferença de performance é real e cresce com o tamanho do dataset.
4. `.apply` é a ferramenta de propósito geral: qualquer coisa que devolva um objeto pandas ou escalar funciona (top-N, preenchimento por grupo, regressão, correlação).
5. `cut`/`qcut` produzem `Categorical` que pode ser usado diretamente como chave de `groupby` — combina discretização e agregação num só passo.
6. `pivot_table`/`crosstab` são conveniências sobre `groupby` + reshape; use `margins=True` quando subtotais fazem parte da pergunta.

## Connects To
- **Ch 7**: `cut`/`qcut` (discretização) introduzidos ali, retomados aqui como chave de agrupamento.
- **Ch 8**: `unstack`/`MultiIndex`, base estrutural dos resultados de `groupby` com múltiplas chaves e de `pivot_table`.
- **Ch 11**: agregação de séries temporais (`resample`) é tratada como um caso especial de `groupby`, com capítulo próprio.
- **Ch 14**: usa `groupby` extensivamente em exemplos reais (MovieLens, nomes de bebês, doações eleitorais).
</content>
