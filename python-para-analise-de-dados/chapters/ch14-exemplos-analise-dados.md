# Capítulo 14: Exemplos de análises de dados

## Core Idea
Capítulo de síntese: cinco estudos de caso reais (bit.ly/1.usa.gov, MovieLens, nomes de bebês da SSA, banco de dados nutricional do USDA, doações eleitorais da FEC) aplicam em conjunto — não isoladamente — as ferramentas dos capítulos anteriores (JSON, `groupby`, `merge`, `pivot_table`, `cut`, plotagem), mostrando como um pipeline de análise real se compõe na prática.

## Frameworks Introduced
- **JSON de linha → lista de dicts → DataFrame**: padrão recorrente para logs/feeds semi-estruturados (`[json.loads(line) for line in open(path)]` → `pd.DataFrame(records)`), tolerando campos ausentes por linha.
  - Quando usar: qualquer feed de eventos onde cada linha é um objeto JSON independente e o schema pode variar entre linhas.
- **"Contar e visualizar" como fluxo padrão**: `value_counts()` (ou `Counter`/`groupby(...).size()`) → `fillna`/limpeza de sentinelas → `nlargest`/`sort_values` → `sns.barplot`/`.plot`. Esse ciclo se repete em todos os 5 estudos de caso.
- **Normalização por grupo como padrão recorrente**: seja `groupby(...).apply(func)` com uma função que divide pela soma do grupo, seja `df.div(df.sum(axis=), axis=0)` — a mesma operação ("proporção dentro do grupo") reaparece em nomes de bebês, doações por estado, e distribuição de gêneros de filme.

## Key Concepts (por estudo de caso)
- **1.usa.gov (JSON de cliques bit.ly)**: `json.loads` linha a linha; contagem de fusos horários com `Counter`/`value_counts`; `fillna('Missing')` + indexação booleana para strings vazias (`'Unknown'`); `groupby(['tz','os']).size().unstack()` para tabular por duas dimensões; `argsort()`/`take()` (ou o atalho `nlargest`) para ordenar por soma de linha.
- **MovieLens 1M**: três tabelas (`users`, `ratings`, `movies`) unidas com `pd.merge` encadeado; `pivot_table('rating', index='title', columns='gender', aggfunc='mean')` para média por filme×gênero; filtro por `groupby('title').size() >= 250` para remover filmes com poucas avaliações antes de comparar; diferença de médias (`mean_ratings['M'] - mean_ratings['F']`) para achar filmes mais polarizados por gênero; desvio-padrão por grupo para polarização independente de gênero.
- **Nomes de bebês (SSA)**: `pd.concat` de ~130 arquivos anuais com `ignore_index=True`; `groupby(['year','sex']).apply(add_prop)` com verificação de sanidade (soma de `prop` == 1 por grupo); `top1000` via `groupby(...).apply(lambda g: g.sort_values('births', ascending=False)[:1000])`; `cumsum().searchsorted(0.5)` (vetorizado, sem laço) para calcular quantos nomes cobrem 50% dos nascimentos — a métrica de "diversidade de nomes".
- **USDA Food Database (JSON aninhado)**: cada alimento tem uma lista aninhada de nutrientes; padrão de achatamento é "para cada registro, `pd.DataFrame(item['nutrients'])` + adicionar `id`, depois `pd.concat` de todas as listas" — o mesmo padrão genérico para qualquer JSON com listas aninhadas por registro; `drop_duplicates()` antes do merge final; `groupby(['nutgroup','nutrient']).apply(lambda x: x.loc[x.value.idxmax()])` para achar o alimento com maior valor de cada nutriente.
- **Doações da FEC (eleição 2012)**: `map(dict)` para adicionar coluna derivada (partido) a partir de um dicionário de correspondência; `dict.get(x, x)` como "passthrough se não mapeado" para normalizar strings de profissão/empregador variantes; `pd.cut(valores, bins)` para discretizar valores de doação em buckets (`(0,1]`, `(1,10]`...); `groupby(['cand_nm', bins]).size().unstack(0)` para histograma comparativo entre candidatos.

