# Capítulo 17 — Árvores de Decisão

## O Que É
Estrutura em árvore onde cada nó interno é uma pergunta (baseada em um atributo) e cada folha é uma previsão — analogia direta com o jogo "Vinte Perguntas". **Vantagens**: fáceis de interpretar (processo de decisão transparente), lidam nativamente com atributos numéricos e categóricos misturados, toleram atributos faltantes. **Desvantagens**: encontrar a árvore ótima é computacionalmente difícil (o livro usa uma heurística gulosa, não a ótima); propensas a **sobreajuste severo** se deixadas crescer livremente. O capítulo foca em **árvores de classificação** (saída categórica) via algoritmo **ID3**, restrito a saídas binárias.

## Entropia
Mede incerteza de um conjunto rotulado: `entropy(p) = Σ -pi·log2(pi)` (convenção `0·log(0)=0`). Baixa quando uma classe domina (`pi` perto de 0 ou 1), alta quando as classes estão bem distribuídas. `class_probabilities(labels)` via `Counter`; `data_entropy(labeled_data)` aplica `entropy` às proporções de classe observadas.

## Entropia de uma Partição
Ao dividir os dados por um atributo, a entropia da partição é a **média ponderada** das entropias de cada subconjunto resultante (`partition_entropy`), pesada pelo tamanho relativo de cada subconjunto. Queremos a divisão que **minimiza** essa entropia ponderada (mais "resolve" a incerteza).

**Armadilha explícita**: um atributo com muitos valores únicos (ex.: CPF/SSN de cada cliente) sempre produz entropia zero por definição (cada subconjunto tem um único membro) — mas um modelo baseado nele **não generaliza**. Regra prática: evitar (ou agrupar) atributos de alta cardinalidade ao escolher divisões.

## Construindo a Árvore (ID3, manual)
Exemplo de contratação (nível, linguagem, tweets, PhD → boa/má entrevista). Calculando `partition_entropy_by` para cada atributo na raiz, `level` tem a menor entropia → primeira divisão. Dentro de `Senior`, `tweets` zera a entropia (sim→True, não→False sempre). Dentro de `Junior`, `phd` resolve o resto. `Mid` já é puro (sempre True) e vira folha direto.

**Algoritmo ID3 (guloso)**:
1. Se todos os rótulos são iguais → folha com esse rótulo.
2. Se não há mais atributos candidatos → folha com o rótulo majoritário.
3. Senão, escolhe o atributo que minimiza a entropia ponderada da partição, cria um nó de decisão, e recursivamente repete em cada subconjunto (removendo o atributo já usado da lista de candidatos).

É "guloso" — escolhe o melhor passo imediato a cada nível, sem garantia de árvore globalmente ótima, mas simples de implementar/entender.

## Implementação
**Representação de árvore minimalista**: `True` (folha), `False` (folha), ou tupla `(atributo, dict_de_subarvores)`. Caso `None` na sub-árvore trata valores ausentes/inesperados, prevendo o rótulo majoritário daquele nó.
- `partition_by(inputs, attribute)` — agrupa via `defaultdict(list)`.
- `classify(tree, input)` — recursivo: folha retorna direto; nó de decisão busca `input.get(attribute)`, cai em `None` se a chave não existir na sub-árvore (trata gracilmente valores nunca vistos em treino).
- `build_tree_id3(inputs, split_candidates=None)` — implementa o algoritmo acima; a sub-árvore `subtrees[None]` guarda o rótulo majoritário como fallback.

O modelo resultante classifica **perfeitamente** o conjunto de treino (folhas puras) — sinal de sobreajuste inerente ao método sem poda, mas ainda generaliza razoavelmente em exemplos citados (`Intern`, valores nunca vistos, caem no ramo `None`).

## Florestas Aleatórias (Random Forests)
Solução para o sobreajuste de árvores individuais: construir **muitas árvores** e deixá-las votar (`forest_classify`, majoritário via `Counter`). Duas fontes de aleatoriedade para árvores diferentes a partir do mesmo processo determinístico:
1. **Bagging (bootstrap aggregating)**: cada árvore treina em uma amostra bootstrap (Capítulo 15) diferente dos dados, não no dataset completo — dados não usados numa árvore servem como teste "justo" para ela.
2. **Seleção aleatória de atributos candidatos** a cada divisão: em vez de considerar todos os atributos remanescentes, sorteia-se um subconjunto (`num_split_candidates`) e escolhe-se o melhor **dentro dele** — isso decorrelaciona as árvores entre si.

Classificado como uma instância de **ensemble learning**: combinar muitos "weak learners" (alta polarização, baixa variância individualmente) para produzir um modelo agregado forte. Random forests são descritas como "um dos modelos mais populares e versáteis disponíveis".

## Por Que Isso Importa
`build_tree_id3`/`classify` são autocontidos — não dependem de `distance`, `gradiente descendente` ou álgebra linear dos capítulos anteriores, sendo o modelo mais "isolado" do livro. O conceito de bagging/bootstrap conecta diretamente de volta ao Capítulo 15 (erro padrão de coeficientes de regressão via bootstrap).
