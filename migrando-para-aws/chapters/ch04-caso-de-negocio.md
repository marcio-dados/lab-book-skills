# Capítulo 4: Criando seu caso de negócio

## Core Idea
O caso de negócio traduz a descoberta técnica em uma narrativa e uma projeção financeira de cinco anos que a alta gerência possa aprovar — e sua qualidade depende de eliminar primeiro a "gordura" (aplicações que não devem migrar) e de tratar toda estimativa como uma aproximação suficiente ("lançar um foguete"), não uma previsão de centavos ("pousar na Lua").

## Frameworks Introduced
- **Equação de duração da migração**: `duração = servidores / (servidores por dia por engenheiro × engenheiros ajustados por férias) × (1 + buffer)`, dividida pelos dias úteis para converter em semanas/meses.
  - Como: (1) conte servidores a migrar; (2) estime taxa por engenheiro (~2/dia para consultor experiente, 0,5–1/dia para equipe interna); (3) reduza o número de engenheiros para compensar férias (nº de meses de férias agregadas ÷ 12); (4) aplique buffer de 10% (equipe experiente + muito COTS) a 20% (equipe nova + muito software interno).
  - Quando usar: antes do caso de negócio, para orçar duração e, consequentemente, o período de despesa duplicada.
- **Os 7 R's de migração (7 R Framework, metodologia da Amazon)**: Refactor, Redeploy, Rehost, Repurchase, Retire, Re-platform, Retain — classificação obrigatória de toda aplicação antes de projetar custo de execução.
  - Como: classifique cada aplicação descoberta em um dos 7 R's; some apenas os custos de Rehost + Re-platform + Redeploy + Refactor na projeção (Retire e Retain não entram; Repurchase é substituído pelo custo do novo software).
  - Distribuição típica observada pelo autor: Rehost ~80%, Re-platform ~20%, Refactor ≤5%, Repurchase ~5%, Retire <5%, Retain <5% (não somam 100% porque a ordem de grandeza varia por empresa).
- **Estrutura do caso de negócio**: narrativa escrita (introdução equilibrada → respostas às perguntas da FAQ do Ch 1 → conclusão com visão de futuro plausível) + projeção financeira de 5 anos em uma única página (10–15 linhas) + apêndice com detalhes de descoberta.
  - Regra de tom da narrativa: nem "tudo perfeito hoje" nem "tudo uma catástrofe" — o autor mostra o contraste entre uma resposta equilibrada (Pergunta 1 da FAQ) e uma resposta tendenciosa que soa como "sentença de morte" para quem escreveu (Pergunta 2 da FAQ).
- **Modelagem do custo de execução (planilha de projeção)**: sequência de 8 passos — (1) custo base de EC2/Storage/S3; (2) acréscimos de rede e serviços auxiliares; (3) custo de ferramentas; (4) custo de consultoria/prestadores de serviço; (5) modificadores de instância reservada / Savings Plans; (6) percentuais de migração por ano; (7) economias de agilidade (pipelines, Service Catalog); (8) pressupostos documentados.

## Key Concepts
- **TCO (Total Cost of Ownership)**: o objetivo final da projeção de 5 anos — comparar custo total on-premises vs. AWS ao longo do tempo, incluindo o período de gasto duplicado.
- **Burn-up / burn-down**: burn-up é o crescimento (linear, em passos) do gasto na AWS à medida que levas migram; burn-down é a queda (mais lenta, concentrada no final) do gasto on-premises — porque infraestrutura compartilhada (SAN, hosts de virtualização) só é desativada quando os *últimos* servidores dependentes saem. O autor recomenda **não** modelar burn-down em detalhe — o esforço de calcular não compensa o valor agregado.
- **Instâncias Reservadas (RI) vs. Savings Plans**: RI trava tipo de instância + SO por 1–3 anos (desconto médio 40%/1 ano, 60%/3 anos); Savings Plans trava só o volume de computação por família de instância, sem região fixa (desconto ~10 p.p. menor, mas mais flexível). Regra prática: empresas pequenas usam RI (previsibilidade de uso conhecida), médias usam Savings Plans, grandes avaliam o overhead de gestão de RI antes de escolher.
- **Pressupostos (assumptions)**: toda estimativa não determinística deve ser documentada explicitamente junto da projeção (mesma aba, não em anexo separado) — evita que alguém trate uma aproximação como número imutável.
- **Reidratação (rehydration)**: destruir e recriar servidores periodicamente com patches/imagens atualizadas via pipeline — reduz superfície de ataque, útil mesmo para aplicações COTS em ambientes de alta segurança.

## Mental Models
- **"Foguete para o espaço" vs. "pouso na Lua" (retomado do Ch 3)**: aplicado agora à própria projeção financeira — a precisão exigida no caso de negócio é a do lançamento, não a do pouso.
- **"Ser como Scotty de Jornada nas Estrelas"**: sempre subestime sua própria velocidade e adicione buffer generoso ao cronograma — ser "o herói que entrega antes do prazo" é preferível a prometer curto e atrasar repetidamente.
- **"Eliminar a gordura antes de servir o filé"**: aplicar os 7 R's e remover do orçamento tudo que não vai migrar (Retire, Retain) é pré-requisito para uma projeção de custo confiável — incluir custo AWS de algo que ficará on-premises infla e distorce o caso de negócio.
- **Não comparar maçãs com laranjas**: uma infraestrutura on-premises sem redundância nenhuma (Cenário 4.3) vai parecer mais cara na AWS em termos absolutos — nesse caso, a narrativa deve enfatizar disponibilidade ganha, não economia de custo.

