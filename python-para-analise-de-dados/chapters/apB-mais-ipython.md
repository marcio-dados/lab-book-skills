# Apêndice B: Mais sobre o sistema IPython

## Core Idea
IPython/Jupyter é mais que um REPL bonito: histórico pesquisável, integração com shell, depurador pós-morte (`%debug`), profiling (`%time`/`%timeit`/`%prun`/`%lprun`) e um sistema de configuração por perfis formam um ambiente completo de desenvolvimento interativo — e escrever código "amigável ao IPython" (namespace plano, módulos não pequenos demais) é uma escolha de design, não um acidente.

## Frameworks Introduced
- **Escada de profiling: macro → micro**: `%time`/`%timeit` medem uma instrução isolada; `%prun` (cProfile) agrega por função num bloco inteiro; `%lprun` (line_profiler) desce ao nível de linha dentro de funções específicas.
  - Quando usar: comece largo (`%prun`) para achar a função culpada, depois estreite (`%lprun -f func`) para achar a linha exata — nunca o inverso (monitorar linha a linha tudo tem overhead alto).
- **Depuração pós-morte vs. depuração proativa**: `%debug` logo após uma exceção entra no stack frame onde ela ocorreu; `%run -d`/`set_trace()`/`debug(f, *args)` permitem entrar deliberadamente antes que o erro aconteça.
  - Quando usar: pós-morte para diagnosticar um erro que já ocorreu; proativa para inspecionar estado passo a passo numa função suspeita.
- **Design de código "amigável ao IPython"**: mover a lógica de `main()` para o namespace global do módulo (ou expor via `if __name__ == '__main__':` sem esconder as variáveis dentro de uma função), preferir módulos coesos e não pequenos demais, evitar aninhamento profundo — tudo para que `%run` deixe o estado inspecionável interativamente depois.

## Key Concepts
- **Histórico de comandos**: Ctrl-P/seta-para-cima (busca incremental por prefixo), Ctrl-R (busca reversa estilo readline); variáveis especiais `_`/`__` (última/penúltima saída), `_iX`/`_X` (entrada/saída da linha X); `%hist`, `%reset`, `%xdel` para gerenciar o namespace e liberar memória (objetos referenciados no histórico não são coletados pelo GC mesmo após `del`).
- **Integração com shell**: `!cmd` executa no shell do sistema; `output = !cmd` captura stdout numa lista Python; `$variável` interpola valores Python dentro de um comando `!`; `%alias` define atalhos; `%bookmark` persiste marcadores de diretório entre sessões (diferente de `%alias`, que não persiste).
- **`%debug`**: entra no depurador (`ipdb`) no ponto da última exceção; comandos `u`/`d` (up/down na pilha), `s`/`n` (step/next), `c` (continue), `b linha` (breakpoint), `!variável` (inspecionar quando o nome conflita com comando do depurador).
- **`%run -d`**: inicia o depurador antes de executar o script; `-b N` já define um breakpoint na linha N.
- **`set_trace()`/`debug(f, *args, **kwargs)`**: receitas para entrar no depurador em qualquer ponto do código ou ao chamar uma função específica, sem precisar de `%run -d`.
- **`%time` vs. `%timeit`**: `%time` roda uma vez (rápido, mas ruidoso); `%timeit` roda a instrução repetidamente com heurística para média mais estável — preferir `%timeit` para comparar performance de alternativas.
- **`%prun`/`python -m cProfile`**: profiling agregado por função; `-s cumulative` ordena por tempo cumulativo (mais útil que a ordem default por nome).
- **`%lprun`** (requer extensão `line_profiler`): profiling linha a linha de funções explicitamente nomeadas com `-f`; overhead alto, por isso não se aplica automaticamente a tudo.
- **`importlib.reload(modulo)`/`dreload(modulo)`**: recarrega um módulo já importado (Python cacheia imports); `dreload` tenta recarregar recursivamente as dependências.
- **`__repr__`**: IPython usa o retorno de `__repr__` para exibir objetos no console — definir um `__repr__` customizado é a forma de tornar uma classe própria legível interativamente.
- **Perfis de configuração** (`ipython profile create [nome]`, `~/.ipython/profile_*/ipython_config.py`): permitem cores, prompts, imports automáticos, extensões sempre ativas, por projeto/perfil.