## Mental Models
- Pense em cada estudo de caso como uma instância do mesmo ciclo: **carregar (formato heterogêneo) → normalizar para tabular → limpar sentinelas/ausência → agrupar/agregar → normalizar por grupo → ordenar/filtrar → visualizar**. A ferramenta muda (JSON vs. CSV vs. múltiplas tabelas), o ciclo não.
- `idxmax`/`idxmin` dentro de `apply` é o padrão geral para "linha que atinge o extremo de uma métrica dentro do grupo" — mais expressivo que ordenar e pegar a primeira linha.
- Um `dict.get(x, x)` (passthrough) é o idioma padrão para normalizar categorias variantes textualmente sem descartar as que não têm mapeamento explícito.

## Anti-patterns
- **Comparar médias entre grupos pequenos sem filtrar por tamanho mínimo**: o autor filtra filmes com menos de 250 avaliações antes de comparar médias por gênero — médias de amostras pequenas são ruidosas e distorcem rankings.
- **Concatenar arquivos anuais sem `ignore_index=True`**: preserva índices duplicados de cada arquivo (0, 1, 2... repetido por ano), quebrando indexação posicional depois.
- **Ignorar duplicatas ao achatar JSON aninhado**: o autor encontra 14.179 duplicatas explícitas em ~389 mil linhas de nutrientes antes do merge — checar `duplicated().sum()` é rotina, não exceção.
- **Deixar valores negativos de contribuição (estornos) na análise de doações sem filtrar**: distorce somas e proporções — filtrar `contb_receipt_amt > 0` explicitamente antes de agregações.

## Code Examples
```python
import pandas as pd
import numpy as np

# Padrão geral: achatar JSON aninhado (uma lista por registro) em tabela única
pieces = []
for item in db:
    frame = pd.DataFrame(item['nutrients'])
    frame['id'] = item['id']
    pieces.append(frame)
nutrients = pd.concat(pieces, ignore_index=True).drop_duplicates()

# Métrica de "diversidade": quantos nomes cobrem 50% dos nascimentos (vetorizado)
prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
n_names_for_half = prop_cumsum.values.searchsorted(0.5) + 1
```
- **O que demonstra**: o padrão genérico de achatamento de JSON aninhado por registro, e uma métrica de concentração calculada sem laço (soma cumulativa + busca binária) — mais rápido e mais idiomático que iterar manualmente.

## Worked Example
Cálculo da "revolução da última letra" nos nomes de bebês: `names.name.map(lambda x: x[-1])` extrai a última letra de cada nome; `names.pivot_table('births', index=last_letters, columns=['sex','year'], aggfunc=sum)` produz uma tabela de nascimentos por última-letra × sexo × ano; `table.reindex(columns=[1910,1960,2010], level='year')` seleciona três anos representativos; dividir pela soma da coluna (`subtable / subtable.sum()`) normaliza para proporção. O resultado mostra que a proporção de nomes masculinos terminados em "n" cresceu drasticamente desde 1960 — uma tendência histórica descoberta puramente por manipulação tabular (pivot + normalização), sem nenhum modelo estatístico. Isso ilustra a tese do capítulo: a maior parte do valor analítico vem de reorganizar e agregar dados corretamente, não de modelagem sofisticada.

## Key Takeaways
1. O ciclo carregar→normalizar→limpar→agrupar→normalizar-por-grupo→ordenar→visualizar se repete em qualquer análise real, independentemente do formato de origem.
2. Sempre filtre por tamanho mínimo de grupo antes de comparar médias entre grupos — médias de amostras pequenas enganam rankings.
3. `groupby(...).apply(idxmax/idxmin)` é o padrão geral para "encontrar a linha extrema dentro de cada grupo".
4. `cumsum().searchsorted(valor)` calcula métricas de concentração/cobertura sem laço explícito — mais rápido e mais idiomático em pandas/NumPy.
5. `dict.get(x, x)` é o idioma padrão para normalizar strings variantes preservando as não mapeadas.
6. Sempre verifique duplicatas (`duplicated().sum()`) antes de um merge quando os dados vieram de uma estrutura aninhada achatada.

## Connects To
- **Ch 6**: leitura de JSON e CSV, retomada em contexto real com múltiplas fontes.
- **Ch 7**: limpeza de sentinelas (`fillna`, `cut`) aplicada nos 5 estudos de caso.
- **Ch 8**: `merge`/`concat` usados extensivamente (MovieLens, USDA).
- **Ch 9/10**: plotagem (`seaborn.barplot`) e `groupby`/`pivot_table` são a espinha dorsal de todos os exemplos deste capítulo.
</content>
