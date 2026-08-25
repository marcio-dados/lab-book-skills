# Capítulo 6: Definindo sua landing zone e a governança na nuvem

## Core Idea
A landing zone (estrutura de contas, logging protegido, contas de suporte) e a governança na nuvem (suporte, gerenciamento de regiões/contas/root, acesso federado, KMS, continuidade de negócios em níveis) são a fundação que decide se a migração será estável — e devem ser implantadas em paralelo ao planejamento (Ch 7), nunca como reflexão tardia.

## Frameworks Introduced
- **Três modelos de estrutura de contas**: por unidade de negócio (facilita chargeback e M&A, mas segmenta pouco ambientes), por ambiente (segmenta dev/teste/produção bem, mas dificulta cisão/aquisição de unidades), e híbrido (combina os dois — recomendado acima de ~300 servidores, overhead de gestão não compensa abaixo disso).
  - Como escolher: regulamentação e necessidade de segmentação de ambiente → por ambiente ou híbrido; M&A frequente ou chargeback rígido por unidade → por unidade de negócio ou híbrido.
- **Contas mínimas recomendadas para qualquer landing zone**: conta principal (billing, sem VPC, hospeda Route 53), conta de serviços compartilhados (hub-and-spoke: AD, bastion hosts, ferramentas de segurança), conta de logging (somente leitura, CloudTrail/Config protegidos), conta sandbox (limpeza automática, isolada do hub-and-spoke), e opcionalmente conta PCI (isola CHD de Categoria 1 para reduzir escopo de auditoria).
- **Quatro maneiras de comprometer uma conta root**: exposição de chaves de acesso, funcionário mal-intencionado com a senha, força bruta, e a própria existência de chaves de acesso de root. Mitigação: criar conta de backup de administrador e nunca mais usar root, senha de 32–64 caracteres em um gerenciador de senhas, MFA físico (não só software), e nunca gerar chaves de acesso para a conta root.
- **BC em quatro níveis (bronze/prata/ouro/platina)**: framework de classificação de disponibilidade por aplicação, análogo a SLAs em camadas já usados on-premises.
  - Bronze: sem HA, restauração de snapshot em outra AZ (mais barato; aplicações legadas sem valor para refatorar).
  - Prata: HA multi-AZ (banco ativo/passivo, app ativo/ativo com load balancer) — passagem formal de DR para BC.
  - Ouro: sobrevive à falha de uma região inteira via replicação entre regiões (DMS para banco "quente", snapshots para servidor "frio") — nível em que a maioria das aplicações se enquadra.
  - Platina: multi-região ativo/ativo simultâneo com Route 53 geolocation/latency routing — reservado a aplicações realmente críticas; a camada de banco de dados é o fator limitante técnico.
  - Como usar: defina a política de qual nível cada classe de aplicação recebe **antes** da migração — nem toda aplicação merece ouro/platina; o custo de HA deve ser proporcional ao impacto real no negócio.

## Key Concepts
- **AWS Control Tower**: serviço que automatiza a implantação da AWS Landing Zone (produto) — recomendado para a maioria das empresas, exceto pequenas, onde o overhead de recursos padrão (ex.: NAT gateways redundantes em múltiplas AZs) pode não compensar o custo.
- **Faturamento consolidado / conta pagante principal (master payer account)**: ponto único de cobrança; múltiplas contas pagantes só se justificam para multinacionais com P&L separado por entidade legal — o custo é perder desconto por volume em serviços de escala gradual (S3, transferência) e complicar o EDP (Enterprise Discount Program, só disponível acima de US$ 1M/ano de gasto).
- **AWS Support Plans**: do gratuito ao Enterprise (>US$ 15k/mês, inclui TAM — Technical Account Manager); custo não é linear e é cobrado por conta nos níveis abaixo de Enterprise — acima de ~100 contas, o nível Business pode custar tanto quanto o Enterprise sem os benefícios.
- **Gerenciamento de regiões**: regiões lançadas antes de 2019 vêm habilitadas por padrão (risco de shadow IT em região "obscura"); regiões após 2019 vêm desabilitadas — política de expansão deve ter gatilhos explícitos (nova exigência de BC, expansão geográfica, soberania de dados, latência).
- **Federação/SSO vs. usuários IAM**: acesso administrativo deve sempre passar por federação (SAML via ADFS, Okta, Google SSO) mapeada a grupos existentes no diretório corporativo; usuários IAM ficam reservados a contas de serviço de ferramentas terceiras e à conta de backup de root — nunca para humanos no dia a dia.
- **AWS KMS**: segmentar chaves de criptografia por conta, unidade de negócio, equipe ou aplicação (não usar só a chave padrão) reduz o raio de ação de um comprometimento — trade-off é mais chaves = mais gestão de acesso a gerenciar.

