# Capítulo 2: Básico da linguagem Python, IPython e notebooks Jupyter

## Core Idea
Uma revisão autocontida dos fundamentos de Python (semântica, tipos escalares, controle de fluxo) e do ambiente interativo IPython/Jupyter — a base mínima necessária para acompanhar o resto do livro, sem exigir proficiência completa em engenharia de software Python.

## Frameworks Introduced
- **Workflow execução-exploração**: em vez do ciclo edição-compilação-execução, trabalhar interativamente no shell IPython/Jupyter, testando e inspecionando resultados a cada passo.
  - Quando usar: exploração de dados, prototipagem, depuração.
  - Como: usar `%run` para executar scripts no namespace da sessão; inspecionar variáveis resultantes diretamente no shell.
- **Duck typing via `isiterable`**: verificar comportamento de um objeto (ele é iterável?) em vez do seu tipo exato.
  - Quando usar: funções genéricas que aceitam listas, tuplas, `ndarray` ou qualquer iterador.
  - Como: `try: iter(obj); return True except TypeError: return False`; converter para `list` só se necessário.

## Key Concepts
- **Comandos mágicos (`%`)**: comandos exclusivos do IPython (não Python puro), ex. `%run`, `%timeit`, `%paste`, `%matplotlib`.
- **Introspecção (`?`, `??`)**: `obj?` mostra docstring/tipo; `obj??` mostra o código-fonte quando disponível.
- **Referência vs. cópia**: atribuição (`b = a`) cria uma nova referência ao mesmo objeto, não uma cópia — mutação em `a` é visível em `b`.
- **Tipagem forte e dinâmica**: variáveis não têm tipo fixo, mas objetos sim; `'5' + 5` levanta `TypeError` (sem cast implícito entre str/int).
- **Objetos mutáveis vs. imutáveis**: listas, dicts, arrays NumPy são mutáveis; strings e tuplas são imutáveis.
- **`is` vs `==`**: `is` compara identidade de objeto (mesma referência); `==` compara igualdade de valor. Padrão idiomático: `x is None`.
- **Tipos escalares**: `None`, `str`, `bytes`, `float` (double-precision, sem tipo `double` separado), `bool`, `int` (precisão arbitrária).
- **`datetime`/`date`/`time`/`timedelta`**: tipos do módulo `datetime` da stdlib; `strftime` formata, `strptime` faz parse.

## Mental Models
- Pense em "tudo é um objeto" como a base da flexibilidade de Python: até funções podem ser passadas e manipuladas como qualquer outro valor.
- Ao passar objetos para funções, pense em "referência compartilhada, sem cópia automática" — mutações internas (`list.append`) se propagam ao chamador; reatribuições locais não.

## Anti-patterns
- **Confundir `is` com `==`**: `is` verifica identidade, não igualdade de valor — usar `==` para comparar conteúdo, `is` só para `None`/singletons.
- **Empilhar várias instruções numa linha com `;`**: tecnicamente válido, mas reduz legibilidade; evitar.
- **Abusar de expressões ternárias com condições complexas**: sacrifica legibilidade; preferir `if/else` explícito quando a lógica não é trivial.

## Code Examples
```python
# Duck typing: aceitar qualquer objeto iterável
def isiterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:  # não é iterável
        return False

if not isinstance(x, list) and isiterable(x):
    x = list(x)
```
- **O que demonstra**: como escrever funções tolerantes ao tipo de entrada usando duck typing em vez de checagem de tipo explícita.

```python
# Referência compartilhada entre variáveis
a = [1, 2, 3]
b = a
a.append(4)
b  # -> [1, 2, 3, 4]  (b aponta para o mesmo objeto que a)
```
- **O que demonstra**: atribuição em Python vincula um nome ao objeto existente, não copia dados.

## Reference Tables
| Operador | Descrição |
|---|---|
| `a // b` | Divisão pelo piso (floor division), descarta o resto |
| `a ** b` | Potência |
| `a is b` / `a is not b` | Identidade de objeto (mesma referência ou não) |
| `a == b` / `a != b` | Igualdade de valor |

| Tipo | Descrição |
|---|---|
| `None` | Valor nulo; única instância de `NoneType` |
| `str` | String Unicode (UTF-8) |
| `bytes` | Bytes puros ou Unicode codificado como bytes |
| `float` | Ponto flutuante 64-bit (não há `double` separado) |
| `int` | Inteiro com sinal, precisão arbitrária |

## Worked Example
Cenário do livro: um script `ipython_script_test.py` com `def f(x, y, z): return (x + y) / z` e variáveis `a=5, b=6, c=7.5`. Ao rodar `%run ipython_script_test.py` no IPython, o script executa em namespace vazio (como `python script.py`), mas ao final todas as variáveis (`a`, `b`, `c`, `result`) ficam acessíveis na sessão interativa — permitindo inspecionar `c` (`7.5`) e `result` (`1.4666...`) sem reexecutar nada. Isso ilustra por que `%run` é preferível a `python script.py` durante desenvolvimento exploratório: o estado final do script vira o ponto de partida da próxima investigação interativa.

## Key Takeaways
1. Use IPython/Jupyter como ambiente padrão de trabalho: `%run`, `%timeit`, `Tab`-completion e `?`/`??` aceleram o ciclo exploratório.
2. Atribuição em Python é vinculação de referência, não cópia — crucial ao passar listas/arrays grandes para funções.
3. Python é fortemente tipado (sem casts implícitos entre tipos incompatíveis) mas dinamicamente tipado (variáveis não têm tipo fixo).
4. Prefira `isinstance`/duck typing (`iter(obj)`) a checagens de tipo rígidas ao escrever funções genéricas.
5. `is`/`is not` são para identidade (principalmente `None`); `==`/`!=` são para igualdade de valor.
6. Objetos mutáveis (listas, dicts) podem gerar efeitos colaterais silenciosos; documente-os explicitamente ou favoreça imutabilidade.

## Connects To
- **Ch 3**: aprofunda estruturas de dados embutidas (listas, dicts, tuplas), funções e arquivos.
- **Ap. B**: descrição mais detalhada dos recursos do IPython.
- **Ch 11**: retoma `datetime`/`timedelta` em profundidade para séries temporais.
</content>
