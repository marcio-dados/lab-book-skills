# Cheatsheet — Platform Engineering Decision Guide

## Decision Rules

- **When deciding if you're "doing platform engineering"**: check all four pillars — curated product approach, software-based abstractions, broad application-developer base, operating as a foundation. Missing any one → you're doing something else (ops, a feature shop, a niche tool, an unreliable system). (Ch 2)
- **When a team asks for a full API encapsulation of an OSS/vendor system**: ask "does this make application engineers more productive, or just make our job easier?" If unsure, default to allowing direct access. (Ch 2)
- **When deciding paved path vs. railway**: paved path if the gap is "these exist but aren't glued together"; railway if the gap is "nothing exists and many teams need it." (Ch 2)
- **When staffing on-call**: use merged DevOps (software + systems engineers, one rotation) unless you're FAANG-scale with 10+ dedicated engineers per platform. (Ch 6)
- **When on-call pages exceed 5/week (business-impacting)**: stop feature work, prioritize stability — this is a business-priority signal, not a personnel failure. (Ch 6)
- **When choosing customer-facing vs. internal SLOs**: customer-facing → few, minimize false positives, use to start a trade-off conversation. Internal → many, tolerate false positives (missing a real issue is worse). (Ch 6)
- **Before starting a v2 rewrite**: ask whether the team's actual mindset (pioneer/settler/town planner) matches what a from-scratch build demands. If not (most mature teams), rearchitect instead. (Ch 8)
- **Before betting on a rising OSS/vendor wave**: require all three — adjacent business need justifying investment, real feature gaps in the current system, clear ecosystem trajectory disparity. Missing any one → be wary. (Ch 8)
- **Before proposing a rearchitecture**: always factor in migration cost explicitly (ask "how will existing customers move to it?") before committing to the vision. (Ch 8)
- **When a migration deadline is >12 months out**: invest in engineering (transparent migration tooling), not heavy coordination — industry deadlines often slip or get solved collectively. (Ch 9)
- **Before hiring a project manager for a migration or big project**: prove automation has been exhausted first. (Ch 7, Ch 9)
- **When deciding true sunsetting vs. migration**: sunset only if very few users, disproportionate support cost, or genuine need to redirect focus — otherwise find a migration path instead. (Ch 9)
- **When a stakeholder request can't be fully met**: prefer "yes, with compromises" (narrower scope now, fuller later) over binary yes/no. (Ch 10)
- **When deciding whether to say a hard "no"**: distinguish priority ("not yet"), technical readiness ("not yet"), product-strategy mission creep ("no"), and true infeasibility ("no") — always offer an alternative path. (Ch 10)
- **In a budget crunch**: come with your own proposed cuts grouped by project-team size (3-12 people); never report person-by-person. (Ch 10)
- **When adoption is used to justify a mandatory migration**: check whether it reflects genuine organic demand or has become "a stick to use on customers." (Ch 11)
- **When considering a reorg to fix overlapping platforms**: reserve for high-cost, clear-benefit misalignment — it doesn't shortcut rearchitecture/migration/sunsetting work. (Ch 11)
- **When a platform becomes a business bottleneck**: check if surface area × application diversity × low user trust are combining structurally before assuming it's a staffing problem. (Ch 12)
- **Before building a unified "single pane of glass" UI**: invest in a coherent, documented, REST-consistent API layer first — the UI is secondary and persona-specific. (Ch 13)
- **When customers ask for a specific OSS system**: ask if it's a genuine must-have feature or a preference/habit before granting it. (Ch 13)
- **Before adopting a trending external technology internally**: check awareness, compatibility, engineering quality, and time-to-market alignment — don't assume popularity transfers. (Ch 14)
- **Before launching a platform meant to displace a legacy system**: never rely on "build it and they'll come" — build explicit off-ramps, on-ramps, and incremental cutover tooling. (Ch 14)

## Thresholds & Defaults

| Metric | Threshold | Source |
|---|---|---|
| Sustainable on-call pages | < 5 business-impacting/week (< 2 = happy, 2-5 = some unhappiness, > 5 = attrition risk) | Ch 6 |
| On-call rotation frequency | ≤ 1 week in 4 (ideally 1 in 6-8) | Ch 6 |
| Synthetic monitoring investment (AWS-scale reference) | ~25% dev time, ~10% resource cost | Ch 6 |
| System-improvement project size cap | ≤ ~3 developer-months (else → rearchitecture) | Ch 7 |
| KTLO share of team workload | ≤ 40% | Ch 7 |
| Non-KTLO work split (Google 70/20/10, lens not budget) | 70% core / 20% adjacent / 10% transformational | Ch 7 |
| Roadmap merge depth | one level up (skip-manager) only | Ch 7, Ch 11 |
| FinOps dedicated specialist justified | ~200+ engineers | Ch 7 |
| Rearchitecture planning horizon | 3-5 years, with 12-month incremental win cycles | Ch 8 |
| Migration deadline "real" horizon | ~12 months (beyond that, treat as soft) | Ch 9 |
| Combined support + on-call load ceiling | ≤ ~50% of team capacity | Ch 6 |
| Dunbar's number (formal ownership trigger) | ~50-250 people | Ch 3, Ch 10 |
| PjM ratio guideline | ~1 per 50 platform engineers, never exceed | Ch 3 |
| 1:1 cadence | quarterly (Keep Satisfied/Informed), monthly (Manage Closely) | Ch 10 |
| Release-engineering investment warning | > 12 developer-months/year → may be overbuilding | Ch 6 |

## Trade-off Matrix: Rearchitecture vs. v2 Rewrite

| Dimension | Rearchitecture | v2 Rewrite |
|---|---|---|
| Risk of scope creep (second-system effect) | Low — bounded by existing platform | High |
| Mindset match for mature (settler/town-planner) teams | Good fit | Poor fit — needs pioneer agility |
| Customer-visible disruption | Minimized by design | High — requires full migration |
| Delivery cadence | Incremental, yearly wins | Often "big bang," years to any value |
| Recommended default | **Yes, in nearly all cases** | Only when truly starting from nothing |

## Tells & Smells

- Team refuses to hire outside their own technical background ("no software engineers need apply" or vice versa) → single-focus team stuck in a self-reinforcing hiring bias (Ch 4).
- Constant "wall of shame" dashboards and clipboard-chasing during migrations → engineering/communication investment was skipped, now relying on last-resort enforcement (Ch 9).
- Multiple "not GA-ready yet" platforms competing for the same customer base to justify headcount → product-strategy misalignment, not healthy duplication (Ch 11).
- Stakeholders say "you just build things for the sake of building things" → likely a "batteries included" deep-coupling failure mode, or history of unfulfilled big-investment promises (Ch 8, Ch 12).
- A team's support/on-call queue has significant items open at end of every week → noncritical support and on-call have not been separated, or team is past sustainable combined load (Ch 6).
- Same OSS/vendor "next industry standard" argument used to justify a rearchitecture, without feature-gap or business-need criteria met → hype-driven bet, be wary (Ch 8).
