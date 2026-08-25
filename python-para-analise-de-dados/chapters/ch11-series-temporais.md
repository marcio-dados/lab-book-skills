# Capítulo 11: Séries temporais

## Core Idea
pandas oferece uma pilha coerente para séries temporais: `Timestamp`/`DatetimeIndex` para instantes, `Period`/`PeriodIndex` para intervalos, offsets/frequências para geração e deslocamento de datas, e `resample`/`rolling` (com a mesma "forma" de `groupby`) para conversão de frequência e estatísticas de janela móvel.

## Frameworks Introduced
- **Timestamp vs. Period**: `Timestamp` representa um instante específico; `Period` representa um intervalo de tempo não sobreposto (mês, trimestre, ano). Escolher um ou outro depende se o dado é "um ponto no tempo" ou "um bucket de tempo".
  - Quando usar: `Timestamp`/`DatetimeIndex` para a maioria dos dados observados a instantes; `Period`/`PeriodIndex` para dados contábeis/fiscais organizados por período (trimestre fiscal, ano).
  - Como: `pd.to_datetime(strings)` para timestamps; `pd.Period(str, freq=)`/`pd.PeriodIndex(...)` para períodos; `asfreq`/`to_period`/`to_timestamp` convertem entre granularidades e entre os dois mundos.
- **`resample` como `groupby` para tempo**: mesma API (split-apply-combine), mas a "chave" é implicitamente derivada da frequência-alvo.
  - Quando usar: downsampling (frequência alta→baixa, precisa de agregação) ou upsampling (baixa→alta, precisa de interpolação/`ffill`).
  - Como: `ts.resample(freq).mean()` (downsampling); `ts.resample(freq).ffill()`/`.asfreq()` (upsampling); controlar bordas com `closed=`/`label=`.
- **Funções de janela móvel (`rolling`/`expanding`/`ewm`)**: estatísticas calculadas sobre uma janela deslizante, expansiva, ou com peso exponencialmente decrescente, análogas em API a `groupby`/`resample`.
  - Quando usar: suavizar séries ruidosas (`rolling(window).mean()`), acompanhar tendência desde o início da série (`expanding()`), ou dar mais peso a observações recentes (`ewm(span=)`).

## Key Concepts
- **`datetime`/`timedelta` (stdlib)**: base para representação de data/hora e diferenças; `strftime`/`strptime` formatam/parseiam com códigos (`%Y-%m-%d` etc.).
- **`dateutil.parser.parse`**: parse flexível de datas "legíveis por humanos" sem especificar formato (cuidado: reconhece strings ambíguas como datas, ex. `'42'` vira ano 2042).
- **`pd.to_datetime`**: parser vetorizado para arrays de strings de data; trata `None`/string vazia como `NaT` (Not a Time, o "NaN" de timestamps).
- **`DatetimeIndex`/`Timestamp`**: internamente `datetime64[ns]` (resolução de nanossegundos); indexação parcial por string funciona em múltiplos níveis de granularidade (`ts['2001']`, `ts['2001-05']`).
- **Fatiamento por data é uma view** (como arrays NumPy) — não copia; `truncate(before=, after=)` é o método de instância equivalente.
- **Índices de data duplicados**: `is_unique` detecta; agregação por timestamp duplicado via `groupby(level=0)`.
- **`pd.date_range(start, end, periods, freq)`**: gera `DatetimeIndex` com frequência fixa; `normalize=True` zera a hora.
- **Offsets de data (`Hour`, `Day`, `MonthEnd`...)**: objetos que representam frequências; somáveis (`Hour(2) + Minute(30)`); offsets "ancorados" (`MonthEnd`, `BM`) não são uniformemente espaçados — dependem do calendário.
- **`shift(n, freq=)`**: desloca valores (`freq=None`, índice fixo, introduz `NaN`) ou desloca o próprio índice (`freq=` informado, sem introduzir `NaN`) — base para calcular retornos percentuais (`ts / ts.shift(1) - 1`).
- **Fuso horário (`tz_localize`/`tz_convert`)**: por padrão séries pandas não têm fuso; `tz_localize` atribui um fuso a dados "naive"; `tz_convert` converte entre fusos já localizados; internamente tudo é armazenado como UTC em nanossegundos.
- **`Period.asfreq(freq, how='start'|'end')`**: converte a granularidade de um período, escolhendo o sub/superperíodo correspondente ao início ou fim.
- **`resample(...).ohlc()`**: agregação financeira padrão (open/high/low/close) em uma única varredura.
- **`rolling(window, min_periods=)`**: por padrão exige janela completa sem NA; `min_periods` permite resultado parcial no início da série.
- **`ewm(span=)`**: média móvel exponencialmente ponderada — mais peso a observações recentes, mais responsiva a mudanças que a média móvel simples.
- **`rolling(...).apply(func)`**: janela móvel com função customizada, desde que devolva um escalar por janela (ex. `scipy.stats.percentileofscore`).

## Mental Models
- Pense em `Period` como um "cursor apontando para um intervalo, subdividido conforme a frequência-alvo" — converter frequência é perguntar "esse instante pertence a qual subperíodo/superperíodo?".
- Pense em `resample` como `groupby` onde a chave de agrupamento é sempre derivada da própria data — controle `closed=`/`label=` para decidir a qual bucket cada timestamp de borda pertence.
- Pense em `rolling`/`expanding`/`ewm` como três formas de responder "qual peso cada observação passada recebe?": peso igual numa janela fixa, peso igual desde o início, peso decrescente exponencialmente.

