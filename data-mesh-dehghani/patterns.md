# Patterns & Techniques

## Bitemporal Data Serving
**When to use**: any data product needs safe temporal analysis, reproducible ML training, or safe correlation across other independently-cadenced data products.
**How**: tag every served tuple with `actual_time` (when it really happened) and `processing_time` (when the data product recorded/published it). Corrections are always new appended tuples with a new processing time, never in-place mutations. Consumers use processing time as their monotonic read cursor.
**Trade-offs**: adds modeling and storage overhead versus a simple mutable table, but is what makes point-in-time-consistent cross-product correlation and reproducible ML training possible without distributed transactions.

## Federated Computational Governance
**When to use**: centralized, manual data governance has become a bottleneck, but full deregulation would sacrifice interoperability and compliance.
**How**: a federated team (domain product owners + platform reps + SMEs) decides *global* policies only for genuinely cross-cutting concerns (security, legal, interoperability standards); everything else stays local to the domain. Global policies are always executed locally — embedded as code in each data product's sidecar/control port, never via a central runtime gatekeeper.
**Trade-offs**: requires investment in policy-as-code platform capability up front; in exchange, governance stops being a synchronization bottleneck as the mesh scales.

## Dynamic Equilibrium via Feedback Loops
**When to use**: balancing domain autonomy against mesh-wide consistency (e.g., preventing duplicate/low-quality data products) without a manual certification gate.
**How**: use discoverability/observability signals (usage, satisfaction ratings) to drive a *balancing* feedback loop (low-quality/duplicate products get less visibility, naturally pruned) and a *reinforcing* loop ("success to the successful" — high-quality products get more visibility). Tune leverage points (e.g., system goals) deliberately — "number of data products" as a goal pushes the wrong direction; "rate of new data products" or "network effect" doesn't.
**Trade-offs**: requires building observability/ranking infrastructure, but replaces a manual certification bottleneck with a self-correcting, automatable mechanism.

## Data Product as Architecture Quantum
**When to use**: designing the unit of scale-out for any data mesh implementation.
**How**: bundle transformation code, interfaces-as-code (input/output/discovery/control ports), policy-as-code, data + metadata, and platform dependency declarations into one independently-deployable unit. Scale the mesh by adding more quanta, never by growing one shared component.
**Trade-offs**: more upfront design discipline per data product than a shared pipeline/warehouse table, but yields autonomous, independently-deployable, loosely-coupled nodes that don't create cross-team synchronization bottlenecks.

## Distributed Type System for Composability
**When to use**: correlating/joining data across independently-owned data products without a shared central schema.
**How**: each data product owns and versions its own semantic schema; schemas reference/extend types owned by other data products (GraphQL-federation style) or link via globally unique URIs (Linked-Data/JSON-LD style). Shared entities ("polysemes" like *artist*) get a global identifier minted by their owning data product.
**Trade-offs**: rejects the speed/simplicity of fact-table joins in a single warehouse schema, in exchange for loose coupling that lets each data product's schema evolve independently.

## Design by Affordances
**When to use**: designing any data product capability (serve, consume, transform, discover, compose, manage, govern, observe).
**How**: for each capability, explicitly name which agents (people or systems) it affords which actions to — and, just as importantly, which actions it deliberately does NOT afford (e.g., serving data affords analytical reads, not transactional updates). Borrow from complex adaptive systems: design simple local rules per data product (its own ports) and let mesh-level properties (lineage graphs, knowledge graphs) emerge, never centrally author them.
**Trade-offs**: requires more deliberate design thinking than "add a feature," but prevents a data product from accidentally affording unsafe/unintended usage.

## Business-Driven, Atomic-Step Legacy Migration
**When to use**: migrating off an existing data warehouse/lake toward data mesh.
**How**: connect new data products directly to domain sources (never to the warehouse/lake as an intermediary); treat a migration step as complete only when all three happen together: new data product built, its consumers migrated to it, and the old pipeline/tables retired. A warehouse may remain only as a shrinking "edge consumer node" for reports too costly to reverse-engineer.
**Trade-offs**: slower than a big-bang cutover, but each atomic step actually reduces architectural entropy instead of accumulating parallel old-and-new systems.

## Team Topologies for Data Mesh
**When to use**: structuring or diagnosing a data mesh organization.
**How**: map domain data product teams to stream-aligned teams (end-to-end ownership); the data platform to a platform team (capabilities as-a-service); federated governance to a looser enabling "group" (not a standing team) that collaborates with both, explicitly avoided from becoming a bottleneck. Minimize complicated-subsystem teams (e.g., encryption, anomaly detection specialists).
**Trade-offs**: requires deliberate boundary discipline (see data product boundary heuristics), but keeps governance from recreating the very centralization data mesh removes.

## Movement-Based Organizational Change
**When to use**: driving the cultural/organizational shift required by data mesh adoption.
**How**: select early "beacon" business initiatives aligned with the specific organizational objective at hand (e.g., establishing domain ownership), staffed by the domains most receptive to change; let their visible wins build momentum for wider adoption, matched to the same iterations that deliver technical value (Ch 15's execution framework).
**Trade-offs**: slower than a top-down mandate, but produces durable buy-in instead of resistance, and lets the change be refined by the people actually doing it.
