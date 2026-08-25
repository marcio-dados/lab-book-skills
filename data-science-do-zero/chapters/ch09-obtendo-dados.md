# Capítulo 9 — Obtendo Dados

## stdin / stdout
Scripts Python podem ser encadeados via pipe Unix (`cat arquivo | python script1.py | python script2.py`), lendo `sys.stdin` linha a linha e escrevendo em `sys.stdout`. Exemplos construídos: `egrep.py` (filtra linhas por regex passado em `sys.argv[1]`), `line_count.py` (conta linhas), `most_common_words.py` (tokeniza por espaço, `Counter`, imprime as `N` palavras mais comuns). Padrão: ferramentas de linha de comando Unix (grep, wc) já fazem isso melhor — construir do zero é só para entender o mecanismo.

## Lendo Arquivos
- `open(caminho, modo)` — modos `'r'` (leitura), `'w'` (escrita, destrutiva), `'a'` (anexar). **Sempre usar `with open(...) as f:`** para garantir fechamento automático mesmo em caso de exceção.
- Iterar linha a linha com `for line in f`; cada linha traz `\n` — usar `.strip()`.
- Exemplo: extrair domínio de e-mails com `email.lower().split("@")[-1]` (aproximação simplificada, não trata a Lista Pública de Sufixos corretamente).

## Arquivos Delimitados (CSV/TSV)
**Nunca faça parsing manual de CSV** (vírgulas/tabs/newlines dentro de campos quebram uma implementação ingênua) — usar o módulo `csv` (ou pandas). No Python 2, abrir em modo binário (`'rb'`/`'wb'`) por causa de peculiaridades do Windows.
- `csv.reader(f, delimiter='\t')` — sem cabeçalho, cada linha é uma lista posicional.
- `csv.DictReader(f, delimiter=':')` — com cabeçalho, cada linha é um dict indexado pelos nomes das colunas (ou usa `fieldnames=` se o arquivo não tiver cabeçalho).
- `csv.writer(f, delimiter=',')` + `.writerow([...])` — escapa corretamente vírgulas/newlines dentro de campos; um escritor "feito à mão" (`",".join(...)`) corrompe o arquivo caso os valores contenham o próprio delimitador.

## Extraindo Dados da Internet (Web Scraping)
- HTML é estruturado em tags/atributos, mas raramente bem formado — usar **BeautifulSoup** (`bs4`) sobre o parser `html5lib` (mais tolerante que o parser embutido do Python) + **requests** para HTTP.
- API básica: `soup.find('p')` / `soup.p`, `.text` para conteúdo, `tag['atributo']` (levanta `KeyError`) ou `.get('atributo')` (retorna `None`), `soup.find_all('tag')` / `soup('tag')`, filtro por classe (`soup('p', 'important')`).
- **Etiqueta obrigatória antes de raspar**: checar termos de uso do site e o `robots.txt` (`Crawl-delay`, `Request-rate`) — o exemplo do livro respeita 30s entre requisições.

### Estudo de Caso: Catálogo de Livros de Dados da O'Reilly
Passo a passo completo de raspagem: localizar o contêiner repetido (`<td class="thumbtext">`), filtrar itens indesejados por heurística de estrutura (`is_video`: exatamente um `<span class="pricelabel">` começando com "Video"), extrair campos por navegação de árvore (`title`, `authors` via regex `re.sub("^By ", "", ...)`, `isbn` via `re.match` sobre o `href`, `date`). Paginação com `sleep(30)` entre páginas (respeitando `robots.txt`). Resultado agregado com `Counter` por ano de publicação, plotado como série temporal — usado ironicamente no fim para mostrar como uma mesma visualização pode ser mal interpretada ("2013 foi o pico de data science").

## Usando APIs
APIs poupam o trabalho de scraping ao fornecer dados estruturados, tipicamente em **JSON** (às vezes XML). `json.loads(string)` desserializa JSON em dict/list Python nativos.

### API não-autenticada (GitHub)
`requests.get(endpoint).text` + `json.loads(...)` — datas vêm como string; `dateutil.parser.parse` (`pip install python-dateutil`) converte para `datetime`. Recomendação geral: preferir uma biblioteca-wrapper de terceiros já pronta para a API-alvo em vez de lidar com requisições/autenticação manualmente — só vale a pena entender o nível baixo para depurar quando o wrapper falha.

### API autenticada (Twitter via Twython)
Fluxo de credenciais: criar app em apps.twitter.com → `CONSUMER_KEY`/`CONSUMER_SECRET` (identifica a aplicação) + `ACCESS_TOKEN`/`ACCESS_TOKEN_SECRET` (identifica o usuário). **Tratar como senha** — nunca commitar em repositório público; guardar em `credentials.json` ignorado pelo versionamento.
- **Search API**: `twitter.search(q='"data science"')` — busca limitada e não representativa (o Twitter só retorna a fatia que quiser).
- **Streaming API**: subclasse de `TwythonStreamer` sobrescrevendo `on_success`/`on_error`; `stream.statuses.filter(track='data')` consome o stream ao vivo. Padrão de acumulação: anexar a uma lista em memória até atingir um limite e então `self.disconnect()` — ressalva do autor: em produção, persistir em arquivo/banco, não em lista in-memory.
- Cuidado com Unicode: tweets contêm caracteres que quebram `print` no Python 2 sem `.encode('utf-8')`.

## Por Que Isso Importa
Este capítulo é puramente de infraestrutura/aquisição — não introduz técnica analítica nova, mas estabelece os três canais de entrada de dados (arquivo local, scraping, API) usados como pano de fundo narrativo em capítulos posteriores (ex.: Cap. 20 usa texto coletado da web, Cap. 22 usa dados de interação de usuário).
