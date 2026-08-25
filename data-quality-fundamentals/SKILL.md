---
name: data-quality-fundamentals
description: "Knowledge base from \"Data Quality Fundamentals: A Practitioner's Guide to Building Trustworthy Data Pipelines\" by Barr Moses, Lior Gavish, and Molly Vorwerck. Use when applying data observability, anomaly detection, data lineage, incident management (RCA), SLA/SLI/SLO design, or data mesh frameworks for building or troubleshooting reliable data pipelines."
origem: publico-terceiro
classificacao: nao-corporativo
tipo: livro-tecnico
idioma: en
titulo_pt: "Data Quality Fundamentals"
proveniencia:
  titulo: "Data Quality Fundamentals: A Practitioner's Guide to Building Trustworthy Data Pipelines"
  autor: ["Barr Moses", "Lior Gavish", "Molly Vorwerck"]
  editora: "O'Reilly"
  fonte_sha256: "62f794a6ff6326403fd951243b797b806bcb4da7cc4d83d3e6f24d625e9f600e"
  convertido_em: "2026-08-24"
  ferramenta_sha: "7bcfcd5262329f8d57a385903f18a98bc6705e4e"
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Data Quality Fundamentals
**Author**: Barr Moses, Lior Gavish, Molly Vorwerck | **Pages**: ~272 | **Chapters**: 10 | **Generated**: 2026-08-24

## How to Use This Skill

- **Without arguments** — load core frameworks for reference
- **With a topic** — ask about `anomaly detection`, `lineage`, `SLA`, or another indexed topic; I find and read the relevant chapter
- **With chapter** — ask for `ch04`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not covered in Core Frameworks below, I will read
the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**Data downtime** is the book's master concept: periods where data is missing, inaccurate, or otherwise erroneous — the data equivalent of application downtime in SRE. Everything in the book is in service of measuring and reducing it.

**The five pillars of data observability** — freshness, distribution, volume, schema, lineage — are the organizing axis for almost every technique in the book. Build one detector per pillar; none substitutes for another (Ch 4, Ch 5).

**Known unknowns vs. unknown unknowns**: testing (dbt, Great Expectations, Deequ) catches known unknowns — predictable failure modes you can write an assertion for. It structurally cannot catch unknown unknowns (novel drift, silent schema changes) — that's the job of monitoring/anomaly detection. The book's own estimate: testing covers ~20% of real-world issues (Ch 3, Ch 4).

**Precision/Recall/Fβ**: never tune a detector on "accuracy" (misleading for rare-event data — a detector that never alerts can still score 99%+ "accuracy"). Use Precision = TP/(TP+FP), Recall = TP/(TP+FN), and Fβ to explicitly state whether false positives or false negatives are more costly for a given use case (Ch 4).

**Field-level lineage** turns "something broke" into "here is exactly what broke and why": it maps upstream columns to downstream columns (not just table-to-table), enabling both root cause analysis and impact analysis (Ch 7).

**Five-step root cause analysis**: lineage → code → data → operational environment → peers, in that order (cheapest/most-informative first) (Ch 6).

**SLA / SLI / SLO triad** (borrowed from SRE): SLA is the promise, SLI is the measured number, SLO is the target value. A good SLA names the asset, the deadline, and the response protocol — "reliable data at all times" is not a real SLA (Ch 5, Ch 8).

**Data Downtime Total**: `DDT = N × (TTD + TTR)` — incidents times (time to detect + time to resolve). This is the equation to reach for whenever you need to justify data quality investment in dollars, not culture (Ch 5, Ch 10).

**Data mesh**: a domain-oriented, self-serve, federated-governance architecture (Zhamak Dehghani) — not a product you buy, and not real unless it distributes both infrastructure autonomy AND long-term accountability. A 5-factor readiness score (data sources, team size, domains, engineering bottleneck, governance priority) tells you if you're ready (Ch 1, Ch 9).

**Data as a product / data certification**: treating data with product-management discipline (roadmaps, KPIs, ownership via RACI) and certifying high-value tables (bronze/silver/gold) against agreed SLAs is how data quality scales past a single engineering team (Ch 8).

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-why-data-quality-deserves-attention.md) | Why Data Quality Deserves Attention—Now | Data downtime, DataOps |
| [ch02](chapters/ch02-assembling-building-blocks.md) | Assembling the Building Blocks of a Reliable Data System | Operational vs. analytical data, warehouse vs. lake, throughput/latency trade-off |
| [ch03](chapters/ch03-collecting-cleaning-transforming-testing.md) | Collecting, Cleaning, Transforming, and Testing Data | Entrypoint taxonomy, circuit breaker, ETL vs. ELT, dbt/Great Expectations/Deequ |
| [ch04](chapters/ch04-monitoring-anomaly-detection.md) | Monitoring and Anomaly Detection for Your Data Pipelines | Five pillars, known/unknown unknowns, precision/recall/Fβ |
| [ch05](chapters/ch05-architecting-for-data-reliability.md) | Architecting for Data Reliability | SLA/SLI/SLO, TTD/TTR, cost-of-downtime equation |
| [ch06](chapters/ch06-fixing-data-quality-issues-at-scale.md) | Fixing Data Quality Issues at Scale | Data reliability life cycle, five-step RCA, blameless postmortem |
| [ch07](chapters/ch07-building-end-to-end-lineage.md) | Building End-to-End Lineage | Field-level lineage, selected/non-selected fields, ANTLR parsing |
| [ch08](chapters/ch08-democratizing-data-quality.md) | Democratizing Data Quality | Data as a product, maturity curve, RACI, data certification |
| [ch09](chapters/ch09-data-quality-real-world.md) | Data Quality in the Real World: Conversations and Case Studies | Data mesh scoring, data discovery, 7 leading indicators |
| [ch10](chapters/ch10-pioneering-the-future.md) | Pioneering the Future of Reliable Data Systems | DDT equation, emerging roles, automation frontiers |

## Topic Index

- **Anomaly detection** → ch04, ch06
- **Blast radius** → ch08
- **Circuit breaker** → ch03
- **Data as a product / certification** → ch08
- **Data catalog / data discovery** → ch02, ch09
- **Data downtime cost / DDT** → ch05, ch10
- **Data mesh** → ch01, ch09
- **Data warehouse vs. data lake** → ch02
- **F-score / precision / recall** → ch04
- **Field-level lineage** → ch07, ch04, ch06
- **Five pillars of data observability** → ch04, ch05
- **Incident management / RCA** → ch06
- **RACI matrix** → ch08
- **SLA / SLI / SLO** → ch05, ch08
- **Testing (dbt, Great Expectations, Deequ)** → ch03
- **Team structures (centralized/decentralized/hybrid)** → ch08

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns
- [cheatsheet.md](cheatsheet.md) — quick reference tables and decision guides

---

## Scope & Limits

This skill covers the book content only (2022 edition; the data-tooling landscape moves fast — treat vendor/tool mentions as a snapshot of that moment, not current state). For hands-on implementation in your codebase, combine with project-specific tools. For topics beyond this book, check related skills or ask the agent directly.

The book's own diagrams/figures were not extractable from the source EPUB (image content, not embedded text) — this skill covers all prose, code listings, tables, and worked examples, but does not reproduce the ~90 figures referenced in the original text.
