# Chapter 6: Choose Team-First Boundaries

## Core Idea
Software should be split along "fracture planes" — natural seams, most often business-domain bounded contexts — sized to a single team's cognitive load, because unclear or accidental boundaries (hidden monoliths) are what actually block flow, not the choice of monolith vs. microservices per se.

## Frameworks Introduced
- **Bounded Context (Domain-Driven Design, Eric Evans)**: a unit for partitioning a larger domain model into smaller, internally consistent parts, each with its own unified, contradiction-free model and ubiquitous language.
  - When to use: as the *primary* fracture plane whenever splitting a monolith or defining new service boundaries.
  - How: identify subdomains that map to genuinely distinct business areas (e.g., media discovery / media delivery / licensing for a streaming service), accept that early boundary placement will need revision, and use techniques like event storming to converge on the model.
- **Fracture Planes**: natural seams in a software system that allow it to split cleanly into team-sized parts, by analogy to a stonemason splitting rock along its natural grain.
  - When to use: whenever splitting a monolith or defining new team/software boundaries, especially when a pure bounded-context split isn't sufficient alone.
  - How: apply (and combine) fracture planes for business-domain bounded context, regulatory compliance, change cadence, team location, risk profile, performance isolation, technology, and user personas; test candidates with "could we, as a team, effectively consume or provide this as a service?"

## Key Concepts
- **Monolith (six kinds)**: application monolith (one large deployable), joined-at-the-database monolith (shared schema), monolithic build (one giant CI build), monolithic release (bundled deploys), monolithic model (one domain language forced everywhere), monolithic thinking (one-size-fits-all standardization).
- **Distributed monolith**: a system split into services that are still coupled at test/release time (e.g., mandatory combined end-to-end testing before any release), giving none of microservices' independence benefits.
- **Regulatory compliance fracture plane**: splitting off the subsystem actually in scope for a regulation (e.g., PCI DSS card-data handling) rather than forcing the whole system through the heaviest process.
- **Change cadence fracture plane**: splitting parts of a system that need to change at different frequencies (e.g., quarterly reporting vs. daily features) so the slowest part doesn't gate everyone else.
- **Technology fracture plane**: splitting along technology lines is usually a bad default (it reduces team autonomy) but can be legitimate when integrating genuinely disparate/legacy stacks with very different pace of change (e.g., mobile, cloud, embedded).

## Mental Models
- Treat "typical" (technology-layered: front end / back end / DBA) boundaries as a default anti-pattern, and team-first (domain-owned, vertical) boundaries as the goal — Figure 3.3's contrast in the book.
- When multiple fracture planes are plausible, combine them rather than picking exactly one; real systems usually need a primary domain split plus a secondary split (e.g., by regulation or risk).
- For genuinely disparate technology stacks (mobile/cloud/embedded), decide which side becomes "the platform" and which side becomes its client/consumer — don't leave the relationship undefined.

## Anti-patterns
- **Splitting a monolith without a team lens**: fracturing the software by size or convenience alone, ignoring team cognitive capacity, location, or interest, risks creating a "distributed monolith" with all the coupling and none of the independence.
- **Monolithic thinking as governance**: standardizing tooling/technology across all teams to simplify management oversight measurably reduces learning, experimentation, and solution quality (per *Accelerate*'s research).
- **Forcing regulatory rigor onto the whole system**: applying PCI-DSS-level process to an entire monolith because *part* of it touches card data increases blast radius of audits and slows everything down.
- **Monolithic workplace**: a single, uniform office layout for every team, ignoring that different work modes (deep focus vs. collaboration) need different physical/virtual environments.

## Reference Tables
| Fracture plane | Split when... |
|---|---|
| Business domain (bounded context) | Distinct, internally-consistent business areas exist (primary/default plane) |
| Regulatory compliance | Only part of the system is in scope for a regulation (e.g., PCI DSS) |
| Change cadence | Parts of the system need to change at very different frequencies |
| Team location | Teams can't achieve full colocation or true remote-first for one unit |
| Risk | Distinct risk appetites coexist (e.g., acquisition vs. retention features) |
| Performance isolation | One part needs scaling/failover the rest doesn't (e.g., seasonal peak load) |
| Technology | Genuinely disparate, hard-to-automate legacy tech with a different pace of change |
| User personas | Distinct user segments need very different feature subsets (e.g., tiered pricing, admin vs. regular users) |

## Worked Example
Poppulo (Stephanie Sheehan, Damien Daly) grew from a single team to eight product teams, one SRE team, and an infra team over three years. Rather than splitting arbitrarily, they invested time up front assessing how independent each business domain really was (people, content, events, email, mobile, analytics) using DDD techniques like event storming, before splitting the monolith along those domain boundaries. They layered a secondary regulatory fracture plane (ISO 27001) as a small specialist concern, and kept a horizontal UX team as an internal consultancy for consistency across all the vertical product teams. The explicit domain-first assessment — checking independence before splitting, rather than splitting first and discovering coupling later — is what let them scale engineering from 16 to 70 people while keeping teams autonomous.

## Key Takeaways
1. Default to business-domain bounded contexts as the primary fracture plane; treat every other plane (regulation, cadence, risk, performance, technology, persona, location) as a secondary or combinable consideration.
2. Watch for the six kinds of hidden monolith beyond the obvious application monolith — a codebase can look modular while still being coupled at the database, build, or release layer.
3. A "distributed monolith" (services that still require combined end-to-end release testing) is a sign the split didn't achieve real team independence.
4. Splitting along technology lines should be the exception, reserved for genuinely disparate stacks with different paces of change — not the default axis for team boundaries.
5. Always test a candidate boundary with "could we, as a team, consume or provide this as a service?" before committing to it.

## Connects To
- **Ch 3**: applies the "team-sized software boundary" principle established there.
- **Ch 5**: fracture planes are how you decide *where* stream-aligned team boundaries actually fall.
- **Ch 7**: once boundaries exist, interaction modes (especially collaboration) are used to validate and refine them.
