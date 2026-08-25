# Capítulo 18 — Redes Neurais

## Motivação e Aviso
Redes neurais são inspiradas (vagamente) no cérebro: neurônios artificiais recebem entradas, computam algo, e "disparam" ou não. Úteis para reconhecimento de padrões (caligrafia, faces), mas o autor é explícito: são **"caixas-pretas"** difíceis de interpretar, redes grandes são difíceis de treinar, e **para a maioria dos problemas de data science não são a melhor escolha** — úteis principalmente quando se está mirando em algo mais ambicioso ("a Singularidade").

## Perceptron
Neurônio único com `n` entradas binárias, pesos e um bias: `perceptron_output = step_function(dot(weights, x) + bias)`, onde `step_function(x) = 1 se x≥0 senão 0`. Geometricamente, separa o espaço de entrada em duas metades por um hiperplano `dot(weights,x)+bias=0`.

Portas lógicas construídas manualmente ajustando pesos: **AND** (`weights=[2,2], bias=-3`), **OR** (`weights=[2,2], bias=-1`), **NOT** (`weights=[-2], bias=1`). **Limite fundamental**: um único perceptron **não consegue representar XOR** — não existe hiperplano que separe linearmente as classes de XOR. Isso motiva empilhar neurônios em camadas.

## Redes Neurais Feed-Forward
Estrutura em camadas: entrada → uma ou mais camadas ocultas → saída, cada neurônio conectado à camada seguinte. Substitui a `step_function` (descontínua) pela **função sigmoid** (`sigmoid(t) = 1/(1+exp(-t))`) — suave e diferenciável, necessária para treinar via cálculo/gradiente. **Nota de nomenclatura**: `sigmoid` aqui é a mesma função `logistic` do Capítulo 16 — "sigmoid" descreve a forma da curva, "logística" é essa função específica; os termos são frequentemente usados de forma intercambiável.

Representação: rede = lista de camadas; camada = lista de neurônios; neurônio = lista de pesos (incluindo peso de bias, alimentado por uma entrada fixa de 1). `feed_forward(neural_network, input_vector)` propaga a entrada camada por camada, retornando as saídas de **todas** as camadas (não só a final).

**XOR resolvido com uma camada oculta**: uma rede com 2 neurônios ocultos (aproximando "and" e "or") alimentando 1 neurônio de saída (aproximando "or mas não and") reproduz XOR — demonstra que uma camada oculta adiciona poder representacional que um único perceptron não tem.

## Backpropagation
Redes reais não são projetadas à mão — são **treinadas com dados**, via **backpropagation**, uma aplicação de gradiente descendente à arquitetura em camadas:
1. `feed_forward` no vetor de entrada → saídas de todos os neurônios.
2. Erro de cada neurônio de saída = saída obtida − alvo.
3. Gradiente do erro em relação aos pesos de saída → ajusta pesos da camada de saída.
4. "Propaga" o erro retroativamente para inferir erro das camadas ocultas.
5. Ajusta pesos ocultos da mesma forma.

`backpropagate(network, input_vector, targets)`: usa a derivada da sigmoid (`output*(1-output)`) para calcular `output_deltas`, atualiza pesos de saída, propaga para `hidden_deltas` via produto escalar com os pesos de saída, atualiza pesos ocultos. Conceitualmente equivalente a escrever o erro quadrado como função dos pesos e aplicar `minimize_stochastic` (Capítulo 8) — mas o gradiente explícito por regra da cadeia é tedioso o bastante para justificar a implementação dedicada.

## Estudo de Caso: Reconhecer Dígitos (mini-CAPTCHA)
Cada dígito é uma imagem 5×5 codificada como vetor binário de 25 posições (1=pixel aceso). Saída: vetor one-hot de 10 posições (`targets[j] = [1 if i==j else 0 for i in range(10)]`). Rede: 25 entradas → 5 neurônios ocultos → 10 saídas, pesos iniciais aleatórios, treinada por 10.000 épocas de backpropagation sobre os 10 dígitos de referência.

**Resultado**: classifica perfeitamente os dígitos de treino; generaliza razoavelmente para variações desenhadas à mão (um "3" estilizado é corretamente reconhecido com alta confiança; um "8" estilizado gera confusão entre 5/8/9) — o autor nota que mais dados de treino ajudariam.

## Interpretando os Pesos (parcialmente)
Apesar da rede ser uma "caixa-preta", é possível visualizar os pesos da camada oculta como grades 5×5 (usando `pyplot.imshow` + hachuras para pesos negativos) e **inferir manualmente** o que cada neurônio oculto parece detectar (ex.: um neurônio reage à coluna esquerda e à linha do meio; outro reage a linhas horizontais mas não diagonais). O capítulo demonstra o cálculo passo a passo de como as 5 ativações ocultas combinam-se (via os pesos do neurônio de saída "3") para produzir a probabilidade final — uma rara janela de interpretabilidade num modelo geralmente opaco.

## Por Que Isso Importa
É o capítulo mais avançado computacionalmente do livro — combina álgebra linear (Cap. 4), sigmoid/logistic (Cap. 16) e gradiente descendente (Cap. 8) em uma arquitetura nova. Serve de ponte conceitual para deep learning, mencionado apenas como área externa ao escopo do livro.
