# Capítulo 3: Estruturas de dados embutidas, funções e arquivos

## Core Idea
Domínio das estruturas de dados nativas de Python (tupla, lista, dict, set), das funções como objetos de primeira classe (lambdas, currying, geradores) e do tratamento de arquivos/exceções é a base sobre a qual pandas e NumPy são construídos — nenhuma biblioteca add-on substitui esse alicerce.

## Frameworks Introduced
- **List/dict/set comprehensions**: construir coleções filtrando/transformando em uma expressão concisa em vez de um laço `for` com `append`.
  - Quando usar: transformação simples de uma coleção existente, com ou sem filtro.
  - Como: `[expr for val in collection if condition]`; variantes `{k_expr: v_expr for ...}` (dict) e `{expr for ...}` (set).
- **Duck typing funcional com `map`/funções como objetos**: passar funções (nomeadas, lambdas, ou métodos como `str.strip`) como argumentos de outras funções para compor pipelines de transformação reutilizáveis.
  - Quando usar: limpeza de dados com múltiplas etapas (trim, remoção de pontuação, capitalização).
  - Como: montar uma lista de operações (`clean_ops = [str.strip, remove_punctuation, str.title]`) e aplicá-las em sequência dentro de um laço genérico.
- **Geradores (`yield`) e expressões geradoras**: iteração lazy, produzindo um valor por vez sob demanda em vez de materializar toda a coleção em memória.
  - Quando usar: sequências potencialmente grandes ou que não precisam existir todas ao mesmo tempo.
  - Como: `yield` dentro de uma função, ou `(expr for val in collection)` como forma concisa (análoga a uma list comprehension entre parênteses).
- **Currying / aplicação parcial (`functools.partial`)**: derivar uma nova função fixando parte dos argumentos de uma função existente.
  - Quando usar: reaproveitar uma função genérica especializando-a para um caso comum.
  - Como: `add_five = partial(add_numbers, 5)`.

## Key Concepts
- **Tupla**: sequência imutável de tamanho fixo; suporta desempacotamento (`a, b, c = tup`), inclusive aninhado e com `*rest`.
- **Lista**: sequência mutável de tamanho variável; `append`/`extend` são preferíveis a `+` para concatenação (evita recriar a lista inteira).
- **Fatiamento (`seq[start:stop:step]`)**: `start` incluso, `stop` exclusivo; índices negativos contam a partir do fim; `step=-1` inverte a sequência.
- **`dict`**: coleção de pares chave-valor; chaves devem ser hashable (imutáveis); `get`/`pop` aceitam valor default; `setdefault`/`collections.defaultdict` evitam checagem manual de existência de chave.
- **`set`**: coleção não ordenada de elementos únicos, hashable; suporta operações de conjunto (`union`/`|`, `intersection`/`&`, `difference`, `symmetric_difference`).
- **Hashability**: pré-requisito para ser chave de dict ou elemento de set; verificável com `hash(obj)`; listas não são hashable (usar tupla).
- **Namespace/escopo**: variáveis atribuídas dentro de uma função são locais por padrão; `global` permite atribuir a uma variável de escopo externo (uso desencorajado pelo autor).
- **Protocolo iterador**: `iter(obj)` produz um iterador; laços `for`, `min`, `max`, `sum`, `list`, `tuple` aceitam qualquer iterável.
- **`try/except/else/finally`**: `except <Tipo>` captura exceções específicas (evitar `except:` genérico, que mascara bugs como `TypeError`); `finally` sempre executa (ex.: fechar arquivo).
- **Modos de arquivo**: `'r'` leitura, `'w'` escrita (sobrescreve), `'x'` escrita exclusiva (falha se existir), `'a'` append, `'b'`/`'t'` binário/texto.

## Mental Models
- Pense em comprehensions aninhadas como laços `for` aninhados na mesma ordem em que apareceriam escritos por extenso — além de 2-3 níveis, prefira um laço explícito por legibilidade.
- Pense em geradores como "promessas de valores futuros": nada executa até que o próximo valor seja solicitado (`for` ou `next()`).
- Use `with open(...) as f:` como padrão default para arquivos — garante fechamento mesmo em caso de exceção, sem precisar de `finally` manual.

