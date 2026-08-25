# Chapter 2: Principle of Domain Ownership

## Core Idea
Decompose analytical data along the seams of business domains — not technology (lake/warehouse/pipeline) or functional team lines — giving each domain long-term product ownership of the data it is closest to, using Domain-Driven Design's Strategic Design (bounded contexts) as the modeling technique.

## Frameworks Introduced
- **DDD Strategic Design applied to data**: adopt *bounded contexts* — each domain models its data according to its own context — instead of one central canonical model, isolated silos, or "no intentional modeling" (a data lake dump).
  - When to use: whenever the organization already has (or can adopt) a domain/microservices decomposition of the business.
  - How: map each domain's analytical data to its own bounded context; use *context mapping* / a shared identification scheme to relate the same real-world entity (a "polyseme") across domains, instead of forcing one shared schema.
- **Three Domain Data Archetypes**: Source-aligned, Aggregate, Consumer-aligned.
  - When to use: to classify any domain's analytical data and decide how it should be modeled, retained, and by whom it should be owned.
  - How: source-aligned data mirrors the business facts as generated (native, long-retained, not fitted to any one consumer); aggregate data composes several source-aligned products into a shared higher-order concept (owned cautiously — see anti-pattern below); consumer-aligned (fit-for-purpose) data is transformed to serve one or a few specific use cases (e.g., ML features).

## Key Concepts
- **Bounded context**: "the delimited applicability of a particular model" that gives a team a clear, shared understanding of what must be consistent internally and what can evolve independently (Eric Evans).
- **Polyseme**: a shared business concept (e.g., "artist," "listener," "song") that different domains model differently but that can be mapped/linked across domains via a global identification scheme.
- **Data ownership (as used in this book)**: shorthand for *product* ownership — long-term accountability to create, model, maintain, evolve, and share data as a product — explicitly not data sovereignty (which remains with the end user/customer whose data it is).
- **Source-aligned domain data**: native representation of business facts, as close as possible to the point of origin, but never modeled directly off the operational database (see anti-pattern).
- **Data pipeline as internal implementation**: in data mesh, cleansing/aggregating pipelines still exist but are hidden inside a domain, not a first-class cross-cutting architectural layer.

## Mental Models
- **"Push data ownership upstream"**: reject the assumption baked into "lake/pipeline/hydration" vocabulary that data becomes valuable only once it flows downstream to a central store — treat source-aligned data at the domain as consumable and valuable in place.
- **"Define multiple connected models, not one canonical model"**: accept that different domains will model the same concept differently; invest in mapping between them instead of chasing a single schema.
- **"Embrace the most relevant data; don't chase a single source of truth"**: long-term domain ownership with high discoverability reduces (but doesn't eliminate) duplicate/stale copies — perfect deduplication isn't the goal.

## Anti-patterns
- **Modeling analytical data directly off the source application's transactional database** (via ETL/CDC/data virtualization straight on the OLTP schema): the operational model is optimized for transactional speed, not for analytical understanding — data mesh treats operational and analytical data as separate but co-owned by the same domain team.
- **Ambitious, all-encompassing aggregate domain data** ("listener 360" style Master Data Management): trying to capture every facet of a concept in one aggregate reproduces monolithic central modeling and becomes unmanageable. Prefer many small, fit-for-purpose aggregates over one grand one.
- **Designing domain boundaries up front from a blank slate**: if the business isn't already organized around domains, forcing a data-mesh decomposition ahead of the organizational seams is premature.

## Worked Example
Daff's media player team originally just dumps raw play events onto a short-retention stream/transactional store, which a central data team later picks up into a lake/warehouse. Under data mesh, the media player domain instead takes end-to-end responsibility for a high-quality, long-retention, real-time-and-aggregated view of play events — sharing it directly as source-aligned data. A new **listener session domain** emerges specifically to aggregate individual play events into longitudinal listener journeys (aggregate domain data), augmented with listener-profile attributes. A **recommendation domain** then consumes the listener-session data to build music-recommendation graphs — this is consumer-aligned (fit-for-purpose) data. The example shows all three archetypes appearing along one real data flow, and shows a new domain (listener session) being created purely because the data need reshaped the organization.

## Key Takeaways
1. Decompose data along business-domain seams (DDD bounded contexts), never along technology or central-team lines.
2. Classify domain data into source-aligned, aggregate, or consumer-aligned to decide its modeling and ownership approach.
3. Never expose analytical data straight from an operational database schema — the domain team owns a separate, purpose-built analytical representation.
4. Resist building one grand, all-purpose aggregate; let consumers compose their own fit-for-purpose aggregates instead.
5. Multiple models of the same business concept, linked via a shared ID scheme, is a feature of the design, not a defect to be centralized away.

## Connects To
- **Ch 1**: domain ownership is the first of the four principles introduced there.
- **Ch 3**: "data as a product" is the principle that prevents domain ownership from degenerating into new silos.
- **Ch 7 / Ch 8**: contrast domain-oriented ownership against the failure modes of centralized, technology-partitioned architectures.
