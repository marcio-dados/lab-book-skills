# Capítulo 7: Limpeza e preparação dos dados

## Core Idea
80% ou mais do tempo de um analista vai para carga, limpeza e reorganização de dados — o pandas oferece um kit consistente para tratar ausência (`NaN`), duplicatas, remapeamento de valores, discretização, outliers, amostragem, variáveis dummy e manipulação de strings/regex vetorizada, sempre com tratamento embutido de NA.

## Frameworks Introduced
- **NaN como sentinela universal de ausência**: pandas usa `float NaN` (e trata `None` como NA em arrays de objeto); toda a família `isnull`/`notnull`/`dropna`/`fillna` parte dessa convenção única.
  - Quando usar: qualquer decisão sobre dados faltantes.
  - Como: detectar com `isnull()`, decidir entre descartar (`dropna`, com `how='all'`/`thresh=N`) ou preencher (`fillna(valor|método|dict)`).
- **`cut`/`qcut` (discretização)**: converter dados contínuos em categorias (bins) — `cut` por fronteiras fixas (bins desiguais em contagem), `qcut` por quantis da amostra (bins iguais em contagem).
  - Quando usar: `cut` quando os limites têm significado de domínio (ex. faixas etárias); `qcut` quando se quer grupos de tamanho comparável para análise por grupo.
- **Variáveis dummy/indicadoras (`get_dummies`)**: converter uma coluna categórica em k colunas binárias — a ponte padrão entre dados categóricos e modelagem estatística/ML.
  - Quando usar: preparar features categóricas para modelos; combinar com `cut` para discretizar-e-binarizar em um passo.
- **Métodos de string vetorizados (`Series.str.*`)**: aplicar operações de string/regex em toda uma coluna, ignorando `NaN` automaticamente (ao contrário de `.map` com lambda, que falha em NA).
  - Quando usar: qualquer limpeza de texto em uma coluna que pode conter valores ausentes.

## Key Concepts
- **`dropna(how=, axis=, thresh=)`**: `how='any'` (default) descarta linha/coluna com qualquer NA; `how='all'` só se tudo for NA; `thresh=N` exige ao menos N valores não-NA.
- **`fillna(value|method=, limit=, inplace=)`**: `value` pode ser escalar, `dict` (valor por coluna) ou resultado de `.mean()`; `method='ffill'`/`'bfill'` interpola; `limit` restringe o tamanho da lacuna preenchida.
- **`duplicated()`/`drop_duplicates(subset, keep=)`**: detecção/remoção de linhas duplicadas; `keep='first'` (default) ou `'last'` define qual ocorrência sobrevive.
- **`Series.map(dict|func)`**: transformação element-wise via dicionário ou função — idiomático para "traduzir" categorias (ex. tipo de carne → animal de origem).
- **`replace(old, new)`**: substituição de valores (não índice, não string em massa) — aceita escalar, lista→lista, ou dict; distinto de `str.replace` (que atua em substrings).
- **`rename(index=, columns=, inplace=)`**: renomeia rótulos de eixo via função ou dict parcial, sem precisar copiar manualmente e reatribuir `.index`/`.columns`.
- **`cut(data, bins, labels=, right=)`**: bins podem ser lista de fronteiras ou inteiro (bins de largura igual); `right=False` torna o intervalo fechado à esquerda; retorna `Categorical` com `.codes`/`.categories`.
- **Detecção de outliers**: `data[(np.abs(data) > 3).any(1)]` seleciona linhas com qualquer valor extremo; `np.sign(data) * 3` faz "capping" (winsorização simples) preservando o sinal.
- **Amostragem (`np.random.permutation`, `.sample(n=, replace=)`)**: `.take(sampler)`/`.sample()` para embaralhar ou amostrar linhas, com ou sem reposição.
- **Regex (`re.compile`, `.findall`/`.search`/`.match`/`.sub`, grupos com `()`)**: `re.compile` é recomendado quando a mesma regex será reaplicada muitas vezes (economiza ciclos de CPU); `match` só casa no início da string, `search` em qualquer posição.

## Mental Models
- Pense em toda limpeza de dados ausentes como uma escolha binária entre **descartar** (`dropna`) e **preencher** (`fillna`) — a decisão de qual usar depende de quanto dado você pode perder vs. quanto viés a imputação introduz.
- `cut` vs. `qcut`: `cut` responde "que faixa este valor ocupa?" (fronteiras fixas, contagens desiguais); `qcut` responde "em que percentil este valor está?" (fronteiras variáveis, contagens iguais).
- `Series.str` é a "versão vetorizada e NA-safe" de tudo que os métodos de string embutidos de Python já fazem — use-o sempre que a coluna puder conter `NaN`.

