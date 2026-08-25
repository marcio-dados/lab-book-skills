# Capítulo 2: Quais são os riscos e como atenuá-los

## Core Idea
O papel do gerente não é eliminar todos os riscos da migração — isso é impossível e leva à "paralisia da análise" — e sim identificar os riscos técnicos e de negócio mais relevantes, atenuá-los sistematicamente e formalizar as decisões recorrentes como **princípios norteadores** que a empresa segue por padrão.

## Frameworks Introduced
- **Princípios norteadores (guiding principles)**: regras-padrão para design/operação na nuvem, seguidas a menos que haja um motivo de negócio explícito para desviar.
  - Quando usar: crie um princípio apenas para **padrões variáveis** (decisões que se repetem com contexto mutável, ex.: "sempre implantar em múltiplas AZs"). Não crie princípio para algo que só será desenhado uma vez (ex.: a landing zone em si) — nesse caso, faça certo da primeira vez.
  - Como: identifique o risco → decida se é variável ou fixo → se variável, escreva o princípio como regra padrão com abertura para exceção justificada por negócio.
- **Quatro pilares de segurança na migração**: landing zone apropriada, menor privilégio, modelo de responsabilidade compartilhada, e evitar padrões de segurança legados (firewall/IDS baseado em zona). O autor observa que incidentes de segurança na nuvem (ex.: Capital One) tipicamente se reduzem à falta de controles adequados sobre os recursos — não a falhas do provedor.
- **RACI por classe de aplicação**: para o modelo de responsabilidade compartilhada, defina uma matriz RACI (Responsible, Accountable, Consulted, Informed) separada para cada classe de aplicação (COTS, desenvolvida internamente convencional, nativa de nuvem) — não uma única RACI genérica.
- **Trigger de threshold para consultoria externa**: defina o uso de consultores/prestadores de serviço por gatilho objetivo (ex.: "se o treinamento interno atrasar a migração de uma aplicação por mais de duas semanas, contratamos consultoria"), não por decisão ad hoc.
- **Chargeback / showback + tags obrigatórias**: framework de controle de custo variável — marcar recursos, exibir ou cobrar o custo real da unidade de negócio, e usar AWS Config Rules para tornar a marcação obrigatória (não opcional).

## Key Concepts
- **Landing zone**: base de segurança, conformidade e estrutura de contas implantada uma vez, antes de qualquer carga de trabalho (ex.: via AWS Control Tower).
- **Modelo de responsabilidade compartilhada**: a AWS assume a segurança "da nuvem" (data center, hipervisor, rede física); o cliente assume a segurança "na nuvem" (configuração de buckets S3, regras de Security Group, patching do SO nas instâncias EC2).
- **Zero trust vs. segurança por zonas**: zero trust nega comunicação entre servidores por padrão; segurança por zonas (firewall/IDS tradicional) cria um único ponto de estrangulamento que não escala horizontalmente (é *stateful*).
- **Lift-and-shift**: migrar a carga de trabalho como está, sem modificação — o caminho mais rápido, usado como padrão inicial.
- **Refatoração**: reconstruir uma aplicação monolítica como arquitetura distribuída para aproveitar serviços nativos da nuvem — aumenta a complexidade percebida no nível macro, mas reduz risco no nível micro (mudanças isoladas por componente).
- **Direct Connect vs. VPN vs. Internet**: três opções de conectividade — VPN para volume baixo/médio (limitada por banda e latência variável da internet), Direct Connect para banda dedicada e alta previsibilidade (custo maior), conexão via internet + bastion host para empresas com pouca dependência de infraestrutura legada.
- **Shadow IT**: recursos/servidores em execução fora de qualquer controle e conhecimento formal da TI — sintoma de landing zone ou tagging malfeitos.
- **PVU (Processor Value Unit)**: unidade de licenciamento da IBM baseada em tipo e quantidade de núcleos de CPU — motivo para revisar dimensionamento antes de presumir aumento de custo de licença na migração.

## Mental Models
- **Trancar todos os cômodos vs. trancar só a porta da frente**: zero trust (todos os cômodos trancados) limita o raio de ação de um invasor a um único servidor comprometido; segurança por zona (só a porta da frente) dá acesso livre a tudo depois do perímetro.
- **Risco técnico é "varrido para debaixo do tapete"; risco de negócio é visível ao público**: falhas técnicas raramente vazam para fora da empresa (exceto violações graves de segurança); riscos de negócio — reputação, obrigações contratuais, perda de expertise — têm impacto público e são mais difíceis de esconder ou reverter.
- **A complexidade distribuída é percepção, não realidade operacional**: uma arquitetura serverless parece mais complexa "no nível macro" (mais componentes no diagrama), mas o trabalho do dia a dia acontece "no nível micro" — em uma peça isolada — o que reduz, não aumenta, o risco de uma mudança quebrar o resto do sistema.
- **A receita do sucesso contra risco de reputação**: planejamento apropriado + testes apropriados + análise de segurança apropriada — "boas intenções não evitam problemas; o processo correto evita".

