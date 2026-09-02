# Chapter 4: Static Team Topologies

## Core Idea
There is no single "right" team topology, only topologies that fit (or fight) a given organization's technical/cultural maturity, size, and engineering discipline at a specific point in time — and several well-known team patterns are actually anti-patterns in disguise.

## Frameworks Introduced
- **DevOps Topologies catalog** (Skelton 2013, expanded by Pais): a catalog of team-design patterns and anti-patterns for Dev/Ops relationships, used as a starting point for reasoning about context-dependent team structures — not a prescriptive "best" topology.
  - When to use: as a conversation-starter for choosing initial team structures around DevOps concerns (build, deploy, operate).
  - How: match a candidate pattern against org size, engineering maturity, and product/software scale (see Figure 4.4 logic below) rather than copying a pattern because it worked elsewhere.
- **SRE as a Dynamic Stream-Aligned Relationship**: Google's Site Reliability Engineering model, where the SRE/application-team relationship shifts through stages (app team alone → SRE guidance → SRE fully involved with an error budget → app team resumes if operability or usage drops).
  - When to use: only at genuine scale, and only with strong engineering discipline — SRE is optional, and de-scaling back to the dev team is a valid outcome, not a failure.
  - How: define SLOs and an error budget to balance feature velocity against reliability work; let the SRE relationship intensity track actual usage/reliability needs rather than staying fixed.

## Key Concepts
- **Team topology (term)**: a deliberately designed team structure and set of interactions, contrasted with ad hoc or accidental team formation.
- **Feature/product team**: a cross-functional, cross-component team delivering a customer-facing feature end to end; only effective with high engineering maturity and trust (otherwise it erodes shared-codebase quality).
- **"Wall of confusion"**: the classic Dev/Ops anti-pattern where releases are thrown over a fence between separate teams, communicating mainly through tickets.
- **DevOps team anti-pattern**: a permanent, siloed "DevOps team" that becomes a hard dependency for every application team's delivery pipeline, rather than a temporary, self-obsoleting capability-building function.
- **Non-blocking dependency**: a dependency satisfied via self-service (e.g., provisioning pipeline, test environment) rather than by scheduling another team's availability — the difference between a soft and a hard dependency.
- **Physical Dependency Matrix / dependency tags**: Dominica DeGrandis's technique for visualizing and tracking cross-team dependencies so they don't silently accumulate.

## Mental Models
- Ask of any team structure: "does the surrounding environment (other teams, platform, culture) support this pattern?" — the same pattern (e.g., feature teams) can be a strength or a liability depending entirely on context, not on the pattern itself.
- Plot org size/software scale against engineering maturity as two axes: low maturity favors specialized-but-collaborating teams; growing scale favors platform/infrastructure-as-a-service; high maturity at high scale can support SRE.
- Use a temporary DevOps team as a bridge with an explicit expiration date and mission ("put itself out of business"), never as a permanent fixture.

## Anti-patterns
- **Ad hoc team design**: teams formed reactively (grown-too-large team split up, a "catch-all COTS team," a DBA team created after an outage) without considering the surrounding topology, eroding autonomy even though each individual decision looks locally sensible.
- **Shuffling team members project-to-project**: assembling and disbanding teams per project ignores the real cost of team formation and context-switching, unlike a computer that performs identically regardless of "which room" it's placed in.
- **Permanent DevOps silo**: a DevOps team that becomes the sole executor of automation/tooling work for every project, instead of building self-service capability and evangelizing until it can dissolve.
- **Copying the "Spotify model" wholesale**: adopting squads/tribes/chapters/guilds as a fixed blueprint, ignoring that Spotify itself described it as "a snapshot... a journey in progress, not completed."

## Worked Example
TransUnion's DevOps journey (Ian Watson, Head of DevOps, 2015) deliberately avoided creating one permanent "DevOps team." Instead they stood up two *temporary* teams — one from Dev, one from Ops — explicitly tasked with bringing the groups together over time, using the DevOps Topologies catalog to reason about the transition path rather than freezing on a single target structure. The explicit temporariness and evolutionary framing (documented across multiple years) let the org avoid the "yet another silo" trap that a permanent DevOps team creates, while still scaling the technology division significantly.

## Key Takeaways
1. Judge a team pattern by fit to current context (maturity, scale, discipline) — never adopt a pattern purely because a famous company used it.
2. A "DevOps team" is legitimate only as a temporary, self-obsoleting bridge; permanence turns it into exactly the silo DevOps was meant to remove.
3. Distinguish hard dependencies (block work, require another team's live availability) from soft/non-blocking dependencies (self-service); design to convert the former into the latter.
4. Track inter-team dependencies explicitly (a matrix, tags, or even a spreadsheet like Spotify's) and set thresholds that trigger a redesign conversation.
5. SRE is an optional, dynamic relationship, not a mandatory phase — scale the relationship with actual reliability/usage needs and be willing to de-scale it.

## Connects To
- **Ch 5**: converts these context-dependent "static" topologies into four fundamental, context-independent team types.
- **Ch 2**: the DevOps team anti-pattern is a direct instance of ignoring Conway's law (a new silo mirrors old fence-throwing behavior).
- **Ch 8**: the TransUnion case continues there, showing the temporary teams' further evolution.
