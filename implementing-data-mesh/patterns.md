# Patterns & Techniques

## Federated Certification Governance (ANSI/ASA Pattern)
**When to use**: centralized data governance is bottlenecking domain teams, but full deregulation would sacrifice consistency and trust.
**How**: a lightweight central body defines standards and a certification process (like ANSI). Data product owners implement, self-verify, and publish a certification status via a governance interface/API, queryable by anyone at any time. Regular re-assessment keeps certification current.
**Trade-offs**: gains speed and local accountability; loses the guarantee of a fully audited, top-down-enforced compliance chain — trust depends on owners' honesty plus periodic spot-checks, not continuous central policing.

## Data Product Harness (Standardized Interface Layer)
**When to use**: designing how any data product exposes itself to the mesh; needed the moment you want templating, factories, or automation across multiple data products.
**How**: implement consistent `/ingest`, `/consume`, `/discover`, `/observe`, `/control` interfaces for every data product. Parameters differ per product; interaction *mechanism* stays uniform. The harness is also the integration point for data-contract and policy enforcement.
**Trade-offs**: upfront design discipline cost vs. long-term reduction in per-product integration effort and enabling of "factory" tooling.

## Data QoS Classification (Periodic-Table Pattern)
**When to use**: "data quality" alone doesn't capture the operational/temporal guarantees consumers need (retention, end-of-life, latency, time-to-repair).
**How**: classify every measurable attribute along two axes — group (Data at rest, Data in motion, Performance, Lifecycle, Behavior, Time) and time/period (does the element have a fixed sequence, like general availability before end-of-support before end-of-life?). Combine the 7 EDM Council data-quality dimensions with an open-ended set of service-level indicators.
**Trade-offs**: more upfront modeling effort than "just measure accuracy and completeness," but yields a reusable, extensible vocabulary that avoids re-litigating definitions per team.

## ODCS-Based Data Contract
**When to use**: standardizing data contracts across an organization instead of inventing a bespoke schema per team.
**How**: adopt the Open Data Contract Standard (Bitol/Linux Foundation AI & Data), a YAML format spanning 8 categories (fundamentals, dataset/schema, data quality, pricing, stakeholders, roles, SLA, custom properties). One contract per dataset+version pair; store in Git for traceability. Use semantic versioning (patch/minor/major) for every change, classified via a severity table (see cheatsheet).
**Trade-offs**: adopting an external standard costs some flexibility versus a fully bespoke format, but buys shared vocabulary, existing tooling, and cross-org portability.

## Human Lineage in the Contract
**When to use**: solving the "tribal knowledge" problem — knowing who to ask when the current data product owner is unavailable.
**How**: track stakeholder succession (role, `dateIn`, `dateOut`, `replacedByUsername`) as structured fields inside the same data contract that already tracks schema and quality — not in a separate HR system or wiki page.
**Trade-offs**: adds a maintenance burden (someone must update the contract on every personnel change) in exchange for structural, queryable continuity instead of relying on institutional memory.

## RAG-Style GenAI Architecture for Enterprise Data
**When to use**: an LLM needs to answer questions grounded in private/enterprise content it was never trained on.
**How**: normalize heterogeneous content (CSV, PDF, docs) → run an embeddings function to vectorize it → store vectors in a vector database → convert the user's query into an embedding → retrieve nearest-neighbor context → combine query + retrieved context into a prompt → send to the LLM → package the resulting capability as a reusable composable component (summarization, tagging, semantic search, code generation) rather than a one-off feature.
**Trade-offs**: requires investment in embeddings/vector-DB infrastructure and prompt engineering discipline; in return, the LLM becomes grounded in current, private, enterprise-specific content instead of only public, stale training data.

## Team Topologies for Data Mesh
**When to use**: structuring or diagnosing a Data Mesh organization — deciding who owns what.
**How**: map Data Product teams to Team Topologies' stream-aligned teams (end-to-end ownership of one product), Data Platform teams to platform teams (shared "X-as-a-Service" infra), and Data Enabling teams to enabling teams (short-term, consultative, never permanently embedded). Keep Data Product teams near the "two-pizza" size (~10-12 people).
**Trade-offs**: clean separation reduces duplicated effort and role confusion, but requires ongoing discipline to prevent Enabling teams from calcifying into a permanent second Platform/Product team.

## Conway's-Law-Aware Operating Model Selection
**When to use**: choosing (or diagnosing a mismatch in) a Data Mesh operating model.
**How**: identify the organization's real operating model on the centralized–matrixed–federated–distributed continuum by looking at actual communication/reporting patterns, then match the data architecture to it — centralized→warehouse, matrixed→data lake, federated→Data Mesh, distributed→microservices. To change the resulting architecture, change the communication structure first.
**Trade-offs**: fighting Conway's Law (imposing Data Mesh on a strongly centralized organization, for instance) costs far more in friction than adapting the target architecture — or the organization — to match.

## Hybrid Global/Regional Governance (Anti-Regionalization Pattern)
**When to use**: a Data Mesh is drifting toward regional silos (or is expected to, given regional organizational divisions) under Conway's Law.
**How**: set universal core principles centrally; allow region-specific guidelines locally; hold regular cross-regional forums; build explicit incentive structures (recognition, bonuses) for inter-regional contribution; invest in interoperable technology (integration tools, cloud platforms, APIs) that can handle diverse regional data formats.
**Trade-offs**: proactive investment in cross-regional coordination mechanisms vs. the higher, compounding cost of untangling entrenched regional silos later.
