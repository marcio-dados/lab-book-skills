# Capítulo 4: Dados ausentes

## Core Idea
Dados ausentes exigem uma decisão explícita — descartar linha, descartar coluna, imputar valor, ou sinalizar a ausência como atributo — e a escolha certa depende de investigar se a ausência é aleatória ou carrega um padrão (correlacionada com outros atributos), não de uma regra fixa.

## Frameworks Introduced
- **Diagnosticar antes de decidir**: usar `missingno` (matriz, barras, heatmap, dendrograma) para visualizar se a ausência de dados segue um padrão (regiões contíguas, correlação entre colunas ausentes) antes de escolher a estratégia de tratamento.
  - Quando usar: sempre, antes de descartar ou imputar.
  - Como: `msno.matrix`/`msno.bar`/`msno.heatmap`/`msno.dendrogram(df)`.
- **Imputação indutiva vs. transdutiva**: algoritmos transdutivos (maioria do `fancyimpute`) só imputam no dataset com que foram ajustados, não aceitam `.transform` posterior — inadequados para produção, onde é preciso aplicar a mesma lógica em dados novos. `IterativeImputer` (migrado do fancyimpute para o scikit-learn) é indutivo.
  - Quando usar: em qualquer pipeline que vá prever sobre dados futuros, prefira sempre um imputer indutivo (`fit` no treino, `transform` em dados novos).

## Key Concepts
- **`df.isnull().mean() * 100`**: forma padrão de calcular o percentual de ausência por coluna (True/False tratados como 1/0).
- **Exceções que toleram dados ausentes nativamente**: XGBoost, CatBoost e LightGBM lidam com `NaN` internamente, ao contrário da maioria dos algoritmos do scikit-learn.
- **Quatro estratégias**: remover linha (`dropna()`), remover coluna (`drop(columns=...)` ou `dropna(axis=1)`), imputar (`SimpleImputer`, `IterativeImputer`, `fillna`), ou criar coluna indicadora de ausência (`df[col].isna().astype(int)`).
- **`SimpleImputer`**: estratégias `mean` (padrão, só numérico), `median` (só numérico), `most_frequent` e `constant` (com `fill_value=`) — as duas últimas funcionam com string ou numérico.
- **Coluna indicadora de ausência**: a própria ausência pode carregar sinal preditivo (ex. "por que a idade não foi informada?") — adicionar `<col>_missing` preserva esse sinal mesmo após imputar o valor.

## Anti-patterns
- **Descartar dados como primeira opção**: o autor trata `dropna` como último recurso — descarte de linha/coluna deve vir depois de diagnosticar o padrão de ausência, não antes.
- **Usar um imputer transdutivo em um pipeline de produção**: impede aplicar a mesma lógica de imputação em dados novos no momento da predição, quebrando a consistência treino/produção.
- **Imputar com `fillna` usando um valor calculado sobre o dataset inteiro (treino+teste)**: mesmo risco de vazamento de informação do capítulo anterior — a estatística de imputação deve vir só do treino.

## Code Examples
```python
# diagnóstico visual de padrões de ausência
import missingno as msno
ax = msno.matrix(orig_df.sample(500))
ax = msno.heatmap(df, figsize=(6, 6))   # correlação entre colunas ausentes
ax = msno.dendrogram(df)                 # clustering de padrões de ausência

# imputação indutiva com SimpleImputer
from sklearn.impute import SimpleImputer
num_cols = df.select_dtypes(include="number").columns
im = SimpleImputer(strategy="median")
imputed = im.fit_transform(df[num_cols])

# coluna indicadora de ausência
def add_indicator(col):
    def wrapper(df):
        return df[col].isna().astype(int)
    return wrapper

df1 = df.assign(cabin_missing=add_indicator("cabin"))
```
- **O que demonstra**: o ciclo diagnosticar (visual) → escolher estratégia → imputar de forma indutiva → opcionalmente preservar o sinal da ausência como atributo novo.

## Key Takeaways
1. Nunca trate ausência de dados como um problema uniforme — diagnostique o padrão (`missingno`) antes de decidir a estratégia.
2. Prefira imputadores indutivos (`SimpleImputer`, `IterativeImputer`) a transdutivos quando o modelo for usado em produção.
3. `dropna` é último recurso, não primeira resposta.
4. A ausência em si pode ser um atributo — considere adicionar uma coluna indicadora antes de descartar o sinal.
5. XGBoost/CatBoost/LightGBM toleram `NaN` nativamente; os demais modelos do sklearn geralmente não.

## Connects To
- **Ch 3**: aplicou `IterativeImputer` no fluxo completo; este capítulo aprofunda as alternativas.
- **Ch 5**: ferramentas de limpeza mais gerais (pyjanitor) que complementam a imputação.
- **Ch 7**: pré-processamento (`col_na`, engenharia de atributos) retoma a coluna indicadora de ausência.
</content>
