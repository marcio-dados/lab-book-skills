# Cheatsheet

## Decision Rules

- **When you're about to add a manual data-certification gate before publishing**, replace it with a feedback loop (usage/satisfaction-driven visibility ranking) instead — manual gates don't scale in a distributed mesh. (Ch 5)
- **When a policy concern is cross-cutting** (security, legal, interoperability standard), decide it globally in the federated team, but always **execute it locally**, embedded in each data product — never through a central runtime gatekeeper. (Ch 5, Ch 9)
- **When a data product needs to correct past data**, append a new tuple with a new `processing_time` — never mutate the original. (Ch 12)
- **When a transformation is genuinely trivial (a plain query)**, don't create an intermediary data product at all — let the consumer query the source directly. (Ch 12)
- **When correlating data across two data products**, use a distributed type system (shared global IDs / schema linking) — never a fact table with foreign keys across product boundaries. (Ch 13)
- **When the source system is legacy and hard to change**, prefer domain events over change-data-capture as the input mechanism — CDC is the least desirable, last-resort option. (Ch 12)
- **When migrating off a warehouse/lake**, connect new data products directly to the domain source, never to the warehouse as an intermediary — and don't call a migration step "done" until consumers are moved AND the old pipeline is retired. (Ch 15)
- **When setting a mesh-wide adoption goal**, use "rate of new data products" or "network effect / links between data products" — never raw "number of data products," which pushes exploration in the wrong direction. (Ch 5, Ch 15)
- **When a data product only makes sense joined to others**, its boundary is wrong — redesign so it's independently meaningful. (Ch 16)
- **When two datasets in one data product change on different, unrelated triggers**, split them into separate data products — high cohesion around one life cycle is a boundary-correctness signal. (Ch 16)
- **When linking reward systems to data mesh progress**, use forward-looking OKRs (usage growth, SLO attainment) — never backward-looking bonuses tied to data-product counts. (Ch 16)

## Decision Tree: Is Data Mesh the Right Choice Now?

1. Does the organization have real data/organizational complexity (many sources, many use cases) that current warehouse/lake solutions block? → If no, **stop** — data mesh won't add value yet.
2. Is there an explicit data-oriented business strategy (not just "we should use our data better")? → If no, **stop**.
3. Is there executive/C-level backing for a multi-year transformation? → If no, **stop**.
4. Is the organization already domain-oriented (tech teams aligned to business domains)? → If no, fix that first.
5. Does the organization have modern engineering practices (CI/CD, distributed architecture) in place? → If no, build that foundation first.
6. All yes? → Proceed with a **business-driven, iterative, evolutionary** execution (Ch 15).

## Trade-off Matrix: Data Composability Approaches

| Approach | Coupling | Verdict |
|---|---|---|
| Fact/dimension tables (star/snowflake) | Tight, homogeneous-syntax assumption | Rejected for cross-product use |
| Distributed type system (GraphQL-federation style) | Loose, per-domain-owned schema | Adopted direction |
| Linked Data / JSON-LD (global URIs, ontologies) | Loose, global identifiers | Closest philosophical fit |

## Thresholds & Defaults

- **Governance metric window**: measure mesh health by network effect (interconnections used), not by petabytes/tables certified.
- **Fitness functions > KPIs**: prefer objective functions tied to each principle's outcome (e.g., "lead time to adopt a new policy") over vanity counts.
- **Manifest, not code, for target state**: declare URI, ports, SLOs, and local policies in the data product manifest; keep transformation logic and custom adapters as versioned code.
- **Observability's three pillars**: logs, traces, metrics — standardize their structure (global URI, actual/processing timestamps, output port URI) across every data product.
- **Migration atomicity**: a step is complete only when (1) new data product built, (2) consumers migrated, (3) old pipeline/tables retired — all three, together.

## Tells & Smells

- Zero-line usage/telemetry for a data product is not proof no one uses it — check whether the measurement mechanism itself is broken before concluding "unused."
- A "data product" that's really a mechanical join/glue table (no value without being combined with others) is a warehouse migration artifact, not a real data product — retire it.
- A governance group that starts meeting daily and making unilateral calls has drifted from an "enabling group" into a de facto centralized bottleneck.
- If a business initiative's data product can't be reused by any other future initiative, check whether it was scoped as a point solution instead of following domain/product boundaries.
