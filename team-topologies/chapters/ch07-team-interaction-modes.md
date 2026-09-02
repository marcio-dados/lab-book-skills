# Chapter 7: Team Interaction Modes

## Core Idea
Every inter-team relationship should be one of exactly three deliberately chosen modes — collaboration, X-as-a-Service, or facilitating — because ambiguous or default "everyone talks to everyone" interaction is what actually produces coupled, hard-to-evolve systems.

## Frameworks Introduced
- **The Three Team Interaction Modes**: Collaboration (working closely together, high value/high cognitive-load, boundary-blurring, best for discovery), X-as-a-Service (consuming/providing with minimal collaboration, clear ownership, lower cognitive load, best for predictable delivery), Facilitating (one team helps another clear impediments or learn, time-boxed, the main mode of enabling teams).
  - When to use: choose collaboration during genuine discovery/innovation where boundaries aren't yet known; choose X-as-a-Service once a boundary is proven and predictable delivery matters more than further discovery; choose facilitating when a capability gap (not an ownership question) is the problem.
  - How: name the mode explicitly per team-pair relationship; a team should use collaboration mode with at most one other team at a time (it's expensive), can use X-as-a-Service with many teams simultaneously, and should use facilitating with only a small number of teams at once.
- **Use Awkwardness to Sense Misplaced Boundaries**: friction in an interaction is diagnostic information about the underlying architecture, not just an interpersonal problem.
  - When to use: whenever a supposed X-as-a-Service relationship requires heavy ongoing back-and-forth, or a supposed collaboration relationship shows no real interaction.
  - How: ask "is the component boundary in the right place? Is the API well specified? Does the providing team have a missing capability (e.g. UX/DevEx)?" and treat the answer as a trigger to redraw the boundary or fix the gap, not to tolerate the friction indefinitely.

## Key Concepts
- **Collaboration mode**: two teams substantially share responsibility and blur boundaries for a defined period; investment pays off through rapid mutual discovery, at the cost of higher combined cognitive load.
- **X-as-a-Service mode**: one team consumes something (API, library, platform, component) that another provides "as a service," with a clean, well-managed boundary; requires strong product/service-management discipline from the providing team.
- **Facilitating mode**: the primary operating mode of enabling teams — one team actively helps another learn, adopt a practice, or discover a capability gap, without taking part in building the main system.
- **Promise theory** (Mark Burgess): inter-team relationships work better framed as voluntary promises (e.g., SemVer as a promise not to break dependents) than as commands or enforceable contracts.
- **Team-interaction-mode-to-topology mapping**: stream-aligned teams typically use both collaboration and X-as-a-Service (occasionally facilitating); enabling teams typically use facilitating; complicated-subsystem and platform teams typically use X-as-a-Service (occasionally collaboration).

## Mental Models
- Think of team-interaction-mode choice like a concert band changing musical style (jazz, orchestral, choir accompaniment) depending on who it's performing with — same people, deliberately different "style" of behavior per relationship.
- Use collaboration explicitly to *discover* a viable X-as-a-Service boundary, then deliberately transition to X-as-a-Service once the boundary is proven — don't let collaboration continue indefinitely once discovery is done.
- Apply "Intermittent collaboration gives the best results" (Bernstein et al.'s research): groups that interact only intermittently found solutions of comparable average quality to constantly-interacting groups, while also finding more of the very best solutions — constant interaction isn't automatically better.

## Anti-patterns
- **Everyone-to-everyone communication**: the absence of named interaction modes leaves teams needing to interact with "many other teams" to get anything done — the opposite of curated, jazz-band-like coordination the chapter argues for.
- **Permanent collaboration where a service boundary should exist**: an ongoing need for close collaboration long after initial discovery usually signals wrong domain boundaries, wrong team responsibilities, or a missing skill in the team — not a stable long-term state.
- **X-as-a-Service without service-management discipline**: providing something "as a service" without genuine product-management rigor (versioning promises, roadmap, DevEx focus) produces an interaction that looks clean on a diagram but fails in practice.
- **Collaborating with more than one team at once**: violates the mode's own constraint and multiplies cognitive load beyond what any team can sustain.

## Reference Tables
**Table 7.4 — Team interaction modes of the fundamental team topologies (Typical / Occasional):**

| Team Topology | Collaboration | X-as-a-Service | Facilitating |
|---|---|---|---|
| Stream-aligned | Typical | Typical | Occasional |
| Enabling | Occasional | — | Typical |
| Complicated-subsystem | Occasional | Typical | — |
| Platform | Occasional | Typical | — |

**Advantages/disadvantages by mode (Tables 7.1–7.3, condensed):**

| Mode | Advantages | Disadvantages | Constraint |
|---|---|---|---|
| Collaboration | Rapid innovation/discovery; fewer hand-offs | Higher cognitive load; possible reduced short-term output | Use with at most one other team at a time |
| X-as-a-Service | Clear ownership; lower cognitive load | Slower boundary innovation; flow risk if boundary is poor | Can be used with many teams simultaneously |
| Facilitating | Unblocks stream-aligned teams; surfaces capability gaps | Needs experienced staff not "building/running"; can feel unfamiliar | Use with only a small number of teams at once |

## Worked Example
A stream-aligned Team A (personal-finance software) uses collaboration mode with complicated-subsystem Team B to jointly work through new cloud-monitoring tooling — an active discovery problem neither team has solved before — while simultaneously using X-as-a-Service mode to consume the platform built by Team C, with no meaningful daily interaction required. When Team A later starts spending unusual amounts of time in chat and in-person with a complicated-subsystem team it's supposed to be consuming "as a service," that heavy interaction itself is the diagnostic signal: either the component's API is poorly specified, the boundary is in the wrong place, or the providing team lacks a capability (e.g., DevEx) it needs to make the service genuinely self-service.

## Key Takeaways
1. Name the interaction mode explicitly for every significant team-to-team relationship — never leave it as unstated "just talk to them."
2. Use collaboration sparingly and temporarily (at most one partner team at a time) — it is a discovery tool, not a steady state.
3. Use X-as-a-Service as the default for stable, well-understood boundaries; it scales to many simultaneous relationships precisely because it needs minimal ongoing interaction.
4. Treat facilitating relationships as inherently time-boxed — an enabling team's presence indefinitely is itself a signal something is wrong.
5. Read friction (too much talk under X-as-a-Service, too little under collaboration) as an architecture/boundary signal, not merely an interpersonal one.

## Connects To
- **Ch 5**: the four fundamental team topologies map onto characteristic interaction-mode profiles (Table 7.4).
- **Ch 2**: interaction modes are the concrete mechanism for "restricting unnecessary communication."
- **Ch 8**: describes how interaction modes should deliberately *evolve* over time (collaboration → X-as-a-Service) as part of organizational sensing.
