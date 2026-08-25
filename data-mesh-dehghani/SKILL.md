---
name: data-mesh-dehghani
description: "Knowledge base from \"Data Mesh: Delivering Data-Driven Value at Scale\" by Zhamak Dehghani. Use when applying Dehghani's frameworks for domain ownership, data as a product, self-serve data platforms, federated computational governance, data quantum architecture, or data mesh strategy/execution; studying the book; or referencing its concepts."
origem: publico-terceiro
classificacao: nao-corporativo
tipo: livro-tecnico
idioma: en
titulo_pt: "Data Mesh (Dehghani)"
proveniencia:
  titulo: "Data Mesh: Delivering Data-Driven Value at Scale"
  autor: ["Zhamak Dehghani"]
  editora: "O'Reilly"
  fonte_sha256: "948f6cb6d033e3fcd0058db4dc7db0ea00fb0edde70a9bd437c7dfa0682b6abc"
  convertido_em: "2026-08-24"
  ferramenta_sha: "7bcfcd5262329f8d57a385903f18a98bc6705e4e"
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Data Mesh: Delivering Data-Driven Value at Scale
**Author**: Zhamak Dehghani | **Pages**: ~33 | **Chapters**: 16 | **Generated**: 2026-08-24

## How to Use This Skill

- **Without arguments** — load core frameworks for reference
- **With a topic** — ask about `domain ownership`, `data quantum`, `federated governance`, `bitemporality`, or another indexed topic; I find and read the relevant chapter
- **With chapter** — ask for `ch09`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not covered in Core Frameworks below, I will read
the relevant chapter file before answering.

This is the original book that coined the term "data mesh" (Zhamak Dehghani,
the founder of data mesh). It is a **different** book from `implementing-data-mesh`
(Perrin & Broda) already in this lab — that one is a practitioner's implementation
guide written after data mesh existed; this one is the source that defines the
four principles and the architecture from first principles.

---

## Core Frameworks & Mental Models

**The Four Principles** (must be applied together, never in isolation): **Domain
Ownership** (decentralize analytical data to the business domains closest to its
origin/use, via DDD bounded contexts) + **Data as a Product** (apply product
thinking — discoverable, addressable, understandable, trustworthy, natively
accessible, interoperable, valuable on its own, secure — to counter the siloing
risk domain ownership creates) + **Self-Serve Data Platform** (extract
domain-agnostic infrastructure so generalist technologists build/consume data
products autonomously, countering cost/duplication) + **Federated Computational
Governance** (global policies decided by domain+platform+SME representatives,
enforced as embedded code in every data product, never by manual central
gatekeeping).

**Data (product) quantum**: data mesh's architecture quantum — the smallest
independently-deployable unit bundling transformation code, interfaces-as-code
(input/output/discovery/control ports), policy-as-code, data+metadata, and
platform dependencies. The mesh scales by adding quanta, never by growing one
shared component. Data products are *active* (they run code); files/tables are
passive artifacts.

**Serve data as multimodal, immutable, bitemporal, read-only**: every output
port serves the same domain semantic in multiple formats (SQL, files, streams,
graph); once published, data never mutates — corrections are new tuples with a
new `processing_time` (vs. unchanging `actual_time`); the only sanctioned
"update" is crypto-shredding via the control port for right-to-be-forgotten.