## Anti-patterns
- **Prometer prazos "enxutos" para parecer competente**: o autor relata ter aprendido isso "da forma difícil" no início da carreira — cronogramas sem buffer geram atrasos repetidos que erodem a credibilidade, não constroem.
- **Ignorar férias e feriados no cronograma**: pode facilmente representar meses de trabalho não computado em empresas grandes (Cenário 4.1: 6 pessoas × 1 mês de férias = 150 servidores "perdidos" se não compensado).
- **Narrativa excessivamente crítica do ambiente atual ("Pergunta 2 da FAQ")**: pintar o on-premises como decrépito e catastrófico parece convincente à primeira vista, mas implica que o autor da narrativa (você) será responsabilizado por resolver tudo que descreveu como problema — "pode ser como assinar a sua própria sentença de morte".
- **Prometer tecnologia "solução para tudo" na conclusão da narrativa (blockchain, etc.)**: tecnologias aclamadas como panaceia raramente cumprem a promessa; a visão de futuro deve ser alcançável, não fantasiosa.
- **RI de 3 anos por padrão**: contraria agilidade, perde acesso a instâncias mais novas e mais baratas, exige desembolso alto adiantado, e trava você fora de futuras reduções de preço da AWS — o autor recomenda deixar 10–20% da capacidade sob demanda mesmo com RIs de 1 ano.
- **Calcular burn-down em detalhe**: consome semanas de esforço de engenharia para um dado que agrega pouco valor ao caso de negócio — a maior parte da redução on-premises só acontece no fim da migração, quando componentes compartilhados (SAN, instalações) são finalmente desativados.
- **Escolher perguntas técnicas de nicho para a narrativa** (ex.: conversão para SSD gp2): fascinante para quem é técnico, entediante e sem impacto perceptível para a alta gerência — escolha as perguntas certas para o público-alvo.

## Worked Example
**Cenário 4.5 — o ROI do Service Catalog (Bridget).** A empresa de Bridget, regulamentada, cria e valida manualmente imagens de sistema: 80 implantações/mês, 3,5 horas cada, a US$ 100/hora → custo atual de US$ 28.000/mês (US$ 336.000/ano). Para automatizar via AWS Service Catalog: custo de criação do produto = 3 semanas de trabalho = US$ 12.000 (100 × 15 dias × 8h); custo operacional após automação = 10 minutos por implantação × 80/mês × 12 meses = US$ 16.000/ano (100/6 × 80 × 12). Economia líquida no primeiro ano: US$ 336.000 − US$ 12.000 − US$ 16.000 = **US$ 308.000**. A lição do autor: antes de comprometer esforço de engenharia em automação, procure padrões repetitivos de alto custo *administrativo* (não necessariamente de infraestrutura complexa) — o Cenário 4.6 (buckets S3 simples, mas com uma hora de burocracia por implantação, 3.546 vezes/ano) mostra o mesmo padrão: a tarefa técnica é trivial, o desperdício está no processo em torno dela.

## Key Takeaways
1. Calcule a duração da migração antes do caso de negócio, com buffer (10–20%) e compensação explícita de férias/feriados — sem isso, os custos de gasto duplicado ficam subestimados.
2. Classifique toda aplicação descoberta pelos 7 R's antes de modelar custo — não inclua no orçamento AWS nada que será Retido ou Aposentado.
3. Estruture o caso de negócio como narrativa (tom equilibrado, baseada na FAQ do Ch 1) → projeção de 5 anos em uma página → apêndice de detalhes; nunca inverta essa ordem de prioridade de atenção do leitor.
4. Trate todo custo não determinístico (banda de saída, serviços auxiliares, LCU de ALB/NLB, burn-down) com acréscimos percentuais ou omissão justificada — não invista semanas de precisão onde a decisão não muda.
5. Escolha RI vs. Savings Plans pelo porte da empresa e overhead de gestão disponível; nunca comprometa 100% da capacidade — deixe 10–20% sob demanda.
6. Capture economias de agilidade (pipelines de implantação, Service Catalog) com uma fórmula simples: custo atual (horas × frequência × custo/hora) menos custo de automação (criação + operação) — isso é frequentemente a maior e mais defensável linha de economia do caso de negócio.
7. Documente todos os pressupostos não óbvios na mesma aba da projeção financeira — isso previne que uma aproximação seja tratada como compromisso contratual depois.
8. Não modele burn-down em detalhe; o esforço de calcular supera o valor que agrega à decisão.

## Connects To
- **Ch 1**: a FAQ do porquê é a matéria-prima direta da narrativa do caso de negócio.
- **Ch 2**: custos de consultoria/prestadores de serviço retomam a discussão de risco de "diversidade de tecnologias".
- **Ch 3**: os dados de descoberta (dimensionamento, licenciamento, custos auxiliares) alimentam a modelagem de custo de execução deste capítulo.
- **Ch 7**: o planejamento detalhado da migração (levas, cronograma real) refina as estimativas percentuais de "porcentagem de migração por ano" usadas aqui.
- **Ch 8**: pipelines de implantação e reidratação retornam como parte dos preparativos finais e da refatoração.
