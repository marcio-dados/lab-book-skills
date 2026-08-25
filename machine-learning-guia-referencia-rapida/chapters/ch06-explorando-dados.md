# Capítulo 6: Explorando os dados

## Core Idea
Antes de modelar, um catálogo de visualizações (histograma, dispersão, pares, correlação, RadViz, coordenadas paralelas) revela distribuição, relação entre atributos e colinearidade — pandas cobre o básico, seaborn e Yellowbrick cobrem versões mais ricas ou orientadas a comparar classes do alvo.

## Frameworks Introduced
- **Colorir/comparar por classe do alvo em toda visualização**: sempre que possível, sobrepor ou colorir (`hue=`) o gráfico pela variável alvo (`sns.distplot` por máscara, `pairplot(hue="target")`, `RadViz(classes=[...])`) para ver se a distribuição de um atributo já separa visualmente as classes.
  - Quando usar: exploração inicial, antes de qualquer modelo, para ter intuição sobre quais atributos provavelmente serão úteis.
- **Detectar colinearidade sistematicamente, não só visualmente**: a função `correlated_columns(df, threshold=0.95)` percorre a matriz de correlação triangular inferior e lista pares acima de um limiar — mais confiável que inspecionar um heatmap grande a olho.
  - Quando usar: antes de treinar modelos sensíveis a colinearidade (regressão linear/logística) ou antes de confiar em `feature_importances_`/coeficientes.
  - Como: `df.corr()` → zerar triângulo superior (`np.tril`) → `.stack()` → filtrar por `abs() > threshold` → excluir a diagonal (`level_0 != level_1`).

## Key Concepts
- **`.describe()`**: estatísticas resumidas (count, mean, std, quartis) por coluna numérica; `count` menor que o total já denuncia dados ausentes.
- **`.loc`/`.iloc`**: acesso por rótulo vs. por posição inteira, ambos aceitando escalar, lista ou fatia, com vírgula separando linhas de colunas.
- **Histograma** (`df.plot(kind="hist")`, `sns.distplot`): forma de distribuição e número de modos de um atributo numérico.
- **Gráfico de dispersão / gráfico conjunto (joint plot)**: relação entre dois atributos numéricos; o joint plot acrescenta histogramas nas bordas e linha de regressão.
- **Matriz de pares (`pairplot`)**: grade de dispersões + densidade kernel entre várias colunas de uma vez, colorida por classe.
- **Box plot / violin plot**: comparam a distribuição de um atributo numérico entre categorias (ex. idade por sobrevivência).
- **RadViz**: projeta amostras em um círculo com atributos na borda — visualiza separação entre classes de forma mais compacta que um pairplot.
- **Coordenadas paralelas**: cada atributo é um eixo vertical paralelo; cada amostra é uma linha conectando seus valores — bom para ver agrupamentos multivariados.
- **`X.corr()`**: correlação par a par (Pearson por padrão; aceita `'kendall'`, `'spearman'` ou callable customizado).

## Anti-patterns
- **Confiar apenas em inspeção visual de heatmap para achar colinearidade em datasets com muitas colunas**: usar a função sistemática `correlated_columns` em vez de depender do olho.
- **Manter colunas com correlação quase perfeita (ex. `sex_male`/`sex_female`, `pclass`/`pclass_mean`)**: distorce a interpretação de coeficientes/importância — remover uma das colunas do par correlacionado.

## Code Examples
```python
# detecção sistemática de colinearidade acima de um limiar
def correlated_columns(df, threshold=0.95):
    return (
        df.corr()
        .pipe(lambda df1: pd.DataFrame(
            np.tril(df1, k=-1), columns=df.columns, index=df.columns
        ))
        .stack()
        .rename("pearson")
        .pipe(lambda s: s[s.abs() > threshold].reset_index())
        .query("level_0 not in level_1")
    )

correlated_columns(X)  # DataFrame vazio == sem colinearidade acima do limiar
```
- **O que demonstra**: transformar uma matriz de correlação em uma lista acionável de pares problemáticos, em vez de depender de leitura visual de um heatmap.

## Reference Tables
| Visualização | pandas | seaborn | Yellowbrick |
|---|---|---|---|
| Histograma | `.plot(kind="hist")` | `distplot` | — |
| Dispersão | `.plot.scatter` | `jointplot` | `JointPlotVisualizer` |
| Matriz de pares | — | `pairplot` | — |
| Box/violin | — | `boxplot`/`violinplot` | — |
| Correlação | `.corr()` | `heatmap` | `Rank2D` |
| RadViz | `pandas.plotting.radviz` | — | `RadViz` |
| Coordenadas paralelas | `pandas.plotting.parallel_coordinates` | — | `ParallelCoordinates` |

## Key Takeaways
1. Explorar dados antes de modelar é também uma desculpa produtiva para conversar com especialistas do negócio (SMEs) sobre nuances dos dados.
2. Sempre que possível, colorir visualizações pela variável alvo para antecipar separabilidade entre classes.
3. Detectar colinearidade com uma função sistemática (`correlated_columns`), não só visualmente, antes de confiar em coeficientes/importância.
4. pandas cobre o básico rapidamente; seaborn e Yellowbrick entram quando é preciso comparar por classe/alvo com mais nuance.

## Connects To
- **Ch 3**: usou `pandas_profiling` como visão geral rápida; este capítulo detalha as visualizações individuais.
- **Ch 8**: seleção de atributos usa a mesma detecção de colunas colineares para decidir o que remover.
- **Ch 10/14**: modelos de classificação/regressão se beneficiam de saber, já nesta fase, quais atributos parecem separar bem as classes ou correlacionar com o alvo.
</content>
