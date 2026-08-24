# Chapter 4: Building Great Platform Teams

## Core Idea
Great platform teams deliberately balance software-engineering strength with systems-engineering depth across four distinct engineer roles, plus supporting product/program roles, because single-focus teams (too systems-heavy or too development-heavy) each get structurally stuck in their own way.

## Frameworks Introduced
- **The Four Platform Engineer Roles**: Software engineer, Systems engineer (broad generalist, often "DevOps engineer"), Reliability engineer (depth in reliability specifically), Systems specialist (deep single-domain expert: kernel, network, performance, storage).
  - When to use: as a hiring/recognition map — decide which roles you actually need before hiring, and don't collapse them into one title/ladder.
  - How: hire software engineers who are drawn to understanding systems, comfortable being on business-critical on-call, and comfortable shipping at a deliberate pace (not "pioneers" chasing novelty); hire one broad systems engineer before specialists; add reliability engineers only once you need dedicated incident/SLO/chaos-engineering leadership; add systems specialists only once the need and org size clearly justify full-time depth (a large org, not a curiosity).
- **Two failure archetypes for single-focus teams**: "Too Much Systems Focus" (operationally excellent, but only writes automation/one-off tooling, leans on rules/wikis/PMs instead of building better abstractions, and hiring filters out software engineers) vs. "Too Much Development Focus" (loves building "vNext"/"golden path" systems, treats the current system as a "haunted graveyard," under-invests in operations, and is chronically over-optimistic on estimates).
  - When to use: diagnose why a platform team is stuck by matching its symptoms to one archetype, then hire deliberately for the missing role/culture rather than assuming "just hire good people" fixes it.
- **Title / Level-matrix / Interview-process separation**: these three are independent dials, not one bundle — allow role-specific titles (e.g. kernel engineer) without forcing a new level matrix or interview process for each.
  - How: keep software engineers (platform, data, mobile, frontend) on one shared ladder graded by outcomes, not methods; create at most one additional level matrix for all non-software "systems" roles combined (not three); fork the interview process for platform roles when the company-wide software interview doesn't map (e.g. platform work needs systems-breadth discussion, not pure algorithms).

## Key Concepts
- **Haunted graveyard** (Carla Geisser): a legacy system a development-focused team treats as a curiosity to poke at, not something to understand and own — leads to operational neglect.
- **Customer empathy (vs. "user empathy")**: interview trait distinct from technical skill — screen for genuine appreciation that engineers are building for other humans; "customer implies obligations, users are just some schmucks" (Camille Fournier).
- **Take-home coding interview for systems roles**: time-boxed take-home problem plus a discussion interview, used instead of live whiteboard coding — avoids penalizing systems engineers for whom whiteboard performance doesn't predict job performance, while still validating real coding ability.
- **Product owner vs. product manager**: in internal platform contexts (no external marketing need), there's no reason to split these roles — hire for strategic judgment plus backlog mechanics.
- **Specialist-as-internal-evangelist (anti-pattern)**: a systems specialist who spends full time on OSS contribution, conference talks, and evangelism internally without concrete delivery, undermining their own credibility.

## Mental Models
- Diagnose a "stuck" team by asking which side of the software/systems divide dominates its hiring filter — a technical interview bias becomes a cultural filter that self-reinforces (churn of the "wrong" hires confirms the team's own bias).
- When you can't get a platform engineer promoted on a generic software-engineering ladder, "stretch within the system" — find someone one level up, outside platform engineering, willing to vouch that "this person's impact is as high as mine," using concrete evidence (widely adopted tools/dashboards, quality of customer interactions, postmortem contributions).
- For engineering managers moving into platform leadership: value operational experience, comfort with long, careful, high-stakes delivery timelines (vs. "move fast" instincts), and enough attention to detail to substitute for instinct until it's earned — but avoid becoming an actual micromanager.
- For product management on internal platforms, prefer staff engineers who are strong two-way communicators (roughly a quarter of staff engineers fit this) over engineering managers or TPMs when you can't hire a dedicated PM — TPMs and EMs default to treating ambiguous product trade-offs as execution problems to be stack-ranked.

## Reference Tables
| Role | Title flexibility | Interview | Level matrix |
|---|---|---|---|
| Software engineer | "software engineer"; "platform software engineer" only if unavoidable | Custom behavioral fit interview | Shared, company-wide |
| Systems engineer | Allow specialized (e.g. DevOps engineer) | Same base, more design-question flexibility on systems breadth | One shared "systems" matrix (impact ≈ software engineer, different levers) |
| Reliability engineer | Allow specialized (e.g. SRE) | Same base + depth on reliability practice | Same shared systems matrix |
| Systems specialist | Allow per-role (kernel/perf/network/storage engineer) | Same base + depth in specialty | Same shared systems matrix |

## Anti-patterns
- **"No software engineers need apply" hiring filter**: systems-focused teams that screen only for deep operational trivia end up self-selecting away the engineers who could build better abstractions.
- **Whiteboard-only coding bar for systems engineers**: penalizes candidates whose real skill doesn't show under artificial time pressure; prefer take-home + discussion.
- **Forcing one job title/ladder/interview onto all roles for administrative simplicity**: demeans specialists' identity and produces a bad fit for none of the roles it tries to serve.
- **Hiring product managers or restructuring before the team has demonstrated delivery** (echoes Ch 3): PMs without an engineering-side product culture become backlog groomers.
- **Letting a "development team" culture default to "SRE's problem"**: a separate, undersized SRE org lets the majority team avoid owning reliability, entrenching finger-pointing.

## Worked Example
A compute platform team split into a PhD-heavy development team (hired on a generic "software engineer" bar with no systems/customer-empathy screening) and a separate, understaffed SRE org. The dev team treated every problem as solvable by "build something new," ignored migration plans ("build it and they will come"), and blamed SRE for reliability. The fix: merge both teams under a manager from the SRE side with strong operational and stakeholder-management experience; deliberately mix "builders" with people happy to operate/scale existing systems and those closer to customers; move from a "one engineer, one feature" model to a roadmap model; accept attrition among purely research-minded developers who preferred the old SRE-absorbs-reliability arrangement; then bring in a product manager, carefully preserving technical leads' and engineering managers' sense of ownership. Stabilization took about six months.

## Key Takeaways
1. Deliberately staff all four engineer roles (software, systems, reliability, specialist) rather than letting a hiring bias produce a single-focus team.
2. Separate title, level matrix, and interview process — allow flexibility on the first without duplicating the other two for every role.
3. Interview for customer empathy explicitly (concrete behavioral questions), because "don't hire jerks" is too blunt a filter and misses defensive, not just abrasive, behavior.
4. Great platform managers need operational experience, comfort with long/careful delivery, and enough attention to detail to compensate until instinct is built — application-engineering backgrounds without this context are a risk.
5. When you can't hire dedicated PMs, look to staff engineers with strong two-way communication skills before defaulting to engineering managers or TPMs.
6. Merging culturally divergent subteams (e.g. dev-heavy vs. SRE-heavy) requires deliberate leadership: new shared management, mixed team composition, and active reinforcement of a balanced culture — it won't happen on its own.

## Connects To
- **Ch 1**: revisits the systems-engineer/software-engineer dichotomy first introduced there.
- **Ch 5**: the product-management theme (product owners, PMs) continues into "Platform as a Product."
- **Ch 6**: expands on the operational practices (on-call, support) that platform engineer roles must be comfortable with.
- **Ch 8**: the "pioneer" engineer archetype is revisited as a good fit for early-stage platforms specifically.
- **Ch 10**: stakeholder-management techniques for platform managers are developed further.
