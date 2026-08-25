# Patterns — Migrando para a AWS

## FAQ do Porquê
**When to use**: antes de qualquer comunicação formal sobre a migração, para reduzir resistência.
**How**: escolha o público-alvo (alta gerência, dev, unidade de negócio) → antecipe as perguntas/objeções que farão → reformule perguntas tendenciosas em termos neutros → responda com dados concretos da própria empresa → itere por equipe até as perguntas novas se esgotarem.
**Trade-offs**: consome tempo de análise antecipada, mas reduz retrabalho de convencimento repetido depois.

## Escalabilidade horizontal por padrão
**When to use**: qualquer nova carga de trabalho web/stateless.
**How**: comece sempre pela escalabilidade horizontal (Auto Scaling + ELB); só recorra à vertical se houver motivo técnico explícito (COTS não desenhado para escalar, pico previsível e temporário).
**Trade-offs**: exige aplicação stateless; software legado licenciado por CPU pode não se beneficiar.

## DR → BC em níveis (bronze/prata/ouro/platina)
**When to use**: ao classificar qualquer aplicação para disponibilidade na migração.
**How**: bronze = snapshot + restauração em outra AZ; prata = multi-AZ HA (ativo/passivo banco, ativo/ativo app); ouro = multi-região com DMS (dados "quentes") + snapshots (servidores "frios"); platina = multi-região ativo/ativo simultâneo.
**Trade-offs**: custo cresce fortemente do bronze ao platina; nem toda aplicação justifica ouro/platina — combine com impacto de negócio real, não aplique por padrão.

## Landing zone antes de qualquer carga de trabalho
**When to use**: sempre, antes da primeira migração de produção.
**How**: implante conta principal (sem VPC) + serviços compartilhados (hub-and-spoke) + logging protegido (somente leitura) + sandbox (limpeza automática) via IaC (Control Tower para a maioria dos casos).
**Trade-offs**: adia o início da migração em semanas, mas corrigir depois custa ordens de magnitude mais (ver Cenário 2.1 do Ch 2).

## Equação de duração da migração
**When to use**: no caso de negócio, antes de comprometer prazo com a gerência.
**How**: `duração = servidores / (taxa_por_engenheiro × engenheiros_ajustados_por_férias) × (1 + buffer 10–20%)`.
**Trade-offs**: é uma aproximação ("lançamento ao espaço"), não uma previsão fina — refine só na análise minuciosa por aplicação (Ch 8).

## Classificação pelos 7 R's antes de orçar
**When to use**: para toda aplicação identificada na descoberta, antes de modelar custo de execução.
**How**: classifique em Refactor / Redeploy / Rehost / Repurchase / Retire / Re-platform / Retain; some no orçamento AWS só Rehost + Re-platform + Redeploy + Refactor.
**Trade-offs**: exige análise manual por aplicação — nenhuma ferramenta de descoberta faz essa classificação automaticamente.

## Acréscimo percentual para custo não determinístico
**When to use**: banda de saída, serviços auxiliares serverless, LCU de ALB/NLB.
**How**: banda de saída +8–10% sobre gasto EC2; serviços auxiliares (Config/CloudWatch/SNS) +5% sobre EC2; ALB/NLB: multiplique custo básico por 4 para cobrir LCU.
**Trade-offs**: menos preciso que uma POC real, mas evita gastar semanas de engenharia em precisão que não muda a decisão.

## Construção da pirâmide operacional
**When to use**: para disseminar mudança de processo (segurança, change management, agilidade) por toda a empresa.
**How**: (1) fundação = patrocinador executivo C-level; (2) base = prototipe na própria TI; (3) expansão = leve para um departamento aliado; (4) topo = venda para o resto, com história de sucesso comprovada.
**Trade-offs**: processo sequencial e lento — pular etapas (ex.: ir direto ao topo) tende a gerar desconfiança e rejeição.

## Segurança como revisor via gate de pipeline
**When to use**: ao migrar para IaC e deploy automatizado.
**How**: equipe de segurança revisa o diff do IaC no repositório antes do deploy (gate no pipeline), não a aplicação inteira a cada commit.
**Trade-offs**: exige repositório de código como fonte única de verdade e pipeline maduro; sem isso, o gate não tem onde se apoiar.

## Teste de alto acoplamento entre aplicações
**When to use**: ao decidir quais aplicações devem migrar no mesmo sprint.
**How**: se a aplicação A acessa diretamente o banco de dados/dados internos da aplicação B (muitos acessos de ida e volta) → alto acoplamento, migre junto; se a comunicação é via API REST bem definida → baixo acoplamento, pode migrar separado.
**Trade-offs**: acoplamento via banco compartilhado com alto volume de transações também conta como alto, mesmo sem dependência "visível" na topologia.

## Refatoração pela regra 80/20
**When to use**: ao decidir o que refatorar durante (não antes) da migração.
**How**: selecione aplicações com código acessível, linguagem moderna (Java, .NET Core), em desenvolvimento ativo; selecione serviços de alto impacto real (troca de engine, S3, Redshift, site estático, SES); valide esforço com ferramentas como o SCT (≥95% de conversão automática = sinal verde).
**Trade-offs**: refatoração contínua (perseguir todo novo serviço da AWS) estende o cronograma indefinidamente — feche o design e siga.

## Reequipagem com novas ferramentas (WAF + SSM + CloudFront)
**When to use**: aplicações web, por padrão, exceto onde já existe ferramenta equivalente on-premises.
**How**: adicione WAF (proteção camada 7, baixo custo) + Systems Manager (patching escalonado dev→teste→produção) + CloudFront (CDN + primeira defesa contra DDoS), sem alterar código da aplicação.
**Trade-offs**: se já há Chef/Puppet/Ansible implantado, adotar o SSM é refatoração, não reequipagem — trate como tal (avalie separadamente).

## Tagging obrigatório + Cost Explorer + chargeback/showback
**When to use**: antes da migração começar em volume.
**How**: defina esquema de tags (departamento, centro de custo, ambiente, responsável) → torne obrigatório via AWS Config Rules → ative tags no Cost Explorer → implemente chargeback ou showback por unidade de negócio.
**Trade-offs**: chargeback total é mais trabalho para o financeiro; showback é mais simples mas depende de disciplina voluntária das equipes.
