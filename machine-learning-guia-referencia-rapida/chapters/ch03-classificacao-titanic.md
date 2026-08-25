# Capítulo 3: Descrição da classificação — conjunto de dados do Titanic

## Core Idea
Este capítulo é o percurso de ponta a ponta que todos os capítulos seguintes detalham: coletar dados, limpar, criar atributos, separar treino/teste, imputar, normalizar, testar várias famílias de modelo, treinar, avaliar (matriz de confusão, ROC, curva de aprendizado) e implantar — usando o dataset do Titanic como classificação binária (sobreviveu / não sobreviveu).

## Frameworks Introduced
- **`X`/`y` como convenção universal**: `X` é a matriz de atributos (uma linha por amostra, uma coluna por atributo), `y` é o vetor de rótulos/alvo — convenção herdada da notação `y = f(X)` usada por toda a literatura e por todas as bibliotecas de ML em Python.
  - Quando usar: sempre, ao estruturar qualquer problema supervisionado.
  - Como: `y = df[coluna_alvo]; X = df.drop(columns=coluna_alvo)`.
- **Vazamento de informação (leaky features)**: qualquer atributo que carregue informação do futuro/do próprio alvo (ex. `boat`/`body` no Titanic entregam a sobrevivência) deve ser removido antes de treinar, mesmo que melhore artificialmente a métrica.
  - Quando usar: sempre que um atributo só existiria depois do evento que o modelo tenta prever.
  - Como: inspecionar manualmente cada coluna perguntando "essa informação estaria disponível no momento da predição real?" e descartar (`.drop(columns=[...])`) as que não estariam.
- **Imputar/normalizar só depois do split treino/teste, ajustando (`fit`) apenas no treino**: evita vazamento de informação do conjunto de teste para o de treino.
  - Quando usar: sempre, antes de qualquer `.fit_transform`.
  - Como: `imputer.fit_transform(X_train)` seguido de `imputer.transform(X_test)` (nunca `fit_transform` no teste).
- **Comparar várias famílias de modelo via k-fold antes de escolher uma**: nenhum algoritmo (teorema "No Free Lunch") é o melhor em todo dataset; testar várias famílias com validação cruzada revela qual se ajusta a este problema específico.
  - Quando usar: fase de seleção de modelo, antes de otimizar hiperparâmetros.
  - Como: laço sobre lista de classes de modelo + `model_selection.cross_val_score(cls, X, y, scoring="roc_auc", cv=kfold)`, comparando média e desvio-padrão do AUC.

## Key Concepts
- **Modelo de base (`DummyClassifier`)**: baseline ingênuo que revela se a métrica-padrão (accuracy) é enganosa — essencial quando classes são desbalanceadas.
- **`GridSearchCV`**: busca exaustiva de hiperparâmetros sobre um dicionário de grades de valores, treinando e validando cada combinação via k-fold, devolvendo `best_params_`.
- **`feature_importances_`** (modelos baseados em árvore): mede o quanto cada atributo contribui, mas remover um atributo importante não necessariamente derruba a pontuação na mesma proporção (colinearidade entre atributos redistribui a importância).
- **Matriz de confusão**: contagem cruzada de predições vs. rótulos reais (verdadeiro/falso positivo/negativo); permite otimizar deliberadamente para menos falso-positivos ou menos falso-negativos.
- **Curva ROC / AUC**: taxa de verdadeiros positivos vs. falso-positivos em vários limiares; AUC resume em um único número (1 = perfeito, 0.5 = aleatório).
- **Curva de aprendizado**: pontuação de validação cruzada em função do tamanho da amostra de treino — se ainda está subindo, mais dados provavelmente ajudam.
- **Stacking**: combina as saídas de vários modelos-base como entrada de um meta-classificador; nem sempre supera os modelos individuais (neste exemplo, piorou).
- **Persistência via `pickle`**: forma mais simples de salvar (`pickle.dumps`) e recarregar (`pickle.loads`) um modelo treinado para implantação.

## Mental Models
- Pense no pipeline de modelagem como uma sequência estritamente ordenada — split antes de imputar/normalizar, sempre — porque cada etapa fora de ordem é uma forma sutil de vazamento de dados do teste para o treino.
- Um modelo de base não é burocracia: é a régua que diz se o "bom desempenho" do modelo real é realmente bom ou só reflexo do desbalanceamento das classes.

