# Capítulo 6: Carga de dados, armazenagem e formatos de arquivo

## Core Idea
O pandas oferece uma família de funções `read_*`/`to_*` (CSV, JSON, HTML/XML, Excel, HDF5, SQL) que padroniza a leitura/escrita de dados heterogêneos em `DataFrame`, tratando categorias recorrentes de complexidade: indexação, inferência de tipo, parsing de data, iteração em partes e "dados sujos".

## Frameworks Introduced
- **Categorias de argumentos dos parsers de texto**: qualquer função `read_csv`-like resolve o mesmo conjunto de decisões — indexação (`index_col`), tipos (`dtype`/`converters`/`na_values`), datas (`parse_dates`), iteração (`chunksize`/`iterator`), dados sujos (`skiprows`/`comment`/`thousands`).
  - Quando usar: ao encontrar um arquivo malformado, primeiro identifique em qual categoria o problema se encaixa, depois procure o argumento correspondente — evita reinventar parsing manual.
- **Leitura em partes (`chunksize`)**: iterar um arquivo grande em pedaços em vez de carregá-lo inteiro, agregando incrementalmente.
  - Quando usar: arquivos que não cabem confortavelmente em memória, ou quando só se precisa de uma agregação (ex. `value_counts`).
  - Como: `chunker = pd.read_csv(path, chunksize=1000)`; iterar com `for piece in chunker:` acumulando com `.add(..., fill_value=0)`.

## Key Concepts
- **`read_csv`/`read_table`**: leitura de dados delimitados; `read_csv` tem +50 opções — a complexidade reflete a variedade real de "CSVs sujos" no mundo real, não acidente de design.
- **`header=None`/`names=[...]`**: controla se/como os nomes de coluna vêm do arquivo.
- **`index_col`**: define coluna(s) como índice de linha; lista de colunas cria índice hierárquico (`MultiIndex`).
- **`na_values`**: lista (ou dict por coluna) de strings adicionais a tratar como ausente, além dos sentinelas default (`NA`, `NULL`, etc.).
- **`sep` com regex**: `sep='\s+'` lida com delimitadores de largura variável (espaços múltiplos).
- **Módulo `csv` (stdlib)**: `csv.reader`/`csv.writer` para parsing manual de delimitados quando o formato foge do que `read_csv` cobre (ex. delimitador multicaractere não suportado — nesse caso usar `str.split`/`re.split`).
- **`json.loads`/`json.dumps`**: conversão string JSON ↔ objetos Python nativos (dict/list); `pd.read_json`/`.to_json(orient=...)` para o caminho direto a/de `DataFrame`.
- **`pd.read_html`**: extrai todas as tabelas `<table>` de um documento HTML como lista de `DataFrame`s (usa `lxml`/`beautifulsoup4`/`html5lib`).
- **`lxml.objectify`**: parsing de XML genérico (mais flexível que HTML) navegando a árvore de elementos manualmente.
- **Pickle (`to_pickle`/`read_pickle`)**: serialização binária rápida, mas **apenas para armazenagem de curto prazo** — não garantido estável entre versões de biblioteca.
- **HDF5 (`pd.HDFStore`)**: formato binário hierárquico para datasets grandes, com compressão e leitura parcial; formato `'table'` aceita consultas (`store.select(..., where=...)`) mas é mais lento que `'fixed'`.
- **`sqlite3`/SQLAlchemy + `pd.read_sql`**: caminho padrão para carregar resultados de consulta SQL diretamente como `DataFrame`, abstraindo diferenças entre drivers.

## Mental Models
- Pense nos +50 parâmetros de `read_csv` não como complexidade acidental, mas como um catálogo de "formas conhecidas de o mundo real quebrar um CSV" — antes de escrever parsing manual, verifique se já existe um parâmetro para o caso.
- HDF5 é "write-once, read-many" — não é um banco de dados; múltiplos escritores simultâneos podem corromper o arquivo.
- Pickle é conveniência de cache de curto prazo (mesma sessão/pipeline), não um formato de arquivamento de longo prazo.

