# Capítulo 8: Refatoração, novas ferramentas e preparativos finais

## Core Idea
Depois do plano fechado (Ch 7), ainda há três passos antes de migrar de fato: identificar oportunidades de refatoração que sigam a regra 80/20 (grande impacto, baixo esforço), avaliar "reequipagem" com ferramentas nativas de baixo custo e alto valor (WAF, Systems Manager, CloudFront), e fazer a análise minuciosa por aplicação (status, disponibilidade de equipe, detalhes técnicos, planos de teste/transição/rollback) — só agora a precisão sai do "lançamento ao espaço" e chega ao "pouso na Lua".

## Frameworks Introduced
- **Regra 80/20 aplicada à refatoração**: visar mudanças que sejam ~20% do esforço de uma refatoração completa, mas capturem ~80% do impacto possível no negócio (custo, desempenho, ou capacidade de lançar funcionalidade) — não é precisão matemática, é uma metáfora de triagem.
  - Como aplicar: (1) selecione aplicações candidatas — evite COTS (sem acesso a código-fonte), evite Visual Basic/C (baixo suporte/alto esforço), prefira Java e .NET/.NET Core em desenvolvimento ativo; (2) selecione serviços-alvo com impacto real (mudança de engine de banco, S3, conteinerização seletiva, Redshift, site estático, SES) — não serviços "legais" mas de baixo impacto (SNS, SQS); (3) meça o esforço real com ferramentas como o SCT (Schema Conversion Tool) — se a conversão automática de esquema ficar abaixo de ~95%, adie a refatoração para depois da migração.
  - Regra dura: nunca refatore on-premises antes de migrar — perde acesso a ferramentas nativas de nuvem e corre o risco de comprar hardware novo que nunca será usado ("comprar alimento para um cavalo morto").
  - Regra dura: não permita refatoração contínua — feche o design e não persiga cada novo serviço lançado pela AWS durante o processo, sob pena de estender indefinidamente o cronograma.
- **Reequipagem com novas ferramentas** (não é refatoração — não exige mudança de código): WAF (firewall de camada 7 serverless, ~US$5/ACL + US$1/regra gerenciada), Systems Manager/SSM (gestão de estado + patching escalonado por ambiente: dev imediato, teste em +7 dias, produção em +14 dias), CloudFront (CDN + primeira linha de defesa contra DDoS). Recomendação: considerar os três como padrão em toda aplicação web, a menos que já exista uma ferramenta equivalente on-premises (ex.: Chef/Puppet/Ansible já implantados tornam a adoção do SSM uma refatoração, não uma reequipagem — adie).
- **Análise minuciosa por aplicação (checklist pré-migração)**: status da aplicação (última atualização, versão suportada pelo fornecedor na nuvem) + disponibilidade de equipe (dev e QA, sem conflito com outras migrações simultâneas) + detalhes técnicos (IPs/portas fixas, domínios em proxy/firewall de terceiros, licenças vinculadas a MAC address) + plano técnico + processo de testes + processo de transição (cutover) + processo de rollback.

## Key Concepts
- **Aurora vs. RDS**: RDS replica fielmente a topologia on-premises (não reduz custo de computação, só custo de licença); Aurora permite escalar leitura horizontalmente (nós de leitura menores e mais baratos) e tem modo Serverless (escala a zero quando ocioso).
- **Redshift**: banco colunar (rápido para analytics, lento para updates linha a linha, sem PK/FK — a aplicação garante integridade); custo de nós depende de classe (compute-optimized vs. dense-storage) e capacidade de armazenamento por nó (ex.: ds2.8xlarge = 16TB); recomendação do autor é sempre usar preço de RI de 1 ano, pois a capacidade de um data warehouse tende a ser estável.
- **SPA + S3 + API Gateway**: padrão de site estático moderno — HTML/JS/imagens servidos do S3, dados dinâmicos via API Gateway → Lambda/EC2, renderização no cliente (React/Angular).
- **SES (Simple Email Service)**: substitui servidores de retransmissão de email (não o servidor de email dos funcionários); primeiras 62.000 mensagens/mês grátis, depois US$0,10/1.000 — custo irrelevante mesmo em grande escala.
- **Aplicações .NET Core / Java como bons alvos de conteinerização**: .NET Core roda em Linux; Java já é virtualizada na JVM. WinForms e WCF (exclusivos Windows) e VB são maus alvos.

## Mental Models
- **"Comprar alimento para um cavalo morto"**: refatorar/atualizar hardware on-premises pouco antes de migrar é desperdício certo — o equipamento não terá seu potencial usado.
- **"Molho secreto" da refatoração**: aplicação certa (código acessível, linguagem moderna, ativamente mantida) + serviço certo (alto impacto real) = candidato válido; falta de qualquer um dos dois ingredientes invalida o alvo.
- **Do "lançamento ao espaço" ao "pouso na Lua"** (fio condutor dos Caps. 3, 4 e 7): a análise minuciosa por aplicação é o momento em que a precisão de fato importa — antes disso, aproximações bastavam.

