# Chapter 8: Rearchitecting Platforms

## Core Idea
When incremental system improvements can no longer keep up with growth, the answer is rearchitecture (evolving a live system's architecture while it keeps serving load) rather than a "v2" rewrite — because a v2 conflates building a new product with rebuilding a scaled architecture, demanding an agility (pioneer) mindset from a team culturally suited to settler/town-planner work.

## Frameworks Introduced
- **Pioneers / Settlers / Town Planners (Simon Wardley)**: three engineering mindsets, not fixed people-types, each suited to a different stage of platform maturity. Pioneers explore ambiguous, unproven territory and fail often but generate wonder; Settlers turn prototypes into trustworthy, profitable products; Town Planners industrialize for scale, cost, and efficiency. Teams waste time arguing implementation details when they haven't first agreed which mindset the work calls for.
  - How: map platform maturity stage → dominant mindset (Table 8-1): Scrappy platform → Pioneer (agile feature delivery, low reliability/security bar, efficiency an afterthought); Scalable platform → Settler (balancing agility for new customers vs. certainty for big ones, operational rigor, paved-path security, performance optimization); Robust platform → Town Planner (metric-driven reliability, secure-by-design, system-wide efficiency, forward planning across all four).
- **Rearchitecture vs. v2**: rearchitecture is iterative reimplementation of a live system's architecture with natural limits on customer-visible change (delivered within the existing platform's logical boundary); v2 is a from-scratch replacement requiring a full migration. Rearchitecture avoids both the second-system effect (v2 scope creep from "fixing everything wrong with v1") and the mindset mismatch (settler/town-planner teams don't have a pioneer's agile, ambiguous-requirements instincts).
- **Four rearchitecture goal categories**: Features (what's currently impossible/prohibitively expensive that a new architecture enables), Efficiency (aggregate cost-effectiveness, performance headroom), Reliability (operational-issue reduction at higher load), Security (breach likelihood/compliance cost reduction) — a real rearchitecture proposal should push on all four, plus look at subsuming adjacent/shadow systems and evaluating big bets on rising OSS/vendor ecosystems.
- **Four-step rearchitecture planning framework**: (1) Think big on final goals (3–5 year horizon, all four capability categories, subsuming adjacent systems, evaluating OSS/vendor big bets) → (2) Factor in migration costs (many "great" proposals collapse once realistic migration effort — e.g. "hundreds of development-years" — is honestly estimated; see Ch 9) → (3) Determine major 12-month wins (three fallback goals: Goal 1 audacious/business-moving, Goal 2 smaller-but-real value, Goal 3 just get new components serving real load — repeated yearly across the 3–5 year project to avoid the "long slog") → (4) Get leadership buy-in and be prepared to wait (leaders must actively commit reputationally, since they'll have to defend it through layoffs/reorgs/mandates over years).
- **Three-criteria test for betting on a rising OSS/vendor ecosystem**: (1) an adjacent business need already justifying large rearchitecture investment/headcount, (2) the current platform has real feature gaps the new ecosystem fills for subsuming adjacent systems, (3) clear disparity in ecosystem trajectory (community momentum, new-project adoption). Meet all three before betting; otherwise be wary.

## Key Concepts
- **Second-system effect** (Fred Brooks, 1964/1975): a team's second system balloons in scope as it tries to correct every perceived v1 flaw, often failing to ship or shipping to a user base that's moved on. Brooks' own mitigation: staff with people who've been through 2+ system builds already.
- **Security by design / by default**: architecting so secure behavior doesn't depend on human vigilance and creates real separation between users and hazards (eliminate hazards — e.g. memory-safe rewrite; or reduce them — e.g. standardized auth) — contributed by Kelly Shortridge (*Security Chaos Engineering*). Paved paths make the resilient option the path of least resistance (opt-out, not opt-in).
- **Rearchitecture guardrails**: compatibility (avoid backward-breaking API changes; if unavoidable, ship as a new versioned API with long migration lead time; cap how many live versions you support), testing (integration tests with real user code in monorepos, property-based testing/fuzzing, synthetic monitoring as a substitute for some functional integration testing — not a substitute for real safety), lower/staging environments (customers' own pre-release testing catches what yours misses — but don't let "test in prod" habits creep in), and slow/tranche rollouts (canaries, staying a version behind bleeding-edge OSS to let the community find issues first, without falling out of the security-patch support window).
- **New-hire-led rearchitecture anti-pattern**: a new senior hire with relevant experience elsewhere is valuable for feedback on rearchitecture proposals but shouldn't lead a rearchitecture in their first ~12 months — they lack context on your specific platform, culture, and customer trust relationships.
- **Pioneer/shadow-platform integration tension**: when a robust, town-planner-culture platform team needs fast movement on a sudden capability gap (e.g. public cloud adoption), embedding pioneers with application teams to move fast (accepting "some mess") works, but the eventual integration back into core platforms will make pioneers, their early customers, and the core platform team all unhappy to some degree — manage it deliberately rather than let duplicate platforms persist.

## Mental Models
- Before proposing a v2, ask whether the team's actual working mindset (pioneer vs. settler vs. town planner) matches what a from-scratch build demands — if not, rearchitecture is the safer path even though it looks harder.
- When evaluating a rearchitecture proposal, insist on an honest migration-cost estimate before endorsing the "think big" vision — teams chronically underestimate this until directly asked "how will existing customers move to it?"
- Treat "we made it through this year on incremental patches" as ambiguous evidence, not proof a rearchitecture is unnecessary — leadership sometimes wrongly reads survival as validation that the old architecture is fine.
- For security, favor architecture that removes the need for human vigilance (paved paths, secure defaults) over training/awareness programs — the platform, not the individual engineer, is the highest-leverage point of control.

## Reference Tables
| Maturity stage | Feature delivery | Reliability | Security | Efficiency | Mindset |
|---|---|---|---|---|---|
| Scrappy | Agile, frequent revision | Low, high outage tolerance | Low, assumes good faith | Afterthought | Pioneer |
| Scalable | Big vs. small customer tension | Operational rigor, tension with new onboarders | Paved paths limit blast radius | Optimize for dominant loads | Settler |
| Robust | New/small customers wait behind big ones | Metric-driven (3-9s baseline, 5-9s desired) | Secure by design, zero ad hoc trust | System-wide $ efficiency | Town Planner |

## Anti-patterns
- **v2 rewrite instead of rearchitecture**: couples product redesign with architecture rebuild, triggering the second-system effect and a mindset mismatch.
- **New hires leading a rearchitecture in their first year**: pattern-matches to a previous employer's solution without the context to know it doesn't transfer cleanly.
- **"Kill it with fire" all-in replacement instinct**: abandoning incremental system improvements (Ch 7) entirely in favor of an all-or-nothing rewrite under operational pressure.
- **Letting pioneer-built shadow capabilities calcify into permanent duplicate platforms**: happens when leadership doesn't actively force and manage the integration decision.
- **Skipping migration-cost analysis in a rearchitecture proposal**: "think big" visions routinely collapse once real migration effort is estimated.

## Worked Example
A platform team running Mesos for ~20% of workload faced Kubernetes' rising momentum. They bet on migrating using three criteria: (1) an adjacent business need — the on-prem-to-cloud move — already justified rearchitecture headcount over 5 years; (2) Mesos had real feature gaps (less "out of the box" support) that blocked containerizing 100% of workloads; (3) ecosystem trajectory clearly favored Kubernetes (conference momentum, vendor investment, no new Mesos bets anywhere). The bet paid off in hindsight. The chapter contrasts this with peer companies that made the same bet without matching criteria (e.g. Mesos already ran nearly all their load and they were already on the cloud, making migration a costly sideways move that didn't pay off) — the lesson is that all three criteria must hold, not just ecosystem hype.

## Key Takeaways
1. Prefer rearchitecture (live, incremental) over a v2 rewrite — it avoids both the second-system effect and a mindset mismatch with your settler/town-planner team.
2. Match engineering mindset to platform maturity stage (pioneer → settler → town planner) rather than expecting one team culture to handle every stage.
3. A real rearchitecture proposal pushes on all four capability categories (features, efficiency, reliability, security), not just the one causing today's pain.
4. Always estimate migration cost honestly before committing to a rearchitecture vision — this alone kills many overambitious proposals, appropriately.
5. Break a 3–5 year rearchitecture into yearly cycles with three fallback goals (audacious / smaller-but-real / just ship components to production) to avoid the "long slog."
6. Invest in security as architecture (paved paths, secure defaults) rather than training — make the safe path the easy path.
7. Use concrete guardrails (compatibility windows, real integration testing, staging environments, slow rollouts) to make rearchitectures invisible to existing customers.
8. Only bet on a rising OSS/vendor wave when adjacent business need, real feature gaps, and ecosystem trajectory all align — not on hype alone.

## Connects To
- **Ch 5**: incremental delivery/POC discovery techniques recur in "Determine major 12-month wins."
- **Ch 6**: synthetic monitoring, change management, and release engineering guardrails are reused directly for rearchitecture safety.
- **Ch 7**: system improvement stack ranks and the 70/20/10 model connect to when a project graduates from "improvement" to full rearchitecture; the "long slog" anti-pattern is revisited here.
- **Ch 9**: migration cost estimation (Step 2 here) is developed in full detail next.
- **Ch 11**: balancing multiple simultaneous rearchitecture requests across platform teams gets further treatment.
