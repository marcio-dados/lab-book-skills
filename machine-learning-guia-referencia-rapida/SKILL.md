---
name: machine-learning-guia-referencia-rapida
description: "Base de conhecimento a partir de \"Machine Learning – Guia de Referência Rápida\", de Matt Harrison. Use ao aplicar scikit-learn/XGBoost/LightGBM para classificação, regressão, clustering e redução de dimensionalidade com dados estruturados, ao estudar o livro, ou ao referenciar seus conceitos e padrões."
origem: publico-terceiro
classificacao: nao-corporativo
tipo: livro-tecnico
idioma: pt-BR
titulo_pt: "Machine Learning – Guia de Referência Rápida"
proveniencia:
  titulo: "Machine Learning – Guia de Referência Rápida"
  autor: ["Matt Harrison"]
  editora: "Novatec Editora"
  fonte_sha256: "d8ef1e1b67632204275cbeb66a2c169ec5383d76d1ab3fe503340e0523699abf"
  convertido_em: "2026-08-25"
  ferramenta_sha: "7bcfcd5262329f8d57a385903f18a98bc6705e4e"
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Machine Learning – Guia de Referência Rápida
**Autor**: Matt Harrison | **Título original**: Machine Learning Pocket Reference (O'Reilly, 2019) | **Capítulos**: 19 + prefácio + sobre o autor | **Gerado**: 2026-08-25

## Como Usar Esta Skill

- **Sem argumentos** — carrega os frameworks centrais para referência
- **Com um tópico** — pergunte sobre `groupby`, `SHAP`, `SMOTE`, `pipeline` etc.; eu localizo e leio o capítulo relevante
- **Com capítulo** — peça `ch10` ou `ch17`; eu carrego o arquivo específico
- **Navegar** — pergunte "quais capítulos você tem?" para ver o índice completo

Quando você perguntar sobre um tópico não coberto nos Frameworks Centrais abaixo, eu lerei o arquivo de capítulo relevante antes de responder.

---

## Frameworks Centrais e Modelos Mentais

**A tese do livro**: é um "bloco de notas" de referência rápida (não um curso) para resolver problemas de machine learning com **dados estruturados** usando Python — cobre o pipeline completo (coleta → limpeza → engenharia de atributos → modelagem → avaliação → explicação → implantação) com exemplos prontos de código, deliberadamente fora do escopo de deep learning.

### O pipeline canônico é sempre o mesmo esqueleto
Coletar → limpar (remover vazamento de informação) → criar atributos → **split treino/teste** → imputar/normalizar (`fit` só no treino) → estabelecer baseline (`DummyClassifier`/`DummyRegressor`) → comparar famílias de modelo via k-fold → treinar → avaliar → otimizar hiperparâmetros → explicar → implantar. Todo capítulo do livro é um zoom em uma etapa deste esqueleto.

### Vazamento de informação é o erro mais silencioso
Qualquer atributo que carregue informação do futuro ou do próprio alvo (ex. `boat`/`body` entregando a sobrevivência no Titanic) infla a métrica de forma enganosa e inútil em produção. Regra: para cada coluna, perguntar "essa informação estaria disponível no momento real da predição?".

### Fit só no treino, transform nos dois
Imputação, escala, encoders de frequência/bayesianos e PCA são todos estatísticas calculadas a partir dos dados — `fit`/`fit_transform` no treino, `transform` no teste, nunca o contrário. É o mesmo princípio repetido em praticamente todos os capítulos de pré-processamento.

### Baseline antes de qualquer modelo real
`DummyClassifier`/`DummyRegressor` (prevê a classe majoritária ou a média) é o piso mínimo contra o qual qualquer modelo real deve ser comparado — essencial para não confundir "accuracy alta" com "modelo útil" sob classes desbalanceadas.

### Nenhum algoritmo vence em todo dataset (No Free Lunch)
Sempre comparar várias famílias de modelo via validação cruzada k-fold antes de investir em otimizar hiperparâmetros de uma família só. Bagging (floresta aleatória) reduz variância combinando árvores independentes; boosting (XGBoost/LightGBM) reduz bias combinando árvores sequenciais que corrigem o erro residual anterior.

### A métrica certa depende do custo relativo do erro, não de hábito
Accuracy trata falso-positivo e falso-negativo como equivalentes — quase nunca verdade no mundo real. Nomear o custo de cada tipo de erro antes de escolher entre precisão/recall/F1/AUC (classificação) ou MAE/MSE/MSLE (regressão).

### Explicação em camadas: nativa → local → global agregado
Modelos lineares/árvore têm explicação nativa e gratuita (`coef_`/`feature_importances_`). Modelos opacos (SVM, redes neurais) exigem modelo substituto ou LIME/SHAP para explicação local (uma amostra) e global (SHAP `summary_plot`) — SHAP e `treeinterpreter` são "aditivos exatos": base + contribuições somam exatamente a predição.

### Pipeline do scikit-learn elimina duplicação treino/produção
Encapsular limpeza customizada em `BaseEstimator`+`TransformerMixin` e encadear com `Pipeline` garante que a mesma lógica exata rode em treino e produção, e permite `GridSearchCV` sobre o pipeline inteiro (`<etapa>__<parametro>`).

---

## Índice de Capítulos

| # | Título | Frameworks-Chave |
|---|-------|----------------|
| [Prefácio](chapters/ch00-prefacio.md) | Prefácio | Escopo (dados estruturados, não deep learning), convenções do livro |
| [ch01](chapters/ch01-introducao-instalacao.md) | Introdução e instalação | Instalação JIT, pip vs. conda |
| [ch02](chapters/ch02-visao-geral-processo-ml.md) | Visão geral do processo de machine learning | CRISP-DM |
| [ch03](chapters/ch03-classificacao-titanic.md) | Descrição da classificação: conjunto de dados do Titanic | Pipeline completo, `X`/`y`, vazamento de informação |
| [ch04](chapters/ch04-dados-ausentes.md) | Dados ausentes | Diagnóstico visual (`missingno`), imputação indutiva vs. transdutiva |
| [ch05](chapters/ch05-limpeza-dados.md) | Fazendo uma limpeza nos dados | `pyjanitor`, nomes de coluna, coalescência |
| [ch06](chapters/ch06-explorando-dados.md) | Explorando os dados | Visualizações por classe, `correlated_columns` |
| [ch07](chapters/ch07-pre-processamento-dados.md) | Pré-processamento dos dados | Escada de encoders categóricos, `add_datepart`, `col_na` |
| [ch08](chapters/ch08-selecao-atributos.md) | Seleção de atributos | Dependência via floresta, RFE, informação mútua |
| [ch09](chapters/ch09-classes-desbalanceadas.md) | Classes desbalanceadas | Upsampling/downsampling, SMOTE/ADASYN |
| [ch10](chapters/ch10-classificacao.md) | Classificação | 9 famílias de modelo, checklist de 4 perguntas |
| [ch11](chapters/ch11-selecao-modelo.md) | Seleção do modelo | Curva de validação, curva de aprendizagem |
| [ch12](chapters/ch12-metricas-avaliacao-classificacao.md) | Métricas e avaliação de classificação | Matriz de confusão, ROC, precisão-recall, limiar |
| [ch13](chapters/ch13-explicando-modelos.md) | Explicando os modelos | LIME, treeinterpreter, PDP, SHAP |
| [ch14](chapters/ch14-regressao.md) | Regressão | Mesmos modelos de ch10, alvo contínuo |
| [ch15](chapters/ch15-metricas-avaliacao-regressao.md) | Métricas e avaliação de regressão | R², MAE/MSE/MSLE, heterocedasticidade |
| [ch16](chapters/ch16-explicando-modelos-regressao.md) | Explicando os modelos de regressão | SHAP para regressão |
| [ch17](chapters/ch17-reducao-dimensionalidade.md) | Redução da dimensionalidade | PCA, UMAP, t-SNE, PHATE |
| [ch18](chapters/ch18-clustering.md) | Clustering | K-means, hierárquico, métricas de cluster |
| [ch19](chapters/ch19-pipelines.md) | Pipelines | `Pipeline`, transformador customizado, grid search |
| [Sobre o autor](chapters/ch20-sobre-o-autor.md) | Sobre o autor | Bio + colofão (sem conteúdo técnico) |

## Índice de Tópicos

- **Baseline** → ch03, ch14 (`DummyClassifier`/`DummyRegressor`)
- **Classes desbalanceadas** → ch09, ch12
- **Clustering** → ch18
- **Colinearidade/multicolinearidade** → ch06, ch08, ch14
- **Dados ausentes / imputação** → ch04, ch07
- **Encoders categóricos** → ch07
- **Explicação de modelos (SHAP/LIME/PDP)** → ch13, ch16
- **GridSearchCV** → ch03, ch11, ch19
- **Matriz de confusão / ROC / precisão-recall** → ch12
- **Métricas de regressão (R²/MAE/MSE)** → ch15
- **Modelos de classificação (regressão logística, SVM, KNN, árvore, floresta, XGBoost, LightGBM, TPOT)** → ch10
- **Modelos de regressão** → ch14
- **PCA / UMAP / t-SNE / PHATE** → ch17
- **Pipeline (`sklearn.pipeline.Pipeline`)** → ch19
- **Reamostragem (upsampling/downsampling/SMOTE)** → ch09
- **Seleção de atributos (RFE, informação mútua)** → ch08
- **Vazamento de informação (leaky features)** → ch03, ch08
- **X/y, split treino/teste** → ch03

## Arquivos de Apoio

- [glossary.md](glossary.md) — todos os termos-chave com definições
- [patterns.md](patterns.md) — todas as técnicas e padrões de design
- [cheatsheet.md](cheatsheet.md) — tabelas de referência rápida e guias de decisão

---

## Escopo e Limites

Esta skill cobre o conteúdo do livro (edição brasileira, tradução de "Machine Learning Pocket Reference", O'Reilly 2019). O foco é exclusivamente **dados estruturados** — deep learning é citado apenas como fora de escopo (recomendado para dados não estruturados: imagem, áudio, vídeo). Muitas versões/APIs de bibliotecas citadas (sklearn 0.21, XGBoost 0.81, pandas 0.23 etc.) são de 2019 — nomes de parâmetros e comportamentos-padrão podem ter mudado em versões atuais; confirme contra a documentação vigente da biblioteca antes de aplicar em produção.

Conteúdo sintetizado a partir do EPUB original (extração de texto direta, sem OCR).
</content>