## Anti-patterns
- **Confiar cegamente em `dateutil.parse` para strings arbitrárias**: reconhece falsos positivos como datas (ex. números curtos) — validar formato quando a entrada não é confiável.
- **Ignorar `NaT` como caso especial de ausência**: operações de igualdade/comparação com `NaT` seguem a semântica de `NaN`; sempre checar com `pd.isnull`.
- **Fazer aritmética entre `Timestamp` com fuso e sem fuso diretamente**: gera erro; é preciso `tz_localize`/`tz_convert` para alinhar antes de operar.
- **Fazer upsampling de `Period` para uma frequência que não é superperíodo exato**: lança exceção — as regras de sub/superperíodo em `Period` são mais rígidas que em `Timestamp`.
- **Usar `rolling(window)` sem pensar em `min_periods`**: por padrão, os primeiros `window-1` valores viram `NaN` — se resultado parcial é aceitável/desejado, ajustar `min_periods`.

## Code Examples
```python
import pandas as pd

# Downsampling com controle explícito de borda e rótulo do bucket
ts.resample('5min', closed='right', label='right').sum()

# Média móvel exponencialmente ponderada vs. simples
ma60 = aapl_px.rolling(30, min_periods=20).mean()
ewma60 = aapl_px.ewm(span=30).mean()

# Correlação móvel entre uma ação e o S&P 500 (janela de 125 dias)
corr = returns.AAPL.rolling(125, min_periods=100).corr(spx_rets)
```
- **O que demonstra**: controle fino de fronteiras de bucket em downsampling, e como janelas móveis (simples, exponencial, correlação bivariada) compartilham a mesma API `rolling`/`ewm`.

## Reference Tables
| Frequência (alias) | Significado |
|---|---|
| `D` / `B` | Dia corrido / dia útil |
| `H`, `T`/`min`, `S` | Hora, minuto, segundo |
| `M` / `BM` | Fim de mês (calendário / dia útil) |
| `W-MON`...`W-SUN` | Semanal, ancorado no dia da semana |
| `Q-JAN`...`Q-DEC` | Trimestral, ancorado no mês fiscal |
| `A-JAN`...`A-DEC` | Anual, ancorado no mês fiscal |

| Argumento `resample` | Papel |
|---|---|
| `closed='left'/'right'` | Qual borda do intervalo é inclusiva |
| `label='left'/'right'` | Rótulo do bucket = início ou fim do intervalo |
| `kind='period'/'timestamp'` | Tipo do índice resultante |
| `convention='start'/'end'` | Upsampling de `Period`: âncora do subperíodo |

## Worked Example
Cálculo de correlação móvel de 6 meses entre o retorno da Apple e o S&P 500: primeiro `spx_rets = spx_px.pct_change()` e `returns = close_px.pct_change()` calculam retornos percentuais diários; depois `returns.AAPL.rolling(125, min_periods=100).corr(spx_rets)` produz uma série temporal da correlação em janela deslizante de 125 dias (mínimo 100 observações válidas). Generalizando para múltiplas ações simultaneamente, `returns.rolling(125, min_periods=100).corr(spx_rets)` (passando um `DataFrame` inteiro em vez de uma `Series`) calcula a correlação de cada coluna com `spx_rets` de uma vez — evitando um laço manual sobre as colunas. Isso ilustra como a API `rolling` generaliza de univariado para "uma Series contra várias colunas" sem mudança de sintaxe.

## Key Takeaways
1. Escolha `Timestamp` para instantes observados e `Period` para intervalos fiscais/contábeis — a conversão entre eles (`to_period`/`to_timestamp`) é explícita e direcional.
2. `resample` é `groupby` temporal: mesma disciplina de split-apply-combine, com `closed=`/`label=` controlando a atribuição de bordas.
3. `shift(n, freq=)` desloca o índice (sem introduzir NaN) quando a frequência é conhecida — a base de qualquer cálculo de retorno percentual em série temporal.
4. Fusos horários são armazenados internamente em UTC; `tz_localize` atribui, `tz_convert` translada — nunca misture Timestamps naive e aware sem normalizar antes.
5. `rolling`/`expanding`/`ewm` compartilham API: escolha pela forma de ponderação temporal que a análise exige (janela fixa, expansiva, ou exponencialmente decrescente).
6. `rolling(...).apply(func_customizada)` só exige que a função devolva um escalar por janela — abre a porta para qualquer estatística de janela não coberta nativamente.

## Connects To
- **Ch 2**: `datetime`/`strftime`/`strptime` da stdlib já introduzidos ali, retomados aqui em profundidade.
- **Ch 5**: alinhamento automático por índice em operações aritméticas — mesma mecânica aplicada a `DatetimeIndex`.
- **Ch 10**: `groupby` é o padrão do qual `resample` é um caso especializado; `dup_ts.groupby(level=0)` reaparece aqui para lidar com timestamps duplicados.
- **Ch 14**: exemplos reais de séries temporais financeiras (preços de ações, retornos) usam extensivamente `resample`/`rolling` deste capítulo.
</content>
