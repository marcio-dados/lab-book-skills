---
name: data-science-do-zero
description: "Base de conhecimento a partir de \"Data Science do Zero: Primeiras Regras com o Python\", de Joel Grus. Use ao implementar algoritmos de data science/ML do zero (sem bibliotecas), ao estudar fundamentos de álgebra linear, estatística, probabilidade, aprendizado de máquina e infraestrutura de dados aplicados a Python, ou ao referenciar seus conceitos e padrões."
origem: publico-terceiro
classificacao: nao-corporativo
tipo: livro-tecnico
idioma: pt-BR
titulo_pt: "Data Science do Zero"
proveniencia:
  titulo: "Data Science from Scratch: First Principles with Python"
  autor: ["Joel Grus"]
  editora: "Alta Books"
  fonte_sha256: "4b47c54f78e0706b39abe3967f75cf7a9bb81198dfd6097cba799b1066a52854"
  convertido_em: "2026-08-25"
  ferramenta_sha: "7bcfcd5262329f8d57a385903f18a98bc6705e4e"
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Data Science do Zero: Primeiras Regras com o Python
**Autor**: Joel Grus | **Páginas**: ~336 | **Capítulos**: 25 | **Gerado**: 2026-08-25

## Como Usar Esta Skill

- **Sem argumentos** — carrega os frameworks centrais para referência
- **Com um tópico** — pergunte sobre `gradiente descendente`, `naive bayes`, `k-means`, `PCA` etc.; eu localizo e leio o capítulo relevante
- **Com capítulo** — peça `ch08` ou `ch17`; eu carrego o arquivo específico
- **Navegar** — pergunte "quais capítulos você tem?" para ver o índice completo

Quando você perguntar sobre um tópico não coberto nos Frameworks Centrais abaixo, eu lerei o arquivo de capítulo relevante antes de responder.

---

## Core Frameworks & Mental Models

**A tese do livro**: os melhores atalhos de data science (bibliotecas prontas) só fazem sentido depois de entender o mecanismo por dentro — por isso cada técnica é implementada "do zero" em Python puro (sem NumPy/pandas/scikit-learn), inclusive gradiente descendente, regressão, árvores de decisão e redes neurais.

### Gradiente descendente é o motor único de otimização
Quase todo modelo do livro (regressão linear/múltipla/logística, PCA, redes neurais) se resolve com a mesma receita: definir uma função de erro/verossimilhança e seu gradiente, e usar `minimize_batch`/`minimize_stochastic` para caminhar na direção que melhora a função. Aprender essa receita uma vez evita reaprendê-la a cada capítulo.

### Suavização com pseudo-contagem evita probabilidade zero
Naive Bayes (Cap. 13) e modelagem de tópicos/LDA (Cap. 20) usam o mesmo truque: nunca deixar uma probabilidade estimada por frequência cair a exatamente zero por falta de dados — somar uma pseudo-contagem `k`/`alpha`/`beta` ao numerador e denominador.

### Sobreajuste vs. sub-ajuste é o eixo central de avaliação
Todo modelo supervisionado é avaliado pela mesma lente (Cap. 11): divisão treino/validação/teste, matriz de confusão (precision/recall/F1 em vez de acurácia bruta), e o compromisso polarização-variância. Adicionar complexidade sempre melhora o ajuste ao treino — a pergunta certa é se generaliza.

### Distância e vetores sustentam tudo
`dot`, `distance`, `magnitude` (Cap. 4, construídos sobre listas Python) reaparecem sem redefinição em k-NN (12), k-means (19), PCA (10) e redes neurais (18) — é a álgebra linear mínima necessária para o resto do livro.

### A maldição da dimensionalidade é o limite prático de "distância como similaridade"
Em muitas dimensões, pontos aleatórios tendem a ficar igualmente distantes uns dos outros — k-NN (Cap. 12) e filtragem colaborativa baseada em usuário (Cap. 22) degradam por esse motivo; a saída recorrente é reduzir dimensionalidade (PCA, Cap. 10) antes.

### Split-apply-combine é o mesmo padrão em três roupagens
`group_by` (manipulação de dados, Cap. 10), `map_reduce` (Cap. 24) e `Table.group_by` (SQL/NotQuiteABase, Cap. 23) são a mesma ideia — agrupar por chave, aplicar uma função a cada grupo — implementada três vezes em contextos diferentes (memória local, distribuído, banco de dados).

### Centralidade em rede é sempre uma definição recursiva ou um caminho mais curto
Vetor próprio (eigenvector) e PageRank (Cap. 21) definem importância circularmente ("central = conectado a quem é central"), resolvida por iteração até convergência; intermediação e proximidade definem importância via caminhos mais curtos (BFS), mais caras de calcular mas mais intuitivas.

---

## Chapter Index

