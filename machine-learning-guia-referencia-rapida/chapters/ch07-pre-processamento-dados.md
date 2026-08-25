# Capítulo 7: Pré-processamento dos dados

## Core Idea
Existe um espectro de técnicas para transformar atributos brutos (numéricos e categóricos) em algo que os modelos consigam consumir bem — escalonamento para SVM/KNN, e uma escada de codificação categórica (dummy → rótulo → frequência → hash → bayesiana) que se escolhe pela cardinalidade e pelo tipo de modelo, não por preferência única.

## Frameworks Introduced
- **Escolha do encoder categórico por cardinalidade**: baixa cardinalidade e sem ordem → `get_dummies`/one-hot; alta cardinalidade com ordem tolerável (árvores) → `LabelEncoder`; alta cardinalidade sem saber o vocabulário de antemão → `HashingEncoder`; alta cardinalidade nominal onde one-hot explodiria em colunas → codificadores bayesianos (`TargetEncoder`, `LeaveOneOutEncoder`, `WOEEncoder`, `JamesSteinEncoder`, `MEstimateEncoder`).
  - Quando usar: decidir isso é o primeiro passo de qualquer engenharia de atributos categóricos.
  - Como: ver Reference Tables abaixo.
- **Guardar estatísticas de treino para aplicar em dados novos**: média/desvio-padrão (`StandardScaler`), min/max (`MinMaxScaler`), mapeamento de frequência (`.value_counts()`) e mapeamento de encoder bayesiano devem todos ser calculados **só no treino** e reaplicados (`.transform`/`.map`) em dados novos — mesmo padrão de "fit só no treino" do Capítulo 3.
- **Extrair estrutura de strings/datas em vez de descartá-las**: título extraído de nome (regex `"([A-Za-z]+)\."`) e `add_datepart` (ano, mês, semana, trimestre, `_na`, elapsed) transformam colunas "opacas" para o modelo em atributos numéricos diretamente utilizáveis.

## Key Concepts
- **`StandardScaler`**: média 0, desvio-padrão 1; expõe `.scale_`, `.mean_`, `.var_` após `fit`. Equivalente manual: `(X - X.mean()) / X.std()`.
- **`MinMaxScaler`**: escala para `[0, 1]`; sensível a outliers (um valor extremo distorce toda a escala).
- **`get_dummies(df, drop_first=True)`**: one-hot encoding; `drop_first` evita a coluna redundante (combinação linear das demais).
- **`LabelEncoder`**: mapeia cada categoria para um inteiro (uma coluna por vez); impõe ordem arbitrária — aceitável para modelos de árvore, arriscado para modelos lineares/de distância. `.inverse_transform` desfaz.
- **Codificação de frequência**: substitui a categoria pela contagem que ela tinha no treino (`.value_counts()` + `.map()`); simples e eficaz para alta cardinalidade.
- **`HashingEncoder`** (`category_encoders`): útil quando o vocabulário de categorias não é conhecido de antemão ou para aprendizado online (streaming).
- **`OrdinalEncoder`** (`category_encoders`): mapeamento explícito categoria→número quando existe ordem real (ex. tamanhos P/M/G); categorias ausentes do mapeamento viram `-1` por padrão.
- **Codificadores bayesianos** (`TargetEncoder` etc.): combinam a probabilidade posterior do alvo dado a categoria com a probabilidade a priori — geram uma única coluna numérica mesmo com alta cardinalidade, mas trazem risco de vazamento se `fit` for feito no dataset inteiro (não só no treino).
- **`add_datepart`** (fastai): gera Year/Month/Week/Day/Dayofweek/Is_month_end/etc. e um "Elapsed" (timestamp) a partir de uma coluna de data — modifica o DataFrame in-place (comportamento atípico do pandas).
- **`col_na`**: padrão de preencher o valor ausente com a mediana **e** manter uma coluna booleana indicando que era ausente — preserva o sinal da ausência (retomado do Capítulo 4).
- **Engenharia manual via `groupby`+`agg`+`merge`**: agregações por grupo (ex. min/max/mean/sum de idade por cabine) viram novos atributos quando religadas ao DataFrame original via `.merge`.

## Anti-patterns
- **Usar one-hot em coluna categórica de altíssima cardinalidade**: explode em centenas/milhares de colunas esparsas; preferir hashing, frequência ou codificação bayesiana.
- **Recalcular o mapeamento de frequência/encoder bayesiano nos dados de teste em vez de reaplicar o mapeamento do treino**: mesmo vazamento de informação já visto nos capítulos de imputação/normalização.
- **Usar `LabelEncoder` em modelos sensíveis a distância/lineares sem avaliar se a ordem imposta faz sentido**: o inteiro atribuído é arbitrário, mas o modelo o trata como magnitude.

## Code Examples
```python
# extrair título do nome via regex (aumenta sinal preditivo do Titanic)
df.name.str.extract(r"([A-Za-z]+)\.", expand=False).value_counts()

# codificação bayesiana (TargetEncoder) — cuidado: fit só no treino em produção
import category_encoders as ce
def get_title(df):
    return df.name.str.extract(r"([A-Za-z]+)\.", expand=False)
te = ce.TargetEncoder(cols="Title")
te.fit_transform(df.assign(Title=get_title), df.survived)["Title"]

# col_na: preserva sinal de ausência ao imputar
data["A_na"] = data.A.isnull()
data["A"] = data.A.fillna(data.A.median())

# engenharia manual via agregação por grupo
agg = df.groupby("cabin").agg("min,max,mean,sum".split(",")).reset_index()
agg.columns = ["_".join(c).strip("_") for c in agg.columns.values]
agg_df = df.merge(agg, on="cabin")
```
- **O que demonstra**: extração de sinal de colunas "opacas" (texto, ausência, agrupamento) transformando-as em atributos numéricos diretamente usáveis pelo modelo.

## Reference Tables
| Situação | Encoder |
|---|---|
| Baixa cardinalidade, nominal | `pd.get_dummies(drop_first=True)` |
| Alta cardinalidade, modelo de árvore, ordem tolerável | `LabelEncoder` |
| Alta cardinalidade, ordem real conhecida | `ce.OrdinalEncoder` com mapeamento explícito |
| Vocabulário desconhecido / aprendizado online | `ce.HashingEncoder` |
| Alta cardinalidade nominal, quer 1 coluna | `ce.TargetEncoder`/`LeaveOneOutEncoder`/`WOEEncoder`/`JamesSteinEncoder`/`MEstimateEncoder` |
| Simples e robusto para alta cardinalidade | Codificação de frequência (`value_counts` + `map`) |

## Key Takeaways
1. A escolha do encoder categórico é guiada pela cardinalidade e pelo tipo de modelo — não existe um encoder universal.
2. Toda estatística de pré-processamento (escala, frequência, encoder bayesiano) deve ser calculada só no treino e reaplicada no teste/produção.
3. Datas e strings livres (nomes) carregam sinal explorável via extração estruturada (`add_datepart`, regex de título) em vez de serem descartadas.
4. `col_na` preserva o sinal da ausência mesmo depois de imputar o valor.
5. Agregações via `groupby`+`merge` são uma via simples e poderosa de engenharia manual de atributos.

## Connects To
- **Ch 3**: aplicou `StandardScaler` e `get_dummies` no fluxo básico; este capítulo detalha as alternativas.
- **Ch 4**: a coluna indicadora de ausência (`col_na`) já apareceu lá; aqui ganha a variante fastai completa.
- **Ch 8**: seleção de atributos assume que a engenharia deste capítulo já gerou candidatos suficientes para filtrar.
</content>
