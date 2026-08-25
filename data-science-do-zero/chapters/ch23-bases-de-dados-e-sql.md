# Capítulo 23 — Bases de Dados e SQL

## Motivação
Bancos relacionais (Oracle, MySQL, SQL Server) armazenam dados em tabelas, consultados via **SQL** (linguagem declarativa). O capítulo constrói **NotQuiteABase**, um mini-banco em Python puro, ensinando SQL "do zero" — resolver problemas em NotQuiteABase para depois reconhecer o padrão em SQL real.

## CREATE TABLE / INSERT
Tabela = esquema fixo (nomes/tipos de coluna) + linhas. `NotQuiteABase` ignora tipos mas se comporta como se os respeitasse. Representação interna: cada linha é um **dict** (nome_coluna → valor) — deliberadamente não-realista (bancos reais não fariam assim), mas mais simples de manipular.
```python
class Table:
    def __init__(self, columns): self.columns = columns; self.rows = []
    def insert(self, row_values): ...  # zip(columns, values) -> dict, append
```
Equivalência direta: `CREATE TABLE` → `Table(["col1","col2",...])`; `INSERT INTO ... VALUES` → `table.insert([...])`.

## UPDATE
SQL `UPDATE tabela SET campo=valor WHERE condição`. NotQuiteABase: `update(self, updates, predicate)` — `updates` é um dict de novos valores, `predicate` é uma função que retorna `True`/`False` por linha; itera todas as linhas, aplica se o predicado bate.

## DELETE
`DELETE FROM tabela` (apaga tudo, "forma perigosa") vs. `DELETE FROM tabela WHERE ...` (forma seletiva). NotQuiteABase: `delete(self, predicate=lambda row: True)` — sem predicado, apaga tudo (comportamento padrão perigoso replicado propositalmente); com predicado, mantém só as linhas que **não** o satisfazem.

## SELECT
Não se inspeciona a tabela diretamente — consulta-se com `SELECT`. NotQuiteABase decompõe em métodos encadeáveis (cada um retorna uma **nova** `Table`, diferente do SQL onde `SELECT` produz um resultado transitório):
- `select(keep_columns=None, additional_columns=None)` — escolhe colunas a manter e/ou computa colunas novas via funções (`additional_columns` é um dict `{nome: função(row)}`), equivalente a `SELECT col, LENGTH(name) AS name_length FROM ...`.
- `where(predicate)` — filtra linhas, equivalente à cláusula `WHERE`.
- `limit(num_rows)` — equivalente a `LIMIT`.

Métodos são **encadeáveis** (`users.where(...).select(...)`) espelhando a composição de cláusulas SQL.

## GROUP BY / HAVING
Paralelo direto com `group_by` do Capítulo 10 (Manipulando Dados). NotQuiteABase: `group_by(group_by_columns, aggregates, having=None)`:
1. Agrupa linhas em `defaultdict(list)` chaveado por **tupla** dos valores das colunas de agrupamento (lista não pode ser chave de dict — por isso tupla).
2. Para cada grupo, aplica cada função de agregação (`aggregates`, dict `{nome_saída: função(rows)}`) e insere uma linha de resultado.
3. `having` filtra **grupos agregados** (diferente de `where`, que filtra linhas individuais **antes** da agregação) — replica a distinção `WHERE` (pré-agregação) vs. `HAVING` (pós-agregação) do SQL.

Agregação sem `GROUP BY` (total geral) = chamar `group_by(group_by_columns=[], ...)` — um único grupo contendo tudo.

## ORDER BY
`order_by(self, order)` — recebe uma função-chave (não uma string de coluna), ordena as linhas com `.sort(key=order)`. SQL `ASC`/`DESC` por campo teria que ser embutido na função `order` (ex.: negar o valor para inverter).

## JOIN
Bancos relacionais são **normalizados** (minimizam redundância) — dados um-para-muitos vão para tabelas separadas relacionadas por chave (ex.: `user_interests(user_id, interest)` separada de `users`). `JOIN` combina linhas de duas tabelas por uma condição de correspondência.

- **INNER JOIN**: só produz combinações onde a condição bate em ambos os lados.
- **LEFT JOIN**: além das combinações, preserva linhas da tabela esquerda **sem** correspondência (campos da direita ficam `NULL`/`None`) — usado para, por exemplo, contar interesses por usuário **incluindo usuários sem nenhum interesse** (que teriam contagem 0, não desapareceriam da consulta).

NotQuiteABase `join(self, other_table, left_join=False)`: simplificação deliberada — junta automaticamente pelas **colunas em comum** entre as duas tabelas (não permite especificar a condição de junção explicitamente, ao contrário do SQL `ON`). Para cada linha da esquerda, procura correspondências na direita (`other_table.where(is_join)`); se `left_join=True` e não há correspondência, insere a linha com `None` nas colunas exclusivas da direita. **RIGHT JOIN e FULL OUTER JOIN não são implementados** — reconhecido explicitamente como fora de escopo.

## Subconsultas
Em SQL, o resultado de um `SELECT` pode ser usado como tabela de outra consulta (subquery). Em NotQuiteABase isso **já funciona de graça**, porque todo método sempre retorna um objeto `Table` — não há distinção entre "tabela" e "resultado de consulta".

## Índices (conceitual, não implementado)
Resolvem três problemas que NotQuiteABase sofre por não os ter: (1) busca por valor exige varrer a tabela inteira; (2) `join` é `O(n·m)` porque compara cada linha da esquerda com todas da direita; (3) não há como impor unicidade (ex.: `user_id` não repetido) sem varredura completa. Descrito como uma "arte negra" que varia por banco de dados — vale aprender bem se você trabalha muito com bancos.

## Otimização de Consulta
Mesma consulta lógica escrita de duas formas — filtrar `user_interests` **antes** de juntar com `users`, vs. juntar primeiro e filtrar depois — produz o mesmo resultado, mas **filtrar antes de juntar é mais eficiente** (menos linhas para o `join` processar). Em SQL de verdade isso normalmente não é sua preocupação: você declara o resultado desejado e o **motor de consulta otimiza** a ordem de execução (usando índices, reordenando joins, etc.) — diferente de NotQuiteABase, que executa exatamente a sequência de métodos como escrita.

## NoSQL (panorama, não implementado)
Menção de bancos não-relacionais: documentos JSON sem esquema fixo (MongoDB), bancos colunares (bons quando há muitas colunas mas consultas tocam poucas), key-value stores, bancos de grafos, bancos distribuídos multi-datacenter, bancos in-memory, séries temporais. O autor reconhece explicitamente não tentar cobrir isso a fundo — só sinaliza que a categoria existe.

## Por Que Isso Importa
`group_by` aqui é uma reimplementação especializada (com `having` e agregações nomeadas) do padrão genérico já visto no Capítulo 10 — mostra a mesma ideia (agrupar + agregar) sob a lente de bancos de dados. É o único capítulo do livro sobre infraestrutura de armazenamento persistente, complementando o Capítulo 9 (aquisição) e o Capítulo 10 (manipulação em memória).
