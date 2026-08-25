# Chapter 9: Data Quality in the Real World: Conversations and Case Studies

## Core Idea
Five industry-defining trends — the data mesh, cloud consolidation, knowledge graphs, data discovery, and the "when to start" question — all ultimately hinge on the same requirement: distributed, self-serve data ownership only works if it's paired with equally distributed data quality and trust mechanisms.

## Frameworks Introduced
- **Data mesh scoring rubric**: sum five factors — # data sources, data team size, # data domains, data engineering bottleneck severity (1–10), data governance priority (1–10).
  - When to use: before deciding to invest in a data mesh migration.
  - How: score 1–15 → probably don't need a mesh yet; 15–30 → adopt mesh *concepts* now to ease a future migration; 30+ → you're in the mesh sweet spot.
- **Data mesh's four defining elements** (per Zhamak Dehghani, direct interview): (1) distribute data ownership to domain teams, (2) give those teams long-term accountability + product thinking, (3) empower with self-serve infrastructure, (4) address new problems via federated governance — a mesh missing any of these four is "just overengineering a centralized team's distribution."
- **Seven leading indicators it's time to invest in data quality**: recent cloud migration; scaling data sources/tables/complexity (~50+ tables is a rough threshold); growing data team; ≥30% of time firefighting; more data consumers than a year ago; moving to self-service analytics; data is part of the customer-facing product.

## Key Concepts
- **Data mesh vs. data virtualization**: virtualization exposes OLTP/microservice data as-is for analytical use — Dehghani explicitly warns this is *not* a data mesh; analytical and operational data need genuinely different, transformed views.
- **Federated data catalog / data discovery**: the mesh-native alternative to a traditional catalog — automated, real-time, and reflecting the *current* state of data rather than a manually maintained "ideal" state.
- **Data mesh self-serve capabilities** (per Dehghani): encryption at rest/in motion, product versioning, product schema, product discovery/catalog registration, governance/standardization, product lineage, product monitoring/alerting/logging, product quality metrics.

## Anti-patterns
- **Building a mesh with a single tool**: "you wouldn't build a microservice architecture with just a database" — a mesh is an organizational/socio-technical shift, not a product you buy.
- **Each domain team running its own separate storage layer**: Dehghani is explicit this is *not* required — autonomy over schema/access/tenancy, yes; duplicated infrastructure, no.
- **Lineage/metadata without a business use case**: "eye candy" (Dehghani's framing) — lineage only has value applied to a specific decision (impact analysis, RCA, or communicating an incident), not as a demo feature.
- **Traditional catalogs in a data lake or mesh**: manual catalogs don't scale to unstructured, distributed, rapidly-evolving data — they were designed for structured warehouse tables.

## Worked Example
**Kolibri Games' 5-year data stack evolution** (a compact case study in "when to invest in what"):
1. **2016** — third-party tools only (Facebook Analytics, Firebase, GameAnalytics); pain: scattered analytics, no KPI transparency.
2. **2017** — added AppsFlyer for performance marketing; pain: no version control on bidding scripts, "basically blindfolded."
3. **2018** — first proprietary stack (Azure Data Factory/Event Hubs/Stream Analytics, Power BI → Looker); pain: SQL database contention between jobs and ad hoc queries, silent job failures.
4. **2019** — added Databricks, then replaced the SQL DB with Snowflake as the compute engine; pain: A/B testing still not transparent, decisions still made on intuition.
5. **2020 (post-Ubisoft acquisition)** — introduced data-specific SLAs, ELT with dbt, Airflow orchestration, domain-specific ownership; explicit KPI: "90% of decisions on Idle Miner Tycoon must be data-backed, time-to-insight <1 hour for 90% of questions."
6. **2021** — invested in end-to-end lineage + observability tooling to formalize the emerging data mesh.

António Fitas's five takeaways: build your own stack (it pays off), know when to swap technology, prioritize observability for trust, get the basics (like hiring analysts) right early, and culture matters more than tooling.

## Reference Tables
| Data mesh score | Recommendation |
|---|---|
| 1–15 | Don't need a mesh yet |
| 15–30 | Adopt mesh concepts now, ease future migration |
| 30+ | You're in the mesh sweet spot |

| Leading indicator | Why it signals "invest now" |
|---|---|
| Recent cloud migration | Users need proof the new stack is as trustworthy as the old one |
| 50+ tables, growing complexity | More moving parts = more break points |
| Growing data team | Tacit knowledge concentration risk increases |
| ≥30% time firefighting | Direct opportunity-cost signal |
| More data consumers YoY | More eyes = more (valid) complaints |
| Moving to self-service analytics | Trust is the prerequisite for adoption |
| Data is customer-facing | Reliability bar rises to product-grade |

## Key Takeaways
1. The data mesh is a socio-technical shift (ownership + accountability + self-serve infra + federated governance), not a technology purchase — evaluate readiness with the 5-factor score before starting.
2. Lineage and metadata are only valuable when tied to a specific use case (impact analysis, RCA, communication) — collecting them for their own sake is wasted effort.
3. Traditional data catalogs break down in lakes/meshes because they assume structured, centrally-updated data; data discovery tools (automated, real-time) are the mesh-native replacement.
4. Use the seven leading indicators as a checklist to decide "is it time to invest in data quality" rather than waiting for a costly incident to force the question.

## Connects To
- **Ch 1**: revisits and deepens the data mesh concept first introduced there.
- **Ch 2**: extends the data catalog vs. data discovery discussion from Ch. 2 into the mesh/lake context specifically.
- **Ch 10**: the "when to invest" question here leads directly into the cost-justification framework in the final chapter.
