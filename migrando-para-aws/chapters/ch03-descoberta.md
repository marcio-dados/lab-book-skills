# Capítulo 3: Descobrindo suas cargas de trabalho

## Core Idea
A descoberta é a primeira fase, obrigatória, de qualquer migração: ferramentas automatizam boa parte do levantamento de servidores, aplicações e dependências, mas uma série de decisões de otimização de custo (dimensionamento, tipo de instância, licenciamento, escalabilidade automática) sempre vai exigir julgamento humano que nenhuma ferramenta do mercado faz sozinha.

## Frameworks Introduced
- **"Lançar um foguete para o espaço" vs. "pousar na Lua"**: nível de precisão esperado em cada fase do processo de migração.
  - Quando usar: na descoberta e no caso de negócio, aceite estimativas aproximadas (SWAG — Scientific Wild-Ass Guess) sobre uso, escalabilidade e custo. Precisão fina (o "pouso na Lua") só é exigida na fase de análise minuciosa por aplicação (Ch 8).
  - Como: não gaste esforço de engenharia detalhando o que ainda será decidido/ajustado adiante.
- **Checklist mínimo de uma ferramenta de descoberta**: identificação de servidores, uso de CPU/memória, capacidade de disco, uso de IOPS, descoberta de aplicações (o que está instalado + versão) e mapeamento de dependências (com opção de lista negra para servidores "ruidosos" como AD).
  - Como: avalie ferramentas por essa lista mínima antes de comprar; aceite que itens fora dela (RDS, tipo de CPU, licenciamento, EFS/FSx, armazenamento efêmero) vão exigir ajuste manual da equipe.
- **Árvore de decisão de conectividade**: sequência de perguntas binárias (aplicações acessíveis via internet? protocolos não criptografáveis? autenticação fraca? restrição de latência? necessidade de muita banda? múltiplas contas? resiliência? banda agregada alta?) que direciona a escolha entre Internet, VPN e Direct Connect.
  - Como: decida pela necessidade do negócio, não pelo custo — migrações que otimizam conectividade pelo preço final tendem a degradar a experiência do usuário.
- **Acréscimo percentual para custos não determinísticos**: regra prática do autor para orçar custos que nenhuma ferramenta calcula com exatidão — banda de saída (+8–10% sobre o gasto com EC2), serviços auxiliares serverless como Config/CloudWatch/SNS (+5% sobre o EC2), e ALB/NLB (multiplicar o custo básico por 4 para cobrir LCUs).

## Key Concepts
- **CMDB**: banco de dados de gerenciamento de configuração — raramente 100% confiável (o autor estima ~70% de precisão em empresas médias/grandes).
- **Coletor com agente vs. sem agente**: agente instalado em cada servidor (mais seguro, dados mais ricos, exige instalação em massa) vs. coleta remota via acesso administrativo (menos aprovado por segurança, dados mais limitados).
- **Dimensionamento correto (right-sizing)**: ajustar o tipo de instância ao uso real medido, não ao hardware alocado on-premises — porque a AWS não compartilha CPU/memória/disco entre clientes como um hipervisor local faz (superalocação de 50–90% é comum).
- **Famílias de instância**: C (CPU otimizada), M (uso geral), T (rajada/burst), A (ARM uso geral), R/X/Z (memória otimizada), P/G/F (GPU), I/D/H (armazenamento otimizado); número após a letra = geração (maior = mais nova); sufixo = tamanho (nano a 32xlarge, em múltiplos de razão).
- **Custo de execução parcial**: desligar servidores de dev/teste fora do horário comercial pode gerar ~70% de economia (10h/dia × 5 dias = 50h vs. 168h semanais).
- **EBS gp2 / io1 / st1 / sc1**: gp2 (SSD geral, 3 IOPS/GB) cobre ~95% dos casos; io1 para IOPS alto com pouco armazenamento; st1/sc1 (discos magnéticos, mínimo 500GB) para throughput sequencial alto (ex.: backups).
- **EFS / FSx**: substitutos gerenciados para servidores NFS (EFS, redundante em 3 AZs nativamente) e servidores de arquivo Windows/Lustre (FSx, multi-AZ opcional).
- **BYOL vs. licença incluída**: BYOL exige instância dedicada/host dedicado/bare metal (mais parecido com gerenciar data center); licença incluída no EC2/RDS elimina risco de auditoria e paga só pelo uso real (inclusive durante autoscaling).
- **ELB clássico vs. ALB vs. NLB**: ELB clássico (Camada 4, legado, obsoleto), ALB (Camada 7, roteia por URL/host, até 100 destinos, cobrado por LCU), NLB (Camada 4, TCP/UDP/TLS, IP estático, sem sticky sessions, sem Security Groups — usa IP de origem).

## Mental Models
- **"Se eu tivesse bananas suficientes, treinaria um macaco"**: mover blocos de disco (CloudEndure) é a parte fácil da migração; a parte difícil é saber *o que* está instalado e *quem* depende daquele servidor — é aí que o esforço real deve ir.
- **Erre para menos no dimensionamento de disco**: EBS pode crescer depois sem problema, mas não pode ser reduzido — subdimensionar é reversível, sobredimensionar não.
- **Decida por necessidade do negócio, não pelo preço final**: escolher conectividade (Internet/VPN/Direct Connect) pelo custo mais baixo tende a produzir experiências ruins para clientes internos/externos — o critério é a necessidade, o custo é consequência.

