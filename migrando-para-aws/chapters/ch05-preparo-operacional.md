# Capítulo 5: Preparando-se para as tarefas operacionais na AWS

## Core Idea
Antes de migrar qualquer carga de trabalho, a empresa precisa mudar seus processos operacionais — segurança, gerenciamento de mudanças, agilidade e controles financeiros — porque continuar operando na AWS como se operava on-premises ("você está fazendo errado") anula a maior parte das vantagens da migração.

## Frameworks Introduced
- **Construção da pirâmide (Pyramid Building)**: método do autor para disseminar mudança operacional por toda a empresa em quatro camadas.
  - Como: (1) **Fundação** — conquiste um patrocinador executivo de nível C (não gerência baixa de TI); (2) **Base** — prototipe segurança/conformidade, gerenciamento de mudanças e agilidade dentro da própria TI, onde os erros custam menos; (3) **Expansão** — leve os processos validados para *um* departamento aliado fora da TI, escolhido por já ter relação de confiança; (4) **Topo** — só depois de ter uma "história de sucesso" comprovada em dois ambientes, venda o processo para o resto da empresa.
  - Quando usar: sempre que a mudança exigir adesão fora do controle direto do gerente de TI — é sequencial, não pule etapas.
- **Segurança como revisor, não executor**: ao migrar para IaC, a equipe de segurança deixa de implementar controles e passa a **revisar** o código antes do deploy (gate no pipeline), comparando apenas o *diff* entre commits — não a aplicação inteira a cada vez.
- **Gerenciamento de mudanças automatizado**: substitua a reunião periódica de comitê por controles embutidos no próprio pipeline, cobrindo os quatro riscos que o processo tradicional mitigava — mudanças simultâneas, janelas de manutenção, planos de rollback (blue-green/canary), e testes automatizados com limiares de bloqueio.
- **Os três inimigos da agilidade**: equipes grandes demais (regra da "equipe de duas pizzas" da Amazon), "muito cacique para pouco índio" (falta de um responsável único pela decisão em cada reunião), e processo pelo processo (burocracia sem propósito). Atacar os três não exige anos — exige dias de decisão de eliminar o desnecessário.
- **Controles financeiros na nuvem**: tagging obrigatório + AWS Cost Explorer + chargeback/showback + conta sandbox com limpeza automática — o conjunto mínimo para não repetir o padrão observado pelo autor de ~2/3 de infraestrutura "esquecida" e nunca desligada.

## Key Concepts
- **Patrocinador executivo (executive sponsor)**: precisa ser C-level, não gerência de TI — sem essa autoridade, a mudança não atravessa silos de negócio.
- **"Ver se funciona" vs. "fazer funcionar"**: dois perfis de patrocinador; só o segundo persiste através da resistência organizacional.
- **AWS Artifact**: repositório de documentos de auditoria/conformidade (ISO, SOC, PCI) que substitui a tarefa manual de coletar evidências de segurança física — a tarefa não desaparece, mas se torna mais simples e mais importante.
- **Implantação blue-green / canary**: técnicas de deploy que embutem rollback automatizado no próprio processo, reduzindo o risco que antes exigia aprovação manual de comitê.
- **Equipe de duas pizzas**: princípio da Amazon de que nenhuma equipe deve ser maior do que o que duas pizzas alimentam — equipes pequenas mantêm agilidade em qualquer escala de empresa.
- **Cost Explorer + Cost Allocation Tags**: ferramenta de BI de custos da AWS; exige ativação manual das tags no console de faturamento (não no próprio Cost Explorer) antes de segmentar custo por departamento/aplicação/tag `aws:cloudformation:stack-name`.
- **AWS-Nuke**: script de limpeza de conta sandbox, citado como exemplo de ferramenta para impedir que ambientes de teste/prototipagem fiquem rodando indefinidamente.

## Mental Models
- **"Você está fazendo errado" (Mr. Mom)**: operar na AWS com os mesmos processos on-premises é possível, mas anula o benefício da migração — a citação do autor resume o capítulo inteiro.
- **Paralelo mainframe → workstation/servidor → nuvem**: a transição para a nuvem exige uma mudança operacional da mesma magnitude que a saída do mainframe — não da magnitude menor da virtualização (que preservou em grande parte os mesmos processos).
- **Comprar uma Ferrari e deixá-la com o tanque vazio na garagem**: ter tecnologia de ponta (a AWS) sem revisar o processo de negócio ao redor (ex.: gerenciamento de mudanças de 45 dias) é desperdiçar o investimento.
- **Empresa pequena tem agilidade por ausência de processo, não por mérito**: à medida que a empresa cresce, processos aparecem por necessidade real — o problema é quando continuam sendo adicionados "porque uma empresa grande tem que ter processo", sem checar se resolvem um risco real.

