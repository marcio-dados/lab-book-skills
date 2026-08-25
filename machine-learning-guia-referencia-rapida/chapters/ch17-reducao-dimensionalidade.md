# Capítulo 17: Redução da dimensionalidade

## Core Idea
PCA, UMAP, t-SNE e PHATE decompõem/projetam atributos em menos dimensões para visualização, pré-processamento ou clustering, mas diferem fundamentalmente em qual estrutura preservam — global (PCA), local (t-SNE), ambas (UMAP, PHATE) — e essa escolha deve guiar qual técnica usar.

## Frameworks Introduced
- **Estrutura global vs. local como eixo de escolha entre técnicas**: PCA preserva estrutura global (distâncias grandes entre grupos fazem sentido) mas assume linearidade; t-SNE preserva estrutura local (clusters próximos são fiéis) mas distorce distâncias globais entre clusters; UMAP e PHATE tentam preservar as duas ao mesmo tempo.
  - Quando usar: se a pergunta é "quais grupos existem e quão distintos são entre si", prefira UMAP/PHATE/PCA; se é só "quais pontos são vizinhos", t-SNE já resolve, mas não confie na distância entre clusters formados.
- **PCA como transformador de duas etapas (`fit` + `transform`)**: aprende combinações lineares ortogonais dos atributos originais, ordenadas por variância decrescente (`explained_variance_ratio_`); útil tanto para visualização (2-3 componentes) quanto como pré-processamento para reduzir ruído antes de outro algoritmo (inclusive antes de UMAP, para acelerar).
  - Como usar: sempre padronizar antes (`StandardScaler`); usar gráfico de declive (scree plot) ou variância cumulativa para escolher quantos componentes manter (regra prática: onde a curva "dobra" ou atinge ~90% de variância acumulada).

## Key Concepts
- **PCA**: componentes são ortogonais entre si e ordenados por variância explicada; `.components_` mostra o peso de cada atributo original em cada componente — permite interpretar "o que" cada componente representa (ex. componente 1 dominado por `pclass`/`age`/`fare`).
- **Gráfico de declive (scree plot) / variância cumulativa**: ferramentas para decidir quantos componentes manter via método do cotovelo.
- **Biplot (gráfico duplo)**: sobrepõe o scatter dos componentes com setas ("cargas") mostrando a contribuição/correlação dos atributos originais — ângulo agudo entre setas sugere correlação positiva, ~90° sugere independência, ~180° sugere correlação negativa.
- **UMAP**: manifold learning; preserva estrutura local e global melhor que t-SNE; muito sensível a `n_neighbors` (visão local vs. global) e `min_dist` (compactação vs. dispersão dos clusters); não paraleliza em múltiplas CPUs.
- **t-SNE**: minimiza divergência entre distribuições de vizinhança no espaço original e no embedding; preserva bem clusters locais, mas a distância *entre* clusters não é significativa; não determinístico (pode não convergir); muito sensível a `perplexity` (5–50, valores menores criam clusters mais rígidos).
- **PHATE**: usa difusão para capturar estrutura global a partir de conexões locais; tende a equilibrar global e local melhor que t-SNE isoladamente; hiperparâmetro-chave é `knn` (vizinhos do kernel).

## Mental Models
- Pense em PCA como "encontrar os eixos onde os dados mais variam e reprojetar nesses eixos" (compressão linear e interpretável); t-SNE/UMAP/PHATE como "preservar quem é vizinho de quem" (compressão não linear, melhor para visualizar clusters mas pior para interpretar eixos).
- A distância entre dois clusters distantes em um gráfico t-SNE não deve ser lida como "quão diferentes" eles são — só a vizinhança local tem significado.

## Anti-patterns
- **Interpretar distância entre clusters distantes em um gráfico t-SNE como medida de dissimilaridade real**: t-SNE não preserva estrutura global; usar PCA/UMAP/PHATE para essa leitura.
- **Não padronizar os dados antes de PCA/UMAP/t-SNE**: todas essas técnicas são sensíveis à escala; atributos de maior magnitude dominariam artificialmente.
- **Escolher hiperparâmetros de UMAP/t-SNE (`n_neighbors`, `min_dist`, `perplexity`) sem testar uma faixa de valores**: o resultado visual muda drasticamente; sempre plotar uma grade de valores antes de fixar um.

## Code Examples
```python
# PCA: fit + transform, e leitura da variância explicada
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
pca = PCA(random_state=42)
X_pca = pca.fit_transform(StandardScaler().fit_transform(X))
pca.explained_variance_ratio_   # quanto cada componente explica
pca.components_[0]              # peso de cada atributo original no componente 1

# UMAP e t-SNE compartilham a mesma interface fit_transform
import umap
X_umap = umap.UMAP(random_state=42).fit_transform(StandardScaler().fit_transform(X))

from sklearn.manifold import TSNE
X_tsne = TSNE().fit_transform(StandardScaler().fit_transform(X))
```
- **O que demonstra**: todas as quatro técnicas compartilham a interface `fit_transform`, permitindo trocar de método sem reescrever o pipeline de visualização.

## Reference Tables
| Técnica | Estrutura preservada | Determinística? | Hiperparâmetro mais sensível |
|---|---|---|---|
| PCA | Global (linear) | Sim | `n_components` |
| UMAP | Global + local | Aproximadamente | `n_neighbors`, `min_dist` |
| t-SNE | Local | Não | `perplexity` |
| PHATE | Global + local (via difusão) | Aproximadamente | `knn` |

## Key Takeaways
1. Escolha a técnica pela estrutura que importa responder: global (PCA), local (t-SNE), ou ambas (UMAP/PHATE).
2. PCA é linear e interpretável (`.components_` liga componentes a atributos originais); t-SNE/UMAP/PHATE são não lineares e melhores para visualização de clusters, mas menos interpretáveis diretamente.
3. Sempre padronizar antes de qualquer uma dessas técnicas.
4. Nunca interpretar distância entre clusters distantes em t-SNE como medida real de dissimilaridade.
5. PCA é frequentemente usado como pré-processamento (redução rápida) antes de UMAP/t-SNE em datasets grandes.

## Connects To
- **Ch 8**: PCA já apareceu como técnica de seleção de atributos não supervisionada; aqui é detalhada como técnica de visualização.
- **Ch 18**: clustering frequentemente usa a saída da PCA (ou visualiza clusters projetados em componentes principais).
</content>
