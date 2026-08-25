# Glossário — Python para Análise de Dados

**Agregação** — transformação que gera valor(es) escalar(es) a partir de um array/grupo (`sum`, `mean`, `count`) (Ch 10).

**Alinhamento de dados** — em operações aritméticas entre objetos pandas, o resultado usa a união dos rótulos de índice, preenchendo `NaN` onde não há correspondência (Ch 5).

**Array estruturado** — `ndarray` cujos elementos têm campos nomeados heterogêneos (como uma struct C); ferramenta de baixo nível para I/O binário (Ap. A).

**Broadcasting** — regra que permite operações aritméticas entre arrays de formatos diferentes, comparando dimensões da direita para a esquerda (Ch 4, Ap. A).

**`Categorical`** — tipo pandas para representação codificada por inteiros (categorias + códigos), economizando memória e acelerando `groupby` (Ch 12).

**Chave de grupo** — array, nome de coluna, dict/Series ou função usada para separar dados em `groupby` (Ch 10).

**`closed`/`label`** — argumentos de `resample` que controlam qual borda do intervalo é inclusiva e qual borda rotula o bucket resultante (Ch 11).

**`combine_first`** — método que preenche valores ausentes de um objeto com valores de outro, alinhado por rótulo (Ch 8).

**Comprehension** (list/dict/set) — sintaxe concisa `[expr for val in coll if cond]` para construir coleções filtrando/transformando (Ch 3).

**`Container` categorizado** — ver `Categorical`.

**`DatetimeIndex`** — índice de timestamps (`datetime64[ns]`) usado para séries temporais (Ch 11).

**Downsampling** — agregar dados de frequência alta para frequência mais baixa (Ch 11).

**Duck typing** — verificar comportamento de um objeto (ex. `iter(obj)`) em vez de checar seu tipo exato (Ch 2).

**Fancy indexing (indexação sofisticada)** — indexar um array com uma lista/array de inteiros; sempre copia os dados (Ch 4).

**Formato longo/largo** — longo: uma linha por observação (chaves em colunas); largo: uma coluna por variável distinta. `pivot`/`melt` convertem entre os dois (Ch 8).

**Generator (gerador)** — função com `yield` que produz valores sob demanda (lazy), sem materializar a sequência inteira (Ch 3).

**`groupby`** — implementação pandas do padrão split-apply-combine (Ch 10).

**Junção (merge/join)** — combinar tabelas por chave(s) compartilhada(s), com semântica `inner`/`left`/`right`/`outer` (Ch 8).

**MultiIndex (índice hierárquico)** — múltiplos níveis de rótulo em um eixo, permitindo representar dados N-dimensionais em 2D (Ch 8).

**`NA`/`NaN`/`NaT`** — sentinelas pandas para ausência: `NaN` (float/dados numéricos e objeto), `NaT` (timestamp) (Ch 5, Ch 7, Ch 11).

**Ordem C/Fortran** — orientação de memória row-major/column-major; afeta desempenho de operações contíguas (Ap. A).

**`Patsy`** — biblioteca de fórmulas estilo-R (`y ~ x0 + x1`) para gerar matrizes de design de modelos lineares (Ch 13).

**`Period`/`PeriodIndex`** — representação de um intervalo de tempo (mês, trimestre, ano), distinta de `Timestamp` (instante) (Ch 11).

**`pivot_table`/`crosstab`** — conveniências sobre `groupby` + reshape para sumarizar/tabular dados (Ch 10).

**Reamostragem (`resample`)** — conversão de frequência de séries temporais; API análoga a `groupby` (Ch 11).

**`reduceat`** — método de ufunc que faz "groupby de array" por fronteiras de bucket contíguas (Ap. A).

**Regex (expressão regular)** — padrão de correspondência de texto processado pelo módulo `re`/`Series.str` (Ch 7).

**`rolling`/`expanding`/`ewm`** — funções de janela móvel: fixa, expansiva desde o início, e com peso exponencialmente decrescente (Ch 11).

**Split-apply-combine** — padrão de 3 passos (separar por chave, aplicar função, combinar resultado) que fundamenta `groupby` (Ch 10).

**`stack`/`unstack`** — pivotar entre índice e colunas usando `MultiIndex` (Ch 8).

**Strides (passos)** — inteiros que informam quantos bytes pular por eixo para avançar um elemento; base das views sem cópia do NumPy (Ap. A).

**`transform`** — variação restrita (e mais rápida) de `apply` em `GroupBy`: deve devolver escalar (broadcast) ou objeto do mesmo formato da entrada (Ch 12).

**Ufunc (função universal)** — função NumPy vetorizada element-wise, unária ou binária, com métodos de instância (`reduce`, `accumulate`, `outer`) (Ch 4, Ap. A).

**Variável dummy (one-hot)** — codificação de coluna categórica em k colunas binárias (`get_dummies`) (Ch 7, Ch 12, Ch 13).

**Vetorização** — substituir laços `for` por expressões de array inteiras, ganho típico de 10-100x (Ch 4).

**View (visualização)** — resultado de fatiamento/reshape que compartilha memória com o array original, sem copiar (Ch 4, Ap. A).
</content>
