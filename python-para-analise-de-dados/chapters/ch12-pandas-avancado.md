# Capítulo 12: Pandas avançado

## Core Idea
Três recursos "de usuário avançado" fecham o domínio prático do pandas: o tipo `Categorical` (representação codificada por inteiros, ganho de memória/performance), `transform`/`TimeGrouper` (variações de `groupby` para casos que `apply` resolve de forma menos idiomática ou eficiente), e encadeamento de métodos (`assign`/`pipe`) para expressar pipelines sem variáveis temporárias descartáveis.

## Frameworks Introduced
- **Representação categorizada (dictionary-encoding)**: armazenar uma coluna de valores repetidos como (a) um array pequeno de categorias distintas + (b) um array de códigos inteiros que referenciam essas categorias — o mesmo padrão de "tabela de dimensão" de data warehousing.
  - Quando usar: colunas com poucos valores distintos repetidos muitas vezes (baixa cardinalidade) em datasets grandes.
  - Como: `df['col'] = df['col'].astype('category')`; ganho de memória e velocidade em `groupby` vêm de graça.
- **`transform` como `apply` restrito e mais rápido**: a função passada deve devolver um escalar (broadcast) ou um objeto do mesmo formato do grupo — nunca modifica a entrada.
  - Quando usar: quando o resultado precisa ter o mesmo índice/formato da entrada original (ex. substituir cada valor pela média do seu grupo) — mais idiomático e potencialmente mais rápido que `apply` + reindex manual.
  - Como: `g.transform('mean')` (usa o "atalho rápido" das agregações otimizadas) ou `g.transform(lambda x: ...)` para lógica customizada.
- **Encadeamento de métodos (`assign`, `pipe`, indexação com callable)**: expressar uma sequência de transformações como uma única expressão fluente, sem variáveis intermediárias descartáveis.
  - Quando usar: pipelines de limpeza/transformação onde cada passo alimenta o próximo e as variáveis intermediárias não têm valor próprio.
  - Como: `.assign(nova_col=lambda x: ...)` para atribuição funcional (não in-place); `.pipe(minha_func, *args)` para funções customizadas/de terceiros que aceitam e devolvem DataFrame/Series.

## Key Concepts
- **`pandas.Categorical`**: tem atributos `.categories` (valores distintos) e `.codes` (inteiros que referenciam `.categories`); acessível numa Series via `.cat.codes`/`.cat.categories`.
- **`Categorical.from_codes(codes, categories, ordered=)`**: constrói diretamente a partir de códigos já codificados externamente; `ordered=True` estabelece relação de ordem entre categorias (`foo < bar < baz`).
- **Transformações baratas em `Categorical`**: renomear categorias ou adicionar novas no fim não exige tocar nos códigos — operação O(1) nas categorias, não O(n) nos dados.
- **`astype('category')`**: custo pago uma vez na conversão; depois disso, `groupby` e outras operações em geral ficam mais rápidas e usam muito menos memória (o autor demonstra ~8x menos memória em 10M de linhas com 4 categorias).
- **Métodos `.cat.*`** (`set_categories`, `remove_unused_categories`, `add_categories`, `rename_categories`, `reorder_categories`): manipulam o conjunto de categorias sem tocar nos dados observados; `remove_unused_categories` é útil após filtrar um DataFrame grande.
- **`pd.get_dummies` em `Categorical`**: mesma operação de codificação one-hot já vista no Ch 7, agora explicada como consumidora natural do tipo `Categorical`.
- **`grouped.transform('mean')`**: "atalho rápido" — usa a implementação otimizada da agregação e faz broadcast automaticamente para o formato original, mais rápido que `apply` equivalente.
- **`TimeGrouper`**: permite combinar `resample` com uma chave de agrupamento adicional (ex. `groupby(['key', pd.TimeGrouper('5min')])`) — exige que o tempo seja o índice.
- **`DataFrame.assign(col=valor|callable)`**: alternativa funcional a `df['col'] = valor`; não modifica in-place, devolve novo objeto — habilita encadeamento fluente.
- **Indexação com `lambda`/callable** (`df[lambda x: x['col'] < 0]`): permite referenciar o objeto "atual" da cadeia sem atribuí-lo a uma variável nomeada.
- **`.pipe(func, *args, **kwargs)`**: `df.pipe(f, arg1=v1)` é equivalente a `f(df, arg1=v1)`, mas permite encadeamento fluente com funções customizadas/de terceiros (não só métodos nativos do pandas).

