# Chapter 14: Design Managing, Governing, and Observing Data

## Core Idea
The last three data product affordances — manage life cycle (via a declarative **manifest**), govern (via embedded policy-as-code enforced through the control port/sidecar), and observe (via standardized logs/traces/metrics) — all share the same inversion: responsibility moves from an external party inspecting things after the fact to the data product itself generating and exposing this information as a first-class part of its design.

## Frameworks Introduced
- **Data Product Manifest**: a declarative specification (inspired by Kubernetes/Istio manifests) of a data product's target state — URI, output ports + their SLOs, input ports, local policies (locality, confidentiality, privacy, retention), and a description of its source artifacts (transformation code, queries). The manifest is developer-experience-centric: it declares *what*, and the platform figures out *how* to provision it, keeping the data product portable across underlying implementations.
  - When to use: as the single artifact a data product developer maintains to communicate infrastructure needs — imperative logic (transformation code, custom adapters) stays as code; everything declarative about target state belongs in the manifest.
- **Policy as Code, embedded and linked**: policies (encryption, access control, privacy/consent) are versioned, tested, and executed like any other code, embedded in the data product's sidecar/control port — and can be **linked** across data products so that when data flows downstream, its governing policy travels (and conceptually breaks) with it exactly as far as the data's lineage is traceable.
- **Three Observability Pillars** (borrowed directly from operational/microservices observability): Logs (immutable, timestamped, structured events — e.g., when new data arrived, transformation steps taken), Traces (causally related distributed events — in data mesh, used to construct data *lineage* across input/output ports rather than a call-tree), Metrics (quantifiable, timestamped build/runtime characteristics — the same trust metrics introduced in Ch 13).
  - How: standardize the *structure* of all three pillars across every data product (common fields: global URI, actual/processing timestamps, output port URI) so mesh-level tooling can aggregate them without special-casing each data product.

## Key Concepts
- **Standardize Policies (esp. Identity & Access Control)**: the book explicitly flags that analytical data has *not* reached the standardization operational APIs achieved (OpenID Connect, JWT, X.509, SPIFFE) — a named gap, and a place where data mesh's cross-vendor sharing motivation could be the catalyst for progress.
- **Data + Policy Integration**: because the data quantum bundles data, code, and policy as one unit, consent/privacy policy cannot be silently lost when data crosses a technical storage boundary the way it can in decoupled architectures — linking policy to data (not to a separate system) is what preserves this.
- **Domain-oriented observability**: apply domain-driven thinking to observability itself — e.g., a "data quality" domain producing its own data product of quality metrics across the mesh — rather than lumping all observability signals into one undifferentiated bucket (echoing the anti-metadata stance from Ch 9/13).
- **Traceability across the operational/analytical boundary**: since source-aligned data products originate from operational systems, full lineage/root-cause analysis must extend traces back into the operational plane, not stop at the data product's own input port.

## Mental Models
- **"Never tell people how to do things. Tell them what to do" (Patton, epigraph)**: the manifest philosophy in one line — declare the target state (what), leave the platform to figure out the mechanism (how).
- **"Don't control, but observe" (Hohpe, epigraph)**: governance and observability in data mesh are not about a central authority policing every action — they're about designing each data product to honestly expose enough about itself that trust and correction can happen locally and automatically.
- **"One must invert, always invert" (Jacobi, chapter's closing thought)**: the chapter's single unifying takeaway — every capability discussed (manifest, policy, observability) inverts the traditional model of "an external party checks after the fact" into "the data product declares/exposes it continuously, by design."
- **Four recurring design characteristics across all affordances**: Standardization (common structure for mesh-wide interoperability), Emergence (mesh-level insight — like lineage — emerging from individual local outputs, never centrally authored), Agency (each data product actively shares its own state), Extensibility (new policies/capabilities can be added over time without redesign).

## Anti-patterns
- **Treating policy configuration as separate from the data it governs**: when consent/privacy policy lives in a system disconnected from the data itself, tracking and honoring that consent breaks down the moment data crosses a storage boundary — bundle policy with the data quantum instead.
- **Relying on proprietary, per-vendor identity/access-control schemes for analytical data**: increases friction and cost of cross-data-product sharing exactly where data mesh needs standardization most; the book calls this out as an unsolved, urgent gap rather than papering over it.
- **Collecting logs/traces/metrics without automated analysis capability**: "futile, similar to collecting any other kind of large-volume data without the ability to analyze it" — observability data is only as useful as the tooling built to consume it.
- **Using computational-notebook-style ad hoc governance/observability checks as production controls**: same caution as Ch 13 — fine for exploration and documentation, not a substitute for standardized, testable, embedded policy-as-code.

## Reference Tables
| Manifest component | Declares |
|---|---|
| Data product URI | Globally unique identifier/address |
| Output ports + SLOs | Access modes offered and the guarantees each makes |
| Input ports | Where data comes from and how it's retrieved |
| Local policies | Locality, confidentiality, privacy, retention configuration |
| Source artifacts | Pointers to transformation code, input port queries (kept as code, not manifest) |

| Observability pillar | Operational-plane analogue | Data-mesh-specific use |
|---|---|---|
| Logs | Application logs | Debugging/root-cause analysis of consume-transform-serve steps |
| Traces | Distributed call tree | Constructing data lineage across input/output ports |
| Metrics | Service SLIs/SLOs | The trust/quality/temporality metrics from Ch 13, tracked over time |

## Key Takeaways
1. The data product manifest is a declarative, portable specification of target state — imperative logic (transformation code) stays separate, as versioned source artifacts.
2. Policy-as-code is embedded in the data product (sidecar + control port) and, ideally, linked to the data it governs so consent/privacy travels with the data rather than being lost at storage boundaries.
3. Analytical data governance lags operational API governance in identity/access-control standardization — a named, unsolved gap the book hopes data mesh's cross-vendor motivation will help close.
4. Observability borrows the three pillars (logs, traces, metrics) from operational systems, standardizes their structure across all data products, and uses traces specifically to construct emergent mesh-wide lineage.
5. The chapter's single takeaway: invert responsibility for management, governance, and observability from an external after-the-fact party to the data product itself, by design.
6. This chapter closes Part IV (data product design); Part V turns to organizational strategy and execution (Ch 15–16).

## Connects To
- **Ch 4**: declarative modeling as a complexity-abstraction technique, applied here concretely as the manifest.
- **Ch 5 / Ch 9**: federated computational governance and the sidecar/control-port architecture this chapter's policy-as-code design directly implements.
- **Ch 13**: the trust metrics and lineage concepts extended here into full observability design.
- **Ch 15 / Ch 16**: Part V's strategy, execution, and organizational/cultural transformation build on the complete data product design established across Ch 11–14.