| # | Título | Frameworks-Chave |
|---|-------|----------------|
| [ch01](chapters/ch01-introducao.md) | Introdução | Grau de centralidade, índice invertido de interesses, motivação narrativa (DataSciencester) |
| [ch02](chapters/ch02-curso-relampago-python.md) | Curso Relâmpago de Python | `defaultdict`, `Counter`, compreensões, geradores, `zip`/desempacotamento |
| [ch03](chapters/ch03-visualizando-dados.md) | Visualizando Dados | `matplotlib.pyplot`, honestidade de eixos, linha/barra/dispersão |
| [ch04](chapters/ch04-algebra-linear.md) | Álgebra Linear | `dot`, `magnitude`, `distance`, matrizes como listas de listas |
| [ch05](chapters/ch05-estatistica.md) | Estatística | Média/mediana/variância, correlação, Paradoxo de Simpson |
| [ch06](chapters/ch06-probabilidade.md) | Probabilidade | Teorema de Bayes, distribuição normal, Teorema do Limite Central |
| [ch07](chapters/ch07-hipotese-e-inferencia.md) | Hipótese e Inferência | p-value, intervalo de confiança, p-hacking, teste A/B, inferência Bayesiana |
| [ch08](chapters/ch08-gradiente-descendente.md) | Gradiente Descendente | `minimize_batch`/`minimize_stochastic`, escolha de step size |
| [ch09](chapters/ch09-obtendo-dados.md) | Obtendo Dados | stdin/CSV, BeautifulSoup, APIs (GitHub, Twitter) |
| [ch10](chapters/ch10-trabalhando-com-dados.md) | Trabalhando com Dados | Histogramas, matriz de correlação, `rescale`, PCA do zero |
| [ch11](chapters/ch11-aprendizado-de-maquina.md) | Aprendizado de Máquina | Overfitting/underfitting, precision/recall/F1, bias-variance |
| [ch12](chapters/ch12-k-vizinhos-mais-proximos.md) | K-Vizinhos Mais Próximos | `knn_classify`, maldição da dimensionalidade |
| [ch13](chapters/ch13-naive-bayes.md) | Naive Bayes | Independência condicional, suavização, filtro de spam |
| [ch14](chapters/ch14-regressao-linear-simples.md) | Regressão Linear Simples | Mínimos quadrados, R², máxima verossimilhança |
| [ch15](chapters/ch15-regressao-multipla.md) | Regressão Múltipla | Variável dummy, bootstrap, erro padrão, Ridge/Lasso |
| [ch16](chapters/ch16-regressao-logistica.md) | Regressão Logística | Função logística, máxima verossimilhança, SVM (conceitual) |
| [ch17](chapters/ch17-arvores-de-decisao.md) | Árvores de Decisão | Entropia, algoritmo ID3, florestas aleatórias/bagging |
| [ch18](chapters/ch18-redes-neurais.md) | Redes Neurais | Perceptron, XOR, feed-forward, backpropagation |
| [ch19](chapters/ch19-agrupamento.md) | Agrupamento | k-means, escolha de k (cotovelo), hierárquico bottom-up |
| [ch20](chapters/ch20-processamento-de-linguagem-natural.md) | Processamento de Linguagem Natural | n-gramas, gramáticas, amostragem de Gibbs, LDA |
| [ch21](chapters/ch21-analise-de-rede.md) | Análise de Rede | Betweenness, closeness, vetor próprio, PageRank |
| [ch22](chapters/ch22-sistemas-recomendadores.md) | Sistemas Recomendadores | Similaridade do cosseno, colaborativo usuário/item |
| [ch23](chapters/ch23-bases-de-dados-e-sql.md) | Bases de Dados e SQL | NotQuiteABase, JOIN, GROUP BY/HAVING, índices |
| [ch24](chapters/ch24-mapreduce.md) | MapReduce | `map_reduce` genérico, combinadores, multiplicação de matriz distribuída |
| [ch25](chapters/ch25-va-em-frente-e-pratique-data-science.md) | Vá em Frente e Pratique Data Science | NumPy/pandas/scikit-learn, projetos pessoais do autor |

## Índice de Tópicos

- **Álgebra linear (`dot`/`distance`/matrizes)** → ch04, ch10, ch12, ch18, ch19, ch21
- **Amostragem de Gibbs / LDA** → ch20
- **Árvores de decisão / florestas aleatórias** → ch17
- **Backpropagation / redes neurais** → ch18
- **Bootstrap (erro padrão)** → ch15, ch17
- **Clustering (k-means, hierárquico)** → ch19
- **Distância e maldição da dimensionalidade** → ch12, ch22
- **Gradiente descendente** → ch08, ch10, ch14, ch15, ch16, ch18
- **Naive Bayes** → ch13
- **NLP (n-gramas, gramáticas, tópicos)** → ch20
- **PCA / redução de dimensionalidade** → ch10
- **Precision/recall/F1/acurácia** → ch11, ch13, ch16
- **Probabilidade / Teorema de Bayes** → ch06, ch07, ch13
- **Redes/grafos (centralidade, PageRank)** → ch21
- **Regressão (linear, múltipla, logística, regularização)** → ch14, ch15, ch16
- **Sistemas recomendadores** → ch22
- **SQL / bancos de dados** → ch23
- **Estatística descritiva / correlação** → ch05
- **Teste de hipótese / p-value / A/B** → ch07
- **MapReduce / processamento distribuído** → ch24
- **Web scraping / APIs** → ch09
- **Visualização (matplotlib)** → ch03

## Supporting Files

- [glossary.md](glossary.md) — todos os termos-chave com definições
- [patterns.md](patterns.md) — todas as técnicas e padrões de design
- [cheatsheet.md](cheatsheet.md) — tabelas de referência rápida e guias de decisão

---

## Scope & Limits

Esta skill cobre o conteúdo do livro (edição traduzida pela Alta Books, código-fonte original em Python 2.7). Os idiomas de código (`print x`, `iteritems`, `except E, e`) refletem o original e exigem adaptação para Python 3 em uso prático. Para bibliotecas de produção (NumPy, pandas, scikit-learn) que substituem as implementações "do zero" aqui descritas, consulte a skill `python-para-analise-de-dados` ou a documentação oficial de cada biblioteca — o próprio Capítulo 25 do livro recomenda essa transição.

Conteúdo sintetizado a partir do EPUB (extração via parser stdlib, sem OCR — boa fidelidade textual, mas a formatação de fórmulas matemáticas do livro original foi perdida na extração e reconstruída em prosa/pseudo-código nos capítulos).
