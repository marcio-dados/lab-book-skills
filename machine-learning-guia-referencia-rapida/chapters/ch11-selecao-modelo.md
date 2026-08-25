# Capítulo 11: Seleção do modelo

## Core Idea
Curva de validação (variando um hiperparâmetro) e curva de aprendizagem (variando o volume de dados) são as duas ferramentas visuais para diagnosticar, respectivamente, "qual valor de hiperparâmetro é bom?" e "mais dados ajudariam este modelo?" — ambas comparam pontuação de treino vs. validação para revelar bias ou variância.

## Frameworks Introduced
- **Curva de validação como varredura de hiperparâmetro**: treina o mesmo modelo repetidamente variando um único hiperparâmetro (ex. `max_depth`) e plota a pontuação de treino vs. validação cruzada em função desse valor — o pico da curva de validação (não a de treino) indica o valor a escolher.
  - Quando usar: ao decidir um valor específico de hiperparâmetro antes de uma busca em grade mais ampla.
  - Como: `yellowbrick.model_selection.ValidationCurve(modelo, param_name=..., param_range=..., cv=..., scoring=...)`.
- **Curva de aprendizagem como diagnóstico de bias/variância**: plota a pontuação em função do tamanho da amostra de treino; variabilidade grande na pontuação de treino → bias alto (modelo simples demais, subadequação); variabilidade grande na validação, ou gap grande treino-validação → variância alta (superadequação); pontuação de validação ainda subindo → mais dados provavelmente ajudam.
  - Quando usar: antes de decidir investir em coletar mais dados, ou para diagnosticar se o problema é modelo simples demais vs. complexo demais.
  - Como: `yellowbrick.model_selection.LearningCurve(modelo, cv=...)`.

## Key Concepts
- **`scoring=` é o parâmetro que conecta ambas as curvas à métrica certa do problema**: classificação (`'accuracy'`, `'f1'`, `'roc_auc'`, `'precision'`, `'recall'`, etc.), regressão (`'r2'`, `'neg_mean_squared_error'`, etc.) ou clustering (`'adjusted_rand_score'`, `'v_measure_score'`, etc.) — a curva é agnóstica ao tipo de problema, só muda a métrica.
- **`n_jobs=-1`**: paraleliza a varredura de hiperparâmetro/tamanho de amostra usando todas as CPUs disponíveis.

## Mental Models
- Pense na curva de validação como "qual valor deste botão específico é bom?" e na curva de aprendizagem como "vale a pena gastar dinheiro coletando mais dados, ou o modelo já saturou?" — são perguntas diferentes que usam a mesma técnica visual (treino vs. validação em função de uma variável).
- Gap grande entre pontuação de treino e validação é a assinatura visual de superadequação; ambas as curvas baixas e próximas é a assinatura de subadequação (bias alto).

## Code Examples
```python
from yellowbrick.model_selection import ValidationCurve, LearningCurve

# qual valor de max_depth é bom para esta floresta?
vc_viz = ValidationCurve(
    RandomForestClassifier(n_estimators=100),
    param_name="max_depth", param_range=np.arange(1, 11), cv=10, n_jobs=-1,
)
vc_viz.fit(X, y)

# mais dados ajudariam este modelo?
lc_viz = LearningCurve(RandomForestClassifier(n_estimators=100), cv=10)
lc_viz.fit(X, y)
```
- **O que demonstra**: as duas curvas compartilham a mesma API do Yellowbrick (`.fit(X, y)` + `.poof()`), variando apenas o que é varrido (hiperparâmetro vs. tamanho de amostra).

## Key Takeaways
1. Curva de validação escolhe o valor de um hiperparâmetro; curva de aprendizagem decide se vale a pena coletar mais dados.
2. Sempre compare a pontuação de treino com a de validação — a diferença entre elas é o diagnóstico, não o valor absoluto isolado.
3. `scoring=` deve refletir a métrica real do problema (accuracy raramente é suficiente sozinha — ver Capítulo 9/12).

## Connects To
- **Ch 3**: já usou `LearningCurve` no fluxo introdutório; este capítulo formaliza a leitura de bias/variância.
- **Ch 9**: escolha de `scoring` adequado quando há classes desbalanceadas.
- **Ch 12**: catálogo completo das métricas usáveis em `scoring=`.
</content>
