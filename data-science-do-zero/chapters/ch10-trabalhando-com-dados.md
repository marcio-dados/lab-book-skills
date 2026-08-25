# Capítulo 10 — Trabalhando com Dados

## Explorando Dados Unidimensionais
Antes de modelar, sempre explorar. Estatísticas sumárias (contagem, min, max, média, desvio padrão) não bastam — duas distribuições podem ter média/desvio quase idênticos e formatos completamente diferentes (exemplo: `uniform` entre -100 e 100 vs. `normal` com mesma média/desvio, ambas com histograma via `bucketize`/`make_histogram`/`plot_histogram`). Só o histograma revela a diferença de forma.

## Duas Dimensões
Duas variáveis podem ter a mesma distribuição individual (mesmo histograma) mas relações completamente diferentes com uma terceira — ilustrado com `ys1 = xs + ruído` (correlação +0,9) e `ys2 = -xs + ruído` (correlação -0,9): olhar cada dimensão isoladamente esconde a relação; o **gráfico de dispersão** e a **correlação par-a-par** a revelam.

## Muitas Dimensões
- **Matriz de correlação**: `correlation_matrix(data)` — entrada `(i,j)` é a correlação entre as colunas `i` e `j`, construída com `make_matrix`.
- **Matriz de gráficos de dispersão** (scatterplot matrix): grade de subplots via `plt.subplots(num_columns, num_columns)`, dispersando cada par de colunas fora da diagonal e anotando o nome da série na diagonal. Forma visual rápida de inspecionar todas as correlações de uma vez, mesmo sem ajuste fino de matplotlib.

## Limpando e Transformando
Fazer parsing (`float`, `dateutil.parser.parse`, etc.) **dentro** do laço de leitura é propenso a erro — melhor envolver o `csv.reader` com uma camada declarativa de parsers:
- `parse_row(input_row, parsers)` — aplica uma lista de funções-parser (ou `None` = não tocar) a cada campo, via `zip`.
- `try_or_none(f)` — decorator que captura exceção e retorna `None` em vez de travar o programa (padrão de "parsing tolerante a falha").
- `parse_rows_with(reader, parsers)` — gerador que aplica `parse_row` a cada linha do `csv.reader`.
- Equivalente para `csv.DictReader`: `parse_dict`/`try_parse_field` usando um dict `{nome_do_campo: parser}`.
- Depois de parsear, checar linhas com algum `None` (`any(x is None for x in row)`) e decidir: descartar, corrigir na fonte, ou ignorar conscientemente. Exemplo citado de dado sujo real: uma data com ano "3014" (erro de digitação) que não gera erro de parsing mas é claramente inválida — não há atalho automático para isso, exige inspeção.

## Manipulando Dados
Padrão recorrente ilustrado com dados de preço de ações (lista de dicts, cada um uma "linha"):
- `picker(field_name)` — retorna uma função que extrai um campo de um dict.
- `pluck(field_name, rows)` — aplica `picker` via `map` a uma coleção de dicts, extraindo uma lista de valores.
- `group_by(grouper, rows, value_transform=None)` — agrupa linhas por uma função-chave (`defaultdict(list)`) e, opcionalmente, aplica uma transformação a cada grupo. É o cavalo de batalha genérico por trás de todas as perguntas do capítulo: preço máximo por símbolo, variação percentual dia-a-dia (`day_over_day_changes`, usando `zip(ordered, ordered[1:])` para parear dia atual com o anterior), e mudança composta por mês (`combine_pct_changes`: `(1+p1)*(1+p2)-1`, não soma simples de percentuais).

## Redimensionamento (Rescaling)
**Problema**: técnicas baseadas em distância (ex.: k-NN, clustering) são sensíveis à unidade de medida — o exemplo mostra que trocar polegadas por centímetros muda qual ponto é o "vizinho mais próximo" de outro, só por causa da escala. **Solução**: `rescale(data_matrix)` transforma cada coluna para média 0 e desvio padrão 1 (`scale` computa média/desvio por coluna), eliminando a dependência de unidade. **Ressalva de bom senso**: se o dado já foi filtrado para uma faixa estreita (ex.: só alturas entre 69,5 e 70,5 polegadas), a variação restante pode ser só ruído — redimensioná-la para desvio padrão 1 a colocaria artificialmente em pé de igualdade com dimensões que carregam sinal real.

## Redução de Dimensionalidade (PCA do zero)
Quando os eixos originais não capturam a estrutura real dos dados (variação concentrada numa direção diagonal, não nos eixos x/y), usa-se **Análise de Componentes Principais**:
1. `de_mean_matrix(A)` — centraliza cada coluna em média 0 (evita que a técnica capture a média em vez da variação).
2. `direction(w)` — normaliza um vetor para magnitude 1 (candidato a direção).
3. `directional_variance(X, w)` — soma de `dot(x_i, direction(w))²` sobre todas as linhas: quanta variância os dados têm ao longo da direção `w`.
4. `directional_variance_gradient` — gradiente analítico dessa função, usado com `maximize_batch` (ou `maximize_stochastic`) do Capítulo 8 para encontrar a direção que **maximiza** a variância — o **primeiro componente principal** (`first_principal_component`).
5. `project(v, w)` / `remove_projection` — projeta cada linha no componente encontrado e subtrai, deixando apenas a variação residual; repetir o processo sobre o resíduo extrai o **segundo componente**, e assim por diante (`principal_component_analysis(X, num_components)`).
6. `transform(X, components)` — reprojeta os dados originais no novo espaço de dimensão reduzida (coordenadas = produto escalar com cada componente).

**Dois benefícios**: (1) remove ruído/redundância entre dimensões correlacionadas; (2) viabiliza técnicas que não funcionam bem em alta dimensão. **Trade-off explícito**: ganha-se poder preditivo, perde-se interpretabilidade — "cada ano extra de experiência aumenta o salário em $10k" é claro; "cada 0,1 a mais no terceiro componente principal aumenta o salário em $10k" não é.

## Por Que Isso Importa
`group_by`/`pluck`/`picker` reaparecem implicitamente em qualquer manipulação tabular do livro. O PCA construído aqui é usado como técnica de pré-processamento antes de algoritmos sensíveis a dimensionalidade (k-NN, Cap. 12) e é a única vez que o livro deriva gradiente analítico de uma função não-trivial para alimentar `maximize_batch`.