## Anti-patterns
- **Usar `data.map(lambda x: ...)` em uma coluna de string com valores ausentes**: falha (lança erro) no primeiro `NaN` — usar `Series.str.*` em vez disso, que ignora NA automaticamente.
- **Confundir `Series.replace` com `Series.str.replace`**: `replace` substitui valores inteiros (correspondência exata); `str.replace` faz substituição de substring/regex dentro de cada string — usá-los trocados produz resultado silenciosamente errado.
- **Ignorar `keep=` em `drop_duplicates`**: o default mantém a primeira ocorrência; se a análise depende do registro mais recente, é preciso `keep='last'` explicitamente.
- **Construir variáveis dummy multi-membro (`get_dummies` por gênero de filme) com loop Python ingênuo em datasets grandes**: não escala; o autor recomenda escrever a lógica diretamente sobre um array NumPy e só depois encapsular em `DataFrame`.
- **Não usar `re.compile` ao reaplicar a mesma regex muitas vezes**: cada chamada de `re.split`/`re.match` sem regex pré-compilada recompila o padrão — custo evitável em loops.

## Code Examples
```python
import pandas as pd
import numpy as np

# Discretização com bins fixos + rótulos customizados
bins = [18, 25, 35, 60, 100]
group_names = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior']
cats = pd.cut(ages, bins, labels=group_names)

# Winsorização simples: cap em +-3 desvios, preservando o sinal
data[np.abs(data) > 3] = np.sign(data) * 3

# Extração de e-mail com grupos regex + métodos vetorizados NA-safe
pattern = r'([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})'
data.str.findall(pattern, flags=re.IGNORECASE)
```
- **O que demonstra**: três padrões recorrentes de limpeza — categorizar valores contínuos, tratar outliers sem descartar linhas, e extrair estrutura de texto livre com regex de forma vetorizada e tolerante a `NaN`.

## Reference Tables
| Método NA | Papel |
|---|---|
| `isnull`/`notnull` | Detecta ausência (booleano) |
| `dropna(how=, thresh=)` | Descarta linhas/colunas com ausência |
| `fillna(value|method=)` | Preenche ausência |

| Método string pandas (`Series.str.*`) | Descrição |
|---|---|
| `contains` | Testa presença de padrão/regex (booleano) |
| `extract` | Extrai grupos regex → DataFrame (1 coluna por grupo) |
| `findall` | Lista de ocorrências por elemento |
| `split` / `get` / `slice` | Separa / indexa / fatia cada string |
| `len`, `strip`, `lower`, `upper` | Equivalentes vetorizados dos métodos nativos |

| Método regex (`re`) | Descrição |
|---|---|
| `match` | Casa só no início da string |
| `search` | Casa em qualquer posição, primeira ocorrência |
| `findall` | Todas as ocorrências (lista) |
| `sub`/`subn` | Substitui ocorrências (todas / N primeiras) |

## Worked Example
Construção de variáveis indicadoras multi-membro para o dataset MovieLens: cada filme tem uma string `genres` como `"Animation|Children's|Comedy"`. O autor extrai a lista de gêneros únicos (`all_genres`), cria uma matriz de zeros `len(movies) × len(genres)`, e para cada filme usa `dummies.columns.get_indexer(gen.split('|'))` para localizar as colunas correspondentes e marcá-las com 1 via `.iloc[i, indices] = 1`. O resultado é unido de volta com `movies.join(dummies.add_prefix('Genre_'))`. Isso ilustra o padrão geral para "uma linha pertence a várias categorias simultaneamente" — diferente do caso simples de `get_dummies` de coluna única — e o autor observa explicitamente que essa abordagem com loop não escala bem para datasets grandes, recomendando uma implementação de mais baixo nível em NumPy puro para esse caso.

## Key Takeaways
1. Trate ausência como decisão binária descartar-vs-preencher; escolha `thresh`/`how` em `dropna` ou `value`/`method` em `fillna` conforme o quanto de dado a operação pode custar.
2. `cut` (fronteiras fixas) e `qcut` (quantis) resolvem problemas diferentes de discretização — não são intercambiáveis.
3. `Series.str.*` é a via padrão para limpeza de texto em colunas com `NaN` — `map`/lambda quebra em ausência.
4. `get_dummies` é a ponte padrão categórico→numérico para modelagem; combine com `cut` para discretizar-e-binarizar.
5. `re.compile` antecipadamente quando a mesma regex será reaplicada muitas vezes.
6. Outliers podem ser tratados sem perder linhas inteiras: capping (`np.sign(data) * limite`) preserva o formato do dataset.

## Connects To
- **Ch 5**: pré-requisito — `isnull`, `fillna`, `apply` já introduzidos ali no básico.
- **Ch 8**: reorganização/combinação de dados (merge, concat, reshape) como continuação natural da limpeza.
- **Ch 10**: `cut`/`qcut` retomados no contexto de agregação por grupo (`groupby`).
- **Ch 14**: usa extensivamente os padrões de limpeza deste capítulo (e o próprio dataset MovieLens) em exemplos completos.
</content>
