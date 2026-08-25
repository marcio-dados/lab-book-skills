# Cheatsheet — Data Science do Zero

## Decisões rápidas

- **Batch vs. estocástico no gradiente descendente?** Dataset pequeno/erro barato de calcular por completo → batch (`minimize_batch`, mais estável). Dataset grande ou erro aditivo por ponto → estocástico (`minimize_stochastic`, mais rápido, mais ruidoso).
- **Naive Bayes vs. regressão logística vs. árvore de decisão?** Features binárias tipo "contém a palavra X" → Naive Bayes. Features numéricas (incluindo dummies) e quer coeficientes interpretáveis → regressão logística. Mistura de numérico/categórico, quer transparência total do processo de decisão → árvore.
- **k-NN vs. modelo paramétrico?** Poucas dimensões, dados abundantes localmente, não precisa explicar o "porquê" → k-NN. Muitas dimensões (maldição da dimensionalidade) ou precisa de interpretabilidade/velocidade em produção → modelo paramétrico.
- **Ridge vs. Lasso?** Quer manter todas as variáveis mas encolher influência → Ridge. Quer um modelo esparso (zerar variáveis irrelevantes) → Lasso (mas não é solucionável por gradiente descendente simples).
- **Centralidade de rede: qual escolher?** Rede pequena, quer identificar "pontes" → intermediação (betweenness, caro: exige todos os caminhos mais curtos). Rede grande, quer algo barato de computar → vetor próprio (eigenvector) ou PageRank (se direcionado).
- **k-means vs. hierárquico bottom-up?** Sabe `k` de antemão (ou tem restrição externa, ex. orçamento) → k-means. Não sabe `k`, quer flexibilidade de gerar qualquer número de clusters depois → hierárquico (guarda ordem de fusão).
- **Filtragem colaborativa: usuário ou item?** Poucos usuários, muitos itens → baseada em item (mais estável). Poucos itens, muitos usuários → baseada em usuário. Muitos itens **e** muitos usuários → cuidado com maldição da dimensionalidade em ambos.

## Limiares e defaults a lembrar

| Situação | Regra prática |
|---|---|
| Testar hipótese com p-value | Significância convencional 5% ou 1% — decidir **antes** de olhar os dados (evitar p-hacking) |
| Suavização de probabilidade (Naive Bayes / LDA) | Nunca deixar `k=0`; valor típico `0.5` (Naive Bayes) ou `0.1` (LDA `alpha`/`beta`) |
| Regularização Ridge | Sempre `rescale()` os dados antes; `alpha=0` reproduz mínimos quadrados puro |
| Divisão treino/teste | 2/3 treino, 1/3 teste é o ponto de partida do livro; 3 conjuntos (treino/validação/teste) se for comparar modelos |
| Escolha de `k` em k-means | Plotar erro quadrático total vs. `k` e procurar o cotovelo — nunca escolher "porque sim" |
| Bootstrap | Centenas de reamostragens (100+) é o ponto de partida típico do livro para estimar erro padrão |
| Backpropagation | Repetir por milhares de épocas (livro usa 10.000 no exemplo de dígitos) até convergência visual |

## Tabela de decisão: qual capítulo revisitar

| Sintoma / necessidade | Capítulo |
|---|---|
| Preciso comparar dois grupos e não sei se a diferença é real | Ch 7 (hipótese, p-value, teste A/B) |
| Meu modelo tem R² alto mas coeficiente "estranho" | Ch 15 (erro padrão via bootstrap, p-value do coeficiente) |
| Distância entre pontos não faz sentido em muitas colunas | Ch 12 (maldição da dimensionalidade) → Ch 10 (PCA) |
| Preciso gerar/entender texto de forma simples | Ch 20 (n-gramas, gramáticas, LDA) |
| Preciso processar mais dados do que cabe em uma máquina | Ch 24 (MapReduce) |
| Preciso decidir se dois clusters "fazem sentido" | Ch 19 (cotovelo do erro quadrático) |
| Preciso recomendar algo sem um modelo de ML pesado | Ch 22 (similaridade do cosseno, colaborativo) |

## Tells / cheiros de problema

- Acurácia altíssima (>95%) em classe rara → suspeitar de desbalanceamento; checar precision/recall, não só acurácia (Ch 11, exemplo do teste de leucemia "Luke").
- R² sobe ao adicionar qualquer variável nova → normal e esperado; **não** é evidência de que a variável é útil — olhar o p-value/erro padrão do coeficiente (Ch 15).
- Frases geradas por modelo n-grama parecem "boas demais" → provavelmente estão copiando trechos literais do corpus (trigrama+ com pouco dado) em vez de generalizar (Ch 20).
- Vizinho mais próximo muda ao trocar unidade de medida (polegadas↔cm) → esqueceu de `rescale()` antes de calcular distância (Ch 10, Ch 12).
- Coeficiente de regressão parece deslocado/contraintuitivo → suspeitar de variável omitida correlacionada com uma variável incluída (viés de variável omitida, Ch 15).
- `P(evento) = 0` trava um classificador probabilístico inteiro → falta suavização com pseudo-contagem (Ch 13).
- Centralidade de rede muda drasticamente com pequenas edições no grafo → normal em redes pequenas (vetor próprio é instável em escala pequena); não indica bug (Ch 21).
