# Capítulo 24 — MapReduce

## O Modelo
MapReduce é um padrão de programação para **processamento paralelo** de grandes coleções de dados, com base conceitual simples em três passos:
1. **map**: uma função `mapper` transforma cada item em zero ou mais pares `(chave, valor)`.
2. **shuffle**: agrupa todos os pares com a **mesma chave**.
3. **reduce**: uma função `reducer` processa cada grupo de valores (por chave) e produz a(s) saída(s) daquela chave.

## Exemplo Canônico: Contagem de Palavras
Versão simples de memória única: `Counter(word for doc in documents for word in tokenize(doc))`. Versão MapReduce:
- `wc_mapper(document)`: para cada palavra tokenizada, `yield (word, 1)`.
- `wc_reducer(word, counts)`: `yield (word, sum(counts))`.
- Orquestração manual (numa única máquina): `collector = defaultdict(list)` acumula todos os valores emitidos por chave; depois aplica o reducer a cada chave.

## Por Que MapReduce
O ganho real é permitir **mover o processamento até os dados** em vez do inverso: com documentos espalhados por 100 máquinas, cada máquina roda o mapper **localmente** nos seus próprios dados; os pares resultantes são distribuídos para máquinas redutoras garantindo que pares da mesma chave cheguem à mesma máquina; cada redutora agrupa e reduz. **Escala horizontalmente**: dobrar o número de máquinas aproximadamente dobra a velocidade (ignorando custos fixos de orquestração), desde que haja chaves suficientemente distintas para distribuir o trabalho de redução também.

## Framework Generalizado
Extraindo o padrão comum:
```python
def map_reduce(inputs, mapper, reducer):
    collector = defaultdict(list)
    for input in inputs:
        for key, value in mapper(input):
            collector[key].append(value)
    return [output for key, values in collector.items() for output in reducer(key, values)]
```
`word_counts = map_reduce(documents, wc_mapper, wc_reducer)` — a lógica específica do problema fica isolada em mapper/reducer, e a "infraestrutura" (agrupamento) é genérica.

**Abstração de reducers comuns**: como muitos reducers só agregam os valores por chave (soma, max, min, contagem de distintos), o livro fatora isso em `values_reducer(aggregation_fn)` — um fabricador de reducers a partir de qualquer função `valores → resultado`. Daí: `sum_reducer = values_reducer(sum)`, `max_reducer`, `min_reducer`, `count_distinct_reducer = values_reducer(lambda values: len(set(values)))`.

## Exemplos de Aplicação
- **Dia da semana mais falado sobre "data science"**: mapper emite `(dia_da_semana, 1)` só quando o texto contém a frase; reduzido com `sum_reducer`.
- **Palavra mais comum por usuário**: decisão de design importante — a chave certa é o **usuário** (não a palavra, nem o par usuário+palavra), porque o reducer precisa ver **todas** as palavras de uma pessoa de uma vez para achar a mais frequente dela. `words_per_user_mapper` emite `(user, (word,1))`; `most_popular_word_reducer` agrega um `Counter` local e retorna a palavra mais comum daquele usuário.
- **Número de curtidores distintos por usuário**: `liker_mapper` emite `(user, liker)` para cada like; reduzido com `count_distinct_reducer`.

## Exemplo: Multiplicação de Matrizes Distribuída
Para matrizes **esparsas** e muito grandes, a representação lista-de-listas é inviável — usa-se lista de tuplas `(nome_matriz, i, j, valor)` só para entradas não-nulas. Cada elemento `A[i][j]` contribui para toda a linha `i` de `C`; cada `B[i][j]` contribui para toda a coluna `j` de `C`. O mapper (`matrix_multiply_mapper`) emite, para cada elemento de `A`, uma entrada por cada possível coluna `k` de `C` na chave `(i,k)`; para cada elemento de `B`, uma entrada por cada linha `k` na chave `(k,j)` — garantindo que tudo que contribui para uma célula `C[i][j]` termine agrupado sob a mesma chave. O reducer (`matrix_multiply_reducer`) casa os pares `(A_ik, B_kj)` por índice comum e soma os produtos.

## Adendo: Combinadores
Otimização para o ambiente **distribuído** real: em vez de emitir `(word, 1)` uma vez por ocorrência (gerando tráfego de rede proporcional ao total de ocorrências), uma máquina mapeadora pode **pré-combinar** localmente (ex.: `("data", 500)` em vez de 500 pares `("data", 1)`) antes de enviar ao redutor — reduz drasticamente o volume de dados transferidos entre máquinas. Só funciona corretamente porque o reducer soma os valores (`sum`) — se tivesse sido implementado como `len(values)` em vez de `sum(values)`, um combinador pré-agregado quebraria a lógica (comentário explícito do autor sobre por que emitir `1` e somar, em vez de emitir `None` e contar).

## Por Que Isso Importa
`map_reduce`/`values_reducer` reaproveitam `defaultdict` (padrão onipresente no livro desde o Capítulo 2) e conectam diretamente de volta à multiplicação de matrizes (Capítulo 21) mostrando a mesma operação sob uma lente distribuída. É o único capítulo dedicado inteiramente a **escala/infraestrutura de processamento**, fechando o arco iniciado no Capítulo 9 (aquisição) → 10/23 (manipulação/armazenamento) → 24 (processamento distribuído).
