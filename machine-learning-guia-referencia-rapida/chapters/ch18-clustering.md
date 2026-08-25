# Capítulo 18: Clustering

## Core Idea
Clustering agrupa amostras sem rótulos (K-means escolhe k centroides e itera; clustering hierárquico aglomera de baixo para cima até um dendrograma) — a parte difícil não é rodar o algoritmo, é decidir quantos clusters existem (várias métricas quantitativas + inspeção visual) e depois explicar o que cada cluster representa (reusando ferramentas de EDA e modelos substitutos).

## Frameworks Introduced
- **Decidir "quantos clusters" combinando métricas + visual, nunca uma única fonte**: gráfico de cotovelo (inércia), coeficiente de silhueta, Índice de Calinski-Harabasz, Índice de Davies-Bouldin e visualização de silhueta por cluster (Yellowbrick) — quando a maioria concorda, a decisão é robusta; quando divergem, complementar com inspeção visual dos clusters projetados (PCA) ou acrescentar atributos.
  - Como usar: rodar K-means para uma faixa de `k`, plotar todas as métricas juntas, e escolher `k` onde a maioria converge (a inércia raramente tem "cotovelo" nítido sozinha).
- **Explicar clusters como um problema de EDA supervisionada disfarçada**: depois de gerar os rótulos de cluster, tratá-los como uma coluna categórica e aplicar `groupby`+`agg` (média/variância por cluster) e um modelo substituto (árvore de decisão treinada para prever o rótulo do cluster) para descobrir quais atributos definem cada grupo.
  - Quando usar: sempre, depois de qualquer clustering — o cluster em si não tem "significado" até ser explicado em termos dos atributos originais.

## Key Concepts
- **K-means**: escolhe k centroides aleatórios, atribui cada amostra ao centroide mais próximo, recalcula centroides, repete até convergir; sensível à escala (padronizar antes); `n_init` roda várias inicializações e mantém a melhor.
- **Clustering hierárquico aglomerativo**: começa com cada amostra em seu próprio cluster e vai unindo os "mais próximos" até restar um só; o resultado é um dendrograma que registra a que altura (distância) cada fusão ocorreu — "cortar" o dendrograma numa altura escolhida define o número de clusters.
- **Inércia**: soma dos quadrados das distâncias de cada amostra ao centroide do seu cluster; sempre cai com mais clusters — usada via método do cotovelo (procurar onde a queda desacelera).
- **Coeficiente de silhueta** (-1 a 1, maior é melhor): separação/coesão de cada amostra em relação ao seu cluster vs. o mais próximo.
- **Índice de Calinski-Harabasz** (maior é melhor): razão entre dispersão inter-cluster e intra-cluster.
- **Índice de Davies-Bouldin** (menor é melhor, mínimo 0): similaridade média entre cada cluster e seu vizinho mais próximo.
- **`AgglomerativeClustering`**: versão do scikit-learn para gerar clusters definitivos (`n_clusters=`) depois de já ter decidido o número via dendrograma.

## Mental Models
- Pense no cluster como uma hipótese que só ganha significado quando traduzida de volta para os atributos originais (`groupby(cluster).agg(['mean','var'])`, ou um modelo substituto) — o número/rótulo do cluster sozinho não diz nada sobre o domínio.
- O dendrograma é uma "árvore genealógica" de fusões: cortar em uma altura é decidir "até que ponto de similaridade dois grupos ainda contam como o mesmo cluster".

## Anti-patterns
- **Confiar em uma única métrica (ex. só inércia/cotovelo) para decidir o número de clusters**: usar múltiplas métricas (silhueta, Calinski-Harabasz, Davies-Bouldin) e ver onde concordam.
- **Deixar o rótulo de cluster sem explicação**: sempre religar o cluster aos atributos originais (agregação por grupo, modelo substituto) — um número de cluster isolado não é acionável.
- **Não padronizar antes de K-means/clustering hierárquico**: ambos dependem de distância; atributos de escala maior dominam artificialmente a formação dos clusters.

## Code Examples
```python
# comparar múltiplas métricas de clustering para decidir k
from sklearn.cluster import KMeans
from sklearn import metrics
inertias, sils, chs, dbs = [], [], [], []
for k in range(2, 12):
    km = KMeans(random_state=42, n_clusters=k).fit(X_std)
    inertias.append(km.inertia_)
    sils.append(metrics.silhouette_score(X, km.labels_))
    chs.append(metrics.calinski_harabasz_score(X, km.labels_))
    dbs.append(metrics.davies_bouldin_score(X, km.labels_))

# explicar clusters via agregação e modelo substituto
km = KMeans(n_clusters=2).fit(X_std)
labels = km.predict(X_std)
X.assign(cluster=labels).groupby("cluster").agg(["mean", "var"]).T

dt = tree.DecisionTreeClassifier()
dt.fit(X, labels)  # o alvo é o próprio rótulo de cluster, não y
```
- **O que demonstra**: o padrão completo de clustering "responsável" — decidir k com várias métricas, depois explicar cada cluster tratando o rótulo como alvo de um modelo interpretável.

## Reference Tables
| Métrica | Direção | Intervalo |
|---|---|---|
| Inércia | menor é melhor (mas sempre cai com mais clusters) | ≥ 0 |
| Silhueta | maior é melhor | -1 a 1 |
| Calinski-Harabasz | maior é melhor | ≥ 0, sem teto |
| Davies-Bouldin | menor é melhor | ≥ 0 |

## Key Takeaways
1. Decida o número de clusters combinando várias métricas (inércia, silhueta, Calinski-Harabasz, Davies-Bouldin), não uma isolada.
2. K-means e clustering hierárquico são sensíveis à escala — sempre padronizar antes.
3. Um cluster só é útil depois de explicado: `groupby`+`agg` e modelo substituto (árvore treinada para prever o rótulo do cluster) são as ferramentas padrão para isso.
4. O dendrograma do clustering hierárquico permite escolher visualmente onde "cortar" para definir o número de clusters.

## Connects To
- **Ch 6**: as mesmas ferramentas de EDA (`groupby`, visualização) são reaproveitadas para explicar clusters.
- **Ch 13**: o "modelo substituto" para explicar clusters é a mesma técnica usada para explicar modelos caixa-preta.
- **Ch 17**: PCA é frequentemente usado para visualizar clusters projetados em 2D.
</content>
