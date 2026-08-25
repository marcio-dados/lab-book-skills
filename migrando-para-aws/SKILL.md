---
name: migrando-para-aws
description: "Knowledge base from \"Migrando para a AWS: Um Guia para Gerentes\" by Jeff Armstrong (Novatec / O'Reilly). Use when applying Armstrong's frameworks for planejamento de migração para AWS, caso de negócio, landing zone e governança, descoberta de cargas de trabalho, gestão de risco, ou referenciando os conceitos do livro."
origem: publico-terceiro
classificacao: nao-corporativo
tipo: livro-tecnico
idioma: pt-BR
titulo_pt: "Migrando para a AWS"
proveniencia:
  titulo: "Migrando para a AWS: Um Guia para Gerentes"
  autor: ["Jeff Armstrong"]
  editora: "Novatec"
  fonte_sha256: "46c97df6d36002190e983f14b028f087f9e0be19a216e6314c633aa2bbf983bf"
  convertido_em: "2026-08-25"
  ferramenta_sha: "7bcfcd5262329f8d57a385903f18a98bc6705e4e"
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Migrando para a AWS: Um Guia para Gerentes
**Autor**: Jeff Armstrong | **Páginas**: ~114.034 palavras (edição traduzida, Novatec) | **Capítulos**: 8 | **Gerado em**: 2026-08-25

## Como usar esta skill

- **Sem argumento** — carregue os frameworks centrais abaixo como referência.
- **Com um tópico** — pergunte sobre `landing zone`, `caso de negócio`, `7 R's`, ou outro tópico do índice; eu encontro e leio o capítulo relevante.
- **Com capítulo** — peça `ch06`; eu carrego esse arquivo específico.
- **Navegar** — pergunte "quais capítulos você tem?" para ver o índice completo.

Ao perguntar sobre um tópico não coberto nos Frameworks Centrais abaixo, eu vou ler o capítulo correspondente antes de responder. Para tabelas de decisão prontas (thresholds, trade-offs, árvores de decisão), veja [cheatsheet.md](cheatsheet.md) primeiro — é o atalho mais rápido antes de abrir um capítulo inteiro.

---

## Frameworks Centrais & Modelos Mentais

**O fio condutor do livro**: antes do "como" migrar vem o "porquê" (Ch1); antes de qualquer carga de trabalho ir para produção vem a landing zone (Ch2, Ch6); e a precisão exigida evolui de aproximação ("lançar um foguete para o espaço") para exatidão ("pousar na Lua") só na análise minuciosa por aplicação (Ch8) — nunca antes.

**FAQ do porquê (Ch1)**: transforme os motivos da migração em perguntas e respostas antecipadas, por público-alvo (alta gerência, dev, unidade de negócio). Reformule perguntas tendenciosas em termos neutros; responda com dados da própria empresa, nunca com material de marketing da AWS.

**Escalabilidade horizontal por padrão (Ch1)**: comece sempre horizontal (Auto Scaling + ELB); use vertical só com justificativa técnica explícita (COTS, pico previsível). Exige servidores stateless.

**DR → BC, formalizado em 4 níveis (Ch1, Ch6)**: mude de "recuperar depois de cair" para "nunca parar". Classifique cada aplicação em bronze (snapshot em outra AZ) / prata (multi-AZ HA) / ouro (multi-região com DMS + snapshot — a maioria das apps) / platina (multi-região ativo/ativo — só apps críticas). Custo cresce fortemente do bronze ao platina; nunca aplique um nível por padrão.

**Zero trust + menor privilégio (Ch1, Ch2)**: nenhum servidor confia em outro por padrão (Security Groups, nunca IP fixo); conceda apenas o acesso mínimo necessário via IAM. Firewall/IDS tradicional baseado em zona é *stateful* e não escala horizontalmente — é o anti-padrão a evitar.

**Princípios norteadores (Ch2)**: crie uma regra-padrão só para decisões que se repetem com contexto variável (ex.: "sempre 3+ AZs"). Decisões de projeto único (a landing zone em si) não geram princípio — faça certo já na primeira vez.

**"Lançar um foguete" vs. "pousar na Lua" (Ch3, Ch4, Ch7, Ch8)**: aceite SWAG (estimativa aproximada) na descoberta e no caso de negócio; só exija precisão fina na análise minuciosa por aplicação, no fim do planejamento. Não gaste esforço de engenharia detalhando o que ainda vai mudar.

**Right-sizing (Ch3)**: dimensione pelo uso real medido, não pelo hardware alocado on-premises — a AWS não compartilha CPU/memória/disco entre clientes como um hipervisor local (superalocação de 50–90% é comum).

**Equação de duração da migração (Ch4)**: `duração = servidores / (taxa_por_engenheiro × engenheiros_ajustados_por_férias) × (1 + buffer 10–20%)`. Subestime sua própria velocidade ("seja como o Scotty").

**Sete R's (Ch4)**: Refactor, Redeploy, Rehost, Repurchase, Retire, Re-platform, Retain — classifique toda aplicação antes de orçar; só Rehost+Re-platform+Redeploy+Refactor entram no orçamento AWS.

**Construção da pirâmide operacional (Ch5)**: disseminação de mudança de processo em 4 camadas sequenciais — fundação (patrocinador C-level) → base (prototipe dentro da própria TI) → expansão (um departamento aliado) → topo (o resto da empresa, só com história de sucesso comprovada). Não pule etapas.

**Três inimigos da agilidade (Ch5)**: equipes grandes demais, decisão sem responsável único, processo pelo processo. Atacar os três é rápido e não exige reestruturação de anos.

