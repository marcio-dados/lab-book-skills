# Capítulo 9: Plotagem e visualização

## Core Idea
matplotlib é a camada de baixo nível (Figure → Subplot/Axes → elementos: linha, tique, legenda, anotação, patch); pandas embute atalhos (`Series.plot`/`DataFrame.plot`) sobre ela para os casos comuns; seaborn adiciona um nível ainda mais alto, orientado a estatística, que agrega dados automaticamente e melhora a estética por padrão.

## Frameworks Introduced
- **Hierarquia Figure → Subplot(Axes)**: nenhuma plotagem existe sem uma `Figure` contendo pelo menos uma subplot; comandos de nível `plt.*` sempre atuam na subplot ativa/mais recente.
  - Quando usar: sempre — é o modelo mental base de toda a matplotlib.
  - Como: `fig = plt.figure(); ax = fig.add_subplot(nrows, ncols, idx)` ou o atalho `fig, axes = plt.subplots(nrows, ncols)` que já devolve um array de eixos indexável.
- **Escada de abstração de plotagem**: matplotlib (controle total, baixo nível) → `pandas.plot` (conveniente para Series/DataFrame já estruturados) → seaborn (agrega e estatística automaticamente, ex. `barplot` calcula média + intervalo de confiança).
  - Quando usar: subir na escada conforme o dado já vem "pronto para plotar" (matplotlib) ou ainda precisa de agregação estatística implícita (seaborn).
- **Grades de faceta (`seaborn.factorplot`/`FacetGrid`)**: expandir uma visualização em um grid de subplots por variável(is) categórica(s) adicional(is), em vez de sobrecarregar uma única plotagem.
  - Quando usar: quando há 2+ dimensões categóricas de agrupamento a mais além dos eixos x/y principais (ex. dia × hora × fumante).

## Key Concepts
- **`plt.subplots(nrows, ncols, sharex=, sharey=)`**: forma preferida de criar grade de subplots — devolve `(fig, axes)` com `axes` como array NumPy indexável.
- **`ax.plot(x, y, 'ko--')`**: string de estilo combina cor+marcador+linha; equivalente explícito via `color=`, `marker=`, `linestyle=`.
- **`ax.set_xticks`/`set_xticklabels`/`set_title`/`set_xlabel`** (ou `ax.set(**props)` em lote): personalização de eixo via API orientada a objetos (preferida pelo autor a `plt.xlim`/`plt.xticks` procedurais quando há múltiplas subplots).
- **`ax.legend(loc='best')`**: precisa ser chamado explicitamente mesmo se `label=` foi passado em cada `plot`.
- **`ax.annotate(text, xy=, xytext=, arrowprops=)`**: anotações com texto+seta em coordenadas de dado.
- **`plt.savefig(path, dpi=, bbox_inches='tight')`**: formato inferido pela extensão; `bbox_inches='tight'` remove espaço em branco; pode escrever em qualquer objeto tipo-arquivo (`BytesIO`), não só disco.
- **`Series.plot`/`DataFrame.plot`**: `kind=` controla o tipo (`'line'`, `'bar'`, `'barh'`, `'hist'`, `'kde'`/`'density'`, `'area'`, `'pie'`); `DataFrame.plot.bar(stacked=True)` empilha barras por linha.
- **`sns.barplot(x=, y=, data=, hue=)`**: agrega automaticamente (média + IC 95% como barra de erro) — diferente de `pandas.plot.bar`, que só plota valores já calculados.
- **`sns.distplot`**: histograma + KDE (density) simultâneos numa chamada.
- **`sns.regplot`**: dispersão + linha de regressão linear.
- **`sns.pairplot`**: matriz de dispersão par-a-par entre variáveis, com histograma/KDE na diagonal.
- **`sns.factorplot`**: grade de facetas com `row=`/`col=`/`hue=` para múltiplas dimensões categóricas.

## Mental Models
- Pense em toda plotagem matplotlib como composição de "patches" (retângulos, círculos, polígonos, linhas) — mesmo tipos "prontos" (histograma, barra) são implementados em cima desses primitivos.
- Pense na escolha entre pandas.plot e seaborn como "os dados já estão na forma exata que quero plotar?" (pandas.plot) vs. "preciso que a biblioteca agregue/agrupe antes de plotar?" (seaborn).
- Grades de faceta são "uma dimensão categórica a mais = um eixo (linha/coluna) a mais de subplots", não uma cor ou marcador extra sobrecarregando o mesmo plot.