## Anti-patterns
- **Usar pickle para armazenagem de longo prazo**: formato pode quebrar compatibilidade entre versões de biblioteca — usar CSV/HDF5/Parquet/feather para persistência duradoura.
- **Escrever vários processos simultaneamente no mesmo arquivo HDF5**: risco real de corrupção — HDF5 não é um banco de dados transacional.
- **Ler um arquivo inteiro na memória só para calcular uma agregação simples**: preferir `chunksize` + acumulação incremental quando o arquivo é grande e a operação final é uma redução (contagem, soma).
- **Reimplementar parsing de CSV malformado do zero**: primeiro checar as opções da Tabela 6.2 (`skiprows`, `na_values`, `sep` como regex, `comment`) — a maioria dos casos "sujos" já tem parâmetro dedicado.

## Code Examples
```python
import pandas as pd

# Índice hierárquico direto do CSV
parsed = pd.read_csv('examples/csv_mindex.csv', index_col=['key1', 'key2'])

# Leitura em partes + agregação incremental (arquivo grande)
chunker = pd.read_csv('examples/ex6.csv', chunksize=1000)
tot = pd.Series([])
for piece in chunker:
    tot = tot.add(piece['key'].value_counts(), fill_value=0)
tot = tot.sort_values(ascending=False)
```
- **O que demonstra**: como agregar um dataset maior que o desejável para memória, processando em partes com `chunksize` e combinando resultados parciais com `fill_value=0` (evita `NaN` de chaves que só aparecem em algumas partes).

## Reference Tables
| Função `read_*` | Formato |
|---|---|
| `read_csv` / `read_table` | Texto delimitado (vírgula / tab) |
| `read_fwf` | Colunas de largura fixa, sem delimitador |
| `read_excel` | Excel XLS/XLSX |
| `read_hdf` | HDF5 escrito pelo pandas |
| `read_html` | Tabelas `<table>` de um documento HTML |
| `read_json` | String/arquivo JSON |
| `read_sql` | Resultado de query SQL (via SQLAlchemy) |
| `read_pickle` | Objeto Python serializado (pickle) |

| Argumento comum de `read_csv` | Papel |
|---|---|
| `header` / `names` | Origem dos nomes de coluna |
| `index_col` | Coluna(s) usada(s) como índice |
| `skiprows` / `nrows` | Pular linhas / limitar quantidade lida |
| `na_values` | Sentinelas adicionais de valor ausente |
| `parse_dates` | Colunas a converter para `datetime` |
| `chunksize` / `iterator` | Leitura incremental em partes |
| `dtype` / `converters` | Controle explícito de tipo por coluna |

## Worked Example
Fluxo de scraping simples com `pd.read_html`: um arquivo HTML da FDIC (lista de falências bancárias) é passado para `pd.read_html(path)`, que devolve uma lista de `DataFrame`s (um por tabela `<table>` encontrada) — `tables[0]` já é a tabela pronta, com colunas como `Bank Name`, `Closing Date`. A partir daí, `pd.to_datetime(failures['Closing Date'])` converte a coluna de string para `datetime`, e `.dt.year.value_counts()` produz a contagem de falências por ano em uma linha — do HTML bruto à estatística agregada em três chamadas, sem parsing manual de tags.

## Key Takeaways
1. Antes de escrever parsing manual, verifique se o parâmetro certo de `read_csv`/`read_table` já resolve o caso "sujo" que você está vendo.
2. Use `chunksize` para arquivos grandes quando a operação final é uma agregação — evita carregar tudo em memória.
3. `pickle` é para cache de curto prazo dentro do seu próprio pipeline, nunca para arquivamento de longo prazo entre versões de biblioteca.
4. HDF5 é ideal para datasets grandes locais com padrão write-once/read-many; não é banco de dados multi-writer.
5. `pd.read_sql` + SQLAlchemy é o caminho padrão para trazer resultados de query SQL direto para `DataFrame`, sem lidar manualmente com cursors/tuplas.
6. `pd.read_html` cobre a maioria dos casos de "tabela dentro de página HTML"; para XML genérico ou HTML malformado, `lxml.objectify`/Beautiful Soup dão mais controle.

## Connects To
- **Ch 5**: pré-requisito — assume familiaridade com `Series`/`DataFrame` já construídos.
- **Ch 7**: uso do `USDA Food Database` (JSON aninhado) como exemplo de limpeza mais aprofundada, referenciado aqui.
- **Ch 11**: `parse_dates`/`pd.to_datetime` introduzidos aqui são pré-requisito para o tratamento de séries temporais.
</content>
