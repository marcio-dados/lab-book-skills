# Glossário — Migrando para a AWS

**ALB (Application Load Balancer)** — balanceador de carga de Camada 7, roteia por URL/host, cobrado por hora + LCU (Ch 3).
**Aurora** — engine de banco de dados da AWS compatível com MySQL/PostgreSQL; permite réplicas de leitura horizontais e modo Serverless (Ch 8).
**AWS Artifact** — repositório de documentos de auditoria e conformidade (ISO, SOC, PCI) para entrega a auditores (Ch 5, Ch 6).
**AWS Control Tower** — serviço que automatiza a implantação da AWS Landing Zone (Ch 6).
**AWS-Nuke** — script de limpeza de recursos usado em contas sandbox (Ch 5).
**BC (Business Continuity)** — continuidade de negócios; mentalidade que substitui DR, focada em nunca parar em vez de recuperar depois de parar (Ch 1, Ch 6).
**Bronze/Prata/Ouro/Platina** — os quatro níveis de continuidade de negócios definidos pelo autor, do sem-HA (bronze) ao multi-região ativo/ativo (platina) (Ch 6).
**BYOL (Bring Your Own License)** — modelo de licenciamento em que o cliente traz sua própria licença; geralmente exige instância dedicada (Ch 3).
**Capex/Opex** — despesa de capital (compra de hardware) vs. despesa operacional (consumo pago pelo uso) (Ch 1).
**Chargeback/showback** — cobrar ou apenas exibir o custo de nuvem à unidade de negócio responsável (Ch 2, Ch 5).
**CloudEndure** — ferramenta de replicação de servidor no nível de blocos, gratuita, principal ferramenta de migração de servidor (Ch 3, Ch 4, Ch 7).
**CloudFront** — CDN da AWS; cache de conteúdo próximo ao usuário e primeira linha de defesa contra DDoS (Ch 1, Ch 8).
**CloudTrail** — logging de chamadas de API; deve ser retido por ≥90 dias (recomendado 1 ano) (Ch 2).
**CMDB (Configuration Management Database)** — banco de dados de gerenciamento de configuração; precisão típica ~70% (Ch 3).
**Config (AWS Config)** — serviço que registra o histórico de configuração do ambiente (Ch 2).
**Conta de logging** — conta AWS dedicada, somente leitura, que armazena CloudTrail/Config para investigação forense (Ch 6).
**Conta sandbox** — conta isolada para experimentação, com limpeza automática de recursos (Ch 1, Ch 5, Ch 6).
**DataSync** — serviço de transferência de arquivos on-premises → S3/EFS/FSx, com deduplicação e compactação (Ch 4, Ch 7, Ch 8).
**DMS (Database Migration Service)** — replicação assíncrona de banco de dados para migração ou troca de engine (Ch 4, Ch 7, Ch 8).
**DR (Disaster Recovery)** — recuperação de desastres; mentalidade anterior à BC, focada em restaurar depois de uma falha (Ch 1).
**EBS (Elastic Block Store)** — armazenamento em bloco da AWS; tipos gp2 (padrão), io1 (IOPS alto), st1/sc1 (magnético, throughput alto) (Ch 3).
**EFS (Elastic File System)** — substituto gerenciado para servidores NFS, redundante em 3 AZs nativamente (Ch 1, Ch 3).
**Federação/SSO** — login único via SAML (ADFS, Okta, Google) mapeado a grupos do diretório corporativo; método preferido de acesso administrativo (Ch 6).
**FSx** — serviço gerenciado de servidor de arquivos Windows/Lustre (Ch 3).
**GuardDuty** — scanner de ameaças baseado em IA sobre logs de VPC/DNS/CloudTrail (Ch 2).
**IAM (Identity and Access Management)** — controle de acesso granular (listar, ler, marcar, escrever) por serviço (Ch 1).
**KMS (Key Management Service)** — gerenciamento de chaves de criptografia; segmentar por conta/equipe/aplicação reduz raio de ação de comprometimento (Ch 6).
**Landing zone** — base de segurança, conformidade e estrutura de contas implantada antes de qualquer carga de trabalho (Ch 2, Ch 6).
**LCU (Load Balancer Capacity Unit)** — unidade de cobrança de ALB/NLB baseada em conexões, bytes e avaliações de regra (Ch 3).
**Lift-and-shift** — migrar a carga de trabalho como está, sem modificação (Ch 2, Ch 4).
**LOE (Level of Effort)** — nível de esforço, calculado por aplicação para o plano de migração (Ch 7).
**Menor privilégio (least privilege)** — conceder apenas o acesso mínimo necessário para a função (Ch 1, Ch 2).
**NAT Gateway** — gateway de tradução de endereço de rede, parte da infraestrutura de landing zone (Ch 6).
**NLB (Network Load Balancer)** — balanceador de carga de Camada 4, TCP/UDP/TLS, IP estático, sem Security Groups (Ch 3).
**PCI-DSS** — padrão de segurança de dados da indústria de cartões de pagamento; recomenda-se conta AWS separada para isolar CHD (Ch 6).
**QuickSight** — ferramenta de BI serverless da AWS, alternativa a Tableau/PowerBI (Ch 1, Ch 8).
**RACI** — matriz de Responsible/Accountable/Consulted/Informed, usada para clarear responsabilidade no modelo compartilhado (Ch 2).
**RDS (Relational Database Service)** — banco de dados relacional gerenciado (patching, backup, HA) (Ch 1, Ch 3).
**Redshift** — data warehouse colunar da AWS, alternativa a Oracle/SQL Server para analytics (Ch 8).
**Regiões / AZs (Availability Zones)** — unidades geográficas da infraestrutura AWS; a maioria das regiões tem ≥3 AZs (Ch 1).
**RI (Reserved Instance)** — instância reservada por 1–3 anos com desconto (40%/60%); o autor recomenda 10–20% sob demanda mesmo com RIs (Ch 4).
**Right-sizing (dimensionamento correto)** — ajustar tipo/tamanho de instância ao uso real medido, não ao alocado on-premises (Ch 3).
**Savings Plans** — alternativa às RIs, sem vínculo a região, ~10 p.p. menos desconto, mais flexível (Ch 4).
**Security Group** — firewall externo à instância na AWS, baseado em referência a grupo, não IP fixo (Ch 1).
**SES (Simple Email Service)** — serviço gerenciado para envio de email, substitui servidores de retransmissão (Ch 8).
**SSM (Systems Manager)** — gestão de estado e patching escalonado de instâncias (Ch 2, Ch 8).
**Sete R's (7 R's)** — Refactor, Redeploy, Rehost, Repurchase, Retire, Re-platform, Retain; classificação de toda aplicação antes de orçar migração (Ch 4).
**Shadow IT (TI invisível)** — recursos fora de controle/conhecimento formal da TI (Ch 2, Ch 5).
**SWAG (Scientific Wild-Ass Guess)** — estimativa aproximada aceitável nas fases iniciais de planejamento (Ch 3, Ch 4).
**TCO (Total Cost of Ownership)** — custo total de propriedade; ferramenta/estimativa da AWS para comparar on-premises vs. nuvem (Ch 1, Ch 4).
**VPC (Virtual Private Cloud)** — rede virtual privada segmentada por cliente na AWS (Ch 2).
**WAF (Web Application Firewall)** — firewall de Camada 7 serverless com regras gerenciadas contra XSS/SQLi (Ch 8).
**Zero trust (confiança zero)** — nenhum servidor confia em outro por padrão; limita o raio de ação de um invasor (Ch 1, Ch 2).
