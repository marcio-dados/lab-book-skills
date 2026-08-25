# Capítulo 2 — Curso Relâmpago de Python

## Nota de Edição
O livro usa **Python 2.7** (não 3.4, que já era a versão atual à época) porque, segundo o autor, "a comunidade de data science ainda está presa ao 2.7". Todo código do livro assume `from __future__ import division` no topo de cada arquivo, para que `5/2` resulte em `2.5` (divisão real), não `2` (divisão inteira). Ao aplicar os exemplos hoje, adaptar sintaxe `print x` → `print(x)`, `except E, e` etc. para Python 3.

## O Básico
- **Formatação por indentação**: blocos são delimitados por espaço em branco, não chaves; espaço é ignorado dentro de `()`/`[]`, o que permite quebrar expressões longas em várias linhas.
- **Módulos**: `import re`, `import re as regex` (alias), `from collections import defaultdict, Counter` (importação seletiva). Evitar `from module import *` — sobrescreve nomes silenciosamente.
- **Funções são de primeira classe**: podem ser atribuídas a variáveis e passadas como argumento. Lambdas existem mas o livro prefere `def` nomeado a atribuir lambda a variável.
- **Argumentos padrão e nomeados**: `def subtract(a=0, b=0)`, chamável como `subtract(b=5)`.
- **Strings**: aspas simples/duplas equivalentes; `r"..."` para string crua (raw); `"""..."""` para múltiplas linhas.
- **Exceções**: `try`/`except` — usadas livremente em Python (diferente de outras linguagens onde são "más práticas"), inclusive como padrão de controle de fluxo (ver `defaultdict` abaixo).

## Estruturas de Dados
- **Listas**: coleção ordenada e mutável; fatiamento (`x[:3]`, `x[-3:]`), `in` é O(n), `.extend()` vs `+` (não modifica), `.append()`, desempacotamento (`x, y = [1, 2]`), `_` para descartar valor.
- **Tuplas**: primas imutáveis das listas; forma idiomática de retornar múltiplos valores de uma função e de trocar variáveis (`x, y = y, x`).
- **Dicionários**: `dict["chave"]` levanta `KeyError`; `.get(chave, padrão)` não levanta; `in` sobre dict é mais rápido que `in` sobre `.keys()` (lista). Chaves devem ser imutáveis (tuplas servem, listas não).
- **`defaultdict`**: resolve o padrão repetitivo de "incrementar contador que pode não existir ainda" (três formas ingênuas mostradas: `if/else`, `try/except KeyError`, `.get`) — `defaultdict(int)`, `defaultdict(list)`, `defaultdict(lambda: [0,0])` chamam a função-fábrica automaticamente na primeira leitura de uma chave ausente.
- **`Counter`**: `defaultdict(int)` especializado para histogramas; `.most_common(n)` é o método mais usado.
- **`set`**: usado por dois motivos — teste de pertencimento (`in`) é muito mais rápido que em lista, e para extrair itens distintos de uma coleção.

## Controle de Fluxo e "Veracidade"
`if`/`elif`/`else`, ternário em uma linha, `while`, `for`/`in` (preferido a `while`), `continue`/`break`. Valores considerados "falsy": `False`, `None`, `[]`, `{}`, `""`, `set()`, `0`, `0.0` — quase tudo mais é "truthy". Idiomas derivados: `first_char = s and s[0]` (curto-circuito do `and`), `safe_x = x or 0`. `all([...])`/`any([...])` para checar listas de booleanos.

## Recursos Não Tão Básicos
- **Ordenação**: `sorted(x, key=..., reverse=True)` não modifica `x`; `.sort()` modifica in-place.
- **Compreensões de lista/dict/set**: `[x*x for x in range(5) if x%2==0]`; podem ter múltiplos `for` encadeados, com os posteriores dependendo dos anteriores.
- **Geradores e iteradores**: `yield` cria um gerador — valores produzidos **preguiçosamente** (lazy), só quando consumidos; evita explosão de memória (`lazy_range` reimplementa `xrange`). Um gerador só pode ser percorrido uma vez.
- **`random`**: `random.random()`, `random.seed(n)` (reprodutibilidade), `random.randrange`, `random.shuffle`, `random.choice`, `random.sample` (sem reposição) vs. `random.choice` em loop (com reposição).
- **Expressões regulares**: `re.match` (início da string), `re.search` (em qualquer lugar), `re.split`, `re.sub`.
- **Programação orientada a objetos**: exemplo completo reimplementando `set` como classe própria (`class Set` com `__init__`, `__repr__`, `add`, `contains`, `remove`) para ilustrar convenções (`self`, `PascalCase` para classes).
- **Ferramentas funcionais**: `functools.partial` para aplicação parcial de argumentos; `map`/`filter`/`reduce` como alternativas a compreensões de lista (o livro prefere compreensões, mas usa essas ocasionalmente).
- **`enumerate`**: forma Pythonic de obter índice + elemento simultaneamente, evita `range(len(...))` manual.
- **`zip` e desempacotamento de argumentos (`*`, `**`)**: `zip(list1, list2)` combina listas paralelas; `zip(*pairs)` "descompacta" uma lista de pares nas suas colunas; `*args`/`**kwargs` permitem funções de ordem superior que envolvem funções de aridade arbitrária (`doubler_correct`).

## Por Que Isso Importa
Este capítulo é referência de sintaxe pura — os idiomas aqui (`defaultdict`, `Counter`, compreensões, geradores, `zip`/desempacotamento) reaparecem sem re-explicação em todos os capítulos seguintes.
