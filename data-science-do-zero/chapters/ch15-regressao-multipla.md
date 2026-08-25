# Capítulo 15 — Regressão Múltipla

## O Modelo
Generaliza o Capítulo 14 para `k` variáveis independentes: `y_i = β0 + β1·x_i1 + ... + βk·x_ik + ε_i`. Truque de representação: incluir o termo constante `β0`/`alpha` como mais um coeficiente, adicionando uma coluna de 1s a cada vetor `x_i` (`x_i = [1, x_i1, ..., x_ik]`, `beta = [alpha, beta_1, ..., beta_k]`) — assim `predict(x_i, beta) = dot(x_i, beta)`, sem caso especial. Variáveis categóricas (ex.: "tem PhD?") viram **variáveis dummy** 0/1.

## Suposições Necessárias
1. **Colunas de x linearmente independentes**: se uma coluna é combinação linear de outras (ex.: `num_acquaintances` sempre igual a `num_friends`), é **impossível** estimar os coeficientes de forma única — somar uma constante a um coeficiente e subtrair da outra coluna redundante não muda a previsão. Violações menos óbvias existem sem ser detectadas facilmente.
2. **Colunas de x não correlacionadas com os erros `ε`**: se violada, a estimativa de `beta` fica **sistematicamente polarizada** (viesada). Exemplo construído: se "horas trabalhadas" reduz minutos no site E está positivamente correlacionada com "número de amigos", omitir "horas trabalhadas" do modelo faz o coeficiente estimado de "amigos" ficar **subestimado** em relação ao valor real — um caso concreto de **variável omitida** distorcendo a estimativa de outra.

## Ajustando o Modelo (Gradiente Descendente)
Sem fórmula fechada simples para múltiplas variáveis — usa-se `squared_error_gradient(x_i, y_i, beta) = [-2*x_ij*error for x_ij in x_i]` com `minimize_stochastic`. `estimate_beta(x, y)` parte de `beta` aleatório. Resultado no exemplo (amigos, horas de trabalho, PhD): `minutos = 30,63 + 0,972·amigos - 1,868·horas_trabalho + 0,911·PhD`.

## Interpretando os Coeficientes
Cada coeficiente é o efeito de **uma unidade a mais naquela variável, com todas as outras mantidas constantes** ("ceteris paribus"). O modelo **não captura interações** entre variáveis por padrão — para isso, seria preciso adicionar explicitamente um termo produto (ex.: `amigos × horas_trabalho`) ou termos não-lineares (ex.: `amigos²`, para capturar um efeito não-monotônico). Aviso: não há limite para quantos termos "engenhosos" se pode adicionar — cresce o risco de sobreajuste.

## Benefício do Ajuste e Erros Padrões
`multiple_r_squared` sobe para 0,68 ao adicionar variáveis — mas **R² sempre aumenta (ou mantém) ao adicionar qualquer variável**, mesmo irrelevante (regressão simples é o caso especial com coeficientes extras = 0). Por isso R² sozinho não valida a utilidade de uma variável — é preciso examinar o **erro padrão de cada coeficiente**.

### Bootstrap (digressão necessária)
Para estimar a incerteza de uma estatística sem fórmula fechada, o livro introduz o **bootstrap**: reamostrar os dados observados **com reposição** (`bootstrap_sample`) muitas vezes e recalcular a estatística em cada reamostragem (`bootstrap_statistic`). A dispersão dessas estatísticas recalculadas estima o erro padrão da estatística original. Demonstrado com a mediana: um dataset concentrado perto de 100 gera medianas bootstrap muito estáveis (baixo erro padrão); um dataset bimodal (metade perto de 0, metade perto de 200, mas com mediana também ~100) gera medianas bootstrap muito dispersas — a mesma mediana pontual esconde confiança totalmente diferente.

### Aplicado aos coeficientes de regressão
Reamostrar pares `(x_i, y_i)` (usando `zip` antes de amostrar, para preservar correspondência) e reestimar `beta` centenas de vezes (`estimate_sample_beta`); o desvio padrão de cada coeficiente ao longo das reamostragens é seu erro padrão bootstrap. Isso permite computar um `p_value` (via aproximação normal, já que `n >> k` no exemplo) para testar `H0: βi=0`. Resultado do livro: coeficientes de `amigos` e `horas_trabalho` têm p-value ≈0 (significativos); **o coeficiente de "PhD" tem p-value 0,36 — não significativamente diferente de zero**, apesar de ter entrado no modelo com valor "0,911".

## Regularização
Com muitas variáveis, dois problemas crescem: sobreajuste e dificuldade de interpretação. **Regularização** adiciona ao erro uma penalidade que cresce com a magnitude de `beta`, minimizando erro+penalidade juntos.
- **Ridge**: penalidade `alpha * dot(beta[1:], beta[1:])` (soma dos quadrados, **excluindo o termo constante**). `alpha` é um hiperparâmetro (nomeado assim para não colidir com `lambda`, palavra reservada em Python). Gradiente da penalidade somado ao gradiente do erro quadrado (`squared_error_ridge_gradient`). Conforme `alpha` cresce: R² piora ligeiramente, mas os coeficientes encolhem — no exemplo, o coeficiente de "PhD" (já suspeito pelo p-value alto) é o que mais encolhe, indo a quase zero com `alpha=10`.
- **Ridge exige redimensionar os dados antes** (Capítulo 10) — mudar a unidade de uma variável (ex.: anos → séculos) multiplicaria seu coeficiente e mudaria artificialmente o quanto ela é penalizada.
- **Lasso**: penalidade `alpha * sum(abs(beta_i))` (valor absoluto, não quadrado) — tende a **zerar** coeficientes completamente (produz modelos esparsos), ao contrário do ridge que só os encolhe. Não é diferenciável em zero, então **não dá para resolver com gradiente descendente simples** — o livro reconhece o limite e não implementa lasso do zero.

## Por Que Isso Importa
Bootstrap é técnica de propósito geral (não específica de regressão) reaproveitável para qualquer estatística sem distribuição conhecida. `rescale` + `estimate_beta` + `train_test_split` reaparecem diretamente no Capítulo 16 (regressão logística) usando o mesmo dataset de contas premium/experiência/salário.