## Anti-patterns
- **Refatoração contínua durante a migração**: perseguir cada novo serviço lançado pela AWS durante o processo de refatoração estende o cronograma indefinidamente — feche o design e siga.
- **Refatorar on-premises antes de migrar**: perde acesso a ferramentas nativas de nuvem (contêineres, S3) e arrisca comprar/atualizar hardware que será descartado na migração.
- **Escolher serviços "chamativos" sem impacto real** (SNS, SQS) como alvo de refatoração: reduzem overhead de gerenciamento, mas não atingem o critério de impacto significativo nos negócios que justifica o esforço extra no cronograma.
- **Tentar conteinerizar uma aplicação de carga constante em um único servidor**: a economia de conteinerização vem de cargas de trabalho díspares que podem escalar independentemente — sem essa disparidade, não há ganho.
- **Migrar um servidor legado de alto risco de negócio (ex.: FTP com quase mil clientes dependentes) sem descoberta detalhada prévia**: pode gerar interrupção de serviço para centenas de clientes e dano de reputação, exatamente o risco descrito no Ch 2.
- **Ignorar disponibilidade real de equipes de desenvolvimento/QA ao planejar refatoração**: conflito de agenda entre refatoração e outras migrações simultâneas gera atraso ou testes malfeitos sob pressão — ambos custam mais do que planejar corretamente.
- **Apresentar um caso de negócio de refatoração sem lista de riscos**: o autor via isso como sinal de imaturidade em sua própria equipe — "propostas sem risco algum" eram devolvidas para inclusão explícita de riscos antes de seguir adiante.

## Worked Example
**Estimativa combinada de economia com engine de banco de dados + BI (caso real do autor).** Uma empresa migrou de Microsoft SQL Server + Tableau para Amazon Redshift + Amazon QuickSight. A instância de banco de dados on-premises custava sozinha ~US$16.000/mês em um caso citado pelo autor; a conversão de licença Oracle evitou, em outro caso, US$3 milhões/ano. Combinando a eliminação da licença cara do RDBMS legado com a substituição da ferramenta de BI comercial pelo QuickSight (serverless, gerenciado), o autor relata ter feito uma empresa economizar **mais de US$ 800.000/ano**. O processo de validação teve três etapas obrigatórias antes de comprometer o cronograma: (1) rodar o SCT para medir % de conversão automática do esquema; (2) contar quantas queries dependiam de estrutura por linha (Redshift é colunar, sem PK/FK) e precisariam ser reescritas; (3) contar quantos relatórios de BI precisariam ser recriados manualmente (não há migração automática de relatórios para o QuickSight). Só depois desses três números o caso de negócio de refatoração era escrito — sem eles, a economia projetada seria uma SWAG sem lastro.

## Key Takeaways
1. Aplique a regra 80/20 com disciplina: refatore só o que combina alto impacto de negócio com baixo esforço mensurável (ex.: SCT reportando ≥95% de conversão automática de esquema).
2. Nunca refatore on-premises antes de migrar, e nunca deixe a refatoração ficar contínua/sem prazo definido durante a migração.
3. Trate WAF, Systems Manager e CloudFront como "reequipagem" de baixo custo e alto valor — adote por padrão em aplicações web, exceto onde já existe ferramenta equivalente on-premises (nesse caso, é refatoração, adie).
4. Ao estimar economia de refatoração, separe sempre custo de computação de custo de licença — a maior economia geralmente está na licença (RDBMS proprietário, ferramenta de BI comercial), não no EC2.
5. Para conteinerização, valide primeiro se há disparidade real de carga entre componentes da aplicação — sem isso, não há economia a capturar.
6. Antes de migrar cada aplicação, rode o checklist de análise minuciosa completo: status, disponibilidade de equipe, detalhes técnicos ocultos (IP fixo, porta não padrão, licença por MAC), e os três planos (técnico, testes, transição/rollback).
7. Documente riscos explicitamente em todo caso de negócio de refatoração — a ausência de riscos listados é sinal de análise incompleta, não de proposta sólida.
8. Não é um fracasso não encontrar nenhuma aplicação para refatorar nesta fase — sempre há "o dia depois da migração" para revisitar oportunidades com mais tempo e menos pressão de cronograma.

## Connects To
- **Ch 1**: CloudFront e a discussão de disponibilidade/segurança retomam vantagens técnicas apresentadas no capítulo de abertura.
- **Ch 2**: o risco de reputação por descoberta incompleta (exemplo do servidor FTP) é o mesmo risco de negócio detalhado no Ch 2.
- **Ch 3/Ch 4**: SCT, DMS e DataSync (ferramentas de descoberta e custo) retornam aqui aplicadas especificamente à validação de viabilidade de refatoração.
- **Ch 7**: a análise minuciosa por aplicação é a continuação direta do plano de migração construído no capítulo anterior — mesmo processo de ajuste de cronograma ("Aprimorando os 10%") se aplica a cada refatoração aprovada.
