# Chapter 3: How and When to Get Started

## Core Idea
Platform engineering has a right time to start — too early wastes scarce resources and slows product-market fit, too late means unmanaged complexity forces a painful transition; the chapter gives stage-based guidance for startups, growth-stage cooperation-to-team transitions, and legacy infrastructure-to-platform cultural transformations.

## Frameworks Introduced
- **Two-stage startup maturity model (adapted from CMM/CMMI)**: Stage 1 "Ad hoc" (whatever works now — no formal process, individual tool choices, organic knowledge sharing) and Stage 2 "Somewhat managed" (principled but still cooperative, not yet a dedicated platform team). Applies roughly up to ~50 engineers.
  - When to use: to decide what to invest in right now versus defer.
  - How, Stage 1: use source control always; adopt off-the-shelf continuous deployment (no Kubernetes on day one); keep process lightweight ("Use a process. Not too much. Mostly agile."); ask "is this core/differentiating for my business?" — if not, outsource it.
  - How, Stage 2: automate local dev environments (colocate dev-env config with source, publish container images, use git hooks); add real CI with growing test coverage; add branch-based/ephemeral deployments and feature flags; extend existing product observability to platform/workflows; adopt a lightweight RFC/ADR process for shared decisions.
- **Dunbar's number as a platform-team trigger**: once a cooperative group crosses ~50–250 people, no one can know all the other members — that's the point informal cooperation breaks down and a formal platform team with clear ownership/accountability becomes necessary. Different groups (infra/backend vs. data/frontend vs. external APIs) cross this threshold at different times.
- **Leverage-vs-coordination-cost test for centralizing ownership**: before creating a platform team, verify that centralizing genuinely produces leverage (hard-to-replicate value), not just marginal "efficiency" (e.g. "2 engineers instead of 5 doing similar work" is not sufficient justification) — do a rough total-cost-of-ownership estimate: high build/maintain cost + reusable with little per-team customization = good centralization candidate; low cost + high per-team customization need = bad candidate.

## Key Concepts
- **The bike shed and the nuclear plant**: bikeshedding — small, visible decisions (UI details) get disproportionate stakeholder attention/investment relative to the invisible but higher-leverage architecture ("nuclear plant").
- **Ticket system black hole**: an anti-pattern where support requests vanish into an opaque backlog, making customers feel like a burden rather than a focus.
- **Customer empathy screening**: an interview technique — ask candidates how they write code for others to understand, or how they'd support users — to select for the platform mindset.
- **Integration/shared-services platforms**: platforms with external-customer-visible surface area (billing, identity, notifications) — trickier because they need earlier product-manager involvement, face discoverability problems, and sit organizationally "stuck in the middle" between core infra and application teams.

## Mental Models
- Think of a new platform team's initial state as "detangling, not rearchitecting" — early trust is built by delivering fast value in the messy inherited system, not by a from-scratch rewrite that may take years.
- Be wary of senior hires from much-bigger companies who reflexively propose "BigCo Technology X" — they've seen a *destination* at a different scale/culture, not necessarily the right *path* for where you are now.
- Delay hiring product/project managers until the engineering team has already demonstrated delivery and built firsthand customer empathy — otherwise those muscles never develop; use rough team-size ratios later (PM count between team-manager and manager-of-managers count; ~1 PjM per 50 platform engineers) as sanity checks, not targets.
- Treat migration ownership as part of your platform's UX — pushing project-management burden onto customers to track migration dependencies is a sign the platform isn't taking ownership of its users' experience.

## Anti-patterns
- **Premature platform team formation**: standing up a dedicated team or heavyweight process at Stage 1/2 (e.g. Kubernetes day one, big-company hires, PMs before delivery proof) diverts scarce resources from finding product-market fit.
- **Rewrite-first response to a messy inherited codebase**: understandable impulse for a new platform team, but a multi-year rewrite doesn't help in-production teams with pressing problems now and burns the goodwill the new team hasn't yet earned.
- **"Rub product managers on it and call it a day"**: hiring PMs to fix a culture problem without willing, ownership-minded engineering teams turns them into backlog groomers, not product leaders.
- **Cutesy platform names** (e.g. "Glengarry" instead of "Billing Platform"): actively hurts discoverability for integration/shared-services platforms.
- **Over-reliance on project managers for migrations**: signals the platform isn't taking ownership of migration UX; forcing engineers to own migration automation (dependency detection, compatibility bridges) saves both platform and customer time.

## Worked Example
A startup with ~15 engineers has no formal platform team; its "platform" is a README, shared Terraform for deploying to a PaaS, and a lightweight ticket board (Stage 1). As the team grows past ~40 engineers and adds a second product line, local dev environments start drifting (each engineer's laptop setup diverges), and deploys directly to production become risky with more contributors. The team responds (Stage 2) by: colocating a `docker-compose`-based dev environment in the repo, publishing the same container images used for deploys, adding CI gates requiring test coverage before merge, and introducing a lightweight RFC process for cross-cutting stack decisions (mirroring the pattern React/Swift/Rust use for their own OSS proposals). No dedicated platform team exists yet — this is still cooperative, part-time work — until the org nears Dunbar's ~50–250 threshold and cooperation on shared infra genuinely breaks down (e.g. after an acquisition or vendor migration), at which point a formal platform team is justified.

## Key Takeaways
1. Don't build a platform team before you need one — at Stage 1/2, cooperative, lightweight investment beats a dedicated team.
2. Use leverage (not just headcount efficiency) as the bar for centralizing any capability into a platform.
3. When forming a new platform team, prioritize fast, incremental value delivery ("detangling") over an immediate rearchitecture — trust must be earned first.
4. Delay product/project managers until engineers have demonstrated delivery and built customer empathy directly.
5. Integration/shared-services platforms need earlier PM involvement, explicit discoverability plans, and deliberate alignment with core/infra platforms despite organizational separation.
6. Transforming a legacy infrastructure org into a platform org is a full cultural change — start with the most "platform-ready" teams, change hiring/support/recognition systems, and accept it will slow ticket throughput short-term.

## Connects To
- **Ch 4**: goes deeper on hiring the right blend of people for a platform team, including customer-empathy interviewing and caution about big-company hires.
- **Ch 6**: expands on the support/on-call practices only touched on here.
- **Ch 1**: the "shadow platform"/"shadow IT" theme recurs when discoverability of integration platforms fails.
