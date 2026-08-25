# Capítulo 13: Introdução às bibliotecas de modelagem em Python

## Core Idea
O ponto de contato entre pandas e qualquer biblioteca de modelagem (statsmodels, scikit-learn) é o array NumPy (`.values`); Patsy formaliza a passagem de "DataFrame + fórmula estilo-R" para matrizes de design prontas para regressão, e statsmodels/scikit-learn cobrem, respectivamente, estatística clássica (com inferência) e aprendizado de máquina (com foco em previsão).

## Frameworks Introduced
- **DataFrame → matriz de design → modelo**: pandas cuida de carga/limpeza/engenharia de características; a fronteira para o código de modelagem é sempre um array NumPy homogêneo (`.values`) ou uma matriz de design do Patsy.
  - Quando usar: sempre que uma biblioteca de modelagem espera arrays NumPy puros em vez de objetos pandas.
  - Como: `df.loc[:, cols].values` para subconjunto de colunas homogêneas; `patsy.dmatrices('y ~ x0 + x1', data)` quando há mistura de tipos, transformações, ou termos categóricos/interação.
- **Fórmulas Patsy (`y ~ x0 + x1`)**: sintaxe declarativa (inspirada em R) para especificar a matriz de design de um modelo linear, incluindo transformações (`np.log`, `standardize`, `center`), termos categóricos (dummy automático) e interações (`key1:key2`).
  - Quando usar: qualquer modelo linear com termos categóricos, transformações ou interações — evita construir a matriz de design manualmente com `get_dummies`.
- **statsmodels vs. scikit-learn**: statsmodels foca em inferência estatística clássica (parâmetros, p-valores, `summary()`); scikit-learn foca em previsão e pipeline de ML (`fit`/`predict`, validação cruzada).
  - Quando usar: statsmodels quando a pergunta é "os coeficientes são significativos e o que significam"; scikit-learn quando a pergunta é "qual é a melhor previsão possível".

## Key Concepts
- **`.values`**: converte DataFrame → `ndarray`; se as colunas forem heterogêneas (mistura de tipo), o resultado é um array `object` (perde a vetorização eficiente).
- **`data.loc[:, cols].values`**: forma recomendada de extrair um subconjunto de colunas já convertido para array, evitando colunas indesejadas no array final.
- **`patsy.dmatrices(formula, data)`**: devolve `(y, X)` como `DesignMatrix` (subclasse de `ndarray` com metadados); `+ 0` na fórmula remove o intercepto automático.
- **Transformações Patsy stateful** (`standardize`, `center`): guardam estatísticas do conjunto de treino (média/desvio) para aplicar consistentemente em dados novos via `patsy.build_design_matrices`.
- **`I(x0 + x1)`**: função de escape do Patsy — `+` em fórmula normalmente significa "adicionar termo ao modelo", não soma aritmética; `I(...)` força a interpretação matemática.
- **Termos categóricos no Patsy**: variáveis não numéricas viram dummies automaticamente; com intercepto, um nível é omitido (evita colinearidade, notação `key1[T.b]`); sem intercepto, todas as colunas aparecem; `C(col)` força tratamento categórico de uma coluna numérica; `key1:key2` expressa termo de interação.
- **`sm.OLS(y, X).fit()`** / **`smf.ols('y ~ x0 + x1', data=data).fit()`**: duas interfaces do statsmodels — array puro (`sm.*`) vs. fórmula+DataFrame (`smf.*`); a segunda já devolve parâmetros nomeados pelas colunas.
- **`results.summary()`**: diagnóstico completo do modelo (R², estatística F, p-valores por coeficiente).
- **`results.predict(novos_dados)`**: aplica os parâmetros estimados a dados fora da amostra.
- **`sm.tsa.AR(values).fit(maxlags)`**: modelo autorregressivo para séries temporais no statsmodels.
- **scikit-learn `fit`/`predict`**: API uniforme — instanciar modelo (`LogisticRegression()`), `model.fit(X_train, y_train)`, `model.predict(X_test)`.
- **Imputação simples de ausência antes de modelar**: statsmodels/scikit-learn não aceitam `NaN` — preencher com `fillna(mediana_do_treino)` (a mesma estatística do treino, nunca recalculada no teste, para evitar vazamento de informação).
- **`cross_val_score(model, X, y, cv=k)`**: validação cruzada k-fold automatizada — mede a estabilidade da métrica de performance em folds diferentes.

## Mental Models
- Pense em Patsy como "o compilador entre a notação de fórmula estatística (estilo R) e a matriz de design que os algoritmos numéricos realmente consomem" — ele resolve dummies, interações e transformações stateful de uma vez.
- Pense em statsmodels como "me diga por que o modelo funciona" (inferência, coeficientes, significância) e scikit-learn como "me diga o quão bem o modelo prevê" (acurácia, validação cruzada).
- Transformações "stateful" (centralizar, padronizar) devem sempre reusar as estatísticas do conjunto de treino ao aplicar em dados novos — nunca recalcular no conjunto de teste.

