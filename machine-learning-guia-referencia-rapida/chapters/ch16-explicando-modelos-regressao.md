# Capítulo 16: Explicando os modelos de regressão

## Core Idea
Quase todas as técnicas de explicação de classificação (Capítulo 13) se transferem diretamente para regressão — SHAP em particular funciona de forma idêntica, mudando apenas a interpretação: em vez de log-odds, o valor SHAP soma diretamente até o valor previsto do alvo contínuo.

## Frameworks Introduced
- **SHAP para regressão é o mesmo fluxo de classificação, valor de saída muda de log-odds para unidade do alvo**: `TreeExplainer` + `shap_values` + `force_plot`/`dependence_plot`/`summary_plot` funcionam sem alteração de API; a leitura muda de "probabilidade" para "valor previsto (ex. preço)".
  - Quando usar: qualquer modelo de regressão baseado em árvore (XGBoost, LightGBM, florestas) onde se quer explicação local e global sem trocar de ferramenta em relação à classificação.

## Key Concepts
- **Gráfico de forças (regressão)**: mostra o valor esperado de base (média do dataset) e como cada atributo empurra a predição para cima ou para baixo até o valor final previsto (ex. base 23 → previsão 27, empurrado por LSTAT e TAX).
- **Gráfico de dependência (regressão)**: relação entre o valor de um atributo (eixo X) e seu valor SHAP (eixo Y, contribuição na mesma unidade do alvo) — cor automática por um segundo atributo (ou definida via `interaction_index`).
- **Gráfico de resumo (regressão)**: mesma leitura do Capítulo 13 — atributos ordenados por importância global, cor indica o valor do atributo, posição indica a direção/magnitude da contribuição.

## Mental Models
- Pense no valor SHAP de regressão como "quantas unidades do alvo este atributo específico adicionou ou subtraiu, partindo da média do dataset" — leitura direta e literal, sem precisar passar por uma função logística como na classificação.

## Code Examples
```python
import shap
exp = shap.TreeExplainer(xgr)
vals = exp.shap_values(bos_X)

# explicação local de uma amostra específica
shap.force_plot(exp.expected_value, vals[sample_idx], bos_X.iloc[sample_idx])

# relação atributo → contribuição, colorida por um segundo atributo
shap.dependence_plot("LSTAT", vals, bos_X)

# importância + direção do efeito, agregado por todo o dataset
shap.summary_plot(vals, bos_X)
```
- **O que demonstra**: a mesma API do Capítulo 13, aplicada sem modificação a um `XGBRegressor` em vez de um classificador.

## Key Takeaways
1. SHAP é model-agnóstico e funciona identicamente para classificação e regressão — só a unidade da contribuição muda.
2. O gráfico de forças traduz a predição em "de onde ela veio" (base + empurrões de cada atributo), útil para justificar uma predição individual a um stakeholder de negócio.
3. O gráfico de resumo é a via mais rápida de obter, de uma vez, importância global e direção do efeito de cada atributo.

## Connects To
- **Ch 13**: explicação de modelos de classificação — este capítulo é sua contraparte direta em regressão.
- **Ch 14**: o modelo XGBoost explicado aqui foi treinado lá.
</content>