## Anti-patterns
- **Paralisia da análise**: tentar mapear e eliminar todos os riscos possíveis antes de agir — prolonga a fase de infraestrutura duplicada (e seu custo) sem eliminar o risco residual de eventos imprevisíveis.
- **Firewall/IDS/IPS de rede tradicional na AWS**: por serem *stateful*, não escalam horizontalmente; forçam escalabilidade vertical cara e criam ponto único de estrangulamento — usar Security Groups (zero trust) e IDS/IPS baseado em host.
- **Conceder privilégio de administrador "para não travar o projeto"**: desistir do menor privilégio por complexidade de configuração raramente é corrigido depois — vira risco de segurança permanente até uma violação forçar a correção.
- **Tratar avaliação de aptidão dos funcionários como ameaça velada**: se a pesquisa de skills parecer uma avaliação de desempenho disfarçada, os funcionários vão subdeclarar lacunas e o diagnóstico de treinamento fica inválido.
- **Não documentar o conhecimento tribal antes da migração**: conhecimento não escrito, que "só é contado ao lado do bebedouro", é o maior risco à implementação de menor privilégio e à continuidade quando o funcionário sai.
- **Consultoria que retém documentação de propósito**: entregar apenas um design de alto nível (não os runbooks operacionais) para forçar dependência contínua do cliente é uma forma de vendor lock-in que a empresa contratante deve prevenir contratualmente.
- **Não marcar (tag) recursos e não cobrar showback/chargeback**: sem visibilidade de custo por equipe, o consumo cresce sem controle — ao contrário do on-premises, na AWS "os recursos não se esgotam".

## Worked Example
**Cenário 2.1 — a landing zone que faltou (Hanna).** Uma rede de supermercados já havia migrado dez cargas de trabalho para produção sem nunca ter implantado uma landing zone: uma única conta AWS sem segmentação, sem menor privilégio e sem CloudTrail ativado. Um desenvolvedor desligou acidentalmente um servidor de produção, causando interrupção em dez lojas e perdas de dezenas de milhares de dólares — e a empresa não conseguiu nem identificar quem havia feito isso, porque não havia log de auditoria. Hanna, contratada depois desse episódio, diagnostica a causa raiz (ausência de landing zone) e recomenda **parar novas migrações** até reconstruir a base: contas segmentadas por ambiente, perfis de menor privilégio, e CloudTrail/Config/GuardDuty ativados antes de mover qualquer nova carga de trabalho. A lição do autor: economizar tempo pulando a landing zone sempre custa mais depois, porque a migração tem de ser interrompida para corrigir a base.

## Key Takeaways
1. Não tente eliminar todo risco — identifique os riscos mais relevantes (técnicos e de negócio) e atenue-os; aceite o resíduo.
2. Implemente a landing zone (contas segmentadas, CloudTrail ≥90 dias, Config, GuardDuty, Inspector, logging protegido em conta separada) *antes* de migrar qualquer carga de trabalho — corrigir depois custa muito mais.
3. Use Security Groups (zero trust) em vez de firewalls/IDS tradicionais baseados em zona — além de mais seguros, escalam horizontalmente sem gargalo.
4. Construa uma RACI por classe de aplicação para deixar claro o que muda (e o que não muda) no modelo de responsabilidade compartilhada.
5. Escolha conectividade (VPN, Direct Connect, internet+bastion) pelo volume de usuários/aplicações legadas e sensibilidade à latência — não por padrão.
6. Trate o risco de perda de funcionários/expertise com comunicação e treinamento antecipados; a migração é uma boa oportunidade para documentar conhecimento tribal antes que ele saia pela porta.
7. Marque (tag) todo recurso desde o início, torne isso obrigatório via Config Rules, e implemente chargeback/showback — sem isso, o consumo na nuvem cresce sem controle porque, ao contrário do on-premises, não há teto físico de capacidade.
8. Um bom plano de migração de aplicação tem no mínimo cinco elementos: descoberta, plano técnico, processo de testes, processo de transição e processo de rollback (detalhados nos Caps. 3–8).

## Connects To
- **Ch 1**: os riscos aqui equilibram as vantagens discutidas antes — a FAQ do porquê e os princípios norteadores juntos formam a base para convencer stakeholders e mitigar objeções.
- **Ch 3**: a fase de descoberta é onde a análise de licenças, RACI e conectividade citadas aqui se tornam dados concretos por aplicação.
- **Ch 4**: o caso de negócio se apoia na FAQ do porquê (Ch 1) e nos dados de descoberta (Ch 3).
- **Ch 6**: landing zone e governança, introduzidas aqui como pré-requisito de segurança, são detalhadas como fase própria do processo de migração.
- **Ch 8**: o plano de migração por aplicação (descoberta, plano técnico, testes, transição, rollback) é aprofundado no capítulo final.

---

*Nota estrutural: entre os Capítulos 2 e 3 o livro insere a introdução da Parte II — "Fases da migração" — que apresenta o mapa geral do processo: Descoberta → Caso de negócio → Preparação operacional → Landing zone/governança → Planejamento da migração → Avaliação para refatoração → Análise minuciosa e planejamento por aplicação. Essa sequência corresponde exatamente à ordem dos Capítulos 3 a 8 deste skill.*