## Mental Models
- Pense em `%prun` como um mapa de "onde o tempo vai" por função, e `%lprun` como um microscópio para "onde dentro desta função específica o tempo vai" — o segundo só vale a pena depois que o primeiro já apontou o suspeito.
- Pense em "código amigável ao IPython" como o oposto de "código para CLI": o objetivo não é só rodar e sair, é deixar todo o estado relevante acessível para inspeção depois que a execução termina.
- Histórico de entrada/saída do IPython mantém referências vivas — isso é uma armadilha de memória silenciosa em sessões longas com dados grandes; `%xdel`/`%reset` existem precisamente para isso.

## Anti-patterns
- **Esconder toda a lógica dentro de `def main(): ...`**: depois de `%run`, nenhuma variável de `main` fica acessível no namespace interativo — perde-se exatamente o benefício de rodar interativamente.
- **Usar `%lprun` sem `-f` explícito na função de interesse**: monitorar tudo tem overhead alto o suficiente para distorcer o próprio resultado do profiling.
- **Confiar em `%time` (execução única) para comparar performance de duas alternativas**: ruído de uma única medição pode inverter a conclusão — usar `%timeit` (múltiplas execuções, heurística de estabilização).
- **Editar um módulo e esperar que `%run` de um script dependente reflita a mudança automaticamente**: Python cacheia imports; é preciso `importlib.reload`/`dreload`, ou reiniciar a sessão.
- **Escrever muitos módulos pequenos (<100 linhas) demais para conveniência "por regra"**: o autor argumenta que isso multiplica recarregamentos e saltos entre arquivos durante desenvolvimento interativo — prefira módulos coesos, refatorando para menor só depois que a solução estabilizar.

## Code Examples
```python
# Receita de set_trace() reutilizável (breakpoint manual em qualquer ponto)
from IPython.core.debugger import Pdb

def set_trace():
    Pdb(color_scheme='Linux').set_trace(sys._getframe().f_back)

def debug(f, *args, **kwargs):
    pdb = Pdb(color_scheme='Linux')
    return pdb.runcall(f, *args, **kwargs)
```
```python
# __repr__ customizado: torna a classe legível no console IPython
class Message:
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return 'Message: %s' % self.msg
```
- **O que demonstra**: como transformar `pdb`/`Pdb` em ferramentas de um comando (`set_trace()`, `debug(f, ...)`) reutilizáveis em qualquer projeto, e o idioma mínimo para uma classe própria se comportar bem no REPL.

## Reference Tables
| Comando de sessão | Ação |
|---|---|
| Ctrl-P / seta-cima | Busca no histórico por prefixo digitado |
| Ctrl-R | Busca reversa incremental (estilo readline) |
| `_` / `__` | Última / penúltima saída |
| `_iX` / `_X` | Entrada / saída da linha X |

| Comando `ipdb` | Ação |
|---|---|
| `s` / `n` | Step (entra na chamada) / Next (avança na mesma profundidade) |
| `u` / `d` | Sobe / desce na pilha de chamadas |
| `b N` / `c` | Breakpoint na linha N / Continue |
| `w` | Stack trace completo com contexto |

| Ferramenta de profiling | Granularidade |
|---|---|
| `%time` / `%timeit` | Uma instrução (execução única / repetida) |
| `%prun` (cProfile) | Agregado por função, num bloco/script |
| `%lprun` (line_profiler) | Linha a linha, dentro de função(ões) nomeada(s) |

## Key Takeaways
1. Suba a escada de profiling do macro (`%prun`) para o micro (`%lprun -f func`) — nunca comece pelo micro.
2. `%debug` pós-morte é o primeiro reflexo depois de uma exceção inesperada; `set_trace()`/`%run -d` são para inspeção proativa.
3. `%timeit` (múltiplas execuções) é confiável para comparação de performance; `%time` (execução única) é ruidoso demais para decisões.
4. Projete módulos para deixar estado no namespace global após `%run` — evite esconder tudo dentro de `main()`.
5. `importlib.reload`/`dreload` resolvem o cache de import do Python durante iteração; sem isso, mudanças em dependências não se refletem em `%run` repetido.
6. Um `__repr__` customizado é o investimento mínimo para tornar classes próprias úteis em sessões interativas.

## Connects To
- **Ch 2**: pré-requisito — uso básico de IPython/Jupyter já introduzido ali (magics, `%run`, tab-completion).
- **Ch 4**: `%timeit` usado extensivamente ali para comparar NumPy vetorizado vs. Python puro — este apêndice explica a ferramenta em profundidade.
</content>
