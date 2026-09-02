# Patterns

## Reverse Conway Maneuver
**When to use**: A target software architecture (e.g., independent microservices, separate data stores) is known before the system is built, or an existing architecture needs to move toward a new shape.
**How**: Design team communication structures to match the target architecture's module boundaries first — e.g., embed a database developer inside each service team instead of routing all teams through a shared DBA. Expect initial pushback and expect the *existing* architecture to "push back" against the new team structure for a period, requiring temporary explicit collaboration mode plus facilitating support to hold the new boundaries while they stabilize.
**Trade-offs**: Requires management willpower and team awareness to sustain through the pushback period; done well it lets teams *discover* the desired architecture rather than fight the org for it; done naively (team shapes look right on paper but communication still flows the old way) it produces no real change.

## Team API Design
**When to use**: Any team whose work (code, services, decisions) is consumed by other teams — i.e., almost every team.
**How**: Deliberately define and publish: runtime endpoints/libraries/UI, a versioning promise (e.g., SemVer as a "team promise" not to break things), wiki/how-to documentation, working practices and principles, communication-channel norms, and visibly current work/priorities. Treat it as a product: test it for usability from another team's perspective, and evolve it continuously.
**Trade-offs**: Upfront investment in documentation/versioning discipline that doesn't ship features directly; pays off by reducing ad hoc, high-friction cross-team communication and reducing dependency risk.

## Domain-Driven Fracture Planes
**When to use**: Splitting a monolith, or defining boundaries for a new system, where the goal is team-sized, independently ownable subsystems.
**How**: Use bounded contexts (DDD) as the default/primary split; where domain boundaries alone aren't sufficient, layer in secondary fracture planes — regulatory compliance, change cadence, team location, risk profile, performance isolation, technology, user personas. Validate each candidate boundary with "could we, as a team, consume or provide this as a service?"
**Trade-offs**: Requires genuine business-domain expertise and iteration (expect early mistakes); a poorly chosen split produces a "distributed monolith" — services with no real independence, all the operational complexity, none of the benefit.

## Thinnest Viable Platform (TVP)
**When to use**: Whenever multiple stream-aligned teams share underlying infrastructure/services and cognitive load from "reinventing" that substrate is becoming a bottleneck.
**How**: Start as thin as possible — even a curated wiki list of components. Grow scope only as the underlying substrate's real complexity demands a dedicated team; manage the platform as a live product (roadmap, user personas for consuming Dev teams, SLAs, DevEx investment) rather than a side project.
**Trade-offs**: Under-investment leaves teams reinventing common capability (waste, inconsistency); over-investment ("developers love building platforms") produces a bloated platform that drags on delivery and outpaces real demand — internal pricing or tiered service levels can regulate demand for "premium" service.

## Collaboration → X-as-a-Service Evolution
**When to use**: A new technology, domain, or team-boundary is being explored and the eventual service boundary isn't yet known.
**How**: Start the relevant team pair in collaboration mode (shared responsibility, blurred boundaries, high cognitive load, high discovery rate) for a defined period. As the boundary/API stabilizes, deliberately transition to X-as-a-Service (clean API, minimal ongoing interaction, lower cognitive load, predictable delivery). Expect multiple such transitions running concurrently across a large organization at different maturity stages.
**Trade-offs**: Collaboration is expensive (higher combined cognitive load, "collaboration tax") and doesn't scale to many simultaneous partners — a team should collaborate with at most one other team at a time; X-as-a-Service innovates more slowly across the boundary by design, trading discovery speed for predictability.

## Facilitating via Enabling Teams
**When to use**: A capability gap exists across one or more teams (a technology, practice, or tooling gap) that the team(s) can't close through their own research bandwidth.
**How**: Stand up (or task) an enabling team of specialists to actively teach, coach, and remove impediments — never to execute the served team's work for them. Set an explicit, short time horizon (weeks to months); the enabling team should plan for its own extinction from day one and broadcast its work widely so the served teams become self-sufficient rather than dependent.
**Trade-offs**: Done well, it multiplies capability without adding permanent headcount to every team; done poorly (no time-box, no self-obsoleting mandate) it becomes an "ivory tower" or permanent dependency, indistinguishable from a functional silo.

## Continuity of Care (Merged New-Work / BAU Ownership)
**When to use**: An organization has (or is tempted to create) a separate maintenance/"business as usual" team distinct from the team building new features.
**How**: Keep one stream-aligned team (or paired team) responsible for both new-service work and BAU of the same system side by side, so operational telemetry and incident learning flow directly back into design decisions. Retro-fit newer telemetry techniques onto older systems using the same team's growing expertise.
**Trade-offs**: Requires accepting that the "new work" team also carries maintenance burden (less pure feature-velocity optics); in exchange it closes the feedback loop that separate BAU teams structurally break, per the book's "cybernetic" framing.

## Organizational Sensing via Named Triggers
**When to use**: Periodically, and especially when a team or delivery pipeline has felt stable for an extended period.
**How**: Watch for three named symptom clusters that signal a topology redesign is due: (1) software too large for one team (routine work bottlenecking on the same person, documentation complaints, team crossing Dunbar's number), (2) delivery cadence slowing (declining velocity, growing cross-team WIP), (3) many business services relying on a large set of underlying services (poor end-to-end visibility, hard reuse) — apply a platform wrapper if so.
**Trade-offs**: Requires deliberate, recurring self-assessment (it doesn't happen automatically); ignoring the triggers lets structural problems compound until a much more disruptive reorg becomes necessary.
