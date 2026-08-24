---
name: implementing-data-mesh
description: "Knowledge base from \"Implementing Data Mesh: Principles and Practice to Design, Build, and Implement Data Mesh\" by Jean-Georges Perrin and Eric Broda. Use when applying Data Mesh frameworks for data contracts, federated governance, data product architecture, team topologies, operating models, or GenAI-enabled data mesh; studying the book; or referencing its concepts."
origem: publico-terceiro
classificacao: nao-corporativo
tipo: livro-tecnico
idioma: en
titulo_pt: "Data Mesh"
proveniencia:
  titulo: "Implementing Data Mesh: Principles and Practice to Design, Build, and Implement Data Mesh"
  autor: ["Jean-Georges Perrin", "Eric Broda"]
  editora: "O'Reilly"
  fonte_sha256: "965fb71a5c40c098aa075cc3694084ae2350713d34a98656b60e99eb4b781100"
  convertido_em: "2026-08-24"
  ferramenta_sha: "7bcfcd5262329f8d57a385903f18a98bc6705e4e"
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Implementing Data Mesh: Principles and Practice to Design, Build, and Implement Data Mesh
**Authors**: Jean-Georges Perrin, Eric Broda | **Pages**: ~23 (Early Release) | **Chapters with content**: 8 of 16 | **Generated**: 2026-08-24

## How to Use This Skill

- **Without arguments** — load core frameworks for reference
- **With a topic** — ask about `data contracts`, `federated governance`, `data product architecture`, or another indexed topic; I find and read the relevant chapter
- **With chapter** — ask for `ch05`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not covered in Core Frameworks below, I will read the relevant chapter file before answering.

