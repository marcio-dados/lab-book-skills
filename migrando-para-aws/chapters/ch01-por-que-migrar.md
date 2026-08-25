# Capítulo 1: Por que devo migrar para a Amazon Web Services?

## Core Idea
Antes de discutir "como" migrar, o gerente precisa de um "porquê" sólido — uma narrativa que combine vantagens tecnológicas (escalabilidade, disponibilidade, segurança) e vantagens de negócio (custo, agilidade, continuidade) para vencer a relutância natural das pessoas à mudança.

## Frameworks Introduced
- **FAQ do porquê**: transformar os motivos da migração em uma lista de perguntas e respostas antecipadas, por público-alvo (alta gerência, equipe de desenvolvimento, unidade de negócio).
  - Quando usar: antes de qualquer comunicação formal da migração, para reduzir resistência e ganhar "adeptos".
  - Como: (1) escolher o público-alvo; (2) colocar-se no lugar dele e antecipar perguntas/objeções; (3) reformular perguntas tendenciosas em termos neutros (ex.: trocar "quanto a AWS vai custar mais?" por "como os custos vão mudar?"); (4) responder com dados concretos da própria empresa, não com material de marketing da AWS; (5) iterar por equipe/departamento até as perguntas novas se esgotarem.
- **Escalabilidade vertical vs. horizontal**: dois modos de adicionar capacidade.
  - Quando usar vertical: cargas com software COTS que não foi desenhado para escalar horizontalmente (ex.: sistema de contabilidade), ou picos temporários e previsíveis (agendar escalabilidade vertical antes/depois do processamento em lote).
  - Quando usar horizontal: regra geral — "comece sempre escalando horizontalmente e trabalhe de trás para frente até achar o motivo técnico pelo qual isso não funciona; só então recorra à vertical". Exige servidores *stateless*.
- **DR → BC (Disaster Recovery → Business Continuity)**: mudança de mentalidade de "recuperar depois de cair" para "nunca parar".
  - Como: usar múltiplas AZs (mínimo três) com configuração ativa/ativa (todos os servidores atendem tráfego) ou ativa/passiva (um assume em caso de falha) para levar RTO/RPO a perto de zero; decidir separadamente se a proteção precisa ser **entre regiões** (DR entre regiões é mais barato, RTO/RPO maiores; BC entre regiões custa mais, RTO/RPO menores).
- **Confiança zero (zero trust) + menor privilégio (least privilege)**: as duas práticas de segurança que a AWS torna simples de implementar via Security Groups e IAM.
  - Confiança zero: nenhum servidor confia em outro por padrão — isso limita o raio de ação de um invasor que comprometa um único host.
  - Menor privilégio: conceder só o acesso mínimo (listar, ler, marcar, escrever) necessário para a função, via IAM.

## Key Concepts
- **Instância**: nomenclatura da AWS para servidor/máquina virtual no EC2.
- **Região**: conjunto de zonas de disponibilidade em uma área geográfica.
- **Zona de disponibilidade (AZ)**: agrupamento de data centers geograficamente separados dentro de uma região, com energia e conectividade independentes; a maioria das regiões tem três.
- **Elastic Load Balancing / AWS Auto Scaling**: serviços serverless que viabilizam a escalabilidade horizontal sem custo fixo de balanceador.
- **11 noves de durabilidade**: garantia do S3 sobre a persistência do arquivo (99,999999999%) — não é o mesmo que disponibilidade.
- **AWS Security Groups**: firewall externo à instância, baseado em referências a grupos (não IPs fixos), ajustando-se automaticamente quando instâncias entram/saem.
- **IAM (Identity and Access Management)**: controle de acesso granular por serviço (listar, ler, marcar, escrever).
- **RPO / RTO**: Objetivo de Ponto de Recuperação (quanto dado pode se perder) e Objetivo de Tempo de Recuperação (quanto tempo até voltar a operar).
- **TCO (Total Cost of Ownership)**: ferramenta/estimativa da AWS para comparar custo total on-premises vs. nuvem; usar com ceticismo (é material da própria AWS) ou complementar com o AWS Pricing Calculator.
- **Vendor lock-in real**: só existe quando se depende de serviços proprietários de um único fornecedor — não pelo simples fato de rodar na nuvem.
- **Capex → Opex**: migração troca despesa de capital fixa (hardware depreciado) por despesa operacional variável ligada ao consumo.

