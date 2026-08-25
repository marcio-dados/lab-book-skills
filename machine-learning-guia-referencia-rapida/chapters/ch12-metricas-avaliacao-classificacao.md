# Capítulo 12: Métricas e avaliação de classificação

## Core Idea
A matriz de confusão (TP/TN/FP/FN) é a fonte primária de todas as métricas de classificação — accuracy, precisão, recall e F1 são todas derivadas dela — e visualizações complementares (ROC, precisão-recall, ganhos cumulativos, elevação, limiar de discriminação) existem para expor trade-offs que uma única métrica escalar esconde.

## Frameworks Introduced
- **Escolher a métrica pelo custo relativo de FP vs. FN**: accuracy trata os dois erros como equivalentes; precisão pune FP (falsos alarmes), recall pune FN (casos perdidos); a escolha certa depende do domínio (ex. fraude: recall alto pode importar mais que precisão, mas custa mais "filas" para analisar).
  - Como usar: nomear explicitamente o custo de um FP vs. um FN antes de escolher a métrica de otimização.
- **Curva/limiar de discriminação como botão ajustável, não constante fixa**: o limiar padrão de 50% (`predict` vs. `predict_proba` + limiar) pode ser deslocado para trocar precisão por recall (ou vice-versa) sem retreinar o modelo — `DiscriminationThreshold` do Yellowbrick varre esse limiar e mostra o impacto em precisão/recall/F1/taxa de fila simultaneamente.
- **ROC vs. precisão-recall**: ROC pode parecer otimista demais em classes desbalanceadas (a taxa de falso-positivo é diluída pela classe majoritária); a curva de precisão-recall é a alternativa mais honesta nesse cenário.

## Key Concepts
- **Matriz de confusão**: TP (verdadeiro positivo), TN (verdadeiro negativo), FP (falso-positivo, erro tipo 1), FN (falso-negativo, erro tipo 2) — mnemônico do livro: "P" de falso-positivo tem uma perna (tipo 1), "N" de falso-negativo tem duas (tipo 2).
- **Accuracy**: `(TP+TN)/(TP+TN+FP+FN)` — enganosa sob classes desbalanceadas (Capítulo 9).
- **Recall (sensibilidade)**: `TP/(TP+FN)` — "de todos os positivos reais, quantos achei?".
- **Precisão**: `TP/(TP+FP)` — "das predições positivas, quantas estavam certas?".
- **F1**: média harmônica de precisão e recall — resume o trade-off em um número.
- **Sufixos multiclasse** (`_micro`, `_macro`, `_weighted`, `_samples`) para `f1`/`precision`/`recall`: `_micro` agrega globalmente, `_macro` não pondera por classe, `_weighted` pondera pela frequência de cada classe, `_samples` calcula por amostra.
- **ROC/AUC**: taxa de verdadeiro positivo vs. taxa de falso-positivo variando o limiar; quanto mais perto do canto superior esquerdo, melhor.
- **Curva de ganhos cumulativos**: ordena as predições por probabilidade e mostra que fração de positivos reais é capturada observando apenas os X% principais — direto para decisões de negócio ("observar os 20% melhores captura 40% dos sobreviventes").
- **Gráfico de elevação (lift)**: mesma informação dos ganhos cumulativos, normalizada pelo baseline aleatório (ex. "2,2x melhor que escolher ao acaso" nos 20% melhores).
- **Taxa de fila (queue rate)**: fração das predições acima do limiar — "quantos casos eu teria que revisar" se estivesse operacionalizando o modelo.
- **Amostragem estratificada** (`train_test_split(..., stratify=y)`): garante que treino e teste mantenham a proporção original das classes.

## Anti-patterns
- **Usar só ROC/AUC em classes fortemente desbalanceadas**: complementar com curva de precisão-recall, que não dilui o efeito da classe minoritária.
- **Deixar o limiar de decisão fixo em 50% sem avaliar o custo real de FP vs. FN**: usar `DiscriminationThreshold` para escolher um limiar alinhado ao custo de negócio.
- **Fazer split treino/teste sem `stratify=` quando as classes são desbalanceadas**: risco de proporções distorcidas entre treino e teste.

## Code Examples
```python
# matriz de confusão manual (para entender a origem das métricas)
y_predict = dt.predict(X_test)
tp = ((y_test == 1) & (y_test == y_predict)).sum()
tn = ((y_test == 0) & (y_test == y_predict)).sum()
fp = ((y_test == 0) & (y_test != y_predict)).sum()
fn = ((y_test == 1) & (y_test != y_predict)).sum()

accuracy = (tp + tn) / (tp + tn + fp + fn)
recall = tp / (tp + fn)
precision = tp / (tp + fp)
f1 = (2 * precision * recall) / (precision + recall)

# equivalentes prontos do sklearn
from sklearn.metrics import (
    accuracy_score, recall_score, precision_score, f1_score, roc_auc_score,
)
```
- **O que demonstra**: todas as métricas escalares de classificação nascem da mesma contagem de 4 valores (TP/TN/FP/FN) — memorizar as fórmulas é entender de onde vêm `accuracy_score`/`recall_score`/etc.

## Reference Tables
| Métrica | Fórmula | String `scoring=` |
|---|---|---|
| Accuracy | `(TP+TN)/total` | `'accuracy'` |
| Recall (sensibilidade) | `TP/(TP+FN)` | `'recall'` |
| Precisão | `TP/(TP+FP)` | `'precision'` |
| F1 | média harmônica de precisão/recall | `'f1'` |
| AUC | área sob curva ROC | `'roc_auc'` |
| Precisão média | resumo da curva precisão-recall | `'average_precision'` |
| Log loss | entropia cruzada (exige `predict_proba`) | `'neg_log_loss'` |

| Visualização (Yellowbrick) | Pergunta que responde |
|---|---|
| `ConfusionMatrix` | Onde o modelo erra (FP vs. FN)? |
| `ClassificationReport` | Precisão/recall/F1 por classe, de relance |
| `ROCAUC` | Trade-off TPR/FPR em todos os limiares |
| `PrecisionRecallCurve` | Trade-off precisão/recall (melhor sob desbalanceamento) |
| `ClassBalance` | As classes de treino/teste estão proporcionais? |
| `ClassPredictionError` | Matriz de confusão em formato de barras |
| `DiscriminationThreshold` | Qual limiar maximiza F1 (ou equilibra precisão/recall/queue rate)? |

## Key Takeaways
1. Toda métrica de classificação escalar deriva da matriz de confusão (TP/TN/FP/FN) — entender a fórmula evita escolher a métrica errada por hábito.
2. A métrica certa depende do custo relativo de FP vs. FN no domínio, não de convenção.
3. O limiar de decisão (padrão 50%) é ajustável — `DiscriminationThreshold` mostra o efeito de movê-lo.
4. Em classes desbalanceadas, prefira curva de precisão-recall a ROC/AUC isolado.
5. Ganhos cumulativos e elevação traduzem a qualidade do modelo em termos de negócio ("observando X% eu capturo Y% dos casos positivos").

## Connects To
- **Ch 3**: usou `confusion_matrix`/`roc_auc_score` no fluxo introdutório; este capítulo cataloga todas as variantes.
- **Ch 9**: classes desbalanceadas motivam a preferência por precisão-recall sobre accuracy/ROC.
- **Ch 11**: `scoring=` desta tabela é o parâmetro usado nas curvas de validação/aprendizagem.
- **Ch 15**: métricas equivalentes para regressão (erro contínuo em vez de matriz de confusão).
</content>
