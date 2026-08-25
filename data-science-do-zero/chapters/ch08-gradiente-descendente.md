# Capítulo 8 — Gradiente Descendente

## Por Que Gradiente Descendente
"Melhor modelo" costuma significar "minimiza erro" ou "maximiza verossimilhança" — um problema de otimização. O livro escolhe **gradiente descendente** como técnica universal por se prestar bem a uma implementação do zero, e a reutiliza pelo resto do livro (regressão, aprendizado de máquina em geral).

## A Ideia
Para uma função `f: vetor → número real`, o **gradiente** (vetor de derivadas parciais) aponta na direção de crescimento mais rápido. Algoritmo: partir de um ponto aleatório, dar um passo pequeno na direção do gradiente (para maximizar) ou na direção oposta (para minimizar), repetir. **Limitação reconhecida**: com mínimos locais múltiplos, o procedimento pode convergir para o mínimo errado — mitigado reiniciando de vários pontos de partida.

## Estimando o Gradiente
Quando a derivada exata não é conhecida/calculável, aproxima-se pelo **quociente diferencial** (`difference_quotient(f, x, h) = (f(x+h)-f(x))/h`, com `h` pequeno). Para funções multivariáveis, a derivada parcial em relação à `i`-ésima variável fixa as demais e perturba só `x_i` (`partial_difference_quotient`); o gradiente completo (`estimate_gradient`) exige `2n` avaliações de `f` para um vetor de tamanho `n` — **caro computacionalmente**, por isso, sempre que possível, deriva-se a fórmula fechada do gradiente em vez de estimá-la numericamente (o que o livro faz nos capítulos seguintes).

## Usando o Gradiente
`step(v, direction, step_size)` — move `v` na direção dada. Exemplo mínimo: minimizar `sum_of_squares` (mínimo conhecido = vetor zero) partindo de ponto aleatório, andando repetidamente na direção `-gradiente` até a mudança cair abaixo de uma tolerância.

## Escolhendo o Tamanho do Passo
Não há solução única — opções: passo fixo, passo decrescente, ou (a escolhida pelo livro) testar uma lista de tamanhos candidatos a cada iteração e ficar com o que minimiza mais a função-alvo (`step_sizes = [100, 10, 1, 0.1, ..., 0.00001]`). Como alguns tamanhos podem levar a entradas inválidas, o wrapper `safe(f)` captura exceções e retorna `float('inf')` (nunca escolhido como mínimo).

## `minimize_batch` / `maximize_batch`
Função central do capítulo: recebe `target_fn`, `gradient_fn` e um `theta_0` inicial; a cada iteração calcula o gradiente, testa todos os `step_sizes`, escolhe o melhor `next_theta`, e para quando a melhora cair abaixo de uma tolerância. Chamado **batch** porque cada passo usa o dataset inteiro (a função de erro soma sobre todos os pontos). Maximizar é implementado minimizando o negativo (`negate`/`negate_all`).

## Gradiente Descendente Estocástico (SGD)
Como funções de erro tipicamente são **aditivas** (erro total = soma dos erros por ponto), pode-se computar o gradiente e dar um passo usando **um único ponto por vez**, iterando os dados em ordem aleatória a cada época (`in_random_order`, via `random.shuffle` sobre índices). `minimize_stochastic`:
- Mantém o melhor `(theta, value)` visto até agora.
- Se não houver melhora por 100 iterações consecutivas, encerra.
- Reduz o tamanho do passo (`alpha *= 0.9`) quando não há melhora, e o restaura ao tamanho inicial ao achar um novo mínimo — evita ficar "circulando" indefinidamente perto do mínimo.
- É tipicamente **mais rápido** que a versão batch, ao custo de trajetória mais ruidosa.

## Por Que Isso Importa
`minimize_stochastic`/`maximize_stochastic` são o motor de treinamento usado literalmente (sem reescrever) em Naive Bayes (13), regressão linear simples e múltipla (14-15) e regressão logística (16). O aviso final do autor é irônico e realista: na prática usa-se a otimização de bibliotecas prontas (ex. `scikit-learn`), mas entender o mecanismo por dentro ajuda a diagnosticar quando ela falha.
