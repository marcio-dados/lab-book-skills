# Capítulo 7: Planejando sua migração

## Core Idea
O plano de migração é, em sua maior parte (~90%), um subproduto direto do mapeamento de dependências feito na descoberta; o trabalho manual real está nos ~10% restantes — analisar fatores de bloqueio, escolher metodologia de desenvolvimento e ferramentas, e negociar o cronograma com as unidades de negócio — e mesmo esse cronograma deve ser tratado como fluido, nunca imutável.

## Frameworks Introduced
- **Cascata ágil (waterfall-agile híbrido)**: aceite que a migração terá trechos sequenciais obrigatórios (Active Directory, servidores de arquivo, bancos de dados fortemente acoplados devem ir antes de suas dependentes) dentro de um plano organizado em sprints ágeis de ~2 semanas.
  - Como: não force a migração inteira a ser 100% ágil; identifique os blocos que exigem ordem fixa e trate o resto com flexibilidade de sprint.
- **Fatores de bloqueio (technology blockers + business blockers)**: checklist a rodar antes do planejamento fino.
  - Tecnológicos: SO sem suporte na AWS (Solaris, macOS — falta driver de rede/disco virtualizado), SO desatualizado sem patch de segurança, hardware incompatível (mainframe/RISC). Mitigação para SO datado sem recompilação possível: AWS End of Support Migration Program (empacotamento tipo App-V/ThinApp) como solução ponte.
  - De negócio: M&A (aquisição/venda de unidade), mudança de gerência (vertical tem mais risco que horizontal, risco maior em empresas pequenas), mudança de prioridade (bug crítico ou pressão competitiva).
- **Equação de nível de esforço (LOE) por aplicação**: `LOE = (servidores × fator_código × fator_idade × (1 + dependentes + dependências)) / (capacidade_da_equipe × dias_do_sprint)` (ajustada por sprint, arredondada sempre para cima).
  - Como usar: calcule para cada aplicação identificada na descoberta; o resultado em sprints determina quantas "notinhas adesivas" ela ocupa no plano visual.
- **Teste de alto acoplamento**: duas aplicações devem migrar juntas (no mesmo sprint) se uma acessa diretamente o banco de dados/dados internos da outra (muitos acessos de ida e volta); podem migrar separadamente se a comunicação é via API REST bem definida (poucos acessos, baixa latência acumulada). Acoplamento via banco de dados compartilhado com volume alto de transações também conta como alto acoplamento, mesmo com poucas dependências aparentes.
- **Método do quadro-branco com notinhas adesivas**: ferramenta de planejamento deliberadamente não-digital — uma notinha = uma unidade de sprint de esforço; linhas horizontais = workstreams (cada um com 2 engenheiros, nunca 1, para resiliência a férias/ausência); eixo horizontal = cronograma em escala real.
  - Por que não uma ferramenta digital: democratiza a colaboração entre equipes de negócio que não usariam a mesma ferramenta de TI — todo mundo sabe mover uma notinha.
- **90/10 do planejamento**: 90% do plano é mecânico, derivado do mapeamento de dependências + LOE; os 10% finais exigem negociação humana com stakeholders de negócio (datas de fechamento contábil, lançamentos de produto, férias) — só essa parte não pode ser automatizada.

## Key Concepts
- **Sprint de migração**: unidade de tempo (recomendação do autor: 2 semanas) usada tanto para trabalho ágil quanto para blocos em cascata dentro do plano.
- **CloudEndure / DMS / DataSync**: as três ferramentas nativas cobrem ~90% das necessidades de migração — CloudEndure para réplica de blocos (servidor completo, físico ou virtual, única opção recomendada pelo autor sobre o AWS SMS), DMS para bancos de dados (inclusive troca de engine, ex. Oracle→MySQL, mas só migra o esquema — mudanças de código da aplicação ficam por sua conta), DataSync para arquivos (NFS/Windows → S3/EFS/FSx).
- **Buffer de cronograma sob restrição de prazo fixo**: se há data inflexível (ex.: desocupar data center), estime com 80% do tempo disponível e planeje/comunique o total — a folga de 20% absorve imprevistos sem quebrar o compromisso externo.
- **Metodologias ágeis de desenvolvimento (XP, Scrum, FDD)**: decisão que deve ser tomada durante o planejamento da migração (não depois) porque define as ferramentas de suporte (CodePipeline, CodeGuru) que as primeiras aplicações migradas já devem seguir — atrasar essa decisão significa retrabalho certo depois.

## Mental Models
- **A migração é como água correndo em um rio**: precisa ser fluida e adaptável a mudanças de prioridade (M&A, bug crítico, pressão competitiva) — tentar ser rígida é "ficar presa às rochas e não ir a lugar nenhum".
- **"Você já foi lançado para o espaço; agora aprimoramos rumo ao pouso na Lua"** (retomado dos Caps. 3–4): a análise de fatores de bloqueio é o próximo refinamento de precisão, não o nível final de detalhe.
- **Notinha adesiva em escala real**: o valor do método manual está em tornar o esforço e o cronograma *visíveis fisicamente* para todos os stakeholders na sala — substituir por uma ferramenta digital sem esse efeito colaborativo perde o ponto principal do exercício.

