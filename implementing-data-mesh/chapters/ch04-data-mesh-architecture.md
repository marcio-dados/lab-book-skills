# Chapter 4: Defining the Data Mesh Architecture

## Core Idea
Every data product is built from three capability groups — Definition, Run-Time, Operations — implemented through a consistent "harness" of standardized interfaces, and the mesh itself is the connective tissue (marketplace, registry, console, fabric) that turns many autonomous data products into one coherent ecosystem.

## Frameworks Introduced
- **The Data Product Harness**: a consistent implementation layer for every interaction with a data product, exposing standardized interfaces regardless of what's underneath.
  - When to use: whenever designing how *any* data product exposes itself to the mesh — this is the architecture goal that makes templating/factories for data products possible.
  - How: implement consistent `/ingest`, `/consume`, `/discover`, `/observe`, `/control` interfaces; parameters differ per product, but interaction mechanisms stay standardized; the harness is also the integration point for data-contract and policy enforcement.
- **Three Capability Groups (Definition, Run-Time, Operations)**: Definition = owner, summary/tags, glossary, artifacts, policies. Run-Time = ingestion + consumption interfaces + policy enforcement. Operations = discoverability, observability, governance, control interfaces.
  - When to use: as the standard decomposition when designing or auditing any data product's architecture.
  - How: verify each group is explicitly addressed — a product missing "Operations" capabilities (e.g., no observability) is architecturally incomplete even if Definition and Run-Time are solid.
- **Data Mesh Fabric layers**: infrastructure services (compute/network/storage) → interaction/communication services (APIs, streaming, CDC) → data access services (federated query, pipelines, bulk transfer) → DevSecOps → data platforms (DB, lake, warehouse, lakehouse) → collaboration services.
  - When to use: when deciding what belongs to shared enterprise infrastructure vs. what belongs inside a single data product.
  - How: shared/common platforms are offered but never mandated — each data product owner retains autonomy over which fabric services to consume.

## Key Concepts
- **Data Product Harness**: the framework/code implementing all interfaces (ingest, consume, discover, observe, control) for a data product.
- **Data Mesh Marketplace**: the user-facing hub for finding, consuming, sharing, and trusting data products — with distinct UX for consumers (catalog, search), producers (usage dashboards), and admins (policy/access management).
- **Data Mesh Registry**: a DNS-like directory holding only summaries and tags for fast discovery; the low-friction, low-barrier entry point for publishing a data product.
- **Data Mesh Console**: a CLI-based counterpart to the marketplace, for scripted/automated interaction, admin tasks, and cross-product observability (lineage/provenance).
- **Data Contract**: the formal agreement covering structure/schema, access/usage rules, quality, security/privacy, versioning, lineage, and error handling — introduced here because retrofitting it later is "expensive and impractical."
- **Data Product Actors**: five roles — Data Product Owners, Data Producers, Data Consumers, Data Mesh Administrators, Data Governance Professionals.

## Mental Models
- Use the ANSI/ASA product-certification analogy (reprised from Ch 1) as the concrete mental model for "Data Product Governance": central body defines standards, data product owners self-certify, governance interfaces make certification status queryable at any time — this is what makes federated governance auditable rather than just a slogan.
- Treat the Registry-then-Marketplace flow as "phone book, then website": the Registry gives you just enough (summary + tags) to route you; the deeper interfaces (discovery, observability, governance) are where you actually evaluate the product.

## Anti-patterns
- **Adding data contracts as an afterthought**: the chapter explicitly warns that applying data contracts after a data product already exists is expensive and impractical — build the contract into the architecture from day one.
- **Inconsistent per-product interfaces**: if every data product implements ingestion/consumption differently, templating and automation ("factories") become impossible — consistency of interaction mechanism (not parameters) is the actual architecture goal.
- **Mandating enterprise tools instead of making them attractive**: repeats Ch 2's point — the Data Mesh Fabric's shared services should be adopted because they're good, not because they're required.

## Reference Tables
| Interface | Purpose | Capability Group |
|---|---|---|
| `/ingest` | bring data into the product (queries, APIs, bulk, pipelines, streaming, scraping) | Run-Time |
| `/consume` | expose data + artifacts to users (queries, APIs, bulk, pipelines, notebooks) | Run-Time |
| `/discover` | register/find the product in the mesh | Operations |
| `/observe` | usage stats, performance, lineage/provenance | Operations |
| `/control` | start/stop/pause/resume/configure | Operations |
| governance API | query/publish certification & compliance status | Operations |

## Worked Example
Climate Quantum's concrete fabric stack, reproduced from the chapter: pipelines run on **Apache Airflow**; metadata/lineage is managed by **OpenMetaData**; APIs follow the **OpenAPI specification**. Three intermediate data products (temperature, precipitation, sea level) feed the primary **Physical Risk** product, all registered through the Climate Data Registry and exposed via the Marketplace, with the Console available for admins/owners who prefer scripted, CLI-driven interaction. This shows the abstract Fabric layers (infrastructure, interaction, data access, DevSecOps, platforms) resolved into named, off-the-shelf tools — a template for choosing your own fabric stack.

## Key Takeaways
1. A data product's architecture decomposes cleanly into Definition (owner, artifacts, policies), Run-Time (ingestion/consumption/policy enforcement), and Operations (discoverability, observability, governance, control) — use this as an audit checklist.
2. The harness is what makes "every data product is different, but interacting with them is not" achievable — standardize mechanism, not content.
3. Data contracts belong in the architecture chapter, not a later one, because retrofitting them is expensive — architect for them from the start.
4. Federated governance is operationalized as a governance interface/API that makes self-certification queryable in real time, not a static document.
5. The Fabric offers shared services (compute, APIs, DevSecOps, data platforms) but data product owners retain autonomy over which to use.

## Connects To
- **Ch 1**: the ANSI/ASA governance analogy introduced there is given concrete architectural form here (governance interfaces).
- **Ch 3**: Climate Quantum's architecture is the worked instantiation of everything defined abstractly in this chapter.
- **Ch 5**: dives deep into Data Contracts, which this chapter deliberately previews rather than fully covers.
