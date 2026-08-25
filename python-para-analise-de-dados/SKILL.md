---
name: python-para-analise-de-dados
description: "Base de conhecimento a partir de \"Python para Análise de Dados: Tratamento de Dados com Pandas, NumPy e IPython\" (2ª ed.), de Wes McKinney. Use ao aplicar pandas/NumPy/IPython para limpeza, reorganização, agregação, séries temporais e visualização de dados, ao estudar o livro, ou ao referenciar seus conceitos e padrões."
origem: publico-terceiro
classificacao: nao-corporativo
tipo: livro-tecnico
idioma: pt-BR
titulo_pt: "Python Para Análise de Dados"
proveniencia:
  titulo: "Python para análise de dados: Tratamento de dados com Pandas, NumPy e IPython"
  autor: ["Wes McKinney"]
  editora: "Novatec"
  fonte_sha256: "63838f96c8da066ffa8903a3f6cee1bb72576d20baee65940fb94971736373b6"
  convertido_em: "2026-08-24"
  ferramenta_sha: "7bcfcd5262329f8d57a385903f18a98bc6705e4e"
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Python para Análise de Dados: Tratamento de Dados com Pandas, NumPy e IPython
**Autor**: Wes McKinney | **Páginas**: ~500 (892 no PDF OCR) | **Capítulos**: 14 + 2 apêndices | **Gerado**: 2026-08-24

## Como Usar Esta Skill

- **Sem argumentos** — carrega os frameworks centrais para referência
- **Com um tópico** — pergunte sobre `groupby`, `merge`, `broadcasting`, `séries temporais` etc.; eu localizo e leio o capítulo relevante
- **Com capítulo** — peça `ch10` ou `ch14`; eu carrego o arquivo específico
- **Navegar** — pergunte "quais capítulos você tem?" para ver o índice completo

Quando você perguntar sobre um tópico não coberto nos Frameworks Centrais abaixo, eu lerei o arquivo de capítulo relevante antes de responder.

---

## Frameworks Centrais e Modelos Mentais

**A tese do livro**: 80%+ do tempo de um analista vai para carga, limpeza e reorganização de dados — dominar esse trabalho (não modelagem sofisticada) é onde está a maior parte do valor prático.

### Vetorização acima de tudo
Substitua laços `for` por expressões de array/Series inteiras. Ganho típico de 10-100x. Prefira, nesta ordem: expressão de array/ufunc → `Series.str.*`/métodos vetorizados do pandas → `apply`/`rolling(...).apply` com função customizada → laço Python explícito (último recurso).

### Split-Apply-Combine é o motor único de `groupby`
Toda operação de grupo — agregação, transformação, filtro por grupo — é uma instância de: separar por chave (coluna, array, dict/Series ou função) → aplicar função a cada grupo → combinar resultado. Escolha a ferramenta pelo formato do retorno: 1 valor por grupo → `.agg`; mesmo formato da entrada (broadcast) → `.transform` (mais rápido, usa o "atalho" das agregações nativas); qualquer outra coisa → `.apply` (genérico, mais lento).

### Alinhamento automático por rótulo
Operações aritméticas entre `Series`/`DataFrame` com índices diferentes produzem a união dos rótulos, preenchendo `NaN` onde não há correspondência — equivalente a um outer join implícito. Use `fill_value=` nos métodos aritméticos nomeados (`.add`, `.sub`) quando ausência deve significar "neutro", não "desconhecido".

### `loc`/`iloc` — ambiguidade impossível de expressar
`loc` é sempre rótulo, `iloc` é sempre posição. O design resolve o problema histórico do operador `ix` (obsoleto) tentando adivinhar — a lição geral: torne a ambiguidade impossível de escrever, não tente resolvê-la automaticamente em tempo de execução.

### `merge`/`concat`/`combine_first` — três formas de combinar dados
`merge` conecta por **chave** compartilhada (estilo SQL, `how=inner/left/right/outer`); `concat` **empilha** blocos com a mesma estrutura ao longo de um eixo; `combine_first` faz **patch** de ausência entre dois objetos sobrepostos. Junções muitos-para-muitos produzem produto cartesiano das chaves repetidas — confira cardinalidade antes.

### Formato longo ↔ largo é uma dualidade central
`stack`/`unstack` (via `MultiIndex`) e `pivot`/`melt` são pares de operações inversas para alternar entre "uma linha por observação" (bom para armazenamento/schema flexível) e "uma coluna por variável" (bom para leitura humana/plotagem). `pivot` é `set_index(...).unstack(...)` com açúcar sintático.

### `resample`/`rolling` generalizam `groupby` para tempo
`resample` é `groupby` cuja chave deriva da própria data (`closed=`/`label=` controlam a atribuição de bordas). `rolling`/`expanding`/`ewm` respondem "qual peso cada observação passada recebe?" — igual numa janela fixa, igual desde o início, ou decrescente exponencialmente.

### `Categorical` é normalização de banco de dados aplicada a arrays
Armazenar uma coluna repetitiva como (categorias distintas + códigos inteiros) — o mesmo padrão de tabela de dimensão. Compensa quando há poucas categorias repetidas muitas vezes: ganho real de memória e velocidade em `groupby`, pago com custo único de conversão.

