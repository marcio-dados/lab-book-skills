# Capítulo 25 — Vá em Frente e Pratique Data Science

## IPython
Reforça a recomendação já feita no Capítulo 2: dominar IPython (shell mais poderoso, funções mágicas, colar código sem quebrar por indentação) e seus "cadernos" (notebooks) — combinam texto, código vivo e visualizações, úteis tanto para compartilhar quanto como diário pessoal de trabalho.

## Matemática
Convite a aprofundar além do que o livro cobriu de raspão: álgebra linear (Cap. 4), estatística (Cap. 5), probabilidade (Cap. 6) e aprendizado de máquina — via livros-texto, cursos online ou presenciais.

## "Não Do Zero" — Use Bibliotecas de Verdade
Mensagem central do capítulo: implementar "do zero" foi um recurso **pedagógico** (entender o mecanismo por dentro), não uma recomendação de prática profissional — o autor revela que sua proposta original incluía uma segunda metade "agora vamos aprender as bibliotecas", vetada pela editora.
- **NumPy**: arrays/matrizes de alta performance — substitui as listas/listas-de-listas usadas no livro inteiro; base de muitas outras bibliotecas.
- **pandas**: `DataFrame` — equivalente muito mais rico e performático da classe `Table` do NotQuiteABase (Capítulo 23).
- **scikit-learn**: biblioteca de referência para aprendizado de máquina em Python — contém (e muito mais que) todos os modelos implementados no livro (k-NN, Naive Bayes, regressão, árvores, SVM, etc.); em um projeto real, você nunca implementaria uma árvore de decisão ou um otimizador do zero.

## Visualização
Além do `matplotlib` (já usado no livro inteiro), cita **seaborn** (embelezamento sobre matplotlib), **D3.js** (visualizações interativas para web, mesmo sem saber JavaScript a fundo — "bons cientistas copiam da galeria D3, ótimos cientistas roubam dela") e **Bokeh** (estilo D3 em Python).

## R
Recomendação de familiaridade mínima com R, mesmo sem adotá-lo como linguagem principal — útil para entender posts/exemplos de blog baseados em R, apreciar por comparação a "elegância" do Python, e participar informado do debate "R vs. Python".

## Onde Encontrar Dados
Data.gov (dados governamentais), fóruns `r/datasets` e `r/data` no Reddit, datasets públicos da Amazon, listas curadas (ex. blog de Robb Seaton), Kaggle (competições de data science).

## Projetos Pessoais do Autor (estudos de caso de motivação)
Três exemplos reais de "coceiras" que viraram projetos:
1. **Classificador de histórias do Hacker News**: Naive Bayes (similar ao filtro de spam do Cap. 13) para prever interesse pessoal em notícias, usando palavras do título e domínio do link como features — construído em Ruby, "aprenda com meus erros" (o autor reconhece a escolha de linguagem como equívoco em retrospecto).
2. **Análise de rede de carros de bombeiros de Seattle**: dados de alarmes públicos em tempo real, análise de rede social (Cap. 21) aplicada a caminhões de bombeiro, com uma métrica de centralidade customizada apelidada de "TruckRank" (paralelo direto ao PageRank).
3. **Classificador de camisetas infantis por gênero**: imagens de camisetas reduzidas a vetores de pixel/cor, classificadas via regressão logística (Cap. 16); uma segunda abordagem usa PCA (Cap. 10) para extrair os 10 componentes principais ("autocamisetas") e classifica pela projeção nesse espaço reduzido — aplicação direta e concreta de PCA fora do contexto abstrato do Capítulo 10.

## Mensagem Final
"O que interessa você? Quais perguntas tiram seu sono? Procure um conjunto de dados e faça um pouco de data science" — o livro termina reiterando sua tese de abertura (Capítulo 1): motivação pessoal e curiosidade concreta valem mais que seguir um currículo abstrato.

## Nota Bibliográfica (não incluída na síntese técnica)
O capítulo é seguido, na edição impressa, pela seção "Sobre o Autor" e o "Colophon" (nota sobre o animal da capa — um lagópode-branco/"galo das neves", `Lagopus muta`) — conteúdo de apresentação editorial, sem relevância técnica para esta skill.
