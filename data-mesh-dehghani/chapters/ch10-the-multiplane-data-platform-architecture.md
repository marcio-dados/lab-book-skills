# Chapter 10: The Multiplane Data Platform Architecture

## Core Idea
Design the self-serve platform bottom-up from user journeys — data product developers, consumers (data scientists, analysts, other data-product developers), owners, governance members, and platform developers/owners — rather than from a list of technical capabilities, and expose that journey through the three planes (infrastructure utility, data product experience, mesh experience) without forcing strict layering between them.

## Frameworks Introduced
- **Five Platform User Personas**: data product developer, data product consumer (data scientist / analyst / another data-product developer / application developer), data product owner, data governance member, data platform product owner/developer.
  - How: use as the starting point for platform design — enumerate each persona's end-to-end journey before choosing any technology.
- **Data Product Development Journey (5 phases)**: Incept/Explore/Bootstrap/Source → Build/Test/Deploy/Run → Maintain/Evolve/Retire.
  - How: map each phase to concrete platform interfaces per plane (see reference table) — this is the book's own worked template for designing a self-serve platform's API surface.
- **CD4ML applied to ML-as-data-product**: an ML model's journey (hypothesize → explore/source → train/test → deploy → monitor/improve) maps almost 1:1 onto the data product developer journey, with the ML model becoming the transformation code of a data product (e.g., `monday_playlists`).

## Key Concepts
- **Plane responsibilities**: Infrastructure (utility) plane = low-level resource provisioning (storage, compute, identity) shared with operational systems; Data Product Experience plane = operations on *one* data product (build/test/deploy/run/monitor); Mesh Experience plane = operations across *many* data products (search, lineage, global policy, mesh-wide monitoring).
- **"Harvesting" pattern**: when a data product developer must drop to the infrastructure plane because the data product experience plane doesn't yet support something (e.g., a graph-query output port), that gap is a signal to eventually build the capability into the standard experience plane — an evolutionary path for growing the platform's abstraction coverage.
- **Dormant vs. retired data product**: a data product with no new transformations but still serving historical data to lingering consumers is dormant (still enforces policy); a data product with zero future consumers and all records purged is fully retired/extinct — a graceful, two-stage decommissioning path.
- **Bimodal ML deployment**: an ML model can be deployed as a microservice (operational plane, online inference) or as a data product's transformation code (analytical plane, batch/periodic inference) — the same model artifact, two different architectural homes depending on the consumption pattern.

## Mental Models
- **"There is no single entity called a platform"**: the platform is a well-integrated set of APIs/services/SDKs satisfying journeys — not a monolithic product to buy. Design for the seams between data-mesh services, operational APIs, and ML-training tooling, since real journeys cross all three.
- **"Optimize the human experience and the machine efficiency separately, by plane"**: the data product experience plane should optimize for developer/consumer delight; the infrastructure utility plane should optimize for resource efficiency (compute/storage separation, colocation) — conflating the two produces a platform that is either inefficient or unpleasant to use.
- **Processing-time versioning instead of copying data for ML repeatability**: since a data product always allows retrieving past data via its processing-time dimension, an ML pipeline doesn't need to keep its own copy of training data for reproducibility — it just records which processing-time revision was used.

## Anti-patterns
- **Designing the platform from a capability checklist instead of a user journey**: produces a platform that has all the "right" components (catalog, orchestrator, storage) but doesn't reduce friction for any actual persona's end-to-end task.
- **Letting master/aggregate data products silently become bottlenecks**: the mesh experience plane's monitoring should specifically detect data products aggregating from too many sources and becoming an unplanned point of centralization — an operational health signal, not just a modeling concern (ties back to Ch 2's caution on ambitious aggregates).
- **Copying training data "just in case" for ML reproducibility**: treated as an artifact of poor data versioning (mitigated historically with tools like DVC) — the intended data mesh pattern is to rely on the source data product's own processing-time revisioning instead.

## Reference Tables
| Development phase | Platform plane | Example interface | Purpose |
|---|---|---|---|
| Incept/Explore | Mesh experience | `/search`, `/knowledge-graph`, `/lineage` | Find and evaluate candidate upstream sources |
| Bootstrap/Source | Data product experience | `/{dp}/discover`, `/{dp}/observe`, `/init`, `/connect` | Scaffold a data product and connect to sources |
| Bootstrap/Source | Mesh experience | `/register` | Assign a global identifier/address, make visible to governance |
| Build/Test/Deploy/Run | Data product experience | `/build`, `/test`, `/deploy`, `/start`, `/stop`, `/local-policies` | Deliver and run the data product |
| Build/Test/Deploy/Run | Mesh experience | `/global-policies` | Apply federally-authored policies to all data products |
| Build/Test/Deploy/Run | Data infrastructure | `/input-ports`, `/output-ports`, `/transformations`, `/containers`, `/controls`, `/storage`, `/models`, `/identities` | Low-level provisioning delegated to by the experience plane |
| Maintain/Evolve/Retire | Data product experience | `/{dp}/status`, `/{dp}/logs`, `/{dp}/cost`, `/{dp}/controls`, `/migrate` | Operate and evolve a running data product |
| Maintain/Evolve/Retire | Mesh experience | `/monitor`, `/notifications`, `/global-controls` | Mesh-wide health, alerting, and privileged operations (e.g., right to be forgotten across many data products) |

## Key Takeaways
1. Start platform design from user journeys (developer, consumer, owner, governance, platform team), not from a feature list.
2. The three planes map cleanly to the development journey's three phases: mesh experience for discovery, data product experience for build/run, infrastructure for the underlying resources.
3. Planes are not strictly layered — dropping to a lower plane is allowed and expected as a temporary escape hatch, with the intent to harvest that capability upward later.
4. ML models fit the data product journey almost exactly, with processing-time-based data revisioning replacing the need to physically copy training datasets for reproducibility.
5. Retirement is graceful and two-staged (dormant → extinct), never an abrupt deletion that breaks lingering consumers.

## Connects To
- **Ch 4**: elaborates the platform-thinking objectives introduced there into concrete phase-by-phase interfaces.
- **Ch 9**: the three planes and their APIs implement the logical architecture (data quantum, sidecar, ports) defined there.
- **Ch 11–14**: Part IV picks up "data product affordances" as the next level of design detail beyond the platform interfaces sketched here.