## Mental Models
- **Landing zone como aeroporto**: contas = pistas onde as cargas de trabalho "pousam"; logging = área de taxiamento; segurança/conformidade = torre de controle. Falta de qualquer peça = caos total, do mesmo jeito que em um aeroporto real.
- **Fundação de uma casa**: a landing zone não é vistosa nem interessante, mas nenhum inspetor aceitaria pular a fundação — o mesmo raciocínio vale para não tratar a landing zone superficialmente.
- **"Se você não pode confiar em seus funcionários, em quem poderá confiar?"**: o autor usa essa tensão para justificar por que, mesmo assim, é preciso segmentar chaves KMS e escopos de acesso — a exceção (o funcionário mal-intencionado ou a conta comprometida) é o que se está mitigando, não a regra.

## Anti-patterns
- **Usar a conta root no dia a dia**: os três cenários do capítulo (Tonya, Betty, Maria) mostram formas distintas de comprometimento — todas evitáveis com MFA físico, backup de admin, e zero chaves de acesso de root.
- **Deixar todas as regiões pré-2019 habilitadas sem necessidade de negócio**: aumenta a superfície de shadow IT / vazamento de dados em regiões que ninguém monitora.
- **Implantar landing zone manualmente, sem IaC**: torna a conformidade e a adição de novas contas extremamente difícil de manter — o autor recomenda sempre partir de um template IaC existente (Control Tower ou pacotes de referência no GitHub).
- **Criar chaves de acesso para a conta root** (Cenário 6.2 — Betty): chaves de acesso de root vazadas em um commit público (padrão comum em ataques que vasculham GitHub) expõem toda a infraestrutura.
- **Reter acesso root de um funcionário desligado** (Cenário 6.3 — Maria): sem federação centralizada e sem MFA obrigatório, a saída de um funcionário pode virar sequestro total da conta.
- **Aplicar o mesmo nível de BC (ex.: ouro/platina) a toda aplicação indiscriminadamente**: gera custo de disponibilidade desnecessário para aplicações sem impacto de negócio proporcional — a classificação em níveis existe exatamente para evitar isso.
- **Múltiplas contas pagantes principais sem necessidade multinacional real**: perde desconto por volume e multiplica o esforço legal/financeiro de gerenciar EDPs separados.

## Worked Example
**Cenário 6.1 — o ataque de ransomware que a MFA teria impedido (Tonya).** Um ataque de DDoS foi acompanhado de uma mensagem de resgate de US$ 200 mil em uma tag de instância EC2. A empresa apenas trocou a senha de root (que não tinha MFA e era usada no cotidiano) e recusou pagar o resgate — mas não fez nenhuma análise forense. Horas depois, o invasor, que provavelmente ainda tinha acesso via uma porta dos fundos não detectada (ex.: um usuário IAM criado por ele), destruiu toda a infraestrutura da empresa na AWS, levando-a à falência. A cadeia de falhas: (1) sem MFA físico na conta root, vulnerável a força bruta; (2) conta root usada operacionalmente em vez de reservada para emergência; (3) nenhuma investigação forense antes de declarar o incidente "resolvido". Qualquer um dos três controles do capítulo — MFA físico, backup de admin com root nunca usado, e conta de logging protegida para permitir forense — teria evitado o desastre.

## Key Takeaways
1. Escolha a estrutura de contas (unidade de negócio / ambiente / híbrida) pelo cruzamento de necessidade de segmentação regulatória e frequência de M&A — não por padrão de mercado.
2. Toda landing zone precisa, no mínimo, de conta principal, serviços compartilhados, logging protegido, e (fortemente recomendada) uma sandbox com limpeza automática.
3. Proteja toda conta root com MFA físico, sem chaves de acesso, com conta de backup de administrador criada primeiro — e trate os três cenários do capítulo como checklist mínimo de segurança de conta.
4. Centralize acesso administrativo via federação/SSO; reserve usuários IAM só para contas de serviço de terceiros.
5. Escolha o nível de suporte AWS (Developer/Business/Enterprise) pelo custo de ficar sem suporte no pior cenário, não pelo custo mensal isolado.
6. Classifique cada aplicação em um dos quatro níveis de BC (bronze/prata/ouro/platina) por impacto real no negócio — não aplique disponibilidade máxima por padrão.
7. Implante a landing zone e a governança **em paralelo** ao planejamento da migração (Ch 7) — isso economiza um a dois meses de cronograma, mas adie o deploy se houver um intervalo grande entre planejamento e início real (para não gerar custo de infraestrutura ociosa).

## Connects To
- **Ch 2**: landing zone, RACI de responsabilidade compartilhada e menor privilégio retornam aqui como implementação concreta.
- **Ch 1**: DR → BC (aqui formalizado nos quatro níveis bronze/prata/ouro/platina) foi introduzido como mudança de mentalidade no primeiro capítulo.
- **Ch 5**: a "fundação" da pirâmide operacional (patrocinador executivo) e a base de segurança/conformidade são o pré-requisito organizacional para a landing zone técnica deste capítulo.
- **Ch 7**: o planejamento da migração, incluindo os 7 R's e fatores de bloqueio tecnológico, é executado em paralelo a este capítulo.
