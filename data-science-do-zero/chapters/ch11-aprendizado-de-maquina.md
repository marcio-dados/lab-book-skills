# Capítulo 11 — Aprendizado de Máquina

## Modelagem
Modelo = especificação de uma relação matemática/probabilística entre variáveis (analogia: planilha de negócios, receita de cozinha, cálculo de odds no pôquer). Data science é mais coletar/limpar/formatar dados do que aprendizado de máquina propriamente — este é "só" um passo subsequente, ainda que essencial.

## O Que É Aprendizado de Máquina?
Criar e usar modelos **aprendidos a partir dos dados** para prever saídas em dados novos (spam, fraude, cliques, resultado esportivo). O livro cobre apenas **supervisionado** (dados rotulados) e **não supervisionado** (sem rótulos) — cita semi-supervisionado e online como fora de escopo. Na prática, escolhe-se uma família parametrizada de modelos (linear, árvore de decisão, etc.) e usam-se os dados para aprender os parâmetros ótimos dessa família.

## Sobreajuste e Sub-Ajuste
- **Sobreajuste**: desempenho ótimo nos dados de treino, ruim em dados novos — aprende ruído ou memoriza pontos específicos em vez de padrão real.
- **Sub-ajuste**: desempenho ruim mesmo no treino.
- Ilustração canônica: ajustar polinômios de grau 0, 1 e 9 a uma amostra — grau 0 sub-ajusta, grau 9 passa por todos os pontos mas explode com dados novos, grau 1 é o equilíbrio.

**Validação por divisão de dados**: `split_data(data, prob)` / `train_test_split(x, y, test_pct)` — treinar em uma fração e medir desempenho na fração retida. **Duas armadilhas**:
1. Padrões compartilhados entre treino e teste que não generalizam (ex.: mesmo usuário aparece em ambos, e o modelo "decora" usuários em vez de aprender relação).
2. Usar o conjunto de teste repetidamente para **escolher entre modelos** o transforma num segundo conjunto de treino disfarçado — a correção é **treino/validação/teste** em três partes: treino (ajustar), validação (escolher modelo), teste (avaliação final, tocado uma única vez).

## Precisão (Acurácia) e Suas Armadilhas
**Exemplo didático propositalmente absurdo**: um "teste de leucemia" que prevê positivo apenas se o nome do bebê for "Luke" atinge >98% de acurácia — porque a doença é rara (1,4%) e o teste nunca acerta os poucos casos reais, só se beneficia da base enorme de negativos verdadeiros. Conclusão: **acurácia bruta é enganosa em classes desbalanceadas**.

**Matriz de confusão** (positivo/negativo verdadeiro/falso) origina métricas melhores:
- `accuracy = (tp+tn)/total`
- `precision = tp/(tp+fp)` — "das previsões positivas, quantas acertei"
- `recall (sensibilidade) = tp/(tp+fn)` — "dos positivos reais, quantos capturei"
- `f1_score` — média harmônica de precision e recall, sempre entre os dois.

**Trade-off precision/recall**: modelo mais "generoso" em prever positivo aumenta recall e reduz precision, e vice-versa — ajustável via limiar de decisão (ex.: "prever doença se houver ≥N fatores de risco").

## Compromisso Polarização-Variância (Bias-Variance)
Reformulação do sobreajuste: medir o que aconteceria treinando o mesmo modelo repetidamente em diferentes amostras da mesma população.
- **Polarização alta / variância baixa** → sub-ajuste (modelos treinados em amostras diferentes ficam parecidos entre si, mas todos erram — ex.: polinômio grau 0).
- **Polarização baixa / variância alta** → sobreajuste (cada amostra produz um modelo bem diferente — ex.: polinômio grau 9).

**Receita prática**: polarização alta → adicionar características/complexidade; variância alta → remover características **ou** conseguir mais dados (mais dados reduz variância mantendo a complexidade constante, mas **não corrige polarização** — se o modelo carece de características suficientes, mais dados não ajuda).

## Extração e Seleção de Características
Características = as entradas fornecidas ao modelo. O **tipo de característica disponível restringe qual família de modelo é aplicável**:
- Naive Bayes (Cap. 13) → características binárias (sim/não).
- Regressão (Cap. 14, 16) → características numéricas (incluindo variáveis dummy 0/1).
- Árvores de decisão (Cap. 17) → numéricas ou categóricas, indiferente.

Às vezes o objetivo é **reduzir** características (PCA do Cap. 10, ou regularização do Cap. 15) para evitar sobreajuste em espaços de muitas dimensões. Escolha de características combina experiência de domínio com tentativa e erro.

## Por Que Isso Importa
`split_data`/`train_test_split` e o vocabulário de precision/recall/f1/accuracy são usados sem redefinição para avaliar Naive Bayes (13), k-NN (12) e os classificadores dos capítulos 16-17.
