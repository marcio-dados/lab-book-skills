# Capítulo 5: Fazendo uma limpeza nos dados

## Core Idea
`pandas` cobre a limpeza genérica de dados; `pyjanitor` adiciona funções especializadas (nomes de coluna, coalescência de valores) no estilo de planilhas/SQL, que reduzem código repetitivo sem substituir o pandas.

## Key Concepts
- **Nomes de coluna válidos como identificador Python**: `jn.clean_names(df)` normaliza nomes (minúsculas, espaços viram `_`), mas não remove espaços nas bordas — para isso é preciso uma função própria (`name.strip().lower().replace(" ", "_")`) via `.rename(columns=...)`.
- **`jn.coalesce(df, columns=[...], new_column_name=...)`**: devolve o primeiro valor não nulo entre várias colunas por linha — equivalente ao `COALESCE` de SQL/Excel.
- **`fillna(valor)` / `jn.fill_empty(df, columns=[...], value=...)`**: preenchimento simples por constante, útil como passo intermediário antes de imputações mais sofisticadas.
- **Verificação de sanidade**: `df.isna().any().any()` devolve um único booleano informando se ainda resta qualquer célula ausente no DataFrame — checagem final antes de treinar.

## Anti-patterns
- **Atualizar colunas por atribuição direta (`df.coluna = ...`)**: risco de colidir com métodos/atributos existentes do DataFrame com o mesmo nome; preferir indexação (`df['coluna'] = ...`), `.assign`, ou `.loc`/`.iloc`.

## Code Examples
```python
import janitor as jn

# nomes de coluna válidos em Python
jn.clean_names(Xbad)

# limpeza mais fina (remove espaços nas bordas, que o pyjanitor não trata)
def clean_col(name):
    return name.strip().lower().replace(" ", "_")
Xbad.rename(columns=clean_col)

# primeiro valor não nulo entre colunas (estilo COALESCE)
jn.coalesce(Xbad, columns=["A", "  sales numbers "], new_column_name="val")

# checagem final antes de modelar
df.isna().any().any()
```
- **O que demonstra**: pyjanitor como complemento (não substituto) do pandas para tarefas repetitivas de limpeza, terminando sempre com uma verificação de sanidade.

## Key Takeaways
1. `pyjanitor` existe para reduzir boilerplate de limpeza comum (nomes de coluna, coalescência), não para substituir imputação real.
2. Nunca atribua colunas por `df.nome = valor` — use indexação ou `.assign` para evitar colisão com métodos existentes.
3. Termine toda etapa de limpeza com `df.isna().any().any()` como verificação de sanidade.

## Connects To
- **Ch 4**: estratégias de imputação mais robustas que complementam o `fillna`/`coalesce` genérico deste capítulo.
- **Ch 6**: exploração de dados assume que os nomes de coluna e valores ausentes já foram tratados aqui.
</content>