## Anti-patterns
- **Escolher um patrocinador que não seja C-level**: o autor relata um caso em que o patrocinador (diretor de nuvem, não C-level) só conseguiu apoio de duas equipes de TI e não conseguiu tração nos resultados de negócio da migração.
- **Manter comitê de gerenciamento de mudanças com reunião periódica em cadência incompatível com deploy contínuo**: o Cenário 5.1 (45 dias para uma mudança de firewall, mais 45 dias para corrigir um erro no pedido) ilustra como um processo de negócio pode paralisar a agilidade que a tecnologia deveria entregar.
- **Aumentar o tamanho da equipe para acelerar entrega**: passa um ponto de retorno decrescente rapidamente — equipes grandes ficam "mais eficientes em fazer o errado", não mais rápidas.
- **Reuniões sem um responsável único pela decisão**: gera "carrossel" de indecisão — o autor relatou ter resolvido uma situação de projeto fracassado simplesmente por assumir a decisão que ninguém mais queria tomar.
- **Adicionar processo sem testar se ele resolve um risco real**: "processo é bom, preencher formulários em três vias é ruim" — cada novo processo deve responder à pergunta "isso deixa o trabalho mais eficiente ou mais lento?".
- **Recursos irrestritos / contas de desenvolvimento sem limpeza automática**: o caso real do autor (6.000 de 9.600 servidores desnecessários, esquecidos por anos) mostra o que acontece sem controle de provisionamento e sandbox com expiração.
- **Chargeback só no primeiro ano de um novo produto**: capitalizar o investimento inicial no caso de negócio da unidade de negócio, mas devolver o custo operacional contínuo para o orçamento de TI depois do primeiro ano, sem revisão — desalinha incentivo e responsabilidade.
- **Pipeline blue-green sem verificação de limpeza da versão antiga**: se a etapa de remoção da infraestrutura antiga falhar silenciosamente, servidores acumulam indefinidamente — especialmente perigoso com deploys frequentes (dez vezes ao dia).

## Worked Example
**Cenário 5.1 — o preço do processo legado (Tim, o próprio autor).** Consultor em uma grande empresa de serviços financeiros, o autor precisava de uma mudança simples de firewall para permitir comunicação entre dois servidores. O processo formal de change management informou um prazo de **45 dias**. Na primeira tentativa, a equipe de infraestrutura cometeu um erro na ordem de serviço — e o autor teve que esperar **outros 45 dias** para a correção. A lição: nenhuma tecnologia de nuvem resolve isso — o gargalo não é técnico, é o processo de negócio em torno da mudança. É exatamente esse tipo de processo que precisa ser revisado (Base da pirâmide, "Gerenciamento de mudanças") antes de esperar que a migração entregue agilidade real.

## Key Takeaways
1. Não pule direto para a migração técnica após aprovar o caso de negócio — o preparo operacional (segurança, change management, agilidade, controles financeiros) é pré-requisito, não um "nice to have" posterior.
2. Construa a mudança organizacional em camadas: patrocinador C-level → prototipagem dentro da TI → um departamento aliado → o resto da empresa. Não tente vender para todo mundo de uma vez.
3. Transforme a equipe de segurança de executora em revisora via gate de pipeline sobre IaC — isso preserva separação de responsabilidades sem recriar o gargalo de zona/firewall do Ch 2.
4. Embuta os quatro objetivos do change management tradicional (não simultaneidade, janela de manutenção, rollback, testes) diretamente na automação do pipeline — não tente rodar o comitê antigo em paralelo com deploy contínuo.
5. Ataque os três inimigos da agilidade (equipes grandes, decisão sem responsável, processo por processo) primeiro — são as vitórias mais rápidas e visíveis antes de expandir para outros departamentos.
6. Implemente tagging obrigatório + Cost Explorer + chargeback/showback + sandbox com limpeza automática antes da migração começar em volume — corrigir depois custa ordens de magnitude mais.
7. Trate a disseminação da mudança como um exercício de vendas interno: tenha uma história de sucesso comprovada (não hipotética) antes de pedir adesão de um novo departamento.

## Connects To
- **Ch 1**: as FAQs do porquê retornam como matéria-prima para a narrativa de "venda" na expansão da pirâmide.
- **Ch 2**: menor privilégio e a discussão de perda de funcionários/expertise se aprofundam aqui na revisão do papel da equipe de segurança e no risco de reorganização de equipes.
- **Ch 4**: pipelines de implantação e Service Catalog, tratados ali como fonte de economia de agilidade, aqui ganham o processo operacional que os torna seguros (gates de segurança, testes automatizados).
- **Ch 6**: a landing zone e a governança na nuvem (próximo capítulo) são a implementação técnica da fundação/base discutida aqui.
