# Cheatsheet

## Decision Rules

- **When governance feels like a bottleneck**, do federated/certification governance (central standards, self-certified compliance, queryable status), because top-down policing doesn't scale to decentralized ownership. (Ch 1, Ch 4, Ch 15)
- **When a data product is missing an empowered owner**, stop and fix that first — the book states plainly that no other "good data product" attribute compensates for its absence. (Ch 2)
- **When you're about to launch a data product without a contract**, write the contract now, because retrofitting it later is "expensive and impractical." (Ch 4, Ch 5)
- **When a schema/API change is proposed**, classify it patch/minor/major using the severity table before deciding how to version it — don't eyeball it. (Ch 5)
- **When an LLM is asked about enterprise-specific facts**, assume it doesn't know unless the answer was retrieved through a RAG-style pipeline (embeddings + vector DB + your content) — the model's training data structurally excludes private data. (Ch 9)
- **When a Data Mesh initiative stalls**, check operating-model fit before blaming technology: a centralized organization will resist a Data Mesh architecture via Conway's Law regardless of tooling. (Ch 15)
- **When staffing a Data Product team**, verify all six roles are covered (Owner, Release, Metadata/Governance, Security, Consumption, Ingestion) — a gap in any one leaves a structural hole, not just a staffing inconvenience. (Ch 14)
- **When enterprise tooling isn't being adopted voluntarily by domain teams**, don't mandate it — make it good enough that owners choose it, because owners retain decision rights under Data Mesh principles. (Ch 2, Ch 4)

## Decision Tree: Choosing an Operating Model / Architecture

1. Is decision-making concentrated at the top, with strong uniformity needs (e.g., regulated manufacturing)? → **Centralized** → centralized data warehouse.
2. Do teams need cross-functional access to diverse data with dual reporting lines? → **Matrixed** → data lake.
3. Do domain units need real autonomy but must align to shared enterprise policy? → **Federated** → **Data Mesh** (the default target for most Data Mesh initiatives).
4. Are units fully self-governing with minimal central coordination (e.g., open-source foundation model)? → **Distributed** → microservices-for-data.
5. Regardless of answer above: if regional divisions exist, assume regionalization will emerge (Conway's Law) — pre-empt with hybrid global/regional governance.

## Trade-off Matrix: Operating Models

| Model | Consistency/Control | Agility | Governance Complexity | Natural Data Architecture |
|---|---|---|---|---|
| Centralized | High | Low | Low (single authority) | Data warehouse |
| Matrixed | Medium | Medium-High | Medium (dual reporting conflicts) | Data lake |
| Federated | Medium | High | Medium (needs certification model) | Data Mesh |
| Distributed | Low | Very High | High (no central authority) | Microservices |

## Thresholds & Defaults

- **Data Product team size**: ~10-12 people ("two-pizza team") is the practical ceiling.
- **Contract versioning**: column addition = minor; column type/name change or removal = major; metadata/stakeholder edits = patch.
- **7 data quality dimensions** (EDM Council, used in Data QoS): Accuracy, Completeness, Conformity, Consistency, Coverage, Timeliness, Uniqueness.
- **Data contract cardinality**: exactly one contract per dataset+version pair (a product can have many contracts).
- **GenAI grounding boundary**: assume any LLM's knowledge stops at its training cutoff and excludes all private/enterprise data, by default.

## Tells & Smells

- If a data product has no Data Product Owner named, its "good data product" attributes (FAIR, enterprise-grade, valuable) are moot — fix ownership first.
- If governance decisions are made by a group detached from the data's actual context, expect misalignment and bottlenecks — a signal to move toward certification-based federated governance.
- If Data Product teams are quietly maintaining their own infrastructure, the Platform team boundary has eroded.
- If an Enabling team has been embedded with one Product team for months, it has effectively become an undisclosed second Platform/Product team.
- If a Data Mesh keeps producing regional variants of the same product with incompatible schemas, that's Conway's Law manifesting as regionalization — respond with hybrid governance, not just a mandate for uniformity.
- If an LLM confidently answers a question about internal company data it was never given, the answer is unsupported — verify it was retrieved via the RAG pipeline, not hallucinated from public training data.
