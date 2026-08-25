# Chapter 11: Design a Data Product by Affordances

## Core Idea
Design a data product not by listing technical components but by inspecting **affordances** — the relationship between a data product's properties and the capabilities of the agents (people or systems) that interact with it (Don Norman's term) — while also treating the mesh as a **complex adaptive system** where mesh-level intelligence should emerge from simple local rules, never from a central orchestrator.

## Frameworks Introduced
- **Design by Affordances**: extend the standard architecture constituents (structure, characteristics, decisions, principles — per *Fundamentals of Software Architecture*) with *affordances* — what a data product's properties allow specific agents to do (discover it, subscribe to it, transform it, govern it).
  - When to use: whenever designing any data product capability, ask explicitly "who/what does this afford, and who does it deliberately NOT afford?" (e.g., serving data affords analytical read access; it deliberately does *not* afford transactional update/delete).
- **Nine Data Product Affordances**: Serve Data, Consume Data, Transform Data (Ch 12); Discover/Understand/Explore/Trust, Compose Data (Ch 13); Manage Life Cycle, Observe/Debug/Audit, Govern (Ch 14).
- **Three Architecture Characteristics common to all data products**: Design for change, Design for scale, Design for value.
  - How: use as an evaluation rubric — "design for change" checks for API-fronting and time-as-attribute; "design for scale" checks for absence of centralized synchronization points (e.g., policy executed in a local sidecar, not a central gateway); "design for value" checks that internal complexity (e.g., bitemporality) doesn't leak into the everyday consumer experience (offer "latest"/"now" shortcuts).
- **Complex Adaptive Systems lens**: two specific borrowings — (1) emergent behavior from simple local rules (like Reynolds' boid flocking rules: separation, alignment, cohesion) instead of centrally orchestrated behavior; (2) no central orchestrator — a small set of shared standards (not central control) is what keeps the system coherent.

## Key Concepts
- **Affordance (Don Norman)**: "a relationship between the properties of an object and the capabilities of the agent" — not a property of the object alone. A chair affords sitting for most agents but doesn't afford lifting for a weak agent; likewise, a data product's bitemporal serving affords correct use only to time-aware consumers.
- **Emergent mesh-level lineage graph**: no data product or central component holds the whole mesh's lineage graph — it emerges purely from each data product's local declaration of its own input/output ports, aggregated (not authored) by the mesh experience plane.
- **Design for extension (subset of design for change)**: loosely-coupled, injectable components (sidecars/agents) are more extensible than statically-linked shared libraries, because new capabilities can be added at deploy/runtime without rebuilding the data product.

## Mental Models
- **"I will show you the ropes, and it's you who will raise the sails"**: the chapter is explicit that this is a *method* (a way of thinking about design), not a finished implementation handbook — apply the affordance lens to any future data product capability the book doesn't enumerate.
- **Starling murmuration as the governing metaphor for mesh coherence**: thousands of birds achieve synchronized, complex group behavior from three simple local rules, with no leader and no global view — the direct inspiration for designing input/output ports as purely local declarations that still produce a coherent, navigable mesh.
- **"A central gateway becomes a chokepoint over time"**: any design choice that funnels access-control or other cross-cutting decisions through one central component reintroduces the exact bottleneck data mesh exists to remove — enforce policy locally (in the sidecar) instead.

## Anti-patterns
- **Designing a data product's capabilities as a list of technical features rather than affordances tied to specific agents**: misses the crucial question of who is *excluded* by design (e.g., a data product should NOT afford transactional update semantics to operational consumers — that's a deliberate non-affordance, not an oversight).
- **A central orchestrator holding the full pipeline/DAG configuration**: contradicts the complex-adaptive-systems design; if the mesh needs a central "conductor" to function, the local-rules design has failed.
- **Overengineering a data product for imagined future flexibility at the expense of "design for value"**: bitemporality must exist internally for integrity, but exposing its full complexity to every consumer (instead of a `latest`/`now` shortcut) violates "design for value" by adding friction nobody asked for.

## Key Takeaways
1. Design each data product capability by asking what it affords, to which specific agents, and — just as importantly — what it deliberately does not afford.
2. All data products must satisfy three architecture characteristics regardless of domain: design for change, design for scale, design for value.
3. Avoid centralized synchronization points anywhere in the design (a lesson reinforced from Ch 5/Ch 7) — enforce cross-cutting concerns locally, in each data product's own execution context.
4. Borrow deliberately from complex adaptive systems: define simple, local rules per data product (its own input/output ports) and let mesh-level properties (lineage, knowledge graph, performance) emerge — never centrally author them.
5. This chapter is a *method*, meant to be applied beyond the specific affordances the book enumerates in Chapters 12–14.

## Connects To
- **Ch 9**: the data product quantum whose affordances this chapter organizes design around.
- **Ch 12**: Serve/Consume/Transform Data — the first three affordances detailed.
- **Ch 13 / Ch 14**: Discover/Understand/Compose and Manage/Observe/Govern — the remaining six affordances.
