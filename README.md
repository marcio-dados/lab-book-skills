# lab-book-skills

Laboratório pessoal de livros/documentos técnicos convertidos em skill pelo
[`book-to-skill`](https://github.com/virgiliojr94/book-to-skill), consultado pelo AI-LAB através da skill
roteadora `book_lab` (`ai-lab/.claude/skills/book_lab/`). Repositório **privado**, conta pessoal
(`marcio-dados`).

Decidido e revisado em `ai-lab/docs/architecture_reviews/2026-08-24_SDD017_book_skill_lab.md` — esse
documento é a fonte de verdade da arquitetura; este README é só o manual operacional.

## O que entra

- Livro técnico.
- Material público/de terceiro usado no trabalho — teste binário: **"eu obteria este arquivo hoje sem
  nenhuma credencial, acesso ou vínculo MaisTodos?"** Sim → entra. Copyright de terceiro continua valendo
  por cima — é por isso que o repo é privado.
- Documento pessoal de **referência/estudo** (manual, apostila, curso, anotação técnica).
- Livro de desenvolvimento pessoal.

## O que NÃO entra

- Arquitetura interna, runbook de dado (Trusted/lake), contrato, PII (própria ou de terceiro), credencial,
  código ou nome de cliente da MaisTodos.
- Qualquer anotação que agregue especificidade interna da MaisTodos a material público — isso converte
  material público em documento interno. Se a anotação é o valor, ela pertence a repositório da empresa,
  não a este.
- Documento pessoal **sensível** (PII própria: contrato, holerite, exame, documento de identidade).

Este repositório é de conta pessoal. Material da empresa exige repositório da empresa.

## Estrutura

Namespace plano de slugs na raiz — **sem** pastas de categoria (`livros/`, `maistodos/`, `pessoal/`...).
Categoria é metadado no front-matter (`tipo:`), não endereço — pasta é decisão que envelhece mal (item que
muda de categoria, slug que precisa mudar de caminho e quebra citação existente).

```
lab-book-skills/
├── README.md
├── vendor/book-to-skill@<sha>/     # snapshot de proveniência da ferramenta usada na conversão
├── <slug>/
│   ├── SKILL.md                    # front-matter obrigatório (ver abaixo) + índice de capítulos
│   ├── chapters/ch01-*.md ...
│   ├── glossary.md
│   ├── patterns.md
│   └── cheatsheet.md
└── _archive/<slug>/                 # baixo uso (ver book_usage) — fora da listagem default do book_lab,
                                      # ainda acessível se o slug for citado explicitamente
```

Deliberadamente **sem** `INDEX.md` mantido à mão — LLM editando catálogo markdown crescente trunca
conteúdo (mesma lição que motivou o `doc_catalog` do `lab-doc-endpoint`). A fonte da verdade do que existe
é a listagem de diretórios + o front-matter de cada `<slug>/SKILL.md`.

## Front-matter obrigatório em cada `<slug>/SKILL.md`

Nada disto é gerado pelo `book-to-skill` — é escrito à mão na ingestão. **Todos os campos são obrigatórios**,
inclusive quando o valor parece redundante (ver `titulo_pt`).

```yaml
origem: publico-terceiro | pessoal | producao-propria
classificacao: nao-corporativo        # atestação explícita na ingestão — espelha o padrão do deepseek_ask
tipo: livro-tecnico | doc-ferramenta | pessoal | desenvolvimento
idioma: en | pt-BR | es | ...           # idioma dos ARQUIVOS GERADOS (chapters/*.md), não do PDF de origem
titulo_pt: "Projetando Aplicações com Uso Intensivo de Dados"
proveniencia:
  titulo: "Designing Data-Intensive Applications"   # exatamente como está na capa, idioma original
  autor: ["Martin Kleppmann"]                       # lista, mesmo com um único autor
  editora: "O'Reilly"
  fonte_sha256: "..."                  # sha256 do arquivo de origem — o arquivo em si não é versionado
  convertido_em: "AAAA-MM-DD"
  ferramenta_sha: "<sha do book-to-skill usado na conversão>"
```

**`titulo_pt` é apelido, não tradução.** O critério é *"o que eu vou digitar quando pedir este livro"*, não *"a
tradução correta da capa"*. Se você chama o livro de "o de sistemas distribuídos do Kleppmann", escreva isso —
é um `titulo_pt` melhor que a tradução literal, porque a tradução literal é justamente o que ninguém digita. Se
você chama o livro pelo título em inglês ("Data Mesh"), repita o inglês: campo opcional é campo que falta no
slug que importa.

**`autor` e `editora` são as âncoras de memória** — é por elas que se lembra quais livros já foram convertidos,
com mais confiabilidade do que pelo slug exato. São também o que a busca por nome varre (seção "Consulta").

⚠️ **Reconferir o front-matter depois de todo fold-in** (`/book-to-skill novo.pdf <caminho-do-slug>`). A
documentação da ferramenta não promete preservar front-matter que ela não escreveu, e um fold-in que apague
`autor`/`titulo_pt` faz o livro sumir da busca por nome sem nenhum aviso.

## Como adicionar um livro/documento

1. `/book-to-skill <arquivo> <slug>` — gera em `~/.claude/skills/<slug>/` (destino default da ferramenta).
2. `mv ~/.claude/skills/<slug> lab-book-skills/<slug>` — mover para dentro deste repo.
3. **Verificar que `~/.claude/skills/<slug>` não existe mais.** Esse é o passo que garante que a skill
   global por livro — o problema que este repositório existe para evitar — não ficou pra trás.
4. Preencher o front-matter (seção acima) no `SKILL.md` do slug, incluindo o teste de triagem ("O que
   entra" acima) e o idioma real observado nos capítulos gerados. **Autor, editora e `titulo_pt` saem do PDF
   de origem — preencha antes de perder o arquivo de vista**, já que ele não é versionado aqui.
5. `git add lab-book-skills/<slug> && git commit`. Fonte original (PDF/EPUB/...) não é versionada — está no
   `.gitignore`.

## Consulta

Não é direta. A skill `book_lab` do AI-LAB só aciona sob pedido explícito e nomeado do usuário — nunca por
varredura especulativa sobre um assunto. Ver `SKILL.md` de `book_lab` para o protocolo completo (gatilho,
delegação de busca ao `buscador`, ponte de idioma pt-BR↔original, protocolo de citação/tradução).

**Não é preciso lembrar o slug.** Citar o autor, a editora ou o título em português resolve: o `book_lab` faz
um `grep` sobre o bloco de front-matter dos `SKILL.md` (só ele — nunca sobre `chapters/`) e chega ao slug.
Autor e palavra distintiva do título discriminam bem; editora sozinha, não — num acervo técnico "O'Reilly" casa
com meia estante, então serve de desempate, não de primeira tentativa. Se nada casar, a resposta é "não achei
**pelo nome**" e para ali — nunca "não tenho esse livro", que seria afirmar inventário a partir de uma busca
falha. Zero resultado quase sempre significa front-matter incompleto.

Deliberadamente **sem** `CATALOG.md`/`INDEX.md`, mesmo gerado: o `grep` só devolve os candidatos que casaram, e
por isso custa o mesmo com 3 ou 300 livros — um índice pagaria por todos eles em toda consulta. Revisar essa
decisão se o acervo passar de ~40 slugs ou se a busca por nome começar a falhar com frequência (SDD-017 §13.6,
que já especifica o que o índice conteria e o que não conteria).

## Uso e arquivamento

Toque de leitura é registrado localmente pelo AI-LAB (`ai-lab/context/telemetry/book_usage.jsonl`, nunca
neste repositório — ver SDD-017 §11.4.3). `tools/host/book_usage/cli.py --relatorio` no `ai-lab` sinaliza
candidatos a arquivar por baixo uso; a decisão e o `git mv <slug> _archive/<slug>` são sempre manuais.
