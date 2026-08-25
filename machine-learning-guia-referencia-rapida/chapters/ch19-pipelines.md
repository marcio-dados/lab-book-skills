# Capítulo 19: Pipelines

## Core Idea
`Pipeline` do scikit-learn encadeia transformadores e um estimador final em um único objeto que se comporta como qualquer modelo (`.fit`/`.score`/`.predict`), eliminando a separação manual entre "código de pré-processamento" e "código de modelo" — e por ser um objeto scikit-learn normal, entra diretamente em `GridSearchCV` e em qualquer lugar que aceite um estimador.

## Frameworks Introduced
- **Transformador customizado via `BaseEstimator`+`TransformerMixin`**: encapsular lógica de limpeza específica do domínio (ex. `tweak_titanic`) como uma classe com `.fit`/`.transform`, permitindo que ela participe do pipeline como qualquer transformador nativo do sklearn.
  - Quando usar: sempre que a limpeza/engenharia de atributos precisa ser reaplicada de forma idêntica em treino e produção — encapsular em um transformador evita duplicar lógica manualmente.
  - Como: `class MeuTransformer(BaseEstimator, TransformerMixin): def fit(self, X, y=None): return self; def transform(self, X): ...`.
- **Grid search sobre um pipeline inteiro**: os nomes dos hiperparâmetros no `param_grid` usam o padrão `<nome_da_etapa>__<parametro>` (dois underscores), permitindo otimizar hiperparâmetros do modelo *e* dos transformadores anteriores em uma única busca.
  - Como usar: `GridSearchCV(pipe, param_grid={"rf__n_estimators": [...], "rf__max_features": [...]})`.
- **Pipeline como qualquer estimador do sklearn**: uma vez montado, o pipeline aceita `.fit`, `.score`, `.predict`, e pode ser passado a qualquer função de métrica (`roc_auc_score(y_test, pipe.predict(X_test))`) exatamente como um modelo isolado.

## Key Concepts
- **`.named_steps["nome"]`**: acessa uma etapa específica do pipeline já treinado para inspecionar seus atributos (ex. `.coef_` de uma regressão linear dentro do pipeline, ou `.explained_variance_ratio_` de uma PCA dentro do pipeline).
- **Pipeline de classificação**: encadeia transformador customizado (limpeza) → imputação → padronização → modelo, tudo dentro de um único objeto `Pipeline`.
- **Pipeline de regressão**: mesma estrutura, tipicamente mais simples (padronização → modelo linear).
- **Pipeline de PCA**: usa `Pipeline` mesmo sem estimador supervisionado no fim — útil para encadear padronização + redução de dimensionalidade como uma única unidade reutilizável.

## Mental Models
- Pense no pipeline como a materialização em código do princípio "fit só no treino, transform em ambos" que perpassa o livro inteiro (imputação, escala, PCA) — o pipeline garante isso automaticamente por construção, eliminando a chance de aplicar `fit_transform` no teste por engano.
- Todo o conhecimento acumulado sobre um modelo isolado (grid search, métricas, `.named_steps`) se aplica sem modificação a um pipeline, porque o pipeline *é* um estimador do sklearn.

## Anti-patterns
- **Duplicar a lógica de limpeza fora do pipeline (uma vez para treino, outra para produção)**: encapsular em um `TransformerMixin` customizado garante que a mesma lógica exata rode nos dois contextos.
- **Esquecer o prefixo `<etapa>__` ao montar `param_grid` para um pipeline**: `GridSearchCV` não encontrará o parâmetro sem o namespace da etapa.

## Code Examples
```python
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

class TitanicTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return tweak_titanic(X).drop(columns="survived")

pipe = Pipeline([
    ("titan", TitanicTransformer()),
    ("impute", impute.IterativeImputer()),
    ("std", preprocessing.StandardScaler()),
    ("rf", RandomForestClassifier()),
])
pipe.fit(X_train2, y_train2)
pipe.score(X_test2, y_test2)

# grid search sobre uma etapa específica do pipeline
params = {"rf__max_features": [0.4, "auto"], "rf__n_estimators": [15, 200]}
grid = model_selection.GridSearchCV(pipe, cv=3, param_grid=params)
grid.fit(orig_df, orig_df.survived)

# inspecionar uma etapa treinada dentro do pipeline
reg_pipe.named_steps["lr"].coef_
pca_pipe.named_steps["pca"].explained_variance_ratio_
```
- **O que demonstra**: o ciclo completo — transformador customizado + etapas nativas + grid search com namespace + inspeção pós-treino via `.named_steps` — tudo tratando o pipeline como um único modelo.

## Key Takeaways
1. `Pipeline` elimina a duplicação e o risco de vazamento entre lógica de treino e produção, encapsulando toda a cadeia (limpeza → imputação → escala → modelo) em um único objeto.
2. Lógica de limpeza customizada vira reutilizável e testável ao ser encapsulada em `BaseEstimator`+`TransformerMixin`.
3. `GridSearchCV` funciona sobre o pipeline inteiro usando o namespace `<etapa>__<parametro>`.
4. `.named_steps` permite inspecionar qualquer etapa interna após o treino, exatamente como se o modelo tivesse sido treinado isoladamente.

## Connects To
- **Ch 3**: as funções `tweak_titanic`/`get_train_test_X_y` daquele capítulo são a base do transformador customizado aqui.
- **Ch 7**: imputação/padronização, já vistas isoladamente, aqui entram como etapas do pipeline.
- **Ch 11**: `GridSearchCV` sobre o pipeline reusa exatamente a mesma lógica de busca de hiperparâmetros.
- **Ch 17**: PCA como etapa de pipeline, reaproveitando `explained_variance_ratio_`/`components_` já vistos.
</content>
