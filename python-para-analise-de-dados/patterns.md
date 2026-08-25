# Padrões e Técnicas — Python para Análise de Dados

## Split-Apply-Combine (groupby)
**Quando usar**: calcular estatística/transformação separadamente por grupo (categoria, período, chave composta).
**Como**: `df.groupby(chave)` (chave: coluna, array, dict/Series, ou função) → `.agg(func|str|list|dict)` para agregação, `.transform(func)` quando o resultado deve ter o mesmo formato da entrada, `.apply(func)` para o caso geral (retorno arbitrário: escalar, Series, DataFrame).
**Trade-offs**: `.agg`/`.transform` com métodos nativos (`'mean'`, `'sum'`) são muito mais rápidos que funções Python customizadas em `.apply` — overhead de chamada de função e reorganização de dados por grupo.

## Alinhamento automático + `fill_value`
**Quando usar**: combinar Series/DataFrames com índices parcialmente sobrepostos sem perder dados de nenhum lado.
**Como**: operador aritmético direto (`a + b`) produz `NaN` onde não há correspondência; usar `.add(b, fill_value=0)` (ou `.sub`/`.div`/`.mul` equivalentes) quando `NaN` deve virar o valor neutro em vez de propagar.
**Trade-offs**: `fill_value` assume que ausência = neutro (0 para soma) — nem sempre correto; avaliar semântica do domínio antes.

## Discretização + agregação por bucket (`cut`/`qcut` + `groupby`)
**Quando usar**: transformar variável contínua em categorias e depois agregar por essas categorias.
**Como**: `pd.cut(dados, bins, labels=)` (fronteiras fixas) ou `pd.qcut(dados, q)` (quantis, contagem igual por bucket); o `Categorical` resultante é usável direto como chave de `groupby`.
**Trade-offs**: `cut` produz buckets de tamanho desigual (interpretável por domínio); `qcut` produz buckets balanceados (melhor para comparação estatística entre grupos).

## Formato longo ↔ largo (`pivot`/`melt`, `stack`/`unstack`)
**Quando usar**: alternar entre "uma linha por observação" (armazenamento, schema flexível) e "uma coluna por variável" (leitura humana, plotagem).
**Como**: `df.pivot(index, columns, values)` (longo→largo) ou `pd.melt(df, id_vars=, value_vars=)` (largo→longo); `set_index([...]).unstack()` é a forma explícita equivalente a `pivot`.
**Trade-offs**: formato largo com muitas categorias distintas gera muitas colunas esparsas (`NaN`); formato longo é mais compacto mas exige `groupby`/`pivot` para leitura direta.

## Junção por chave vs. concatenação por posição
**Quando usar**: `merge` quando as tabelas se relacionam por valor de chave (estilo SQL); `concat` quando são blocos com a mesma estrutura a empilhar.
**Como**: `pd.merge(a, b, on=/left_on=/right_on=, how=)`; `pd.concat([a, b], axis=, join=, keys=)`.
**Trade-offs**: `merge` muitos-para-muitos produz produto cartesiano das chaves repetidas — pode explodir o tamanho do resultado; sempre checar a cardinalidade esperada antes.

## Vetorização em vez de laço Python
**Quando usar**: qualquer transformação element-wise ou lógica condicional aplicada a um array/coluna inteira.
**Como**: expressões de array (`arr * 2`, `np.where(cond, x, y)`), ufuncs (`np.sqrt`), métodos `Series.str.*` (NA-safe) em vez de `.map(lambda)`.
**Trade-offs**: ganho de 10-100x é típico; a única exceção é lógica que genuinamente não se expressa como operação de array (nesse caso, `rolling(...).apply(func)` ou Numba/Cython).

## Normalização por grupo
**Quando usar**: calcular proporção/z-score/percentual dentro de cada grupo (não globalmente).
**Como**: `g = df.groupby(chave); (df[col] - g[col].transform('mean')) / g[col].transform('std')`, ou `df[col] / g[col].transform('sum')` para proporção.
**Trade-offs**: `transform` (broadcast automático) é preferível a `apply` + reindex manual — mais idiomático e com o "atalho rápido" de agregações nativas.

## Achatamento de JSON aninhado
**Quando usar**: cada registro de um feed JSON tem uma lista aninhada (ex. nutrientes de um alimento, itens de um pedido).
**Como**: para cada registro, `pd.DataFrame(registro['lista_aninhada'])` + adicionar coluna de id do registro pai; `pd.concat` de todas as listas; `drop_duplicates()` antes de qualquer merge subsequente.
**Trade-offs**: duplicatas são comuns nesse padrão — sempre checar `duplicated().sum()` antes de prosseguir.

## Imputação de ausência com estatística do treino
**Quando usar**: preparar dados para modelagem estatística/ML que não aceita `NaN`.
**Como**: `valor_imputado = train[col].median()` (ou `.mean()`); aplicar `fillna(valor_imputado)` idênticamente em treino e teste — nunca recalcular no teste.
**Trade-offs**: mediana é robusta a outliers mas ignora estrutura (ex. imputação por grupo pode ser mais precisa, ao custo de mais complexidade).

## Resample como groupby temporal
**Quando usar**: converter frequência de série temporal (downsampling com agregação, upsampling com interpolação).
**Como**: `ts.resample(freq).mean()` (downsampling); `ts.resample(freq).ffill()`/`.asfreq()` (upsampling); controlar bordas com `closed=`/`label=`.
**Trade-offs**: escolha de `closed`/`label` afeta a qual bucket cada timestamp de borda é atribuído — não há default "correto" universal, depende da semântica do domínio (ex. dados financeiros de mercado costumam usar `closed='right'`).

## Encadeamento de métodos sem variáveis temporárias
**Quando usar**: pipeline de transformações onde os passos intermediários não têm valor de inspeção próprio.
**Como**: `.assign(col=lambda x: ...)` (atribuição funcional) + indexação por callable (`df[lambda x: cond]`) + `.pipe(func_customizada, *args)`.
**Trade-offs**: ganha legibilidade de fluxo, perde facilidade de depuração passo a passo — reservar para pipelines já estáveis, não durante exploração.
</content>
