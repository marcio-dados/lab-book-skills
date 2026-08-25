# Cheatsheet — Python para Análise de Dados

## Decisões rápidas

- **Vetorizar ou laço?** Se a operação é element-wise ou uma redução, vetorize (array/ufunc/`Series.str`). Só use laço Python quando a lógica genuinamente não se expressa como array (então considere `rolling(...).apply` ou Numba antes de aceitar o laço).
- **`.agg` vs `.transform` vs `.apply` em GroupBy**: resultado é 1 valor por grupo → `.agg`. Resultado tem o mesmo formato da entrada (broadcast) → `.transform`. Qualquer outra coisa (top-N, regressão, múltiplos valores não-broadcast) → `.apply`.
- **`merge` vs `concat`**: combinando por valor de chave compartilhada → `merge`. Empilhando blocos com a mesma estrutura → `concat`.
- **`cut` vs `qcut`**: fronteiras com significado de domínio (faixas etárias, buckets de valor) → `cut`. Grupos de tamanho comparável para comparação estatística → `qcut`.
- **`loc` vs `iloc`**: por rótulo → `loc`. Por posição inteira → `iloc`. Nunca dependa de `[]` ambíguo para seleção de linha por posição.
- **`Timestamp` vs `Period`**: instante observado → `Timestamp`/`DatetimeIndex`. Intervalo fiscal/contábil (mês, trimestre) → `Period`/`PeriodIndex`.
- **`dropna` vs `fillna`**: pode perder a linha/coluna sem viés relevante → `dropna` (`how=`/`thresh=`). Precisa preservar a linha → `fillna` (`value`/`method=`, sempre com estatística do treino se for para modelagem).
- **`astype('category')`?** Sim se poucos valores distintos repetidos muitas vezes (baixa cardinalidade) e o dataset é grande o suficiente para o custo de conversão compensar em `groupby`/memória repetidos.

## Limiares e defaults a lembrar

| Situação | Regra prática |
|---|---|
| Comparar médias entre grupos | Filtre por tamanho mínimo de grupo antes (ex. `groupby(...).size() >= N`) — médias de amostras pequenas enganam ranking |
| `rolling(window)` | Sempre decidir `min_periods` explicitamente — default exige janela completa sem NA |
| `merge` sem `on=` explícito | Evitar — depende de inferência implícita de colunas em comum, frágil |
| Imputação para modelo | Estatística sempre do conjunto de treino, aplicada idêntica no teste — nunca recalcular no teste |
| `re.compile` | Compilar antecipadamente se a mesma regex roda muitas vezes em loop |
| Ordenar `MultiIndex` | `sort_index(level=0)` antes de seleção repetida em datasets grandes — impacto real de performance |

## Tabela de decisão: reshape

| Tenho... | Quero... | Uso |
|---|---|---|
| Formato longo (uma linha por observação) | Uma coluna por variável | `pivot(index, columns, values)` |
| Várias colunas de valor | Duas colunas (`variable`, `value`) | `melt(df, id_vars=, value_vars=)` |
| `MultiIndex` nas linhas | Nível do índice como coluna | `unstack(level=)` |
| Colunas + `MultiIndex` | Nível de coluna como linha | `stack(level=)` |

## Tells / cheiros de problema

- `KeyError` intermitente em campo de dict/JSON → schema variável por registro; sempre `if campo in registro` antes de list comprehension.
- Resultado de `groupby(...).mean()` "perdeu" uma coluna → coluna não-numérica descartada silenciosamente ("nuisance column"); agregue-a separadamente se precisar dela.
- `merge` devolveu muito mais linhas que o esperado → junção muitos-para-muitos, produto cartesiano de chaves duplicadas — checar cardinalidade das chaves antes.
- `NaN` aparecendo após `unstack`/`reindex`/`shift` sem `freq=` → esperado quando não há correspondência completa entre os rótulos; decidir `fillna`/`fill_value` conscientemente.
- Comparação de dois métodos "equivalentes" com tempos muito diferentes → confirme com `%timeit` (não `%time`, ruidoso) antes de concluir.
- Broadcasting falha com `ValueError: operands could not be broadcast` → uma dimensão do array menor não é 1 nem coincide; usar `np.newaxis`/`reshape` no eixo certo.

## Trade-off matrix: profiling

| Ferramenta | Granularidade | Custo de setup | Quando |
|---|---|---|---|
| `%timeit` | 1 instrução | Nenhum | Comparar duas expressões |
| `%prun` | Por função | Nenhum | "Qual função consome o tempo?" |
| `%lprun -f func` | Por linha | Extensão `line_profiler` | "Qual linha dentro desta função?" |
</content>
