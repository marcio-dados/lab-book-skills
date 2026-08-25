# Capítulo 13: Explicando os modelos

## Core Idea
Existe uma escada de técnicas de explicação que vai de nativa/simples (coeficientes, `feature_importances_`) até model-agnóstica e local (LIME, treeinterpreter, gráficos de dependência parcial, modelos substitutos, SHAP) — quanto mais "caixa-preta" o modelo, mais se depende de técnicas que perturbam ou aproximam o modelo em vez de ler seus parâmetros diretamente.

## Frameworks Introduced
- **Explicação global vs. local**: importância de atributos/coeficientes explicam o modelo como um todo (global); LIME, treeinterpreter e SHAP (`force_plot`) explicam uma predição individual (local) — perguntas diferentes ("o que importa em geral?" vs. "por que este caso específico teve esta predição?") exigem ferramentas diferentes.
  - Quando usar: explicação global para validar/documentar o modelo; explicação local para depurar ou justificar uma decisão específica a um stakeholder.
- **Modelo substituto (surrogate model)**: quando o modelo real é opaco (SVM, rede neural), treina-se uma árvore de decisão para prever as saídas do modelo opaco — a árvore substituta é interpretável e aproxima o comportamento do original.
  - Quando usar: quando a técnica de explicação nativa do modelo real (SVM, rede neural) é fraca ou inexistente.
  - Como: `sur_dt.fit(X_test, modelo_opaco.predict(X_test))`, depois inspecionar `sur_dt.feature_importances_`.
- **SHAP (Shapley Additive exPlanations)**: atribui a cada atributo uma contribuição aditiva a partir de um "valor de base" (média do dataset) até a predição final — funciona para qualquer modelo (`TreeExplainer` para árvores, versões genéricas para outros), local (`force_plot` por amostra) e global (`summary_plot` agregando todas as amostras).

## Key Concepts
- **Coeficientes de regressão**: sinal indica direção do efeito (positivo → aumenta a predição); magnitude (após padronização) indica força relativa.
- **`feature_importances_`**: já visto nos Capítulos 3/8/10 — importância nativa de modelos de árvore.
- **LIME**: explica uma amostra perturbando seus valores localmente e ajustando um modelo linear simples só naquela vizinhança — exige `.values` (array numpy), não aceita DataFrame diretamente.
- **`treeinterpreter`**: decompõe a predição de um modelo de árvore em `bias` (média do treino) + contribuição de cada atributo, que somados reproduzem exatamente a predição final.
- **Gráfico de dependência parcial (PDP)**: fixa um atributo em vários valores, recalcula a predição média sobre todas as amostras, e plota o resultado — mostra a forma da relação atributo→alvo, mas assume atributos independentes (pode enganar sob colinearidade).
- **Valores SHAP**: para classificação, soma de log-odds; para regressão, soma direta do alvo — a soma do "valor de base" com todas as contribuições SHAP reproduz a predição exata, assim como no `treeinterpreter`.
- **`shap.summary_plot`**: combina importância global (ordenação por magnitude média) com efeito individual (cor = valor do atributo) em um único gráfico — mostra não só "o que importa" mas "em que direção" e "para quais valores".

## Mental Models
- Pense em `treeinterpreter` e SHAP como a mesma ideia (decompor a predição em base + contribuições que somam exatamente o resultado), com SHAP sendo a versão model-agnóstica e teoricamente mais fundamentada (baseada em teoria dos jogos).
- PDP responde "como a predição média muda se eu variar só este atributo?"; SHAP dependence plot responde a mesma pergunta mas preservando informação por amostra individual (útil para ver quando o efeito de um atributo depende de outro, como idade × classe no Titanic).

## Anti-patterns
- **Interpretar gráfico de dependência parcial sem considerar colinearidade**: PDP assume atributos independentes; se dois atributos são correlacionados, fixar um enquanto varia o outro pode gerar combinações irreais.
- **Usar LIME/SHAP com DataFrame diretamente sem converter**: LIME exige `.values` (array numpy); confirmar a interface esperada antes de depurar erros de tipo.

## Code Examples
```python
# LIME: explicação local de uma amostra específica
from lime import lime_tabular
explainer = lime_tabular.LimeTabularExplainer(
    X_train.values, feature_names=X.columns, class_names=["died", "survived"],
)
exp = explainer.explain_instance(X_train.iloc[-1].values, dt.predict_proba)

# treeinterpreter: decompor predição em base + contribuições
from treeinterpreter import treeinterpreter as ti
prediction, bias, contribs = ti.predict(rf5, X.iloc[:2])

# SHAP: explicação local (force_plot) e global (summary_plot)
import shap
s = shap.TreeExplainer(rf5)
shap_vals = s.shap_values(X_test)
shap.force_plot(s.expected_value[1], shap_vals[1][20, :], feature_names=X_test.columns)
shap.summary_plot(shap_vals[0], X_test)
```
- **O que demonstra**: três níveis de explicação (local perturbativo, local aditivo exato, global agregado) que se complementam.

## Reference Tables
| Técnica | Escopo | Funciona em qualquer modelo? |
|---|---|---|
| Coeficientes / `feature_importances_` | Global | Não (só linear/árvore) |
| LIME | Local | Sim (perturbação + modelo linear local) |
| `treeinterpreter` | Local (soma exata) | Não (só árvores do sklearn) |
| Gráfico de dependência parcial | Global (média) | Sim, mas assume independência entre atributos |
| Modelo substituto | Global (aproximado) | Sim (via árvore treinada nas predições) |
| SHAP | Local e global (soma exata) | Sim (com `TreeExplainer` otimizado para árvores) |

## Key Takeaways
1. Escolha a técnica pela pergunta: explicação de uma amostra (LIME/SHAP local) vs. explicação geral do modelo (importância/SHAP global).
2. SHAP e `treeinterpreter` são "aditivos exatos" — base + contribuições somam exatamente a predição, diferente de LIME (aproximação local) e PDP (média, não exata por amostra).
3. Modelos opacos (SVM, redes neurais) podem ser explicados via modelo substituto (árvore treinada nas predições) quando não há técnica nativa suficiente.
4. PDP assume independência entre atributos — cuidado com colinearidade ao interpretar.

## Connects To
- **Ch 3/10**: `.feature_importances_`/`.coef_` já vistos como explicação nativa; este capítulo generaliza para modelos sem essa via direta.
- **Ch 8**: seleção de atributos e explicação de modelo compartilham ferramentas (importância, dependência entre atributos).
- **Ch 16**: aplica SHAP ao contexto de regressão.
</content>
