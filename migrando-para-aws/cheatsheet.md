# Cheatsheet — Migrando para a AWS

Referência rápida das decisões que o autor tomaria. Para o "porquê" completo, leia o capítulo indicado.

## Decision Rules

- **Escalabilidade**: comece sempre horizontal (Auto Scaling + ELB); só use vertical se houver motivo técnico explícito — COTS não desenhado para escalar horizontalmente, ou pico previsível e temporário. (Ch1)
- **AZs de produção**: nunca implante em só 2 AZs; use no mínimo 3 — 2 AZs falha silenciosamente se uma cair por desastre regional. (Ch1)
- **Firewall**: referencie sempre Security Group, nunca IP fixo — IPs são reciclados e herdam acesso indevido do dono anterior. (Ch1)
- **Princípio norteador**: crie um princípio só para decisões que se repetem com contexto mutável (variáveis); decisões de projeto único (ex.: a landing zone) não geram princípio — faça certo já na primeira vez. (Ch2)
- **Consultoria externa**: contrate por gatilho objetivo pré-definido (ex.: "treinamento atrasa uma app por >2 semanas"), nunca por decisão ad hoc. (Ch2)
- **Conectividade**: decida pela necessidade do negócio (internet-acessível? protocolo criptografável? latência? banda? contas múltiplas?), nunca pelo menor custo — otimizar por preço degrada a experiência do usuário. (Ch2, Ch3)
- **Dimensionamento de disco**: erre para menos — EBS cresce depois sem problema, mas não reduz. (Ch3)
- **Geração de instância**: prefira sempre a mais nova da família equivalente (ex. T3 sobre T2) — preço nominal menor de gerações antigas custa mais por unidade de desempenho. (Ch3)
- **BYOL vs. licença incluída**: comece assumindo que descartar a licença legada compensa (~90% dos casos do autor); só mantenha BYOL com justificativa de custo real. (Ch3)
- **7 R's antes de orçar**: nunca inclua no orçamento AWS uma aplicação classificada como Retire ou Retain. (Ch4)
- **Cronograma**: sempre aplique buffer (10% equipe experiente + muito COTS, 20% equipe nova + muito software interno) e desconte férias/feriados explicitamente. (Ch4)
- **RI de 3 anos**: nunca comprometa 100% da capacidade — deixe 10–20% sob demanda mesmo com RIs de 1 ano. (Ch4)
- **Burn-down**: não modele em detalhe — o esforço de calcular supera o valor agregado à decisão. (Ch4)
- **Patrocinador de mudança organizacional**: precisa ser C-level; gerência de TI não atravessa silos de negócio. (Ch5)
- **Segurança em pipeline**: revise só o diff do IaC a cada commit, não a aplicação inteira a cada vez. (Ch5)
- **Refatoração**: nunca refatore on-premises antes de migrar ("comprar comida para um cavalo morto"); nunca deixe a refatoração ficar contínua/sem prazo. (Ch8)
- **SCT abaixo de ~95%** de conversão automática de esquema → adie a refatoração para depois da migração. (Ch8)
- **SSM/WAF/CloudFront**: adote por padrão em toda app web; se já existe Chef/Puppet/Ansible, tratar SSM como refatoração (avaliar separado), não como reequipagem grátis. (Ch8)

## Árvore de decisão — Conectividade (Ch2, Ch3)

1. App acessível pela internet, protocolo criptografável, autenticação forte, baixa sensibilidade a latência, baixo/médio volume → **Internet + bastion host**
2. Precisa de banda dedicada, alta previsibilidade, múltiplas contas/resiliência → **Direct Connect**
3. Volume baixo/médio, tolera variação de latência da internet, quer criptografia simples → **VPN**
- Nunca decidir por custo isolado — o critério de entrada é a necessidade, o custo é consequência.

## Árvore de decisão — Nível de BC por aplicação (Ch6)

