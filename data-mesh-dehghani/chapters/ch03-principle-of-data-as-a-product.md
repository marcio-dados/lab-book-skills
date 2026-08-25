# Chapter 3: Principle of Data as a Product

## Core Idea
Apply product thinking to domain-owned data — the second principle exists specifically to counter the siloing risk that domain ownership (Ch 2) introduces, by making every data product discoverable, addressable, understandable, trustworthy, natively accessible, interoperable, valuable on its own, and secure.

## Frameworks Introduced
- **Data Product Usability Attributes (DATNIVS)** — Discoverable, Addressable, Trustworthy/truthful, Natively accessible, Interoperable, Valuable on its own, Secure, plus Understandable — the eight non-negotiable baseline characteristics every data product must have to be part of the mesh.
  - When to use: as an acceptance checklist before any dataset is published to the mesh as a "data product."
  - How: walk each attribute from the data user's journey (discover → access → understand → trust → use), not from the technical implementation's point of view.
- **Data + Code as One Unit ("code serves data")**: inverts the microservices relationship (where data serves code/state) — the data product is a single deployable unit bundling data, metadata, transformation code, and policy.
  - When to use: whenever tempted to separate "the pipeline" from "the dataset it produces" as independent artifacts — that separation is what produces data swamps.
- **New roles: Data Product Owner / Data Product Developer**: product-management accountability embedded inside the domain team, not centralized.

## Key Concepts
- **Data product**: the unit of value exchange in the mesh — not merely "data," but data packaged with the guarantees (SLOs) and interfaces that make it usable by someone else without hand-holding.
- **Service-level objectives (SLOs) of a data product**: interval of change, timeliness, completeness, statistical shape, lineage, precision/accuracy over time, operational qualities (freshness, availability, performance) — the objective measures that build trust instead of requiring detective work through lineage.
- **Polyseme**: (carried over from Ch 2) a shared entity like "artist" that must be identifiable consistently for interoperability across data products.
- **"Trust but verify" culture**: shifting the default assumption from "data is guilty until proven innocent" (requiring lineage investigation) to trust established at the point of creation via automated tests and guarantees.

## Mental Models
- **"Shift left" for data quality**: put the accountability for cleansing and integrity as close to the data's origin as possible, mirroring the shift-left trend in testing/ops — cheaper and more effective than fixing it downstream in a central pipeline.
- **Data as a product, not an asset**: reframes the TOGAF-style "data is an asset" metaphor, which breeds vanity metrics (dataset counts, storage volume); success is instead measured by adoption, user count, and satisfaction.
- **Reframe the vocabulary**: "ingestion" → "consumption," "extraction" → "publish/serve/share." Language shapes behavior (cites Lakoff's *Metaphors We Live By*) — words that imply passivity/intrusion produce passive/intrusive architectures.
- **Marty Cagan's product triad (feasible / valuable / usable)**: a data product must sit at the intersection of all three, same as any successful product.

## Anti-patterns
- **Mechanical "glue"/fact tables promoted to data products**: tables that exist purely to enable joins (e.g., identity-mapping tables carried over 1:1 from a warehouse migration) have no value on their own and should not exist as data products — such correlation optimizations belong to the platform, hidden from users.
- **Confusing "data as a product" with "selling data as a product"**: the principle is about product-thinking applied to internal usability, not commercialization.
- **Leaving trust to after-the-fact lineage archaeology**: if the data product doesn't guarantee its own SLOs at creation, users are forced into costly detective work every time — lineage should be a diagnostic tool for edge cases (postmortems, audits), not the default trust mechanism.

## Reference Tables
| Usability Attribute | What it answers for the data user |
|---|---|
| Discoverable | Can I find out this data exists? |
| Addressable | Can I get a permanent, unique way to reach it? |
| Understandable | Do I know what it means and how it's structured? |
| Trustworthy/truthful | Can I rely on its accuracy and guarantees (SLOs)? |
| Natively accessible | Can I consume it with the tools I already use (SQL, streaming, files, notebooks)? |
| Interoperable | Can I correlate it with other data products via shared standards/IDs? |
| Valuable on its own | Does it deliver value without requiring a join to something else? |
| Secure | Is access controlled, encrypted, and policy-governed as code? |

## Worked Example
Daff's media player domain serves two distinct data products from the same underlying facts: (1) near-real-time play events as an infinite event log — consumed by the support team to catch degrading customer experience quickly — and (2) aggregated play sessions as serialized files on an object store — consumed by the design team to understand longer-term listener journeys. Same domain, same source facts, two differently-shaped data products because the usability requirement (native access mode, latency) differs per consumer. This illustrates that "data as a product" isn't one artifact per domain — it's as many products as there are distinct usability needs.

## Key Takeaways
1. Data as a product exists specifically to prevent domain ownership from becoming domain siloing.
2. Eight baseline usability attributes are non-negotiable for anything calling itself a data product on the mesh.
3. Source-aligned data products must balance known use cases against unknown future ones — capture business reality broadly (e.g., a high-resolution event log) rather than over-fitting to today's question.
4. SLOs (not lineage investigation) are the primary trust mechanism; lineage remains useful for postmortems, audits, and edge-case debugging.
5. Data and the code that produces/maintains it are one deployable unit — never split them into "pipeline" and "orphaned dataset."
6. Reframe vocabulary deliberately: ingestion→consumption, extraction→publish/serve — language changes the culture of accountability.

## Connects To
- **Ch 2**: domain ownership is the principle this one directly counterbalances.
- **Ch 4**: the self-serve platform is what makes fulfilling these usability attributes *feasible* for every domain, not just an elite few.
- **Ch 5**: interoperability standards (global IDs, schema linking) referenced here are detailed there.
- **Ch 16**: the data product owner/developer roles introduced here are elaborated as part of the organizational model.
