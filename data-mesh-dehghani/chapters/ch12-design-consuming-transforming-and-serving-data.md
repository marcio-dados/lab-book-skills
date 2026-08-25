# Chapter 12: Design Consuming, Transforming, and Serving Data

## Core Idea
A data product's core job — consume, transform, serve — must satisfy analytical users' need for multimodal, longitudinal, and point-in-time-consistent data, which architecturally translates into four non-negotiable serving properties: **multimodal, immutable, bitemporal, read-only** access.

## Frameworks Introduced
- **Bitemporal Data Model**: every piece of served data carries two timestamps — **actual time** (when the event/state really occurred) and **processing time** (when the data product recorded/published its understanding of it). Processing time increases monotonically; actual time can fluctuate (corrections, late data, retractions).
  - When to use: any time a data product needs to support temporal analysis, reproducible ML training, or safe correlation across multiple independently-cadenced data products.
  - How: represent data as tuples of `{fields, actual_time, processing_time}`; a correction to the past is *appended* as a new tuple with a new `processing_time`, never an in-place update.
- **Serve Data's Four Properties**: Multimodal (same domain semantic, many serialization/access formats — SQL, files, events, graph), Immutable (once published, a data tuple never changes), Bitemporal (see above), Read-only (updates only ever happen as new appended data from the data product's own transformation code, never via a direct write API).
- **Three Consumption Archetypes** (for input data ports): collaborating operational system (tightly coupled, same domain — via domain events or, least-desirably, change data capture), other data products (standardized input/output port protocol, any domain), self (local computation/ML inference as its own source).
- **Three Transformation Styles**: nonprogrammatic (SQL/Flux/GraphQL-style set operations — simple but limited; the book advises "if it's this trivial, maybe don't create an intermediary data product at all"), programmatic (Beam/Spark/Metaflow-style code — modularizable, testable, more complex), ML-model-as-transformation (a serialized model is the transformation artifact itself).
  - How: "dumb pipes and smart filters" — a dataflow/pipeline style is fine **inside** a single data product's boundary (bounded blast radius, deployed/tested/versioned as one unit); it is never acceptable as an architecture spanning *between* data products.

## Key Concepts
- **Skew**: the time difference between actual time and processing time — always present in practice (true zero-skew real-time systems are rare), and it grows the further a data product sits from the original source. Skew is communicated, not hidden.
- **Retraction**: a correction to previously-published data, always implemented as new data with a new processing time (never a mutation) — e.g., a listener count corrected from 3,000 to 2,005 becomes a second tuple, not an edit of the first.
- **Windowing**: aggregating upstream events over a time span (e.g., a listening "session") — a time-aware operation data users can perform because actual time is always present in the data.
- **Crypto shredding**: the mechanism for the one legitimate exception to "no direct updates" — GDPR's right to be forgotten is implemented as a privileged **control port** operation (not an output-port write) that destroys encryption keys held by the platform, rendering previously-served ciphertext permanently unreadable.
- **Input port synchronizer**: temporary storage that holds partially-arrived data until all the independent sources a transformation depends on (e.g., two upstream data products) have delivered what's needed for that processing cycle.

## Mental Models
- **"No man can cross the same river twice" (Heraclitus, on immutability)**: once a piece of data is published, it is a fact about a specific processing time — it does not change; the "river" (the data product's overall state) evolves only by appending new, distinctly-timestamped tuples.
- **"Processing time is the only time that moves forward monotonically"**: use processing time, not actual time, as the reliable index/cursor for consumers tracking what they've already read — actual time can arrive out of order or be corrected retroactively.
- **The "deadly diamond" of inconsistent correlation**: two downstream data products (e.g., `artists_regional_popularity` and `regional_market_size`) each derived from the same upstream source but refreshed on different cadences can silently combine pre-update and post-update data unless bitemporality make the mismatch visible and preventable.
- **Push complexity control upstream via increased processing latency, not downstream cleansing**: if a source-aligned data product (e.g., `play_events`) is prone to missing/out-of-order signals, the fix is to widen its own processing-time window to reconcile before publishing — not to let every downstream consumer implement its own cleansing logic.

## Anti-patterns
- **Building a nonprogrammatic-only data product that's just a passthrough query**: if the transformation is genuinely trivial (a plain SQL select), don't create an intermediary data product at all — let consumers query the source directly; adding a pass-through product only adds a hop with no value.
- **Treating updates/deletes as a normal output-port capability**: read-only is a hard design constraint — the only sanctioned exception (right to be forgotten via crypto shredding) is deliberately routed through the privileged control port, never the regular data-serving API.
- **Pipelines that span multiple data products**: acceptable and even encouraged *inside* one data product's boundary; unacceptable as a cross-data-product architecture — that's exactly the "smart pipes" pattern data mesh replaces with "dumb pipes, smart endpoints/filters."
- **Ignoring skew and treating "the data" as if it reflects the present moment**: analytical consumers must be told (and design for) the gap between when something happened and when the mesh knows about it — pretending it's zero produces subtly wrong analysis.

## Reference Tables
| Serving property | Why it's required | What it prevents |
|---|---|---|
| Multimodal | Diverse consumer personas need native access (SQL, files, streams, graph) | Forcing every consumer through one unnatural access mode |
| Immutable | Reproducible analysis/ML training; safe cross-product correlation | Non-repeatable results, silent data drift under the same query |
| Bitemporal | Reflects both when something happened and when it was known | The "deadly diamond" of correlating data at inconsistent freshness |
| Read-only | Updates are always transformation-derived appends, never external writes | Distributed-transaction complexity; loss of point-in-time consistency |

| Consumption archetype | Coupling | Typical mechanism |
|---|---|---|
| Collaborating operational system | Tight, same domain | Domain events (preferred) or change data capture (legacy, least desirable) |
| Other data product | Loose, any domain | Standardized input/output port protocol |
| Self | N/A | Local computation / ML inference using locally stored reference data |

## Key Takeaways
1. Serve data as multimodal, immutable, bitemporal, and read-only — these four properties are structural requirements of a distributed, eventually-consistent mesh, not stylistic choices.
2. Bitemporal modeling (actual time + processing time) is what makes retractions, skew, windowing, and reproducible time travel all work without ever mutating already-published data.
3. Consumption has three archetypes (operational system, other data product, self); prefer domain events over change-data-capture when integrating with an operational source.
4. Choose the simplest adequate transformation style — don't reach for programmatic pipelines when a plain query would do, and don't build an intermediary data product for a trivial passthrough.
5. Pipelines are fine *inside* one data product; never let a pipeline architecture span across data product boundaries — "dumb pipes, smart filters" applies to inter-product data flow.
6. The only legitimate write to already-served data (crypto-shredding for right-to-be-forgotten) is routed through the control port, never through the regular output-port read APIs.

## Connects To
- **Ch 9**: input/output ports and the sidecar/control-port machinery this chapter builds directly on.
- **Ch 11**: this chapter is the detailed design of the "Serve Data," "Consume Data," and "Transform Data" affordances introduced there.
- **Ch 13**: "Compose Data" (correlating multiple bitemporal data products) depends on the immutability/bitemporality established here.
- **Ch 5**: the "right to be forgotten" governance policy whose mechanism (crypto shredding via control port) is specified here.