## Anti-patterns
- **Criar uma figura em branco e tentar plotar direto nela**: matplotlib exige pelo menos uma subplot (`add_subplot`) antes de qualquer comando de plotagem funcionar.
- **Empilhar múltiplos comandos de plotagem em células separadas do Jupyter esperando que se acumulem na mesma figura**: cada célula reinicia a plotagem — comandos relacionados devem estar na mesma célula.
- **Ignorar sobreposição de rótulos em grades de subplots com `wspace=0`/`hspace=0`**: matplotlib não verifica sobreposição automaticamente; corrigir manualmente via `set_xticks`/`set_xticklabels`.
- **Usar `pandas.plot.bar` quando o dado ainda não foi agregado (média, contagem, IC)**: produz barras "cruas" por linha; se a intenção é estatística resumida por grupo, `seaborn.barplot` já faz a agregação.

## Code Examples
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Grade 2x2 de subplots com eixos compartilhados
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
for i in range(2):
    for j in range(2):
        axes[i, j].hist(np.random.randn(500), bins=50, color='k', alpha=0.5)
plt.subplots_adjust(wspace=0, hspace=0)

# seaborn: agregação automática (média + IC) por categoria, com hue
sns.barplot(x='tip_pct', y='day', hue='time', data=tips, orient='h')
```
- **O que demonstra**: criação programática de grades de subplots com controle de espaçamento (matplotlib) vs. agregação estatística automática por categoria em uma linha (seaborn).

## Reference Tables
| Argumento `kind=` (pandas `.plot`) | Tipo |
|---|---|
| `'line'` (default) | Linha |
| `'bar'` / `'barh'` | Barras verticais/horizontais |
| `'hist'` | Histograma |
| `'kde'` / `'density'` | Estimativa de densidade |
| `'area'`, `'pie'` | Área empilhada, pizza |

| Opção `savefig` | Papel |
|---|---|
| `dpi` | Resolução (pontos por polegada), default 100 |
| `bbox_inches='tight'` | Remove espaço em branco ao redor |
| `format` | Formato explícito (`'png'`, `'pdf'`, `'svg'`...) |

| Função seaborn | Uso |
|---|---|
| `barplot` | Barras com agregação (média + IC) por categoria |
| `distplot` | Histograma + KDE combinados |
| `regplot` | Dispersão + regressão linear |
| `pairplot` | Matriz de dispersão par-a-par |
| `factorplot` | Grade de facetas (`row=`/`col=`/`hue=`) |

## Worked Example
Análise de gorjetas (`tips.csv`): calcula-se `tip_pct = tip / (total_bill - tip)`, depois `sns.barplot(x='tip_pct', y='day', hue='time', data=tips, orient='h')` produz automaticamente a média de `tip_pct` por dia, separada por `time` (almoço/jantar), com barras de erro representando o IC de 95% — sem que o autor precise calcular manualmente `groupby(['day','time'])['tip_pct'].mean()` antes. Isso ilustra a diferença central do capítulo entre pandas.plot (plota o que já está calculado) e seaborn (calcula e plota em um único passo), evidenciando quando vale a pena subir um degrau na escada de abstração.

## Key Takeaways
1. Toda plotagem matplotlib exige `Figure` + pelo menos uma subplot (`Axes`) antes de qualquer comando de desenho funcionar.
2. Prefira a API orientada a objetos (`ax.set_*`) a `plt.*` procedural quando há múltiplas subplots, para evitar ambiguidade sobre "qual eixo estou configurando".
3. `pandas.plot` cobre o caso "dado já pronto para plotar"; `seaborn` cobre o caso "preciso agregar/comparar por categoria antes de plotar" — escolha pela necessidade de agregação implícita.
4. `sns.factorplot`/`FacetGrid` é a ferramenta certa quando há 2+ dimensões categóricas de agrupamento além dos eixos principais.
5. `savefig(..., bbox_inches='tight')` é o ajuste mais comum para publicação (remove espaço em branco); `dpi` controla resolução.

## Connects To
- **Ch 5**: `Series`/`DataFrame` como fonte de dados para `.plot`.
- **Ch 7/8**: `crosstab`, `groupby`-like agregações usadas para preparar dados antes de plotar (ex. `party_counts` normalizado).
- **Ch 11**: plotagem de séries temporais é aprofundada no capítulo dedicado.
- **Ch 14**: usa extensivamente matplotlib/pandas.plot em exemplos completos de análise.
</content>
