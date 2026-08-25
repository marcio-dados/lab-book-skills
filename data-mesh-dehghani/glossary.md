# Glossary

**Actual time** — the timestamp when an event really occurred or a state really existed in the business, as opposed to when the data product learned about it. (Ch 12)

**Aggregate domain data** — analytical data composed from multiple upstream source-aligned domains into a shared, higher-order concept (e.g., a "listener 360" view); the book cautions against making these too ambitious. (Ch 2)

**Bitemporal data** — data modeled with two timestamps, actual time and processing time, enabling immutability, retractions, and time travel without ever mutating already-published data. (Ch 12)

**Bounded context** (DDD) — the delimited applicability of a particular model, giving a team a clear, shared understanding of what must be consistent internally vs. what can evolve independently; data mesh maps this to each data product. (Ch 2)

**Complex adaptive system** — the lens used to design mesh-level behavior (lineage, knowledge graph) as emergent from simple local rules in each data product, with no central orchestrator. (Ch 11)

**Consumer-aligned (fit-for-purpose) domain data** — analytical data transformed to fit one or a small group of specific consumption use cases (e.g., ML features). (Ch 2)

**Control port** — a data product's standardized interface to configure policies and invoke privileged governance operations (e.g., GDPR's right to be forgotten via crypto shredding). (Ch 9, Ch 12, Ch 14)

**Crypto shredding** — the mechanism for honoring "right to be forgotten": destroying encryption keys (held by the platform) to render previously-served encrypted data permanently unreadable, without mutating the immutable record. (Ch 12)

**Data as a Product** — the second of the four data mesh principles: apply product thinking (discoverable, addressable, trustworthy, valuable on its own, etc.) to domain-owned data. (Ch 3)

**Data contract** — the versioned, backward-compatible guarantee a data product makes to its consumers, allowing domains to change their models continuously without breaking downstream users. (Ch 7)

**Data mesh** — a decentralized sociotechnical approach to share, access, and manage analytical data at scale, built on four principles: domain ownership, data as a product, self-serve data platform, federated computational governance. (Ch 1)

**Data (product) quantum** — data mesh's architecture quantum: the smallest independently-deployable unit encapsulating code, data, metadata, policy, and infrastructure dependencies needed to autonomously serve a data product. (Ch 9, Ch 11)

**Data product manifest** — a declarative specification (à la Kubernetes/Istio) of a data product's target state: URI, ports, SLOs, local policies, source artifact references. (Ch 14)

**Data product sidecar** — a platform-provided process sharing a data product's runtime context, executing standardized cross-cutting concerns (policy execution, discovery APIs) — the same pattern as a service-mesh sidecar. (Ch 9, Ch 14)

**Dumb pipes, smart filters/endpoints** — the principle that pipeline-style transformation is fine *inside* one data product's boundary but must never span across data products. (Ch 12)

**Federated computational governance** — the fourth principle: global policies decided by a federation of domain/platform/SME representatives, enforced by automated, embedded code in every data product — never by manual central gatekeeping. (Ch 5)

**Fitness function** — an objective function (borrowed from evolutionary computing) measuring how "fit" the mesh implementation is toward its target outcomes; preferred over vanity KPIs. (Ch 15)

**Input/output data port** — a data product's mechanism to consume from upstream sources (input) or serve data externally (output), with explicit contracts per port. (Ch 9, Ch 12)

**Manifest** — see *Data product manifest*.

**Multiplane platform** — the self-serve platform's three planes: Data Infrastructure (Utility), Data Product Experience, Mesh Experience — deliberately not "layers," since users may cross planes directly. (Ch 9, Ch 10)

**Polyseme** — a shared business concept (e.g., "artist," "listener") modeled differently across domains but mappable via a global identification scheme. (Ch 2, Ch 5, Ch 13)

**Principle of Domain Ownership** — decentralize analytical data ownership to the business domains closest to its origin or primary use, following DDD bounded contexts. (Ch 2)

**Principle of the Self-Serve Data Platform** — extract domain-agnostic infrastructure into a platform so generalist technologists can build/consume data products autonomously. (Ch 4)

**Processing time** — the timestamp when a data product processed, recorded, and published its understanding of an actual-time event; the only time guaranteed to move forward monotonically. (Ch 12)

**Skew** — the time difference between actual time and processing time; always present in practice and grows the further a data product sits from the original source. (Ch 12)

**Source-aligned domain data** — analytical data reflecting business facts as generated by their origin operational system, captured as close to reality as possible, never modeled directly off the source's transactional database. (Ch 2)

**Team Topologies** (applied to data mesh) — domain data product teams = stream-aligned; platform teams = platform (x-as-a-service); governance = enabling teams/looser groups. (Ch 16)

**Trust metrics / SLOs** — objective, categorized guarantees (quality, maturity, standards conformance, temporality, user-driven) a data product shares to build trust without lineage archaeology. (Ch 3, Ch 13)