## Anti-patterns
- **Recalcular média/desvio-padrão no conjunto de teste ao aplicar `standardize`/`center`**: vazamento de informação do teste para o treino; usar `patsy.build_design_matrices` com o `design_info` do treino, ou equivalente manual.
- **Passar DataFrame com colunas heterogêneas direto para `.values` sem selecionar um subconjunto**: produz array `dtype=object`, perdendo desempenho vetorizado — usar `.loc[:, cols].values` com colunas já homogêneas.
- **Esquecer `+ 0` quando o intercepto não é desejado**: Patsy adiciona intercepto por convenção; omitir isso silenciosamente quando o modelo exige ausência de intercepto gera resultado incorreto.
- **Alimentar `NaN` para statsmodels/scikit-learn**: ambos rejeitam dados ausentes — sempre `isnull().sum()` antes de treinar, e decidir imputação (mediana, etc.) explicitamente.
- **Usar `+` numa fórmula Patsy esperando soma aritmética**: `y ~ x0 + x1` não soma colunas, adiciona termos — usar `I(x0 + x1)` quando a soma é de fato desejada.

## Code Examples
```python
import patsy
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Patsy: matriz de design com termo categórico + interação
y, X = patsy.dmatrices('v2 ~ key1 + key2 + key1:key2', data)

# statsmodels via fórmula: parâmetros já nomeados pelas colunas do DataFrame
results = smf.ols('y ~ col0 + col1 + col2', data=data).fit()
results.params      # Series indexada por nome de coluna
results.predict(data[:5])  # previsão fora da amostra
```
```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

model = LogisticRegression(C=10)
model.fit(X_train, y_train)
scores = cross_val_score(model, X_train, y_train, cv=4)
```
- **O que demonstra**: Patsy expressa termos categóricos e interações declarativamente; statsmodels via fórmula preserva nomes de coluna nos resultados; scikit-learn segue a API uniforme `fit`/`predict` com validação cruzada como função auxiliar separada.

## Reference Tables
| Interface statsmodels | Uso |
|---|---|
| `sm.OLS(y, X)` | Array puro (requer `sm.add_constant` para intercepto) |
| `smf.ols('y ~ ...', data=df)` | Fórmula + DataFrame (intercepto automático, params nomeados) |

| Sintaxe Patsy | Significado |
|---|---|
| `y ~ x0 + x1` | Modelo com intercepto implícito + termos x0, x1 |
| `y ~ x0 + x1 + 0` | Remove intercepto |
| `I(x0 + x1)` | Força soma aritmética (escapa da semântica de fórmula) |
| `C(col)` | Força tratamento categórico de coluna numérica |
| `key1:key2` | Termo de interação |

## Worked Example
Pipeline completo do dataset Titanic (Kaggle): carrega `train`/`test` com `pd.read_csv`; verifica ausência com `train.isnull().sum()` (encontra `Age` com 177 nulos); imputa com a mediana do **treino** (`impute_value = train['Age'].median()`) aplicada em ambos treino e teste — nunca recalculada no teste; cria feature binária `IsFemale = (Sex == 'female').astype(int)`; monta `X_train`/`X_test` a partir de `predictors = ['Pclass', 'IsFemale', 'Age']`; treina `LogisticRegression().fit(X_train, y_train)` e prevê com `.predict(X_test)`. O autor então mostra `LogisticRegressionCV` (busca de grade embutida) e `cross_val_score(model, X_train, y_train, cv=4)` como alternativas para avaliar robustez sem um conjunto de teste rotulado. Isso ilustra o fluxo canônico completo: limpeza (pandas) → engenharia de features (pandas) → modelagem (scikit-learn) → validação (scikit-learn).

## Key Takeaways
1. A fronteira pandas→modelagem é sempre um array NumPy homogêneo; use `.loc[:, cols].values` para controlar exatamente quais colunas entram.
2. Patsy resolve dummies, interações e transformações stateful declarativamente — evita reimplementar `get_dummies` manual para cada modelo.
3. `+` em fórmula Patsy nunca é soma aritmética; use `I(...)` quando a intenção é somar colunas de fato.
4. statsmodels (via `smf.ols`) preserva nomes de coluna nos resultados quando alimentado com fórmula + DataFrame — prefira essa interface a `sm.OLS` com array puro quando os nomes importam.
5. Imputação de ausência deve sempre usar estatísticas do conjunto de treino, aplicadas identicamente ao teste — nunca recalcular no teste (vazamento de dados).
6. scikit-learn segue API uniforme (`fit`/`predict`); `cross_val_score` é a ferramenta padrão para avaliar estabilidade sem precisar de um conjunto de teste rotulado à parte.

## Connects To
- **Ch 7**: `get_dummies`/`fillna` retomados aqui no contexto de preparar dados para modelagem.
- **Ch 10**: engenharia de características (feature engineering) frequentemente usa `groupby`/agregação, mencionado explicitamente.
- **Ch 12**: `Categorical` é a base de como o Patsy trata termos categóricos automaticamente.
- **Ch 1**: retoma explicitamente scikit-learn e statsmodels, introduzidos ali como parte do ecossistema.
</content>