## Anti-patterns
- **Concatenar listas grandes com `+` dentro de um laço**: recria uma lista inteira a cada iteração; use `list.extend` ou acumule com `list.append`/comprehension.
- **`insert` no início/meio de listas grandes repetidamente**: desloca todos os elementos subsequentes; se precisa inserir nas duas pontas com frequência, use `collections.deque`.
- **`except:` genérico (bare except)**: engole exceções inesperadas (ex. `TypeError`) que deveriam sinalizar um bug real; capture o tipo específico (`except ValueError:`).
- **Usar `global` livremente**: indica candidatura a uma classe/objeto em vez de estado global disperso.
- **`seek()` em modo texto (não binário) para posições arbitrárias**: pode cair no meio de um caractere UTF-8 multibyte e gerar `UnicodeDecodeError` em leituras subsequentes.

## Code Examples
```python
from collections import defaultdict

words = ['apple', 'bat', 'bar', 'atom', 'book']
by_letter = defaultdict(list)
for word in words:
    by_letter[word[0]].append(word)
# {'a': ['apple', 'atom'], 'b': ['bat', 'bar', 'book']}
```
- **O que demonstra**: `defaultdict` elimina a checagem manual "chave existe? cria lista: senão usa a existente" para agrupamento incremental.

```python
def clean_strings(strings, ops):
    result = []
    for value in strings:
        for function in ops:
            value = function(value)
        result.append(value)
    return result

clean_ops = [str.strip, remove_punctuation, str.title]
clean_strings(states, clean_ops)
```
- **O que demonstra**: tratar funções como dados (lista de operações) para compor um pipeline de limpeza declarativo e reutilizável.

## Reference Tables
| Tabela 3.2 (itertools) | Descrição |
|---|---|
| `combinations(iterable, k)` | Tuplas de k elementos, sem ordem, sem repetição |
| `permutations(iterable, k)` | Tuplas de k elementos, respeitando ordem |
| `groupby(iterable, keyfunc)` | Gera `(key, sub-iterator)` por grupo de chave |
| `product(*iterables, repeat=1)` | Produto cartesiano dos iteráveis |

| Modo de arquivo | Descrição |
|---|---|
| `'r'` | Somente leitura |
| `'w'` | Somente escrita; cria/sobrescreve |
| `'x'` | Somente escrita; falha se já existir |
| `'a'` | Concatena (append); cria se não existir |
| `'b'` / `'t'` | Binário / texto (default) |

## Worked Example
O autor mostra dois caminhos para a mesma tarefa de limpeza de uma lista de nomes de estados americanos digitados de forma inconsistente (`' Alabama '`, `'FlOrIda'`, `'south   carolina##'`, etc.):
1. Uma função monolítica `clean_strings` que faz `strip()`, `re.sub('[!#?]', '', value)` e `title()` em sequência dentro do laço.
2. Uma versão "mais funcional": extrai cada etapa como uma função independente (`remove_punctuation`), monta `clean_ops = [str.strip, remove_punctuation, str.title]` e reescreve `clean_strings(strings, ops)` para aplicar cada função da lista, em ordem, a cada valor.

A segunda versão é estritamente mais reutilizável: adicionar/remover uma etapa de limpeza não exige tocar no corpo de `clean_strings`, só na lista `clean_ops` — o "pipeline" vira dado, não código.

## Key Takeaways
1. Prefira comprehensions a laços `for` + `append` para transformações simples, mas limite o aninhamento a 2-3 níveis por legibilidade.
2. `list.extend`/`append` batem `+=`/`+` em performance para concatenação incremental de listas.
3. Trate funções como objetos de primeira classe: passe-as como argumentos (`map`, listas de operações) para pipelines de limpeza de dados reutilizáveis.
4. Geradores e expressões geradoras evitam materializar sequências grandes inteiras em memória.
5. Capture tipos de exceção específicos (`except ValueError:`), nunca `except:` puro — evita mascarar bugs reais.
6. Use `with open(...) as f:` sempre que possível para garantir o fechamento do arquivo.
7. Só objetos hashable (imutáveis) podem ser chave de `dict` ou elemento de `set`; converta listas para tuplas quando precisar usá-las assim.

## Connects To
- **Ch 2**: pré-requisito de sintaxe básica (tipos escalares, controle de fluxo) usado aqui.
- **Ch 4/NumPy**: `ndarray` estende a ideia de sequência indexável/fatiável vista aqui para arrays n-dimensionais.
- **Ch 6**: `pandas.read_csv` substitui a manipulação manual de arquivos vista na seção 3.3 para a maioria dos casos práticos.
- **Ch 8**: aprofunda processamento de strings/regex para limpeza de dados.
</content>