## Anti-patterns
- **Presumir que "conhecemos nossa infraestrutura"**: mesmo com CMDB, a taxa real de precisão gira em torno de 70% em empresas médias/grandes — trate isso como uma aposta ruim, não como certeza.
- **Ferramenta que só otimiza por menor preço**: escolher instâncias mais antigas (ex. T2) por custarem centavos menos por hora, ignorando que gerações mais novas (T3, na engine Nitro) entregam ~30% mais desempenho por dólar — o menor preço nominal nem sempre é o menor custo real.
- **Migrar bancos de dados diretamente para EC2 sem avaliar RDS**: a maioria das ferramentas de descoberta recomenda EC2 por padrão para qualquer servidor com RDBMS, perdendo a redução de custo intangível do RDS gerenciado.
- **Usar armazenamento magnético (st1/sc1) "para economizar" sem considerar o mínimo de 500 GB**: pode inflar custos em vez de reduzi-los, dependendo do tamanho real do disco.
- **BYOL por apego às licenças já compradas**: ~90% dos clientes do autor optaram por descartar licenças on-premises na migração — o custo de gerenciamento/auditoria de licenças e o risco de não conformidade (multas de até US$ 150 mil por título) geralmente superam o valor residual da licença.
- **Escolher tipo de conectividade pelo custo, não pela necessidade**: gera migrações "extremamente problemáticas", na experiência do autor — a árvore de decisão deve ser seguida por requisito técnico/de negócio, com custo como consequência, não como critério de entrada.

## Worked Example
**Cenário 3.2 — o custo real de balanceadores de carga (Anna).** A empresa de Anna tem 17 farms de servidores web (produção), mais 17 de teste e 17 de desenvolvimento, replicadas em duas regiões para redundância. Como ALBs não cruzam regiões, contas nem ambientes, o cálculo mínimo de instâncias de ALB é: 2 (produção, uma por região) + 1 (teste) + 1 (desenvolvimento) = 4 ALBs. Ao custo unitário de US$ 0,0225/hora × 730 horas/mês, o custo básico é US$ 65,70 por ALB — mas como o modelo de cobrança por LCU (novas conexões, conexões ativas, bytes processados, avaliações de regra) é difícil de prever sem uma POC real, o autor recomenda **multiplicar o custo básico total por 4** como margem de segurança: US$ 65,70 × 4 = US$ 262,80/mês estimados. A lição: para custos que dependem de padrão de tráfego real (LCU, banda de saída, serviços serverless auxiliares), use multiplicadores/acréscimos percentuais em vez de tentar prever com exatidão — é a fase de "lançar o foguete", não de "pousar na Lua".

## Key Takeaways
1. A descoberta é inegociável — sem ela não há como orçar custo, montar o caso de negócio nem planejar levas de migração.
2. Escolha a ferramenta pelo checklist mínimo (servidores, CPU/memória, disco, IOPS, aplicações+versão, dependências) e aceite que o resto (RDS, tipo de CPU, licenciamento, NFS/Windows file server, storage efêmero, ALB/NLB, conectividade) exige revisão manual da equipe.
3. Dimensione corretamente CPU/memória/disco pelo uso real medido — a ausência de compartilhamento de recursos na AWS (diferente de hipervisores on-premises) torna isso a maior fonte de economia disponível.
4. Prefira sempre a geração de instância mais recente disponível na família equivalente — o preço nominal menor de gerações antigas costuma custar mais por unidade de desempenho.
5. Avalie BYOL vs. licença incluída caso a caso, mas comece com a suposição de que descartar licenças legadas costuma compensar.
6. Use acréscimos percentuais (8–10% para banda de saída, 5% para serviços auxiliares, ×4 para LCU de ALB/NLB) em vez de tentar calcular custos não determinísticos com precisão.
7. Escolha o tipo de conectividade pela árvore de decisão baseada em necessidade (internet-acessível? protocolo criptografável? autenticação forte? latência? banda? contas múltiplas? resiliência?) — nunca pelo menor custo isolado.
8. Migrar tudo via lift-and-shift sem otimizar nada é uma opção legítima e não é motivo de vergonha — mas anula boa parte das vantagens discutidas no Capítulo 1; planeje migrar progressivamente para serviços gerenciados depois.

## Connects To
- **Ch 1**: os serviços gerenciados citados aqui (RDS, EFS, FSx) são exatamente os exemplos de redução de custo intangível discutidos antes.
- **Ch 2**: a árvore de decisão de conectividade aprofunda a seção "Conectividade das aplicações" do capítulo de riscos.
- **Ch 4**: os números de descoberta (dimensionamento, licenciamento, custos auxiliares) alimentam diretamente o caso de negócio.
- **Ch 8**: a análise minuciosa por aplicação é onde as suposições ("lançar o foguete") desta fase são substituídas por precisão real ("pousar na Lua").
