# Capítulo 1: Informações preliminares

## Core Idea
O livro ensina a programação Python necessária para análise de dados — não a metodologia de análise em si — cobrindo o ecossistema de bibliotecas orientadas a dados (NumPy, pandas, matplotlib, IPython/Jupyter, SciPy, scikit-learn, statsmodels).

## Frameworks Introduced
- **Python como "aglutinador" (glue language)**: Python integra facilmente código C/C++/Fortran legado, permitindo que a maior parte "código aglutinador" (que não é o gargalo de performance) fique em Python enquanto os trechos críticos de desempenho ficam em linguagens de baixo nível.
  - Quando usar: ao decidir arquitetura de um sistema que combina bibliotecas numéricas nativas com lógica de alto nível.
  - Como: identificar os hot loops e delegá-los a C/Fortran/NumPy vetorizado; manter orquestração e I/O em Python puro.
- **Resolvendo o problema de "duas linguagens"**: em vez de prototipar em R/SAS e reescrever em Java/C++ para produção, usar Python nos dois estágios.
  - Quando usar: times que hoje mantêm ambientes de pesquisa e produção separados.
  - Como: adotar bibliotecas Python de produção (pandas, NumPy, scikit-learn) desde a fase de pesquisa.

## Key Concepts
- **Dados estruturados**: termo guarda-chuva para dados tabulares, arrays multidimensionais, tabelas relacionadas por chaves e séries temporais.
- **NumPy**: base de processamento numérico; fornece o `ndarray` e operações vetorizadas.
- **pandas**: estruturas de alto nível (`DataFrame`, `Series`) para dados tabulares/rotulados; combina desempenho do NumPy com flexibilidade de planilhas/SQL.
- **matplotlib**: biblioteca padrão de plotagem 2D do ecossistema Python.
- **IPython / Jupyter**: shell interativo e notebooks; viabilizam fluxo de trabalho execução-exploração em vez de edição-compilação-execução.
- **SciPy**: coleção de submódulos (`integrate`, `linalg`, `optimize`, `signal`, `sparse`, `special`, `stats`) para processamento científico.
- **scikit-learn**: kit de ferramentas de aprendizado de máquina de propósito geral (classificação, regressão, clustering, redução de dimensionalidade, seleção de modelos).
- **statsmodels**: pacote de estatística clássica/econometria, com foco em inferência (valores-p, incerteza), em contraste ao foco em previsão do scikit-learn.
- **GIL (Global Interpreter Lock)**: mecanismo do CPython que impede múltiplas threads Python nativas de executarem bytecode simultaneamente — limita paralelismo multithreaded CPU-bound.
- **Munging/wrangling**: processo de converter dados não estruturados/desorganizados em formato limpo e estruturado.

## Mental Models
- Pense em Python como "cola" entre bibliotecas de baixo nível e lógica de alto nível — não competir em velocidade bruta com C/C++, mas eliminar a necessidade de reescrever tudo em C.
- Use "duas linguagens é um sintoma", não um padrão: se pesquisa e produção usam stacks diferentes, o custo organizacional recorrente é maior que o ganho de performance pontual.

## Anti-patterns
- **Escolher Python para HFT/baixíssima latência ou apps multithread CPU-bound**: a GIL e o overhead de interpretação tornam Python inadequado nesses nichos; considerar C++ ou extensões nativas sem GIL.
- **Misturar `conda` e `pip` para atualizar os mesmos pacotes**: pode corromper o ambiente Anaconda/Miniconda; preferir `conda update` quando o pacote foi instalado via conda.

## Key Takeaways
1. O foco do livro é programação Python para dados, não metodologia analítica.
2. NumPy fornece a infraestrutura de arrays; pandas fornece as estruturas de alto nível para dados tabulares e séries temporais.
3. IPython/Jupyter são a interface de trabalho recomendada durante todo o livro (workflow execução-exploração).
4. O livro usa Python 3.6+ (Python 2 chamado de "Python Legado", fim de vida em 2020).
5. Reconhecer os nichos onde Python NÃO é a melhor escolha (baixa latência, alta concorrência CPU-bound) evita decisões de arquitetura erradas.

## Connects To
- **Ch 2/3**: pré-requisitos de linguagem Python para quem não tem experiência prévia.
- **Ap. A**: uso avançado de NumPy, deixado fora do fluxo principal do livro.
- **Ch 13**: retoma scikit-learn e statsmodels em mais profundidade.
</content>
