# Capítulo 19 — Agrupamento (Clustering)

## Aprendizado Não Supervisionado
Diferente da maioria dos capítulos (supervisionado, com rótulos), agrupamento trabalha com dados **sem rótulo**. **Não há agrupamento "correto"** — esquemas alternativos são melhores ou piores conforme a métrica escolhida, e agrupamentos **não se rotulam sozinhos**: cabe ao analista inspecionar o conteúdo de cada um e nomeá-lo.

## O Modelo: k-means
Cada entrada é um vetor em espaço `d`-dimensional. Escolhe-se `k` antecipadamente; o objetivo é particionar os pontos em `k` grupos minimizando a soma das distâncias quadradas de cada ponto à média de seu grupo. Encontrar o particionamento ótimo é difícil — usa-se um algoritmo **iterativo aproximado**:
1. Começar com `k` médias (pontos no espaço `d`-dimensional) — o livro sorteia `k` pontos existentes (`random.sample`).
2. Associar cada ponto à média mais próxima.
3. Se nenhuma associação mudou, parar.
4. Senão, recomputar as médias (`vector_mean`, Capítulo 4) com base nas novas associações e voltar ao passo 2.

Implementado como classe `KMeans` (`.train(inputs)`, `.classify(input)`). **Não há garantia de ótimo global** — resultado depende da inicialização aleatória.

## Exemplo: Escolhendo Locais de Encontro
Dado localizações de usuários em 2D, `KMeans(3)` encontra 3 centros; `KMeans(2)` refaz com apenas 2 (o orçamento da vice-presidente encolheu) — ilustra que `k` muitas vezes é **imposto por uma restrição externa** (aqui, orçamento), não escolhido livremente.

## Escolhendo k (quando não é imposto)
Método heurístico: plotar o **erro total ao quadrado** (`squared_clustering_errors`) em função de `k` e procurar o "cotovelo" (ponto de dobra) onde aumentar `k` deixa de reduzir o erro significativamente. No exemplo do livro, o cotovelo confirma a intuição visual de que `k=3` é o número "certo".

## Exemplo: Quantização de Cores de Imagem
Aplicação criativa: reduzir uma imagem a `N` cores (limitação de impressora) agrupando pixels no espaço RGB 3D via k-means e recolorindo cada pixel para a **média** de seu cluster (`recolor`). Carregamento de imagem via `matplotlib.image.imread` (retorna array NumPy tratável como lista de listas de pixels `[r,g,b]`).

## Agrupamento Hierárquico Bottom-Up
Abordagem alternativa que não exige escolher `k` de antemão:
1. Cada ponto começa como seu próprio cluster (folha).
2. Repetidamente funde os dois clusters mais próximos, até restar um único cluster gigante.
3. A **ordem de fusão** fica registrada — permite reconstruir qualquer número de clusters "desfazendo" as fusões mais recentes primeiro.

**Representação**: cluster-folha = tupla de 1 elemento `(valor,)`; cluster fundido = tupla de 2 `(ordem_de_fusão, [filho1, filho2])`. Funções: `is_leaf`, `get_children`, `get_values` (recupera todos os valores-folha sob um cluster), `get_merge_order` (folhas = `inf`, para que "desfazer" sempre escolha a fusão mais recente primeiro).

**Distância entre clusters** (`cluster_distance`, parametrizada por `distance_agg`):
- `min` (distância mínima entre quaisquer dois pontos dos dois clusters) — tende a criar clusters "em cadeia" alongados.
- `max` (distância máxima) — favorece clusters mais compactos/esféricos.
- `mean` também é comum.

`bottom_up_cluster(inputs, distance_agg=min)` funde iterativamente o par de clusters mais próximo (busca exaustiva sobre todos os pares — **explicitamente reconhecido como ineficiente**: recalcula todas as distâncias par-a-par a cada iteração; uma implementação real pré-computaria e reaproveitaria essas distâncias). `generate_clusters(base_cluster, num_clusters)` desfaz fusões (da última para a primeira) até atingir o número de clusters desejado.

No exemplo de localização de usuários, `min` e `max` como `distance_agg` produzem agrupamentos visivelmente diferentes — `min` tendendo a criar uma cadeia longa, `max` produzindo grupos mais parecidos com o resultado do k-means.

## Por Que Isso Importa
`vector_mean` (Cap. 4), `distance` (Cap. 4) e `squared_distance` são reaproveitados sem redefinição. O bootstrap conceitual de escolha de `k` (plotar métrica vs. hiperparâmetro e procurar o cotovelo) é um padrão geral reaplicável fora de clustering.
