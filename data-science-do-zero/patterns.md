# Padrões e Técnicas — Data Science do Zero

## Gradiente Descendente como Motor Universal de Otimização
**Quando usar**: qualquer problema redutível a "minimizar/maximizar uma função de parâmetros" quando não há (ou não se quer derivar) solução fechada.
**Como**: definir `target_fn` + `gradient_fn` (analítico se possível; `estimate_gradient` via quociente diferencial se não), alimentar `minimize_batch`/`minimize_stochastic`; maximizar = minimizar o negativo (`negate`/`negate_all`).
**Trade-offs**: batch usa o dataset inteiro por passo (estável, lento); estocástico usa um ponto por passo (rápido, ruidoso, precisa reduzir o `step_size` ao estagnar). Reaplicado sem redefinição em regressão linear/múltipla/logística, PCA e redes neurais.

## Suavização com Pseudo-contagem (Laplace/Add-k)
**Quando usar**: estimar uma probabilidade por frequência relativa quando a contagem observada pode ser zero.
**Como**: `P(evento) = (k + contagem) / (2k + total)` — finge ter visto `k` ocorrências extras a favor e `k` contra.
**Trade-offs**: `k` maior suaviza mais (mais viés, menos variância); `k=0` reproduz a frequência crua (frágil a zeros). Usado identicamente em Naive Bayes (Ch 13, parâmetro `k`) e LDA/amostragem de Gibbs (Ch 20, parâmetros `alpha`/`beta`).

## Log-Probabilidade em vez de Produto de Probabilidades
**Quando usar**: multiplicar muitas probabilidades pequenas (Naive Bayes, verossimilhança de regressão logística).
**Como**: somar `log(p_i)` em vez de multiplicar `p_i`; `exp()` no final se precisar do valor original.
**Trade-offs**: evita *underflow* de ponto flutuante; custo é só uma chamada extra de `log`/`exp` por termo.

## Índice Invertido para Evitar Busca Linear Repetida
**Quando usar**: precisa responder repetidamente "quem tem o atributo X?" sobre a mesma coleção.
**Como**: construir uma vez `defaultdict(list)` mapeando atributo → lista de IDs (Ch 1: `user_ids_by_interest`); consultas subsequentes são O(1) em vez de O(n) por consulta.
**Trade-offs**: custo de construção pago uma vez, amortizado por todas as consultas seguintes — só compensa se houver mais de uma consulta.

## Validação Treino/Validação/Teste
**Quando usar**: sempre que for necessário tanto ajustar quanto **escolher entre** modelos.
**Como**: `split_data`/`train_test_split` para treino/teste simples; se for comparar vários modelos, separar um terceiro conjunto de validação — testar cada modelo candidato nele, e reservar o teste para uma única avaliação final.
**Trade-offs**: pular a validação e escolher modelos direto pelo desempenho no teste transforma o teste em treino disfarçado — a métrica final fica otimista e não confiável.

## Bootstrap para Erro Padrão sem Fórmula Fechada
**Quando usar**: preciso saber "quão confiável é esta estatística?" e não há (ou não quero derivar) fórmula analítica para o erro padrão.
**Como**: `bootstrap_sample` (amostra com reposição, mesmo tamanho do original) + `bootstrap_statistic` (recalcula a estatística em N reamostragens); o desvio padrão das reamostragens estima o erro padrão da estatística original.
**Trade-offs**: custo computacional de repetir o cálculo centenas de vezes; para pares `(x,y)` correlacionados, sempre fazer `zip` antes de reamostrar (preserva correspondência).

## Regularização Ridge para Encolher Coeficientes
**Quando usar**: regressão com muitas variáveis, risco de sobreajuste ou coeficientes difíceis de interpretar.
**Como**: somar ao erro uma penalidade `alpha * dot(beta[1:], beta[1:])` (exclui o termo constante); resolver via gradiente descendente com o gradiente da penalidade somado ao gradiente do erro.
**Trade-offs**: `alpha` maior encolhe mais os coeficientes (menos R², menos sobreajuste); **sempre redimensionar os dados antes** — mudar a unidade de uma variável mudaria artificialmente o quanto ela é penalizada. Ridge encolhe todos os coeficientes; Lasso (não implementável com gradiente descendente simples, por não ser diferenciável em zero) tende a zerá-los completamente.

## Representação Recursiva Mínima para Estruturas de Árvore
**Quando usar**: modelar qualquer estrutura hierárquica (árvore de decisão, cluster hierárquico) sem framework externo.
**Como**: representar folha como caso base (valor simples ou tupla de 1) e nó interno como tupla `(critério/ordem, [filhos])`; funções recursivas (`classify`, `get_values`, `expand`) tratam o caso folha primeiro e recursam no caso composto.
**Trade-offs**: leve e fácil de raciocinar, mas sem otimizações (sem índice, sem cache) — adequado para ensino/protótipo, não produção.

## Split-Apply-Combine Genérico (`group_by`)
**Quando usar**: agrupar registros por uma chave derivada e aplicar uma transformação por grupo — praticamente qualquer análise tabular.
**Como**: `group_by(grouper_fn, rows, value_transform=None)` — agrupa via `defaultdict(list)` chaveado pela saída de `grouper_fn`; aplica `value_transform` a cada grupo se fornecido.
**Trade-offs**: reaplicado literalmente (com nomes diferentes) em manipulação de dados (Ch 10), MapReduce (Ch 24, via `map_reduce`) e SQL (Ch 23, via `Table.group_by` com `having`) — é o mesmo padrão em três roupagens.

## Escolha de Hiperparâmetro pelo "Cotovelo" do Gráfico
**Quando usar**: escolher `k` (clusters) ou qualquer hiperparâmetro sem valor "certo" óbvio.
**Como**: plotar uma métrica de erro/qualidade em função do hiperparâmetro e escolher o ponto onde a curva "dobra" (retornos decrescentes começam).
**Trade-offs**: heurística visual, não um teste estatístico formal — mas barata e geralmente suficiente para decisões de engenharia.

## Combinadores para Reduzir Tráfego em MapReduce Distribuído
**Quando usar**: mapper emite muitas ocorrências repetidas da mesma chave antes de enviar para o redutor.
**Como**: pré-agregar localmente na máquina mapeadora (ex.: `("data", 500)` em vez de 500× `("data", 1)`) antes de transmitir; só é seguro se o reducer for uma operação associativa como `sum` (não funciona se o reducer depender de `len(values)` bruto).
**Trade-offs**: reduz drasticamente volume de rede; exige desenhar o reducer para tolerar valores pré-combinados.
