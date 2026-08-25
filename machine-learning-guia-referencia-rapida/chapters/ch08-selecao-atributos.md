# Capítulo 8: Seleção de atributos

## Core Idea
Menos atributos (bem escolhidos) tendem a produzir modelos mais estáveis, mais rápidos de treinar e mais fáceis de interpretar — o capítulo cataloga métodos complementares (correlação, dependência via floresta, lasso, eliminação recursiva, informação mútua, PCA, importância nativa) para decidir o que remover.

## Frameworks Introduced
- **Dependência entre atributos via floresta aleatória (`rfpimp.plot_dependence_heatmap`)**: treina uma floresta para prever cada coluna numérica a partir das demais; um valor de dependência (R² OOB) próximo de 1 indica que o atributo no eixo X já prevê o do eixo Y — mantém-se o previsor, remove-se o previsto. Mais robusto que correlação linear simples porque capta relações não lineares.
  - Quando usar: quando a correlação de Pearson não é suficiente para capturar dependências complexas entre atributos.
- **Eliminação Recursiva de Atributos (RFE/RFECV)**: remove iterativamente os atributos mais fracos (segundo `.coef_`/`.feature_importances_`), refaz o treino, e repete — `RFECV` ainda escolhe o número ideal de atributos via validação cruzada.
  - Quando usar: quando se quer um número específico de atributos ou descobrir automaticamente o número ideal.
  - Como: `RFE(modelo, n_atributos_desejado).fit(X, y)` → `.support_` marca os atributos escolhidos.
- **Regressão Lasso (`LassoLarsCV`) como seleção implícita**: a regularização L1 zera coeficientes de atributos pouco relevantes conforme `alpha` aumenta; visualizar o "caminho" dos coeficientes por `alpha` mostra quais sobrevivem primeiro.

## Key Concepts
- **Maldição da dimensionalidade**: mais dimensões tornam os dados mais esparsos, prejudicando cálculos de vizinhança/distância e exigindo mais dados para manter o sinal.
- **Tempo de treino cresce com o número de colunas** (às vezes pior que linear) — menos colunas relevantes tende a significar modelos mais rápidos, não só mais interpretáveis.
- **Informação mútua** (`mutual_info_classif`): mede, via k-vizinhos-mais-próximos, quanta informação um atributo fornece sobre o alvo; ≥ 0, sem limite superior, 0 significa nenhuma relação — não assume relação linear como a correlação de Pearson.
- **PCA como seleção não supervisionada**: os componentes de maior variância apontam quais atributos originais mais contribuem, mas o alvo `y` não é considerado (ver Capítulo 17).
- **`.feature_importances_`**: já visto no Capítulo 3, é a via mais direta de seleção quando o modelo já é baseado em árvore.

## Anti-patterns
- **Manter colunas agregadas que causam vazamento** (ex. o dataset `agg_df` deste capítulo tinha vazamento remanescente da coluna de sobrevivência): sempre reconferir vazamento ao criar atributos agregados, mesmo depois de já ter feito essa checagem no dataset original.
- **Escolher atributos só por correlação de Pearson**: perde relações não lineares — combinar com dependência via floresta ou informação mútua quando a correlação linear não for suficiente.

## Code Examples
```python
# eliminação recursiva de atributos com número alvo fixo
from sklearn.feature_selection import RFE
model = ensemble.RandomForestClassifier(n_estimators=100)
rfe = RFE(model, 4)
rfe.fit(X, y)
agg_X.columns[rfe.support_]

# informação mútua entre cada atributo e o alvo
from sklearn import feature_selection
mic = feature_selection.mutual_info_classif(X, y)
```
- **O que demonstra**: duas vias independentes de ranquear atributos (uma orientada a modelo/RFE, outra estatística/informação mútua) que costumam ser combinadas para confirmação cruzada.

## Reference Tables
| Método | Quando preferir |
|---|---|
| Correlação (`correlated_columns`) | Relações lineares simples entre pares de atributos |
| Dependência via floresta (`rfpimp`) | Relações não lineares entre atributos |
| Lasso (`LassoLarsCV`) | Modelos lineares, quer regularização + seleção juntas |
| RFE/RFECV | Quer um número específico (ou ótimo) de atributos, model-agnóstico via `.coef_`/`.feature_importances_` |
| Informação mútua | Quer relação atributo↔alvo sem assumir linearidade |
| PCA | Redução de dimensionalidade não supervisionada (não considera `y`) |
| `.feature_importances_` | Já usando modelo de árvore, quer resposta rápida e nativa |

## Key Takeaways
1. Seleção de atributos reduz ruído, instabilidade de coeficientes/importância e tempo de treino — não é só sobre interpretabilidade.
2. Combine métodos: correlação/dependência para colinearidade entre atributos, RFE/informação mútua/importância para relevância em relação ao alvo.
3. PCA seleciona por variância, não por relação com o alvo — é não supervisionado.
4. Sempre reconfira vazamento de informação ao criar atributos agregados, mesmo em cima de dados já limpos.

## Connects To
- **Ch 6**: `correlated_columns` e o heatmap de correlação foram introduzidos lá; aqui ganham a variante de dependência não linear via floresta.
- **Ch 10**: os modelos de árvore usados para `.feature_importances_`/dependência são detalhados lá.
- **Ch 13**: explicação de modelos (SHAP, importância) complementa a seleção de atributos com uma visão pós-treino.
- **Ch 17**: PCA é aprofundado como técnica de redução de dimensionalidade.
</content>