**Early Release note**: this is an unfinished, author-raw manuscript (O'Reilly Early Release). Only 8 of the book's planned 16 chapters had content at the time of extraction (1, 2, 3, 4, 5, 9, 14, 15); chapters 6, 7, 8, 10, 11, 12, 13, and 16 are titled but not yet written and have no chapter file here.

---

## Core Frameworks & Mental Models

**Dehghani's Four Principles** (the baseline vocabulary this whole book builds on): Decentralized Domain Ownership, Data as a Product, Self-Serve Data Infrastructure, Federated Computational Governance.

**Federated Certification Governance** (ANSI/ASA analogy, the book's central governance pattern): a lightweight central body sets standards; data product owners self-certify and publish compliance status via a governance API — queryable at any time. Use whenever centralized governance has become a bottleneck; avoid top-down policing.

**The Five Lenses of a "Good" Data Product**: Principled (adheres to Data Mesh), FAIR (Findable, Accessible, Interoperable, Reusable), Enterprise Grade (security, reliability, observability, operability, deployability, documentation), Valuable (solves a defined problem, has a target state/roadmap/sponsor), Empowered Owner. A data product without an empowered owner cannot be "good" regardless of the other four.

**The Data Product Harness**: standardize the *mechanism* of interaction (`/ingest`, `/consume`, `/discover`, `/observe`, `/control`), not the content — this is what makes templating and automation across many data products possible. It is also the enforcement point for data contracts and policy.

**Data Contracts (ODCS)**: adopt the Open Data Contract Standard (Bitol/Linux Foundation AI & Data) instead of a bespoke format. One YAML contract per dataset+version pair; classify every change as patch/minor/major using the severity table (see cheatsheet); build the contract in from day one — retrofitting is expensive.

**Data QoS**: combine the 7 EDM Council data-quality dimensions (Accuracy, Completeness, Conformity, Consistency, Coverage, Timeliness, Uniqueness) with an extensible set of service-level indicators (availability, throughput, latency, retention, time-to-detect/notify/repair, end-of-support, end-of-life), classified like a periodic table by group and time axis.

**Team Topologies for Data Mesh**: Data Product teams = stream-aligned (end-to-end ownership); Data Platform teams = shared "X-as-a-Service" infrastructure; Data Enabling teams = short-term consultative support, never permanently embedded. Six roles populate a Data Product team: Owner, Release Manager, Metadata & Governance Manager, Data & Security Manager, Consumption Services Manager, Ingestion Services Manager.

**Conway's Law and the Operating Model Continuum**: your organization's real structure (centralized / matrixed / federated / distributed) predicts and constrains your data architecture (warehouse / lake / mesh / microservices). Federated organizations are the natural fit for Data Mesh. Regionalization is Data Mesh's default failure mode under Conway's Law — counter it with hybrid global/regional governance, not after the fact.

**GenAI-Enabled Data Mesh (RAG pattern)**: Content → Embeddings → Vector Database → query embedding → nearest-neighbor retrieval → Prompt (query + context) → LLM → Composable Components (summarization, tagging, knowledge graphs, semantic search, code generation) → High-Value Use Cases. Data Mesh supplies GenAI the enterprise data it was never trained on; GenAI supercharges Data Mesh's own onboarding, tagging, and search burden.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-understanding-data-mesh-essentials.md) | Understanding Data Mesh - The Essentials | Dehghani's 4 principles, ANSI/ASA governance analogy |
| [ch02](chapters/ch02-applying-data-mesh-principles.md) | Applying Data Mesh Principles | FAIR data products, 5 lenses of "good," enterprise-grade attributes |
| [ch03](chapters/ch03-case-study-climate-quantum.md) | Our Case Study - Climate Quantum Inc. | Registry/marketplace/certification mapped to a concrete domain |
| [ch04](chapters/ch04-data-mesh-architecture.md) | Defining the Data Mesh Architecture | Data Product Harness, Definition/Run-Time/Operations, Fabric |
| [ch05](chapters/ch05-data-contracts.md) | Driving Data Products with Data Contracts | ODCS, Data QoS, semantic versioning, human lineage |
| [ch09](chapters/ch09-data-mesh-and-generative-ai.md) | Data Mesh and Generative AI | RAG architecture, composable components |
| [ch14](chapters/ch14-data-mesh-team.md) | Defining and Establishing the Data Mesh Team | Team Topologies, 6-role skills matrix |
| [ch15](chapters/ch15-operating-model.md) | Defining an Operating Model for Data Mesh | Operating model continuum, Conway's Law, regionalization |

## Topic Index

- **ANSI/ASA governance analogy** → ch01, ch04, ch15
- **Artifacts (data product)** → ch02, ch04
- **Climate Quantum Inc. (case study)** → ch03, ch04, ch05, ch09
- **Conway's Law** → ch15
- **Data contract / ODCS** → ch04, ch05
- **Data product harness / interfaces** → ch04
- **Data Product Owner** → ch02, ch04, ch14
- **Data QoS (quality + service levels)** → ch05
- **FAIR principles** → ch02
- **Federated governance / certification** → ch01, ch04, ch15
- **GenAI / RAG architecture** → ch09
- **Human lineage / tribal knowledge** → ch05
- **Operating model continuum** → ch15
- **Regionalization** → ch15
- **Semantic versioning (contracts)** → ch05
- **Team Topologies (Data Product/Platform/Enabling)** → ch14
- **Vector databases / embeddings** → ch09

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns
- [cheatsheet.md](cheatsheet.md) — quick reference tables and decision guides

---

## Scope & Limits

This skill covers the book content only, and only the chapters that had content at extraction time (see Early Release note above). For hands-on implementation in your codebase, combine with project-specific tools. For topics beyond this book — including the never-written chapters on building your first data quantum (Ch 6), experience planes (Ch 7), meshing data quanta (Ch 8), running/operating a Data Mesh (Ch 10), the Data Mesh Marketplace implementation (Ch 11), governance implementation (Ch 12), the Data Mesh Factory (Ch 13), and the practical roadmap (Ch 16) — check for a future edition of this skill once the book is complete, or ask the agent directly. 30 source images (figures/diagrams) were not extracted and are described only where the surrounding text explains them.