## Anti-patterns
- **Migrar um sistema operacional desatualizado só porque "vai ficar mais seguro na AWS"**: aumenta a segmentação, mas não elimina a vulnerabilidade em si — só a torna mais difícil de alcançar, criando falsa sensação de segurança.
- **Migrar uma aplicação para a AWS antes da correção de um bug crítico conhecido**: muda a causalidade de um estado conhecido para um desconhecido (ex.: uma race condition pode "desaparecer" com CPU/RAM diferentes e reaparecer sob carga) — só migrar antes se o cronograma do fornecedor estiver extremamente dessincronizado com o da migração.
- **Sprints de uma semana para migração de aplicações**: funciona para pequenas correções de desenvolvimento, mas raramente é suficiente para o volume de trabalho de migração — o autor viu isso ser tentado e falhar em um projeto real.
- **Colocar aplicações altamente acopladas em sprints separados por conveniência de workstream livre**: desacopla acidentalmente aplicações que dependem uma da outra, quebrando a aplicação principal em produção.
- **Tratar o cronograma inicial como imutável depois de uma mudança de prioridade de negócio**: ignorar M&A, bug crítico ou pressão competitiva e insistir no plano original é perder de vista que "a bola são os seus negócios", não a migração em si.
- **Esquecer um sistema "invisível" mas altamente acoplado** (Cenário 7.3 — sistema de manufatura da CamperSmiths): a contagem inicial de "quatro aplicações" ignorava o sistema de manufatura do qual duas delas dependiam — sempre valide o grafo de dependências completo, não apenas a lista nominal de aplicações.

## Worked Example
**Cenário 7.3 — mapeando acoplamento real (Kara, CamperSmiths).** Quatro aplicações aparentemente independentes (inventário, site, atendimento ao cliente, previsão) na verdade envolvem cinco sistemas, porque duas delas (inventário e previsão) se comunicam com um sistema de manufatura via API REST — baixo acoplamento, podem migrar em momento separado. Já inventário e previsão escrevem diretamente no banco de dados do site — alto acoplamento, devem migrar junto com o site. A aplicação de atendimento ao cliente também acessa o banco do site, mas o veredito de acoplamento depende do volume real de transações: alto volume (milhares de pedidos/dia) = alto acoplamento = migra junto; baixo volume = baixo acoplamento = pode migrar separado. A lição: acoplamento não é uma propriedade fixa da arquitetura — é uma função do volume real de interação, e deve ser avaliado caso a caso, não assumido pela topologia do diagrama.

## Key Takeaways
1. Trate seu plano como cascata-ágil híbrido — identifique os blocos com ordem obrigatória (AD, storage compartilhado, bancos fortemente acoplados) e deixe o resto fluido em sprints de ~2 semanas.
2. Rode a checklist de fatores de bloqueio (SO sem suporte, hardware incompatível, M&A, mudança de gerência, mudança de prioridade) antes de fechar o plano fino — cada um pode reescrever cronograma ou orçamento.
3. Use a equação de LOE para transformar dados de descoberta em esforço em sprints por aplicação, mas nunca arredonde para baixo.
4. Teste o acoplamento real (não suposto) entre aplicações antes de decidir quais migram no mesmo sprint — banco de dados compartilhado geralmente é acoplamento alto; API REST bem definida geralmente é baixo.
5. Escolha metodologia de desenvolvimento (XP/Scrum/FDD) durante o planejamento da migração, não depois — isso define as ferramentas de pipeline que as primeiras aplicações migradas devem seguir.
6. As três ferramentas nativas (CloudEndure, DMS, DataSync) cobrem ~90% das necessidades; só busque terceiros para casos de borda explícitos (upgrade de SO durante a migração, replicação multi-região customizada).
7. Reserve os últimos 10% do plano para negociação humana direta com stakeholders de negócio — datas de fechamento contábil, lançamentos e férias não aparecem em nenhuma ferramenta de descoberta.
8. Se um workstream não conseguir acomodar as necessidades de uma unidade de negócio, as três opções são: migrar essa equipe antes da landing zone estar completa (arriscado), adicionar workstream (mais caro, mais flexível), ou estender o prazo (mais caro, às vezes impossível por restrição de data center).

## Connects To
- **Ch 3**: o mapeamento de dependências da descoberta é a matéria-prima direta de ~90% deste plano.
- **Ch 4**: a estimativa de duração da migração (Ch 4) é o ponto de partida revisado aqui com os fatores de bloqueio.
- **Ch 5**: a escolha de metodologia ágil de desenvolvimento conecta-se à discussão de agilidade organizacional (equipes pequenas, decisão única) do Ch 5.
- **Ch 6**: a landing zone deve estar em implantação paralela a este planejamento — um workstream antecipado "durante a criação da landing zone" é citado aqui como opção de contingência.
- **Ch 8**: a análise minuciosa por aplicação, os preparativos finais e a execução real dos sprints de migração continuam no capítulo final.