## Anti-patterns
- **Ajustar (`fit`) o imputer/scaler no dataset inteiro antes do split**: vaza estatísticas do teste para o treino; sempre `fit` só no treino, `transform` nos dois.
- **Manter colunas como `boat`/`body`/`name` sem avaliar vazamento**: infla artificialmente a métrica com informação que não existiria no momento real da predição.
- **Confiar apenas em `.score` (accuracy) sem checar um baseline (`DummyClassifier`)**: em classes desbalanceadas, accuracy alta pode ser só a proporção da classe majoritária.
- **Usar `get_dummies` sem `drop_first=True` (ou remoção manual)**: cria colunas perfeitamente colineares (ex. `sex_male`/`sex_female`), prejudicando a interpretação de coeficientes/importância.

## Code Examples
```python
# fluxo completo refatorado em duas funções (limpeza + split/imputação/normalização)
def tweak_titanic(df):
    df = df.drop(
        columns=["name", "ticket", "home.dest", "boat", "body", "cabin"]
    ).pipe(pd.get_dummies, drop_first=True)
    return df

def get_train_test_X_y(df, y_col, size=0.3, std_cols=None):
    y = df[y_col]
    X = df.drop(columns=y_col)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X, y, test_size=size, random_state=42
    )
    num_cols = ["pclass", "age", "sibsp", "parch", "fare"]
    fi = impute.IterativeImputer()
    X_train.loc[:, num_cols] = fi.fit_transform(X_train[num_cols])
    X_test.loc[:, num_cols] = fi.transform(X_test[num_cols])
    if std_cols:
        std = preprocessing.StandardScaler()
        X_train.loc[:, std_cols] = std.fit_transform(X_train[std_cols])
        X_test.loc[:, std_cols] = std.transform(X_test[std_cols])
    return X_train, X_test, y_train, y_test
```
- **O que demonstra**: o padrão "fit só no treino, transform nos dois" encapsulado em uma função reutilizável — a espinha dorsal de qualquer pipeline de classificação do livro.

## Reference Tables
| Etapa | Ferramenta típica |
|---|---|
| Coleta | `pd.read_excel`/`read_csv` |
| Diagnóstico de dados ausentes | `df.isnull().sum()`, `pandas_profiling.ProfileReport` |
| Remoção de vazamento | `df.drop(columns=[...])` |
| Codificação categórica | `pd.get_dummies(df, drop_first=True)` |
| Split | `model_selection.train_test_split` |
| Imputação | `impute.IterativeImputer` / `df.fillna(df.median())` |
| Normalização | `preprocessing.StandardScaler` |
| Baseline | `sklearn.dummy.DummyClassifier` |
| Seleção de família | `model_selection.cross_val_score` + k-fold |
| Otimização | `model_selection.GridSearchCV` |
| Avaliação | `confusion_matrix`, `roc_auc_score`, Yellowbrick (`ConfusionMatrix`, `ROCAUC`, `LearningCurve`) |
| Implantação | `pickle.dumps`/`pickle.loads` + Flask/Clipper/Cloud ML Engine |

## Key Takeaways
1. O pipeline canônico é: coletar → limpar (remover vazamento) → criar atributos → **split** → imputar/normalizar (fit só no treino) → baseline → comparar famílias → treinar → avaliar → otimizar → implantar.
2. Sempre estabeleça um `DummyClassifier` como baseline antes de confiar em accuracy.
3. Vazamento de informação (leaky features) é o erro mais silencioso e mais grave: revisar manualmente toda coluna antes de treinar.
4. Comparar famílias de modelo via k-fold AUC (média + desvio-padrão) antes de escolher qual otimizar.
5. `GridSearchCV` otimiza hiperparâmetros; a métrica de otimização (`scoring=`) deve ser escolhida de acordo com o problema (Capítulo 12).
6. Matriz de confusão, ROC/AUC e curva de aprendizado são o kit mínimo de avaliação visual de um classificador.

## Connects To
- **Ch 4/5**: aprofundam dados ausentes e limpeza, resumidos aqui.
- **Ch 6**: exploração de dados (histogramas, correlação) mencionada de passagem aqui via `pandas_profiling`.
- **Ch 7/8**: pré-processamento e seleção de atributos, tratados superficialmente neste fluxo introdutório.
- **Ch 9**: classes desbalanceadas — o alerta sobre accuracy enganosa é expandido lá.
- **Ch 10**: cada família de modelo testada aqui (regressão logística, árvore, KNN, Naive Bayes, SVM, floresta aleatória, XGBoost) tem capítulo dedicado.
- **Ch 12**: métricas de avaliação de classificação além de accuracy/AUC.
- **Ch 13**: explicação de modelos (SHAP), citada aqui como alternativa à importância de atributos padrão.
</content>
