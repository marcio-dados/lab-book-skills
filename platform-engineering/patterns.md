# Patterns & Techniques

## Curated Product Approach: Paved Path
**When to use**: multiple existing offerings need to be layered into an easy, common workflow; the gap is "these things exist but aren't glued together well."
**How**: identify the ~20% of use cases covering ~80% of needs (Pareto), build an opinionated default workflow for them, and let outlier needs step off the path.
**Trade-offs**: high leverage for the common case; requires discipline to say no to edge-case demands that would dilute the opinionation. (Ch 2)

## Curated Product Approach: Railway
**When to use**: a genuine infrastructure gap exists that no current offering covers, often surfaced by an application team's own prototype.
**How**: generalize the prototype into a broadly useful platform (e.g. a batch job platform, notifications system).
**Trade-offs**: requires major investment; only pursue when the pattern of need spans multiple teams. (Ch 2)

## Merged DevOps On-Call
**When to use**: nearly all platform teams (except FAANG-scale with 10+ dedicated engineers per platform).
**How**: staff a single on-call rotation with both software and systems engineers, rather than splitting a separate SRE/DevOps team.
**Trade-offs**: excludes engineers unwilling/unable to be on-call; avoids the "spread thin across many platforms" failure of split rotations. (Ch 6)

## Sustainable On-Call Load Management
**When to use**: any team staffing 24x7 on-call.
**How**: target <5 business-impacting pages/week; rotate no more than 1 week in 4-8; eliminate false alarms (offer dashboards as an alternative "pulse"); prioritize stability over features when above threshold.
**Trade-offs**: may require pausing feature delivery; don't try to fix load with on-call pay — it doesn't address root cause. (Ch 6)

## Four-Stage Support Escalation Ladder
**When to use**: growing support load on a platform team.
**How**: (1) formalize support levels/SLA and categorize tickets; (2) separate a business-hours support rotation from on-call once load stacks up (keep total ops <~50%); (3) hire a support specialist only once truly overloaded, preferring growth-path hires (T1→T2→platform engineer) over permanent T1-only staff; (4) at scale, build a company-wide T1 Engineering Support Organization with tiered SLAs and an embedded expert-customer network.
**Trade-offs**: skipping stages either burns out the team (no separation) or over-hires prematurely (permanent specialist before need is proven permanent). (Ch 6)

## Change Management as CI/CD Precursor
**When to use**: stateful, complex platforms not yet ready for full automated CI/CD.
**How**: mandate documentation + review + pre-production testing for all production changes; use it to surface where release-engineering automation investment is needed before the one engineer who "knows the sharp edges" leaves.
**Trade-offs**: adds toil until automation is built; skipping it risks outages like the 2017 AWS S3 incident (one mistyped CLI parameter). (Ch 6)

