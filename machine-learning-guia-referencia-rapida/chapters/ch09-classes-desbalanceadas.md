# Capítulo 9: Classes desbalanceadas

## Core Idea
Quando uma classe domina o dataset, accuracy vira uma métrica enganosa e o modelo tende a ignorar a classe minoritária — a resposta é combinar métrica adequada (não accuracy), modelos/parâmetros que penalizam a classe minoritária de forma mais dura, e/ou reamostragem (upsampling, downsampling ou geração sintética de dados).

## Frameworks Introduced
- **Reamostragem como três famílias distintas**: upsampling da minoria (repete amostras existentes, com ou sem reposição), downsampling da maioria (descarta amostras majoritárias, **sem** reposição) e geração sintética de minoria (SMOTE/ADASYN, cria pontos novos interpolando vizinhos) — a escolha depende de quanto dado se pode perder (downsampling) ou de quanto se pode arriscar overfitting em repetições (upsampling).
  - Quando usar: quando ajustar métrica/parâmetros de penalização não é suficiente.
  - Como: `sklearn.utils.resample` (simples) ou a biblioteca `imbalanced-learn` (catálogo mais amplo, incluindo variantes de downsampling inteligente como `NearMiss`/`TomekLink`/`ClusterCentroids`).
- **`class_weight='balanced'`** em modelos do scikit-learn como alternativa à reamostragem: regulariza o custo do erro para dar mais peso à classe minoritária sem duplicar/descartar amostras.

## Key Concepts
- **Por que accuracy falha**: com 1 positivo para 99 negativos, prever sempre negativo já dá 99% de accuracy — métricas como AUC, precisão e recall são preferíveis.
- **Modelos de árvore/ensemble** (florestas aleatórias, XGBoost) tendem a lidar melhor com desbalanceamento nativamente, especialmente se a classe minoritária forma clusters.
- **Parâmetros específicos de penalização**: XGBoost tem `scale_pos_weight` (razão negativo/positivo) e `max_delta_step` (passo mais conservador); KNN tem `weights='distance'` para dar peso maior a vizinhos mais próximos.
- **SMOTE**: gera amostra sintética da minoria escolhendo um dos k-vizinhos mais próximos e amostrando um ponto na linha que os conecta.
- **ADASYN**: como SMOTE, mas gera mais amostras sintéticas nas regiões onde a classe minoritária é mais difícil de aprender.
- **Variantes de downsampling inteligente** (`imbalanced-learn`): `ClusterCentroids` (sintetiza centroides via k-means), `NearMiss`/`TomekLink` (remove amostras próximas entre classes), `EditedNearestNeighbours`/`AllKNN`/`CondensedNearestNeighbour`/`OneSidedSelection`/`NeighbourhoodCleaningRule`/`InstanceHardnessThreshold` — cada uma usa uma heurística diferente de "qual amostra majoritária é segura remover".
- **`SMOTEENN`/`SMOTETomek`**: combinam upsampling sintético seguido de downsampling de limpeza, no mesmo passo.

## Anti-patterns
- **Usar reposição (`replace=True`) ao fazer downsampling**: não faz sentido reduzir uma classe repetindo suas próprias amostras — downsampling deve ser sem reposição.
- **Avaliar modelo em dados desbalanceados usando só accuracy**: sempre reportar/otimizar por AUC, precisão, recall ou F1 em paralelo (ver Capítulo 12).
- **Fazer upsampling/downsampling antes do split treino/teste**: mesmo risco de vazamento — reamostrar apenas o conjunto de treino, nunca duplicar informação de teste no treino.

## Code Examples
```python
# upsampling da minoria (sklearn)
from sklearn.utils import resample
mask = df.survived == 1
surv_df, death_df = df[mask], df[~mask]
df_upsample = resample(surv_df, replace=True, n_samples=len(death_df), random_state=42)
df2 = pd.concat([death_df, df_upsample])

# downsampling da maioria (sem reposição)
df_downsample = resample(death_df, replace=False, n_samples=len(surv_df), random_state=42)
df3 = pd.concat([surv_df, df_downsample])

# geração sintética (imbalanced-learn)
from imblearn.over_sampling import RandomOverSampler
ros = RandomOverSampler(random_state=42)
X_ros, y_ros = ros.fit_sample(X, y)
```
- **O que demonstra**: as duas formas manuais de reamostragem (upsampling com reposição, downsampling sem reposição) e a via de biblioteca especializada (`imbalanced-learn`) para os mesmos objetivos.

## Key Takeaways
1. Nunca avalie um problema de classes desbalanceadas só por accuracy — a métrica precisa refletir o custo real do erro (AUC/precisão/recall/F1).
2. Downsampling é sempre sem reposição; upsampling pode ser com ou sem reposição (mas repetir demais aumenta risco de overfitting).
3. SMOTE/ADASYN geram dados sintéticos plausíveis em vez de só duplicar amostras existentes.
4. `class_weight='balanced'` e parâmetros específicos (XGBoost `scale_pos_weight`, KNN `weights='distance'`) são alternativas à reamostragem, sem alterar o dataset.
5. Reamostragem deve acontecer só no conjunto de treino, nunca antes do split.

## Connects To
- **Ch 3**: o alerta sobre accuracy enganosa (`DummyClassifier`) é a origem deste capítulo.
- **Ch 10**: os modelos citados (árvores, XGBoost, KNN) têm capítulo próprio com mais detalhe de hiperparâmetros.
- **Ch 12**: métricas de avaliação (AUC, precisão, recall, F1) recomendadas aqui como substitutas de accuracy.
</content>
