# Chapter 3: Team-First Thinking

## Core Idea
The team, not the individual, is the fundamental unit of software delivery — organizations must build small, stable, long-lived teams, size their responsibilities to the team's cognitive capacity, and design everything else (office space, rewards, tooling, software boundaries) around that team.

## Frameworks Introduced
- **Dunbar's Number applied to team size**: anthropological limits on group trust/cognition — around 5 (close personal relationships), 15 (deep trust), 50 (mutual trust), 150 (remembered capabilities) — used to bound team and grouping sizes.
  - When to use: setting team size, and sizing "families/tribes" and larger groupings.
  - How: keep a single team at 5–9 people (up to ~15 only in high-trust organizations); group teams into "tribes" of no more than 50 (or 150 in high-trust orgs); expect to split when a limit is crossed.
- **Team Cognitive Load** (Sweller's three types, applied to teams): the total mental effort a team can sustain — intrinsic (fundamental to the problem, e.g. language syntax), extraneous (environment/tooling friction, e.g. deploy steps), germane (the valuable, differentiating domain knowledge).
  - When to use: whenever assigning a team responsibility for a new domain, subsystem, or service.
  - How: minimize intrinsic load (training, tech choice, hiring), eliminate extraneous load (automation), and protect space for germane load; classify each domain a team owns as simple, complicated, or complex, and apply the domain-count heuristics below.
- **Team API**: the complete surface by which other teams interact with a team — code (endpoints, libraries), versioning promises (e.g. SemVer), documentation/wiki, practices/principles, communication channels, and current work/priorities.
  - When to use: whenever a team's work will be consumed, reviewed, or depended on by another team.
  - How: continuously define, advertise, test, and evolve it as a product — ask "will other teams find it easy and straightforward to interact with us?"

## Key Concepts
- **Team (book's definition)**: a stable grouping of 5–9 people working toward a shared goal as a unit; the smallest entity to which work should ever be assigned (never to individuals).
- **Brooks's Law**: adding people to a late team doesn't immediately (and may never) increase capacity, due to ramp-up and rising communication overhead.
- **Continuity of care**: a team owning a system across exploration, exploitation, and long-term maintenance horizons, rather than handing it off after a project.
- **Team-toxic individuals**: people who put personal goals above team goals; must be removed if coaching fails, because they can destroy team cohesion.
- **Relative domain complexity**: classify each domain a team owns as simple (procedural, clear path), complicated (needs analysis/iteration), or complex (needs experimentation/discovery) — this classification, not lines of code, is what drives cognitive load.
- **Team-first software architecture**: choosing subsystem/service boundaries to match team cognitive capacity, instead of choosing an architecture style first and forcing teams to fit it.

## Mental Models
- Think of code ownership as gardening, not policing: teams are stewards/caretakers of the software, not territorial owners excluding others.
- Use "flow work to the team," not "reassign people to the work" — stable teams take weeks to months to become effective (Tuckman's forming/storming/norming/performing, understood as continuous, not one-time).
- When judging whether a team can take on one more domain, use these four heuristics: (1) each domain maps to exactly one team; (2) a team can hold 2–3 *simple* domains; (3) a team with one *complex* domain should get no other domain, not even a simple one; (4) never give one team two *complicated* domains — split into two smaller teams instead.

## Anti-patterns
- **Rewarding individuals over teams**: individual bonuses and merit ratings (per Deming) damage team behavior and misalign incentives with collective outcomes; reward and fund the whole team instead.
- **Ad hoc team growth without cognitive-load checks**: letting a successful team absorb more and more responsibility (as with the OutSystems example) until it becomes a bottleneck spread across too many unrelated domains.
- **Monolithic workplace / forced open-plan seating**: neither individual cubicles nor pure open-plan support both focused work and team collaboration; office layout imposed uniformly ignores that different tasks need different environments.

## Reference Tables
<!-- omitted: chapter has no author-presented table/matrix (Dunbar figures are prose lists, not a formal table) -->

## Worked Example
The mobile team at IKEA (2017, led by Albert Bertilsson and Gustaf Nilsson Kotte) kept absorbing new product responsibilities after a run of successful delivery. Work streams started blocking each other's releases. Despite being a high-performing team with strong autonomy, mastery, and purpose, the team was still overloaded. Applying Conway's law and cognitive-load reasoning, the leads realized the team actually owned two distinct products crammed into one codebase, and split the team in two — one team per product — restoring flow even though morale and skill were never the underlying problem; capacity allocation was.

## Key Takeaways
1. Assign all work to teams, never to individuals; a team that becomes highly effective (weeks to months to form) should stay stable, not be reshuffled at project boundaries.
2. Cap team size at 5–9 (rarely up to 15 in high-trust cultures) — this is a trust and communication-overhead limit, not a bureaucratic rule.
3. Diagnose overload with the domain-complexity heuristic (simple/complicated/complex counts per team), not with lines-of-code or headcount metrics.
4. Treat every team's outward interface as a "team API" and manage it deliberately — including docs, versioning promises, and visible priorities — the same way you'd manage a software API.
5. Reward, train, and fund the team as a unit; individual-level incentives undermine the "team as fundamental unit" premise.
6. Design office space (or virtual space) explicitly to support all three needed modes: focused individual work, intra-team collaboration, and inter-team collaboration.

## Connects To
- **Ch 1**: operationalizes the cognitive-load concern first raised there.
- **Ch 5**: the four fundamental team topologies exist specifically to keep each team's cognitive load within these bounds.
- **Ch 6**: "team-sized" software boundaries here become "fracture planes" in the next chapter's deeper treatment.