| Nível | Quando | Mecanismo |
|---|---|---|
| Bronze | Legado sem valor de negócio para refatorar | Snapshot + restauração em outra AZ |
| Prata | Passagem formal DR→BC | Multi-AZ HA (banco ativo/passivo, app ativo/ativo) |
| Ouro | Maioria das aplicações | Multi-região: DMS (dados "quentes") + snapshot (servidores "frios") |
| Platina | Só aplicações realmente críticas | Multi-região ativo/ativo simultâneo, Route 53 geo/latency routing |

Custo cresce fortemente do bronze ao platina — case por impacto real no negócio, nunca por padrão.

## Trade-off matrices

**RI vs. Savings Plans (Ch4)**
| | RI | Savings Plans |
|---|---|---|
| Trava | Tipo de instância + SO, 1–3 anos | Só volume de computação por família |
| Desconto | 40% (1a) / 60% (3a) | ~10 p.p. menor |
| Flexibilidade | Baixa (região fixa) | Alta (sem região fixa) |
| Melhor para | Empresa pequena, uso previsível | Empresa média |

**Estrutura de contas (Ch6)**
| Modelo | Prós | Contras |
|---|---|---|
| Por unidade de negócio | Facilita chargeback, M&A | Segmenta pouco ambiente (dev/prod) |
| Por ambiente | Segmenta dev/teste/prod bem | Dificulta cisão/aquisição |
| Híbrido | Combina os dois | Overhead só compensa acima de ~300 servidores |

**Balanceadores (Ch3)**: ELB clássico (L4, legado, evitar) · ALB (L7, roteia por URL/host, até 100 destinos, cobrado por LCU) · NLB (L4, TCP/UDP/TLS, IP estático, sem Security Groups).

**EBS (Ch3)**: gp2 cobre ~95% dos casos · io1 para IOPS alto com pouco espaço · st1/sc1 (magnético, mín. 500GB) só para throughput sequencial alto.

## Thresholds & defaults

| Item | Valor |
|---|---|
| AZs mínimas em produção | 3 |
| CloudTrail — retenção mínima / recomendada | 90 dias / 1 ano |
| Durabilidade S3 | 11 noves (99,999999999%) |
| Buffer de cronograma | 10% (equipe experiente) a 20% (equipe nova) |
| Acréscimo de banda de saída sobre EC2 | +8–10% |
| Acréscimo de serviços auxiliares (Config/CloudWatch/SNS) | +5% sobre EC2 |
| Multiplicador de custo básico de ALB/NLB para cobrir LCU | ×4 |
| Capacidade reservada máxima recomendada | 80–90% (deixe 10–20% sob demanda) |
| Economia por desligar dev/teste fora do horário | ~70% |
| Precisão típica de CMDB | ~70% |
| Estrutura de contas híbrida compensa a partir de | ~300 servidores |
| Limite de conversão automática de esquema (SCT) para seguir com refatoração | ≥95% |
| Distribuição típica dos 7 R's | Rehost ~80%, Re-platform ~20%, Refactor ≤5%, Repurchase ~5%, Retire <5%, Retain <5% |
| Multa por título de software não conforme (auditoria de licença) | até US$150 mil |
| SES gratuito até | 62.000 mensagens/mês |
| Sprint de migração recomendado | ~2 semanas |
| Patching escalonado via SSM | dev imediato → teste +7 dias → produção +14 dias |
| Nível de suporte AWS Enterprise | a partir de ~US$15k/mês |

## Tells & smells

- Ninguém sabe quem desligou o servidor / não há CloudTrail → **landing zone ausente**, pare novas migrações até corrigir.
- Chave de acesso de conta root existe → **vetor de comprometimento aberto**; remova e crie conta de backup de admin.
- "Ajusto as permissões em uma ou duas semanas" → vira permanente; trate como risco de segurança agora.
- Mudança simples de firewall leva 45 dias → gargalo é o **processo de negócio**, não a tecnologia (Ch5).
- Alguém propõe caso de negócio de refatoração sem lista de riscos → sinal de análise incompleta, devolva.
- Duas aplicações "independentes" escrevem no mesmo banco com alto volume → **alto acoplamento real**, migrar junto mesmo sem dependência visível no diagrama.
- ~2/3 da infraestrutura nunca é desligada sem tagging + sandbox com limpeza automática → controle financeiro ausente.