## Mental Models
- **A doca flutuante vs. a doca fixa**: infraestrutura on-premises é uma doca de altura fixa (superdimensionada ou subdimensionada); a AWS é uma doca flutuante que acompanha a maré do consumo real — você paga só pelo nível mínimo e escala conforme o uso.
- **Custos tangíveis vs. intangíveis**: separe sempre os dois grupos ao montar o caso de negócio. Tangíveis (hardware, energia, licenças) são fáceis de medir; intangíveis (tempo de patching, backup, negociação de contratos) são o "parasita" do orçamento de TI e costumam ser subestimados.
- **Falhar rápido custa caro on-premises, é barato na nuvem**: sem compromisso de hardware, testar e descartar uma ideia custa "quantias insignificantes" repetidas vezes, em vez de imobilizar capital em equipamento parado.
- **Agilidade de negócios é o combinado de ferramentas + processos humanos**: automação (CI/CD, pipelines) sem mudança de processo/mentalidade das equipes não entrega agilidade.

## Anti-patterns
- **Duas AZs "bastam"**: implantar em só duas zonas de disponibilidade parece suficiente, mas se uma cair por desastre natural ela pode ficar fora do ar por muito tempo — a recomendação é mínimo de três AZs desde o início.
- **Regras de firewall com referência a IP fixo**: ao trocar/desativar servidores, um IP antigo pode ser reaproveitado por outro sistema (ex.: banco de dados de folha de pagamento) e herdar acessos indevidos — usar sempre referência a Security Group, nunca a IP.
- **Conceder acesso de administrador "temporariamente"**: a exceção de conveniência ("ajusto as permissões em uma ou duas semanas") tende a nunca ser corrigida e vira uma superfície de risco permanente.
- **Expandir para múltiplas regiões "pela diversidade"**: sem um motivo de negócio concreto, isso só adiciona custo — inclusive o anti-padrão simétrico de ir para multicloud, que costuma dobrar custos de segurança, auditoria e, às vezes, de equipe.
- **Usar custos intangíveis não quantificados no caso de negócio**: se não puder mensurar a economia de tempo/esforço, não a inclua na justificativa — a alta gerência pode enxergar isso como "agenda sem base sólida" e prejudicar a credibilidade da migração inteira.

## Worked Example
**Cenário 1.18 — o custo real de disponibilidade (Jimmy).** On-premises, Jimmy mantém um cluster ativo/passivo em dois data centers: um servidor de produção (US$ 100/mês) e um servidor de standby idêntico só para failover (outros US$ 100/mês) — ou seja, paga 200% do necessário (100% para servir e 100% só para estar pronto). Na AWS, com pelo menos três AZs disponíveis, ele reestrutura para um cluster **ativo/ativo**: três servidores dividindo 50% de carga cada, a US$ 50/mês cada, totalizando US$ 150/mês. O resultado: mesma tolerância a falha (perder um servidor ou uma AZ ainda atende 100% da carga), mas 25% mais barato que o modelo on-premises — porque a capacidade de standby deixa de ser um custo morto e passa a fazer parte do pool que atende tráfego.

## Key Takeaways
1. Construa o "porquê" da migração antes do "como" — sem uma narrativa que combine vantagem técnica e de negócio, a resistência das pessoas trava o projeto.
2. Trate custos tangíveis e intangíveis separadamente no caso de negócio; só inclua intangíveis que você pode de fato quantificar.
3. Escale horizontalmente por padrão; reserve a escalabilidade vertical para casos com justificativa técnica explícita (COTS, picos previsíveis).
4. Migre a mentalidade de DR (recuperar) para BC (nunca parar), decidindo separadamente se a proteção precisa cruzar AZs, regiões, ou ambas.
5. Zero trust + menor privilégio (via Security Groups e IAM) são baratos de implementar na AWS e caros de implementar on-premises — use isso a seu favor na narrativa de segurança.
6. Vendor lock-in real só existe em serviços proprietários; a portabilidade de "hardware para bits" já é, por si, uma redução de lock-in comparada ao on-premises.
7. Construa a FAQ iterando por público-alvo — as perguntas se repetem entre equipes, e o esforço de antecipação compensa.

## Connects To
- **Ch 2**: os riscos técnicos e de negócio que devem ser pesados junto com essas vantagens antes de decidir migrar.
- **Ch 4**: o caso de negócio (business case) formaliza em números as vantagens de custo tangíveis/intangíveis discutidas aqui.
- **Ch 6**: landing zone e governança são onde zero trust e menor privilégio se tornam política institucionalizada, não decisão pontual.