**Federated computational governance's three pillars**: systems thinking
(balance domain autonomy vs. global interoperability using feedback loops and
leverage points — prefer automatable feedback over manual certification gates),
federation (a cross-functional team of domain/platform/SME reps decides only
genuinely cross-cutting policy), computation (policy-as-code embedded in every
data product's sidecar/control port, executed locally, never centrally).

**Design by affordances**: design each data product capability (serve, consume,
transform, discover, compose, manage, govern, observe) by asking what it affords
to which specific agents — and what it deliberately does NOT afford. Borrow from
complex adaptive systems: simple local rules per data product (its own ports)
let mesh-level properties (lineage graph, knowledge graph) emerge; there is no
central orchestrator.

**Composability via a distributed type system**: reject fact-table/foreign-key
joins across data product boundaries (too tightly coupled, assumes homogeneous
syntax). Prefer GraphQL-federation-style type linking or Linked-Data/JSON-LD
style global URIs — each data product owns and versions its own schema; shared
entities ("polysemes" like *artist*) get a global identifier minted by their
owning data product.

**Execution is business-driven, iterative, and evolutionary** — never a
big-bang rearchitecture. Trace every data product/platform feature back to a
strategic business initiative. Use fitness functions (value/connectivity-driven:
"network effect," "lead time to adopt a policy") instead of vanity KPIs ("number
of data products"). Apply an explore→expand→extract S-curve separately to each
of the four principles. Migrate off legacy warehouses/lakes in atomic steps:
build the new data product, migrate its consumers, retire the old
pipeline/tables — all three together, or the step isn't done.

**Organization mirrors Team Topologies**: domain data product teams = stream-
aligned; the platform = platform team (capabilities as-a-service); governance =
a looser "enabling group" (not a standing team) — deliberately avoided from
becoming a bottleneck. Data product boundaries follow domain lines, require
long-term ownership, an independent life cycle, independent meaningfulness, and
actual (not hypothetical) usage.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-data-mesh-in-a-nutshell.md) | Data Mesh in a Nutshell | Four principles overview, operational vs. analytical data |
| [ch02](chapters/ch02-principle-of-domain-ownership.md) | Principle of Domain Ownership | DDD bounded contexts, 3 domain data archetypes |
| [ch03](chapters/ch03-principle-of-data-as-a-product.md) | Principle of Data as a Product | 8 usability attributes, data-as-product vs. asset |
| [ch04](chapters/ch04-principle-of-self-serve-data-platform.md) | Principle of the Self-Serve Data Platform | 5 platform objectives, generalist-technologist design |
| [ch05](chapters/ch05-principle-of-federated-computational-governance.md) | Principle of Federated Computational Governance | 3 governance pillars, feedback loops, leverage points |
| [ch06](chapters/ch06-the-inflection-point.md) | The Inflection Point | Macro drivers, two planes of data, plateau of return |
| [ch07](chapters/ch07-after-the-inflection-point.md) | After the Inflection Point | 3 outcomes mapped to mechanisms, data quantum intro |
| [ch08](chapters/ch08-before-the-inflection-point.md) | Before the Inflection Point | 3 architecture generations, monolithic/centralized critique |
| [ch09](chapters/ch09-the-logical-architecture.md) | The Logical Architecture | Data quantum, sidecar, control port, 3 platform planes |
| [ch10](chapters/ch10-the-multiplane-data-platform-architecture.md) | The Multiplane Data Platform Architecture | User-journey-driven platform design, plane interfaces |
| [ch11](chapters/ch11-design-a-data-product-by-affordances.md) | Design a Data Product by Affordances | Affordance design, complex adaptive systems |
| [ch12](chapters/ch12-design-consuming-transforming-and-serving-data.md) | Design Consuming, Transforming, and Serving Data | Bitemporality, immutability, dumb pipes/smart filters |
| [ch13](chapters/ch13-design-discovering-understanding-and-composing-data.md) | Design Discovering, Understanding, and Composing Data | Shift-left discovery, distributed type system, trust metrics |
| [ch14](chapters/ch14-design-managing-governing-and-observing-data.md) | Design Managing, Governing, and Observing Data | Manifest, policy-as-code, logs/traces/metrics |
| [ch15](chapters/ch15-strategy-and-execution.md) | Strategy and Execution | Readiness assessment, fitness functions, S-curve adoption |
| [ch16](chapters/ch16-organization-and-culture.md) | Organization and Culture | Star Model, Team Topologies, data product boundaries |

## Topic Index

- **Affordances (design by)** → ch11, ch12, ch13, ch14
- **Bitemporal data / actual & processing time** → ch12, ch13
- **Complex adaptive systems** → ch11
- **Composability / distributed type system** → ch13
- **Data as a Product (principle)** → ch03, ch07
- **Data mesh readiness assessment** → ch15
- **Data product boundaries (heuristics)** → ch16
- **Data (product) quantum** → ch09, ch11
- **DDD / bounded contexts / polysemes** → ch02, ch05, ch13
- **Domain Ownership (principle)** → ch02, ch07
- **Federated Computational Governance (principle)** → ch05, ch09, ch14
- **Fitness functions** → ch15
- **Legacy migration (atomic steps)** → ch15
- **Manifest (data product)** → ch14
- **Multiplane platform (3 planes)** → ch09, ch10
- **Observability (logs/traces/metrics)** → ch14
- **Self-Serve Data Platform (principle)** → ch04, ch07, ch10
- **Sidecar / control port** → ch09, ch12, ch14
- **Team Topologies / organizational design** → ch16
- **Warehouse / lake / lakehouse (critique)** → ch06, ch08

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns
- [cheatsheet.md](cheatsheet.md) — quick reference tables and decision guides

---

## Scope & Limits

This skill covers the book content only (all 16 chapters had content at extraction
time — no early-release gaps, unlike the companion `implementing-data-mesh`
skill). For hands-on implementation in your codebase, combine with
project-specific tools. For topics beyond this book, check the related
`implementing-data-mesh` skill (a different book, by different authors, focused
on practitioner implementation) or ask the agent directly. Figures/diagrams from
the source EPUB were not extracted and are described only where the surrounding
text explains them.
