# Cheatsheet

## Team size defaults (Dunbar's Number)
| Grouping | Normal limit | High-trust org limit |
|---|---|---|
| Single team | 5–8 (up to 7–9) | up to ~15 |
| Tribe/family (group of teams) | ~50 | ~150 |
| Division/stream/P&L line | ~150 | ~500 |

**Rule**: when a grouping crosses its limit, split off a new semi-independent unit — don't just add headcount to the existing one.

## Team ratio default
**Rule**: aim for 6:1 to 9:1 stream-aligned-to-other teams (i.e., about 1 in 7 to 1 in 10 teams is enabling/platform/complicated-subsystem). If your ratio is far off this, you likely have too many non-stream-aligned teams (functional silos) or too few (under-supported streams).

## Choosing a team interaction mode
| Question | Answer → Mode |
|---|---|
| Is the boundary/API still unknown or unproven? | **Collaboration** (temporary, ≤1 partner team at a time) |
| Is the boundary proven and predictable delivery matters more than discovery? | **X-as-a-Service** (can scale to many simultaneous partners) |
| Is the issue a capability gap, not an ownership question? | **Facilitating** (time-boxed, small number of teams at once) |

## Diagnosing interaction friction (signal → likely cause)
| Symptom | Likely cause |
|---|---|
| X-as-a-Service relationship needs constant back-and-forth | Boundary in wrong place, API poorly specified, or provider missing a capability (e.g. DevEx) |
| Collaboration mode shows little real interaction | Team doesn't see the value, lacks the skill, or the collaboration boundary is too ambitious |
| Enabling relationship has lasted many months with no end in sight | Not really facilitating anymore — check for ivory-tower or permanent-dependency anti-pattern |
| Team collaborating with 2+ teams simultaneously | Violates the collaboration constraint — cognitive load will exceed capacity |

## Cognitive-load domain-count rules (per team)
1. Each domain maps to exactly **one** team (split the domain, not the ownership, if it's too big).
2. A team can hold **2–3 simple** domains (low switching cost).
3. A team with **one complex** domain gets **no other domain** — not even a simple one.
4. **Never** give one team two **complicated** domains — split into two teams instead.

## Choosing a fracture plane (in priority order)
1. **Business domain (bounded context)** — default/primary plane.
2. **Regulatory compliance** — if only part of the system is in scope.
3. **Change cadence** — if parts change at very different frequencies.
4. **Risk** — if distinct risk appetites coexist.
5. **Performance isolation** — if one part needs different scaling.
6. **Team location** — only if neither full colocation nor true remote-first is achievable.
7. **Technology** — only for genuinely disparate/legacy stacks with different pace of change; avoid as a default.
8. **User personas** — if distinct segments need very different feature subsets.

**Litmus test for any candidate plane**: "Could we, as a team, effectively consume or provide this subsystem as a service?" If yes → good split candidate.

## Converting legacy team types to the four fundamentals
| Legacy team | Becomes | Condition |
|---|---|---|
| Infrastructure team | Platform team | Adopts product-management discipline, self-service |
| DBA team | Enabling team | Focuses on advisory/awareness, not schema-level execution |
| DBA team | Platform (component) | Provides Database-as-a-Service |
| Component/tooling team | Enabling team | Short-lived, focused remit |
| Component/tooling team | Platform | Clear roadmap, ongoing service |
| Component team | Complicated-subsystem | Genuinely requires deep specialist knowledge |
| Architecture team | Part-time enabling team | Shapes team APIs, never mandates |

## Interaction-mode profile by team type (Table 7.4)
| Team type | Collaboration | X-as-a-Service | Facilitating |
|---|---|---|---|
| Stream-aligned | Typical | Typical | Occasional |
| Enabling | Occasional | — | Typical |
| Complicated-subsystem | Occasional | Typical | — |
| Platform | Occasional | Typical | — |

## Recognition signals — time to redesign topology
- A startup crosses ~15 people (Dunbar's number) — expect a first split.
- Same person/team is *always* the bottleneck for certain changes — specialization has calcified into a silo.
- Velocity/throughput trending down year-over-year (beyond normal variance) — check for creeping hard dependencies or tech debt.
- WIP keeps growing, with items waiting on another team's action — hard-dependency signal.
- Multiple business services rely on a large, hard-to-reuse set of underlying services — candidate for a platform wrapper.

## Quick defaults
- **Team lifespan before high effectiveness**: 2 weeks to 3 months.
- **Team reassignment cadence**: ~once a year max, even in high-trust orgs (longer, 18–24 months, in lower-trust orgs).
- **Collaboration partner limit**: at most 1 team at a time.
- **Enabling engagement length**: weeks to months — plan for self-obsolescence from day one.