## Mental Models
- Pense em `Categorical` como "guardar o índice de uma tabela de dimensão em vez do valor por extenso" — o ganho de memória/velocidade vem exatamente da mesma lógica de normalização de banco de dados.
- Pense em `transform` como "`apply` com uma promessa extra": o formato do resultado é previsível (escalar broadcast ou mesmo formato da entrada) — isso é o que permite o atalho de performance.
- Pense em encadeamento de métodos (`assign`/`pipe`/callable-indexing) como trocar "estado nomeado em variáveis" por "estado implícito na posição da cadeia" — ganha legibilidade de pipeline, perde a capacidade de inspecionar passos intermediários facilmente.

## Anti-patterns
- **Converter para `category` colunas de alta cardinalidade (quase todos os valores distintos)**: perde o benefício de memória/performance — o ganho vem de poucas categorias repetidas muitas vezes.
- **Usar `apply` quando `transform` resolveria**: perde o atalho de performance das agregações otimizadas e escreve mais código para reindexar o resultado no formato original.
- **Encadear métodos ao ponto de esconder passos de depuração importantes**: o autor nota explicitamente que é "questão de gosto pessoal" — separar em passos nomeados pode ser mais legível quando o pipeline é complexo ou precisa de inspeção intermediária.
- **Esquecer que `assign` não modifica in-place**: `df.assign(k=v)` devolve um novo objeto; `df['k'] = v` é a versão que modifica in-place — confundir as duas leva a "a coluna não apareceu" quando o retorno de `assign` não foi capturado.

## Code Examples
```python
import pandas as pd

# Conversão para category: ganho de memória em dado repetitivo
df['fruit'] = df['fruit'].astype('category')

# transform: substitui cada valor pela média do seu grupo (mesmo formato da entrada)
g = df.groupby('key').value
normalized = (df['value'] - g.transform('mean')) / g.transform('std')

# Encadeamento fluente com assign + pipe + indexação por callable
result = (load_data()
          [lambda x: x.col2 < 0]
          .assign(col1_demeaned=lambda x: x.col1 - x.col1.mean())
          .groupby('key')
          .col1_demeaned.std())
```
- **O que demonstra**: `transform` como ferramenta de "normalização por grupo" sem laços manuais, e o estilo de encadeamento fluente que evita variáveis temporárias descartáveis usando `assign` + indexação por `lambda`.

## Reference Tables
| Método `.cat.*` | Descrição |
|---|---|
| `add_categories` | Adiciona categorias novas (não usadas) no fim |
| `remove_categories` | Remove categorias, valores viram nulo |
| `remove_unused_categories` | Remove categorias que não aparecem nos dados |
| `set_categories` | Substitui o conjunto de categorias (pode adicionar/remover) |
| `rename_categories` / `reorder_categories` | Renomeia / renomeia+reordena categorias |

| Ferramenta de encadeamento | Papel |
|---|---|
| `df.assign(col=valor\|callable)` | Atribuição funcional (não in-place) |
| `df[lambda x: cond]` | Filtro sem nomear variável intermediária |
| `df.pipe(func, *args)` | Encadeia função customizada que aceita/devolve DataFrame |

## Worked Example
Comparação de memória para uma coluna repetitiva: com 10 milhões de linhas e apenas 4 valores distintos (`'foo'`, `'bar'`, `'baz'`, `'qux'`), a versão `object` (`labels`) usa `labels.memory_usage()` ≈ 80.000.080 bytes, enquanto a versão `category` (`categories = labels.astype('category')`) usa `categories.memory_usage()` ≈ 10.000.272 bytes — quase 8x menos. O autor destaca que a conversão em si tem custo (medido com `%time`), mas é pago uma única vez, enquanto o ganho em `groupby` e outras operações se repete a cada uso subsequente — o trade-off clássico de pré-processamento único vs. economia recorrente.

## Key Takeaways
1. `category` compensa quando há poucos valores distintos repetidos muitas vezes — ganho real de memória e velocidade em `groupby`, pago com um custo único de conversão.
2. `transform` é a ferramenta certa quando o resultado deve ter o mesmo formato da entrada (normalização por grupo, broadcast de agregação) — mais rápida e mais idiomática que `apply` equivalente.
3. `TimeGrouper` combina `resample` com uma chave de agrupamento adicional, mas exige que o tempo seja o índice.
4. `assign`/`pipe`/indexação por `lambda` habilitam pipelines fluentes sem variáveis temporárias — trade-off consciente entre legibilidade de fluxo e facilidade de depuração passo a passo.
5. `pipe` é o ponto de entrada certo para incluir funções customizadas (não métodos nativos do pandas) numa cadeia fluente.

## Connects To
- **Ch 7**: `get_dummies`/`cut`/`qcut` retomados aqui como consumidores/produtores naturais de `Categorical`.
- **Ch 10**: `groupby`/`apply` são pré-requisito direto; `transform` é apresentado como variação mais restrita e específica.
- **Ch 11**: `resample`/`TimeGrouper` estendem o capítulo de séries temporais para o caso de múltiplas séries com chave de grupo adicional.
</content>
