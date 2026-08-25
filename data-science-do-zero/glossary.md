# Glossário — Data Science do Zero

**Acurácia (accuracy)** — fração de previsões corretas (`(tp+tn)/total`); enganosa em classes desbalanceadas (Ch 11).

**Amostragem de Gibbs** — técnica MCMC para amostrar de distribuições conjuntas multidimensionais conhecendo apenas as distribuições condicionais (Ch 20).

**Backpropagation** — algoritmo de treinamento de redes neurais que propaga o erro da camada de saída para trás, ajustando pesos via gradiente (Ch 18).

**Bagging (bootstrap aggregating)** — treinar múltiplos modelos em amostras bootstrap distintas dos mesmos dados para reduzir variância (Ch 17).

**Bootstrap** — reamostragem com reposição para estimar a incerteza (erro padrão) de uma estatística sem fórmula fechada (Ch 15).

**Centralidade de intermediação (betweenness)** — mede quanto um nó aparece nos caminhos mais curtos entre outros pares de nós (Ch 21).

**Centralidade de vetor próprio (eigenvector centrality)** — centralidade definida recursivamente: um nó é central se conectado a nós centrais; calculada via autovetor da matriz de adjacência (Ch 21).

**`Counter`** — `defaultdict(int)` especializado do módulo `collections`, usado para histogramas em praticamente todos os capítulos.

**Correlação** — covariância normalizada pelos desvios padrão, sempre entre -1 e 1 (Ch 5).

**Covariância** — medida de como duas variáveis variam juntas em torno das médias, sem normalização (Ch 5).

**Distribuição Beta** — priori conjugada da Binomial, usada em inferência Bayesiana sobre probabilidades (Ch 7).

**Entropia** — medida de incerteza de um conjunto rotulado, usada para escolher divisões em árvores de decisão (Ch 17).

**Erro Tipo 1 / Tipo 2** — falso positivo (rejeitar H0 verdadeira) / falso negativo (não rejeitar H0 falsa) (Ch 7).

**Estimativa de máxima verossimilhança (MLE)** — princípio que justifica escolher os parâmetros que tornam os dados observados mais prováveis; equivalente a mínimos quadrados sob erro normal (Ch 14).

**Feature (característica)** — entrada fornecida a um modelo; tipo de feature restringe qual família de modelo é aplicável (Ch 11).

**`defaultdict`** — dicionário que aplica uma função-fábrica a chaves ausentes na primeira leitura, evitando checagem manual de existência (Ch 2).

**Gradiente descendente** — técnica de otimização iterativa: mover na direção oposta ao gradiente para minimizar uma função (Ch 8).

**Gradiente descendente estocástico (SGD)** — variante que dá um passo por ponto de dado (não pelo dataset inteiro), tipicamente mais rápida (Ch 8).

**ID3** — algoritmo guloso de construção de árvore de decisão que escolhe, a cada nó, o atributo que minimiza a entropia ponderada da partição (Ch 17).

**k-means** — algoritmo de agrupamento que particiona pontos em `k` grupos minimizando a distância quadrada à média do grupo (Ch 19).

**k-NN (k-vizinhos mais próximos)** — classificador que vota entre os `k` pontos rotulados mais próximos; não aprende parâmetros (Ch 12).

**Maldição da dimensionalidade** — em espaços de muitas dimensões, pontos aleatórios tendem a ficar igualmente distantes uns dos outros, esvaziando a noção de "vizinhança" (Ch 12).

**Matriz de confusão** — tabela de positivos/negativos verdadeiros/falsos usada para derivar precision, recall, F1 (Ch 11).

**MapReduce** — modelo de programação para processamento paralelo: map (emite pares chave-valor) → shuffle (agrupa por chave) → reduce (agrega por chave) (Ch 24).

**Naive Bayes** — classificador probabilístico que assume independência condicional entre features dado a classe (Ch 13).

**NotQuiteABase** — mini-implementação de banco de dados relacional em Python puro, construída para ensinar SQL "do zero" (Ch 23).

**Overfitting (sobreajuste)** — modelo que se ajusta bem aos dados de treino mas generaliza mal (Ch 11).

**p-value** — probabilidade de observar um resultado tão ou mais extremo que o observado, assumindo a hipótese nula verdadeira (Ch 7).

**PageRank** — algoritmo que pondera a importância de um nó em grafo direcionado pela importância de quem aponta para ele, com fator de amortecimento (Ch 21).

**PCA (Análise de Componentes Principais)** — técnica de redução de dimensionalidade que encontra as direções de maior variância nos dados via gradiente descendente (Ch 10).

**Precision / Recall** — precision: fração de previsões positivas corretas; recall: fração de positivos reais capturados (Ch 11).

**Produto escalar (dot product)** — soma dos produtos componente a componente de dois vetores; mede projeção de um vetor sobre outro (Ch 4).

**R² (coeficiente de determinação)** — fração da variância de `y` capturada por um modelo de regressão (Ch 14).

**Regressão logística** — modelo que aplica a função logística ao produto escalar `x·β` para prever probabilidade de classe binária (Ch 16).

**Regularização (Ridge/Lasso)** — penalidade sobre a magnitude dos coeficientes de regressão para reduzir sobreajuste (Ch 15).

**Rescale (redimensionamento)** — transformar cada coluna de dados para média 0 e desvio padrão 1, eliminando dependência de unidade (Ch 10).

**SVM (Máquina de Vetor de Suporte)** — classificador que busca o hiperplano de máxima margem entre classes; usa "truque do kernel" para dados não linearmente separáveis (Ch 16).

**Similaridade do cosseno** — mede o ângulo entre dois vetores; usada em sistemas recomendadores para medir similaridade entre usuários/itens (Ch 22).

**Teorema de Bayes** — `P(E|F) = P(F|E)P(E)/P(F)`, permite inverter probabilidades condicionais (Ch 6).

**Teorema do Limite Central** — a soma/média de muitas variáveis i.i.d. se aproxima de uma distribuição normal (Ch 6).

**Teste A/B** — comparação estatística de duas variantes usando a diferença de proporções normalizada (Ch 7).

**Tokenização** — quebrar texto em unidades (palavras) processáveis, tipicamente via regex + lowercase (Ch 13, 20).

**train/test/validation split** — separar dados em conjuntos de treino, validação (escolha de modelo) e teste (avaliação final) para evitar sobreajuste na avaliação (Ch 11).

**Variável dummy** — variável categórica codificada como 0/1 para uso em modelos numéricos (Ch 15).

**Vetor próprio / valor próprio (autovetor/autovalor)** — vetor que, aplicado por uma matriz, retorna um múltiplo escalar de si mesmo (Ch 21).
