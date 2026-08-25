# Capítulo 3 — Visualizando Dados

## Ideia Central
Visualização serve a dois propósitos distintos: **explorar** dados (para si mesmo) e **comunicar** dados (para os outros). O capítulo cobre o suficiente de `matplotlib.pyplot` para os dois usos ao longo do livro, sem tentar esgotar o assunto.

## `matplotlib.pyplot`
API de estado: você constrói o gráfico passo a passo (`plt.plot(...)`, `plt.title(...)`, `plt.xlabel(...)`) e finaliza com `plt.show()` ou `plt.savefig()`.

## Gráfico de Linhas
`plt.plot(xs, ys, color=..., marker=..., linestyle=...)` — bom para mostrar tendência ao longo de uma variável contínua (ex.: PIB por ano). Múltiplas chamadas de `plt.plot` no mesmo eixo sobrepõem séries; com `label=` em cada uma, `plt.legend(loc=9)` gera legenda automaticamente.

## Gráfico de Barra
`plt.bar(xs, alturas, largura)` — bom para comparar quantidades entre categorias (ex.: Oscars por filme) ou para plotar um histograma de valores numéricos (usando `Counter` sobre valores discretizados/"decis" com `grade // 10 * 10`).

**Padrão de honestidade visual**: `plt.axis([xmin, xmax, ymin, ymax])` controla a escala dos eixos — não iniciar o eixo Y em zero em gráficos de barra é uma forma fácil (e citada como antipadrão explícito) de exagerar visualmente uma diferença pequena. O livro mostra lado a lado a mesma série com eixo Y cortado ("Olhe o Grande Aumento!") e com eixo Y completo ("Não Tão Grande Agora").

## Gráfico de Dispersão
`plt.scatter(xs, ys)` — a escolha certa para visualizar a relação entre dois conjuntos de dados pareados (ex.: nº de amigos vs. minutos no site). `plt.annotate(rótulo, xy=..., xytext=..., textcoords='offset points')` anota pontos individualmente.

**Armadilha de escala**: ao comparar duas variáveis na mesma unidade (ex.: notas de duas provas), deixar o matplotlib escolher escalas independentes para X e Y pode distorcer visualmente a comparação — usar `plt.axis("equal")` quando as unidades forem comparáveis.

## Para Mais Esclarecimentos
Alternativas citadas: **seaborn** (construído sobre matplotlib, visual mais bonito), **D3.js** (JavaScript, web interativo), **Bokeh** (estilo D3 em Python), **ggplot** (porta Python do ggplot2 do R).

## Por Que Isso Importa
As convenções deste capítulo (linha para tendência, barra para categoria/histograma, dispersão para correlação, sempre desconfiar de eixos cortados) são reaplicadas sem comentário adicional em quase todos os capítulos posteriores.