**Estrutura de contas e landing zone (Ch6)**: escolha entre modelo por unidade de negócio, por ambiente, ou híbrido (compensa acima de ~300 servidores) pelo cruzamento de regulamentação e frequência de M&A. Toda landing zone precisa, no mínimo, de conta principal, serviços compartilhados, logging protegido (somente leitura) e sandbox com limpeza automática — implantada *antes* de qualquer carga de trabalho de produção.

**Cascata-ágil híbrida + fatores de bloqueio (Ch7)**: identifique blocos com ordem obrigatória (AD, storage compartilhado, bancos fortemente acoplados) e deixe o resto fluido em sprints de ~2 semanas. Rode o checklist de bloqueadores técnicos (SO sem suporte, hardware incompatível) e de negócio (M&A, mudança de prioridade) antes de fechar o plano fino — trate o cronograma como fluido, nunca imutável.

**Teste de alto acoplamento (Ch7)**: duas aplicações que trocam muito acesso direto a banco/dados internos migram juntas; comunicação via API REST bem definida permite migrar separado. Acoplamento é função do volume real de interação, não da topologia do diagrama.

**Refatoração pela regra 80/20 (Ch8)**: refatore só o que combina alto impacto de negócio com baixo esforço mensurável (SCT ≥95% de conversão automática de esquema). Nunca refatore on-premises antes de migrar; nunca deixe a refatoração ficar contínua/sem prazo.

Para decisões operacionais, thresholds numéricos e tabelas de trade-off completas, vá direto ao [cheatsheet.md](cheatsheet.md).

---

## Índice de Capítulos

| # | Título | Frameworks-chave |
|---|-------|----------------|
| [ch01](chapters/ch01-por-que-migrar.md) | Por que devo migrar para a AWS? | FAQ do porquê, escalabilidade horizontal vs. vertical, DR→BC, zero trust + menor privilégio |
| [ch02](chapters/ch02-riscos-e-mitigacao.md) | Quais são os riscos e como atenuá-los | Princípios norteadores, 4 pilares de segurança, RACI por classe de aplicação, chargeback/showback |
| [ch03](chapters/ch03-descoberta.md) | Descobrindo suas cargas de trabalho | Foguete vs. Lua (SWAG), checklist de ferramenta de descoberta, árvore de decisão de conectividade, right-sizing |
| [ch04](chapters/ch04-caso-de-negocio.md) | Criando seu caso de negócio | Equação de duração, 7 R's, estrutura do caso de negócio, RI vs. Savings Plans |
| [ch05](chapters/ch05-preparo-operacional.md) | Preparando-se para as tarefas operacionais na AWS | Construção da pirâmide, segurança como revisor, 3 inimigos da agilidade, controles financeiros |
| [ch06](chapters/ch06-landing-zone-governanca.md) | Definindo sua landing zone e a governança na nuvem | 3 modelos de estrutura de contas, contas mínimas da landing zone, BC em 4 níveis, KMS |
| [ch07](chapters/ch07-planejando-migracao.md) | Planejando sua migração | Cascata-ágil, fatores de bloqueio, LOE, teste de alto acoplamento, notinhas adesivas |
| [ch08](chapters/ch08-refatoracao-preparativos-finais.md) | Refatoração, novas ferramentas e preparativos finais | Regra 80/20, reequipagem (WAF/SSM/CloudFront), análise minuciosa por aplicação |

## Índice de Tópicos

- **7 R's (classificação de aplicação)** → ch04
- **Acoplamento entre aplicações** → ch07
- **Agilidade (3 inimigos)** → ch05
- **ALB / NLB / ELB** → ch03
- **Aurora / RDS / Redshift** → ch08
- **BYOL vs. licença incluída** → ch03
- **Caso de negócio (estrutura)** → ch04
- **Chargeback / showback** → ch02, ch05
- **CloudEndure / DMS / DataSync** → ch07
- **Conectividade (VPN / Direct Connect / internet)** → ch02, ch03
- **Conta root (segurança)** → ch06
- **DR → BC / níveis bronze-prata-ouro-platina** → ch01, ch06
- **Escalabilidade horizontal vs. vertical** → ch01
- **Estrutura de contas (unidade de negócio / ambiente / híbrida)** → ch06
- **FAQ do porquê** → ch01, ch04
- **Fatores de bloqueio (tecnológicos e de negócio)** → ch07
- **Federação / SSO** → ch06
- **KMS (chaves de criptografia)** → ch06
- **Landing zone** → ch02, ch06
- **LOE (nível de esforço)** → ch07
- **Pirâmide operacional (disseminação de mudança)** → ch05
- **Princípios norteadores** → ch02
- **RACI (responsabilidade compartilhada)** → ch02
- **Refatoração (regra 80/20)** → ch08
- **Reequipagem (WAF, SSM, CloudFront)** → ch08
- **Right-sizing** → ch03
- **RI vs. Savings Plans** → ch04
- **Sprints / cascata-ágil** → ch07
- **SWAG / "foguete vs. Lua"** → ch03, ch04, ch07, ch08
- **Tagging obrigatório** → ch02, ch05
- **Zero trust / menor privilégio** → ch01, ch02

## Arquivos de Apoio

- [glossary.md](glossary.md) — todos os termos-chave com definições
- [patterns.md](patterns.md) — todas as técnicas e padrões de projeto
- [cheatsheet.md](cheatsheet.md) — tabelas de referência rápida e guias de decisão

---

## Alcance & Limites

Esta skill cobre apenas o conteúdo do livro. Para implementação prática no seu ambiente AWS,
combine com ferramentas específicas do projeto (Terraform, Control Tower, AWS CLI). Para tópicos
além deste livro, consulte outras skills relacionadas ou pergunte diretamente ao agente.
