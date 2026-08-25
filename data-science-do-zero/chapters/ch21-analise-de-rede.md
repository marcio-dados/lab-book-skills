# Capítulo 21 — Análise de Rede

## Redes: Nós e Vínculos
Vínculos podem ser **não-direcionados** (amizade Facebook — se A é amigo de B, B é amigo de A) ou **direcionados** (hyperlinks — meu site linka para whitehouse.gov, o inverso não é garantido). O capítulo revisita a rede de amigos do Capítulo 1, insatisfeito com o grau (número de conexões) como medida de importância.

## Centralidade de Intermediação (Betweenness)
Ideia: um nó é importante se está **frequentemente no caminho mais curto** entre outros pares de nós. Requer primeiro achar **todos os caminhos mais curtos entre todos os pares** — implementado com **busca em largura (BFS)** usando `collections.deque` como fila:
- `shortest_paths_from(from_user)` mantém `shortest_paths_to` (dict: id → lista de caminhos mais curtos até ele) e uma fronteira (`frontier`) de pares `(usuário_anterior, próximo_usuário)` a explorar.
- Ao retirar um usuário nunca visto da fila, os caminhos mais curtos até ele são os caminhos até seu predecessor + um passo.
- Ao retirar um usuário já visto, só adiciona o novo caminho se tiver o **mesmo comprimento** do mais curto já conhecido (podem existir múltiplos caminhos mínimos empatados) — caminhos mais longos são descartados.

Com os caminhos mais curtos de todos para todos calculados, a centralidade de intermediação de um nó = soma, sobre todos os pares `(j,k)`, da fração `1/n` dos `n` caminhos mais curtos entre `j` e `k` que passam por aquele nó (excluindo `j` e `k` em si). **Só o valor relativo importa**, não a magnitude absoluta.

## Centralidade de Proximidade (Closeness)
Mais simples: `farness(user) = soma dos tamanhos de todos os caminhos mais curtos daquele usuário para todos os outros`; `closeness_centrality = 1/farness`. No exemplo do livro, varia bem menos entre os nós que a intermediação — "mesmo os nós centrais ainda estão bem longe dos nós nos arredores".

**Limitação prática**: ambas exigem calcular caminhos mais curtos entre todos os pares — caro em redes grandes. Motiva a alternativa a seguir.

## Centralidade de Vetor Próprio (Eigenvector Centrality)
Requer multiplicação de matrizes do zero:
- `matrix_multiply(A, B)` via `matrix_product_entry` (produto escalar linha×coluna, checando compatibilidade de dimensões).
- Tratar vetores como matrizes coluna (`vector_as_matrix`/`vector_from_matrix`) para poder aplicar uma matriz quadrada `A` a um vetor `v` (`matrix_operate`).
- **Autovetor** de `A`: vetor não-nulo `v` tal que `A·v` é um múltiplo escalar de `v` (o **autovalor**). `find_eigenvector(A)` encontra um por **iteração de potência**: chuta um vetor aleatório, aplica `matrix_operate`, reescala para magnitude 1, repete até convergir.

**Limites reconhecidos**: nem toda matriz tem autovetor real (ex.: matriz de rotação 90°, `find_eigenvector` rodaria para sempre); algumas ficam presas em ciclos (matriz que troca coordenadas, ex. `flip`) mesmo tendo autovetor — bibliotecas reais (NumPy) usam métodos mais robustos que contornam isso.

**Aplicação à rede**: constrói-se a **matriz de adjacência** (`1` se conectados, `0` senão) e aplica `find_eigenvector`. Intuição circular resolvida por iteração: centralidade de um nó = soma das centralidades de seus vizinhos (reescalada) — "central" significa "conectado a quem já é central", e o processo de `find_eigenvector` é literalmente essa atualização iterativa até convergência. **Vantagem sobre intermediação/proximidade**: cálculo muito mais barato (multiplicação de matriz, sem busca de caminhos), escala melhor para redes grandes. **Instabilidade em redes pequenas**: pequenas mudanças na rede de exemplo alteram bastante os valores — em redes grandes isso se estabiliza.

## Grafos Direcionados e PageRank
Mudando de "amizade" (simétrica) para "aprovação profissional" (`endorsements`, direcionada: `(source, target)` = source aprova target). **Contar aprovações recebidas é uma métrica fácil de manipular** (contas falsas, conluio de aprovação mútua entre poucos usuários) — motiva o **PageRank**, que pondera aprovações pela importância de quem aprova (mesma lógica circular do vetor próprio, aplicada a grafos direcionados).

Versão simplificada implementada (`page_rank(users, damping=0.85, num_iters=100)`):
1. PageRank total = 1,0, distribuído igualmente entre nós no início.
2. A cada iteração, cada nó distribui uma fração `damping` do seu PageRank atual **igualmente entre seus links de saída** (`endorses`).
3. O restante (`1-damping`) é distribuído igualmente entre **todos** os nós (fator de amortecimento — evita que nós sem saída ou ciclos "prendam" todo o PageRank).

No exemplo, o algoritmo identifica um usuário com **poucas** aprovações totais mas **altamente valorizadas** (vindas de aprovadores que não dividem sua aprovação com mais ninguém) como o mais importante — superando usuários com contagem bruta maior mas aprovações "diluídas" ou circulares entre si.

## Por Que Isso Importa
`matrix_multiply`/`matrix_operate`/`find_eigenvector` são construídos do zero aqui e não reaparecem em outros capítulos — é o único uso "sério" de álgebra linear matricial (além de PCA no Cap. 10) do livro. PageRank e vetor próprio compartilham a mesma ideia central (importância definida recursivamente via importância dos vizinhos), aplicada primeiro a grafo não-direcionado e depois direcionado.