## Synthetic (Active) Monitoring
**When to use**: platforms operating complex OSS/vendor dependencies they didn't build.
**How**: simulate real user/API workflows against production continuously; use for end-to-end monitoring, forced "customer understanding," lower MTTR via practiced troubleshooting, and triangulating platform-wide vs. customer-specific issues.
**Trade-offs**: real investment (~25% dev time, ~10% resource cost at AWS scale per Ian's estimate); not a substitute for real safety nets like canaries. (Ch 6)

## Five-Part Project Proposal
**When to use**: any long-running platform project before implementation.
**How**: write background/tenets, problem details (before solution), alternatives considered, chosen solution + rationale, and a plan of action with milestones; review with management and lead engineers before an action plan.
**Trade-offs**: upfront time investment; skipping it risks overreach or starting too big. (Ch 7)

## Bottom-Up Roadmap Merge
**When to use**: teams under delivery or operational pressure needing more than a pure product roadmap.
**How**: combine KTLO (cap ~40%), mandates (estimate net impact politically), and three separately stack-ranked system-improvement lists (reliability, efficiency, security) with the product roadmap; apply Google's 70/20/10 model as a discussion lens, not a budget; merge across teams only one level up (skip-manager).
**Trade-offs**: rolling up further than skip-manager level loses fidelity and invites headcount politics. (Ch 7)

## Biweekly Wins and Challenges
**When to use**: any platform team, especially those with long-horizon, hard-to-see-progress work.
**How**: line managers write Situation→Action→Result bullets; each level up selects/rewrites the most impactful for a broader audience; always include genuine Challenges, not just Wins.
**Trade-offs**: requires mandating and iterating on quality over 6-12 months; omitting Challenges undermines the trust-building purpose. (Ch 7)

## Rearchitecture (vs. v2 Rewrite)
**When to use**: a platform is architecturally underscaled but still critical and live.
**How**: iteratively reimplement the architecture within the existing platform's boundary, limiting customer-visible change; use the four-step planning framework (think big on goals → factor in migration costs → determine 12-month wins with 3 fallback goals → get leadership buy-in).
**Trade-offs**: slower-feeling than a "clean" v2, but avoids the second-system effect and matches the settler/town-planner mindset most mature platform teams actually have. (Ch 8)

## Security by Design / by Default (Paved Paths for Security)
**When to use**: reducing security hazard exposure across application teams.
**How**: build platform-level patterns (automated testing tools, IaC-based deployment with automatic cleanup, config management, secrets management, standardized observability/auth middleware, tenant isolation) that don't depend on human vigilance and separate users from hazards by default (opt-out, not opt-in).
**Trade-offs**: requires iterative investment; don't try to "revolutionize" security overnight — select opportunities aligned with current priorities. (Ch 8)

## Transparent Migration Engineering
**When to use**: any platform anticipating recurring migrations (nearly all).
**How**: minimize glue and version variation; combine judicious APIs with container packaging, autoscaling, and canary/blue-green deployment to run multiple versions simultaneously; back with agreements (chaos-testing expectations, customer-maintained acceptance tests, defined maintenance windows).
**Trade-offs**: requires upfront agreements with customers that may feel unusual (e.g. accepting random node restarts) but pay off in migration flexibility. (Ch 9)

## Automated Migration Tracking (Avoid Clipboards)
**When to use**: complex migrations with dependency trees, before defaulting to project-manager headcount.
**How**: build dependency-tracking code tied to an ownership metadata registry; auto-generate and assign tickets as dependencies clear; invest in observability/tracking tooling designed around what makes the migration easy for the affected team.
**Trade-offs**: significant upfront engineering investment; doesn't eliminate all human coordination, but shifts TPM work from "hand-to-hand combat" to overseeing the genuinely hard ~20%. (Ch 9, Ch 13)

## Stakeholder Power-Interest Mapping
**When to use**: any platform leader with multiple stakeholder groups.
**How**: plot stakeholders on power × interest; prioritize high-power/high-interest even when they're disengaged until unhappy; use quarterly 1:1s for Keep Satisfied/Informed, monthly for Manage Closely, plus interlock meetings/CABs to scale beyond 1:1s.
**Trade-offs**: don't over-prioritize your own team's happiness over powerful stakeholders — it backfires in conflicts. (Ch 10)

## Yes / No / Not-Yet Compromise Framework
**When to use**: any stakeholder feature request you can't fully accommodate.
**How**: distinguish "not yet — priority call" (offer timeline/partner-build), "not yet — technical call" (be honest about the blocker), "no — product strategy call" (resist mission creep), "no — technical call" (not feasible; explain why); default to "yes, with compromises" (narrower scope now, fuller later) over binary yes/no.
**Trade-offs**: always-yes creates a Feature Shop; always-no creates an inflexible, distrusted team. (Ch 10)

## Budget-Defense Three-Step Process
**When to use**: downturns/budget scrutiny threatening team size or roadmap.
**How**: (1) tie every non-KTLO project to a business initiative — pause, shrink-and-fold, or actively build the case for orphaned speculative work; (2) group work into team-sized chunks (3-12 people), never person-by-person; (3) come with your own proposed cuts and strong opinions on what to keep.
**Trade-offs**: requires proactive honesty that can feel like giving ammunition to critics, but preserves credibility and the most important investments. (Ch 10)

## Organization-Wide Alignment Resolution
**When to use**: multiple platform area teams deadlocked over competing priorities/headcount.
**How**: (1) each team builds a bottom-up roadmap; (2) leadership distills cross-cutting themes into shared objectives used to reprioritize; (3) peer roadmap review surfaces hidden cross-team costs; (4) each area head proposes their own cuts.
**Trade-offs**: time-consuming and requires pre-existing trust between leaders; doesn't produce perfect agreement but enables genuine "disagree and commit." (Ch 11)

## Independent Product Management / Architecture Reporting Lines
**When to use**: multi-team platform organizations at risk of siloed product/architecture decisions.
**How**: keep platform PMs reporting to a separate product leadership line (not the engineering managers owning individual areas); give a principal/staff engineer a cross-platform architecture advocacy mandate alongside the product leader.
**Trade-offs**: adds an org-design layer; without it, PMs and architecture decisions default to siloed optimization. (Ch 11)

## Building Blocks over Batteries Included
**When to use**: recovering from or avoiding deeply-coupled, hard-to-rearchitect end-to-end platform offerings.
**How**: treat well-defined, composable APIs as foundational; provide end-to-end workflow wrappers on top, but keep individual platform abstractions isolated and "pierceable" for advanced users.
**Trade-offs**: sacrifices some initial polish/usability for long-term operability, testability, and flexibility. (Ch 12)

## Product Discovery Reset for OSS Sprawl
**When to use**: a platform team supporting multiple overlapping broad-surface-area OSS systems (databases, messaging) is overwhelmed operationally.
**How**: bring in product-infrastructure-experienced leadership to investigate what teams actually require (not merely prefer) across the offerings; find consolidation opportunities that let you sunset one or more systems (including shadow platforms).
**Trade-offs**: multi-year iterative process with likely false starts (vendor-hosted attempts, SLA documentation, partial encapsulation) before landing the right consolidated offering. (Ch 13)

## Migration Strategy for Platform Adoption (Off-Ramp/On-Ramp/A-B Testing)
**When to use**: launching a replacement platform that needs to displace an entrenched legacy system.
**How**: build explicit off-ramps from the old system and on-ramps to the new one; use an A/B/incremental-traffic-dial tool to migrate with near-zero downtime instead of relying on "build it and they'll come."
**Trade-offs**: requires investment beyond the platform's core feature build; skipping it can leave you paying double maintenance cost for an under-adopted platform. (Ch 14)
