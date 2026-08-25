# Chapter 13: Design Discovering, Understanding, and Composing Data

## Core Idea
Discoverability, understandability, trust, and composability must be **shifted left into each data product itself** (self-registration, self-published semantic/syntax models, self-reported trust metrics) rather than achieved by an external catalog curating data after the fact — and cross-product composability must rely on a **distributed type system** (each data product owns and links its own schema), never a shared central schema or fact-table join.

## Frameworks Introduced
- **Shift-left discoverability**: contrasted with the two traditional approaches — *a posteriori curation* (stewards tag/document after the fact) and *a posteriori investigative intelligence* (algorithms infer trust/metadata after the fact from usage patterns). Both are declared insufficient (though useful to bootstrap); data mesh's approach is the data product publishing this information about itself, continuously, from creation onward.
- **Semantic Model vs. Syntax Model**: the semantic model is the machine-and-human-readable domain model (entities, properties, relationships — e.g., a property graph); the syntax model is how each specific output port encodes that semantic (e.g., the same "playlist" concept as JSON columnar files for one port, as SQL rows for another). One semantic model, potentially many syntax models.
- **Categories of Trust Metrics/Guarantees (SLOs)**: data quality (accuracy, completeness, consistency, precision), data maturity (usage, life cycle stage, diversity of access modes, linkage), data standards conformance (e.g., FHIR HL7 in healthcare), temporality metrics (epoch, processing interval, last processing/actual time, timeliness/skew), and user-driven metrics (consumer ratings/satisfaction).
- **Three Composability Approaches contrasted**: fact/dimension tables (star/snowflake schema — tight coupling, homogeneous syntax assumption, rejected for mesh use), distributed type system via GraphQL-style federation (subgraphs referencing/extending each other's types — closer fit, needs refinement for time/versioning), and Linked Data / Semantic Web (JSON-LD, global URIs, ontologies — closest philosophical fit, needs refinement to avoid centrally-managed shared schemas).
  - How: prefer the distributed-type-system / linked-data direction; explicitly reject fact-table joins and foreign-key coupling across data product boundaries.

## Key Concepts
- **Global URI (data product & data entity)**: every data product has a unique root address; every cross-domain entity (a "polyseme" like *artist*) must have a globally unique identifier resolvable back to its owning/source data product (e.g., `artist_profiles` mints the artist URI at onboarding time).
- **Differential privacy for shape exploration**: lets data users explore statistical shape/distribution of sensitive data (e.g., "is one small group skewing the trend?") without accessing individual protected records — mathematically bounded so no one record can be singled out.
- **Computational notebooks as documentation, not production code**: valuable for storytelling/exploration (code + docs + visualization together) but explicitly discouraged as long-lived production artifacts, since they resist modularization/testing at scale.
- **Machine-optimized internal indices vs. human-facing URIs**: the logical/human-facing layer stays loosely coupled via URIs; underneath, a federated query engine may build tightly-coupled internal indices for speed — analogous to how a web search engine indexes hyperlinked pages without users ever touching the index directly.

## Mental Models
- **"All models are wrong, but some are useful" (George Box)**: a data product's semantic model is always an approximation of business reality — good enough for the analytical task, not a claim of ground truth.
- **"Learn how to see. Realize that everything connects to everything else" (da Vinci, epigraph)**: composability is framed as the mesh's payoff — individually useful data products become far more valuable when correlated (e.g., emerging-artist classification needs playlists + play sessions + social mentions joined by a shared artist identity).
- **Optimize the logical layer for humans, the physical layer for machines**: URIs/semantic links stay simple and stable for people; the platform is free to build fast, internally-coupled indices underneath, exactly as search engines separate a clean URL space from an opaque ranking index.

## Anti-patterns
- **Relying solely on a posteriori catalog curation or algorithmic metadata inference as the primary discovery mechanism**: useful for bootstrapping or cross-checking, but insufficient as the mesh's system of record for discoverability — the data product itself must be the source.
- **Cross-data-product composability via shared fact/dimension tables and foreign keys**: creates tight, fragile coupling — one data product's schema can no longer change independently, and it assumes a homogeneous tabular syntax across the whole mesh (breaks the moment one source is a stream and another is a file).
- **A centrally-managed, shared schema registry as the backbone of linking** (the weakness the book flags even in the Linked-Data-inspired approach it otherwise favors): still needs refinement to avoid recreating a single point of coordination for schema evolution.
- **Treating "metadata" as one generic bucket**: repeated from Ch 9 — schema, SLOs, statistical shape, and lineage are distinct, purpose-built, product-generated concerns, not one catch-all.

## Code Examples

GraphQL-style distributed type system (a subgraph referencing a type owned by another data product):
```graphql
// Artist Profile Schema
type ArtistProfile {
    artist: Artist
    active_since: Date
    ...
}
type Artist {
    id : ID!
    name : String
}
// -----------------------------
// Playlist Schema — reuses the Artist type defined above
type Playlist {
    user: String
    tracks : [Tracks]
    ...
}
type Track {
    artist: Artist
    duration: Int
    ...
}
```
- **What it demonstrates**: loose coupling via a distributed type system — the `Playlist` schema references `Artist` (owned by `ArtistProfile`) without collapsing both into one shared central schema; each data product still owns and evolves its own type independently.

Linked-Data / JSON-LD style (global URIs + ontology context, closest philosophical fit for composability):
```json
{
    "@context": {
        "@vocab": "https://schemas.daff.com/playlist#",
        "listeners": "https://schema.org/Person#",
        "artist": "https://schemas.daff.com/artist#",
        "track:id": {"@type": "@id"}
    },
    "@id": "https://daff.com/playlist/19378",
    "@type": "Playlist",
    "name": "Indie Playlist",
    "tracks": [{
        "@id": "https://daff.com/playlist/19378/1",
        "artist:name": "Sonic Youth",
        "track:id": "https://daff.com/tracks/39438434"
    }]
}
```
- **What it demonstrates**: every entity (playlist, track, artist) is addressed by a globally unique URI, and vocabulary terms are resolved via `@context` — enabling cross-data-product linking without a single shared, centrally-owned schema for all data.

## Reference Tables
| Composability approach | Coupling | Verdict for data mesh |
|---|---|---|
| Fact/dimension tables (star/snowflake) | Tight, homogeneous-syntax assumption | Rejected |
| Distributed type system (GraphQL federation-style) | Loose, per-domain-owned schemas | Adopted direction, needs time/versioning refinement |
| Linked Data / Semantic Web (JSON-LD, URIs, ontologies) | Loose, global identifiers | Closest philosophical fit, avoid recreating a central schema registry |

## Key Takeaways
1. Discoverability/understandability/trust must be generated by the data product itself, from inception onward — not bolted on later by an external catalog team.
2. Separate the semantic model (domain meaning) from the syntax model (per-output-port encoding) — one data product can have several syntax models sharing one semantic model.
3. Trust is built from explicit, categorized metrics (quality, maturity, standards conformance, temporality, user-driven) — not from lineage archaeology as the default.
4. Composability requires a distributed type system with globally unique URIs for shared entities (polysemes) — never a shared fact table or centrally-owned canonical schema.
5. Keep the human-facing layer (URIs, semantic links) simple and loosely coupled; let the platform optimize physical/query performance underneath without leaking that complexity upward.

## Connects To
- **Ch 3 / Ch 5**: the usability attributes and governance standards this chapter operationalizes into concrete design (discovery APIs, trust metrics, standardized policies).
- **Ch 9**: the discovery port and sidecar this chapter extends with discoverability-specific responsibilities.
- **Ch 12**: builds directly on the bitemporal/immutable serving properties — composability depends on being able to relate data temporally across independently-cadenced products.
- **Ch 14**: continues Part IV with the remaining affordances (manage life cycle, govern, observe).