### Broadcasting: regra única, aplicação repetida
Dois arrays são compatíveis se, comparando dimensões da direita para a esquerda, cada par coincide ou um dos dois é 1. `np.newaxis`/`reshape` forçam a dimensão "1" no eixo certo quando o broadcast automático (que sempre tenta o eixo final) não é o desejado.

### Patsy/statsmodels/scikit-learn: a fronteira é sempre um array NumPy
pandas cuida de carga/limpeza/engenharia de características; o ponto de contato com qualquer biblioteca de modelagem é `.values` (homogêneo) ou uma matriz de design do Patsy (`y ~ x0 + x1`, com dummies/interações automáticas). statsmodels responde "por que o modelo funciona" (inferência); scikit-learn responde "quão bem ele prevê" (validação cruzada).

---

## Índice de Capítulos

| # | Título | Frameworks-Chave |
|---|-------|----------------|
| [ch01](chapters/ch01-informacoes-preliminares.md) | Informações preliminares | Python como aglutinador, ecossistema (NumPy/pandas/IPython) |
| [ch02](chapters/ch02-basico-python-ipython.md) | Básico da linguagem Python, IPython | Referência vs. cópia, duck typing, magics do IPython |
| [ch03](chapters/ch03-estruturas-funcoes-arquivos.md) | Estruturas de dados, funções e arquivos | Comprehensions, geradores, funções como objetos |
| [ch04](chapters/ch04-numpy-basico.md) | Básico sobre o NumPy | Vetorização, views, indexação booleana/sofisticada, ufuncs |
| [ch05](chapters/ch05-introducao-pandas.md) | Introdução ao pandas | Series/DataFrame, alinhamento automático, `loc`/`iloc` |
| [ch06](chapters/ch06-carga-armazenagem-arquivos.md) | Carga, armazenagem e formatos de arquivo | `read_csv`, JSON, HDF5, SQL, chunksize |
| [ch07](chapters/ch07-limpeza-preparacao-dados.md) | Limpeza e preparação dos dados | `dropna`/`fillna`, `cut`/`qcut`, `get_dummies`, regex |
| [ch08](chapters/ch08-juncao-combinacao-reformatacao.md) | Junção, combinação e reformatação | `MultiIndex`, `merge`/`concat`, `pivot`/`melt` |
| [ch09](chapters/ch09-plotagem-visualizacao.md) | Plotagem e visualização | matplotlib (Figure/Axes), `pandas.plot`, seaborn |
| [ch10](chapters/ch10-agregacao-operacoes-grupos.md) | Agregação de dados e operações em grupos | `groupby`, split-apply-combine, `pivot_table`/`crosstab` |
| [ch11](chapters/ch11-series-temporais.md) | Séries temporais | `Timestamp`/`Period`, `resample`, `rolling`/`ewm`, fusos horários |
| [ch12](chapters/ch12-pandas-avancado.md) | Pandas avançado | `Categorical`, `transform`, encadeamento (`assign`/`pipe`) |
| [ch13](chapters/ch13-bibliotecas-modelagem.md) | Bibliotecas de modelagem em Python | Patsy, statsmodels, scikit-learn |
| [ch14](chapters/ch14-exemplos-analise-dados.md) | Exemplos de análises de dados | 5 estudos de caso completos (síntese) |
| [Ap. A](chapters/apA-numpy-avancado.md) | NumPy avançado | strides, broadcasting detalhado, ufunc methods, Numba |
| [Ap. B](chapters/apB-mais-ipython.md) | Mais sobre o sistema IPython | profiling (`%prun`/`%lprun`), depurador, design de código |

## Índice de Tópicos

- **Agregação por grupo** → ch10, ch12 (transform), ch11 (resample)
- **Arrays estruturados** → Ap. A
- **Broadcasting** → ch04, Ap. A
- **`Categorical`** → ch07, ch12, ch13
- **Depuração/profiling** → Ap. B
- **Discretização (`cut`/`qcut`)** → ch07, ch10
- **Dados ausentes (`NaN`/`NaT`)** → ch05, ch07, ch11
- **Fusos horários** → ch11
- **Índice hierárquico (`MultiIndex`)** → ch08, ch10
- **JSON aninhado** → ch06, ch14
- **`loc`/`iloc`** → ch05
- **`merge`/`concat`** → ch08, ch14
- **Modelagem (Patsy/statsmodels/scikit-learn)** → ch13
- **Plotagem** → ch09
- **`pivot`/`melt`/`stack`/`unstack`** → ch08
- **Regex/strings** → ch07
- **`resample`/`rolling`** → ch11
- **Vetorização** → ch04, Ap. A

## Arquivos de Apoio

- [glossary.md](glossary.md) — todos os termos-chave com definições
- [patterns.md](patterns.md) — todas as técnicas e padrões de design
- [cheatsheet.md](cheatsheet.md) — tabelas de referência rápida e guias de decisão

---

## Escopo e Limites

Esta skill cobre o conteúdo do livro (2ª edição, tradução para Python 3.6). Para implementação prática em código real, combine com o ambiente do projeto atual. Para tópicos além do livro (ex. dask, polars, Apache Arrow em profundidade), consulte outras fontes ou pergunte diretamente.

Conteúdo sintetizado a partir do PDF (OCR de qualidade boa mas imperfeita — pequenas imprecisões residuais no texto-fonte podem existir).
</content>
