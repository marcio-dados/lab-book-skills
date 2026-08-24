# Chapter 7: Planning and Delivery

## Core Idea
Platform teams fail visibly when they don't plan long projects rigorously, don't augment product roadmaps with the operational work needed to avoid "operational hell," or don't communicate progress — this chapter gives concrete practices for all three: proposal/action-plan documents, bottom-up roadmap planning, and biweekly Wins and Challenges.

## Frameworks Introduced
- **Five-part project proposal document**: Background/tenets/guidelines (baseline the current state to resolve disagreements early) → Details of the problem (state the problem before the solution, per Leslie Lamport) → Overview of possible solutions (evaluate alternatives up front to head off "why not X" counterproposals) → Proposed solution and rationale (top 3–5 factors, not a 20-page proof of thoroughness) → Plan of action (what "done" looks like, milestones, staffing/org impact).
  - How: review with management and lead engineers before committing to an action plan; Amazon-style six-pagers work well but the format itself is optional — the five elements are what matter.
- **Action plan (post-buy-in)**: adds testing/acceptance criteria, dependency analysis (especially migration dependencies, often neglected), headcount estimation, an adoption-driving plan (name, early adopters, docs, marketing), and concrete monthly milestones for the first 12 months (quarterly beyond that).
  - When to bring in a project manager: only when there's a firm deadline, heavy task-dependency count, or a bureaucratic scheduling culture — not by default, since early PM involvement creates scheduling bureaucracy and crowds out engineering/product input, making estimates more conservative and less accurate.
- **Bottom-up roadmap**: a second, higher-fidelity roadmap (beyond the Ch 5 product roadmap) built from four pools: KTLO ("keep the lights on" — nondiscretionary on-call/support/incident-remediation work), Mandates (executive top-down edicts — estimate net impact politically, since some get killed once true cost is understood), System improvements (Reliability/operability, Efficiency/performance, Security/compliance — three separate stack-ranked lists), and the Product roadmap itself.
  - How to merge: KTLO ≤ 40% of team workload; individual system-improvement projects capped at ~3 developer-months (longer ones become their own project, see Ch 8); apply Google's 70/20/10 model to non-KTLO work (70% core/incremental, 20% adjacent innovation/rearchitecture, 10% transformational/new platforms) as a discussion lens, not a rigid budget; merge roadmaps only one level up (skip-manager level) — further roll-up loses fidelity and becomes political (headcount-driven org gaming, as Ian saw in AWS's OP1 process).
- **Wins and Challenges (biweekly reporting)**: line managers write short bullet updates; each level up selects and rewrites the most impactful ones for a broader audience. Structure each item as Situation → Action → Result (adapted from the STAR interview technique), quantified wherever possible.
  - Why: platform work is long-horizon and easily perceived as "nothing is happening" — this creates a running record for reviews, forces regular reflection beyond output metrics (tickets closed), and — critically — Challenges build external trust and surface cross-team blockers, not just Wins.

## Key Concepts
- **Overreach**: expanding a necessary project's scope into a "revolutionary" one (e.g. redesigning a storage system to also eliminate all POSIX-style file access) based on ivory-tower assumptions about what users need — leads to failed rollouts and forced redesign.
- **Gall's Law**: "A complex system that works is invariably found to have evolved from a simple system that worked... A complex system designed from scratch never works." Starting too big (trying to design a complete platform from a diverse customer base's stated requirements) is a direct violation.
- **"Sh*terating"**: repeatedly tweaking a fundamentally unproven or mismatched solution (e.g. a drag-and-drop UI nobody asked for) instead of declaring it a failed bet and pivoting.
- **KTLO ("keep the lights on")**: nondiscretionary operational work — on-call, essential support, incident/postmortem remediation — estimated from historical data, excluding any single event that consumed more than ~2 months of engineering time (don't plan around expecting another once-in-years crisis).
- **FinOps vs. performance engineering**: FinOps (financial accountability for cloud spend — tagging, spend reports, rightsizing, vendor negotiation) needs a dedicated specialist around ~200 engineers, and works best as a distinct discipline from performance engineering (system-level tuning), which is best done part-time by each platform team's own systems engineers rather than a rare "unicorn" full-time hire.
- **Innersourcing anti-pattern**: allowing any team to contribute code to a platform (like open source) sounds collaborative but creates real operational risk — the platform team gets paged for bugs introduced by third-party contributors exploiting undocumented internal behavior (Hyrum's Law). Amazon's contract-driven "away team" model formalizes this but adds real management overhead; treat frequent reliance on it as a problem, not a standard operating pattern.

## Mental Models
- Before starting a long project, ask "have I stated the problem before proposing the solution?" — if you can't write a concrete proposal your customers can critique, you've likely bitten off more than you can chew and should scope down (revisit Ch 5's "boring parts first" advice).
- Distinguish system improvements that are genuinely reliability/security risk-reduction from those that are really disguised feature requests or vanity rearchitectures — route the latter through the product roadmap, not the system-improvement stack rank.
- When a stakeholder says "the platform is unstable AND you never ship features on time," that's the signal you need a bottom-up roadmap, not just a product roadmap — the two complaints usually share a root cause (unplanned operational load crowding out delivery).
- Treat "away team" / innersourcing arrangements as an early-stage-platform escape valve, not a scalable governance model — frequent use signals unresolved prioritization conflict with customers.

## Anti-patterns
- **Overreach**: expanding a project's scope past what's realistic "since we're already doing something hard."
- **Starting too big / unclear problem space**: trying to design a complete, all-things-to-all-customers platform from scratch, or refusing to commit to a paved-path-or-railway approach (Ch 2) and instead building both halfheartedly.
- **Bringing in a project manager too early**: creates scheduling bureaucracy and crowds out engineering/product judgment, producing worse (overly conservative) estimates.
- **Chargebacks as a reactive, one-off cost-cutting drive**: bureaucratic, assumption-laden programs triggered only after a CFO/CTO hears a waste anecdote — worse than continuous FinOps investment.
- **Relying on innersourcing to avoid hard prioritization conversations**: gives customers false confidence they can "just build it themselves," while leaving the platform team on the hook operationally for code they didn't write.
- **Rolling up roadmaps past the skip-manager level**: loses fidelity and turns into politics (headcount gaming), as seen in AWS's OP1 process.

## Worked Example
A team redesigning an internal storage system starts with a legitimate, bounded goal (fix known security/performance/efficiency gaps) but progressively expands it to also eliminate all network-attached, POSIX-style file storage company-wide — an "overreach" driven by the belief that since the project is already hard, it should also be transformative. They ship the new environment, remove access to the old storage option, and try to migrate users — who revolt, because their existing command-line tooling and scripts depend on POSIX semantics the new APIs don't replicate. The team has to go back to the drawing board. The lesson: a project proposal (with an honest "details of the problem" section) would likely have surfaced this dependency before implementation, not after a failed migration.

## Key Takeaways
1. Write a five-part proposal (background, problem, alternatives, chosen solution + rationale, plan of action) before any long-running platform project — don't skip straight to a design doc.
2. Delay project managers until scheduling risk (deadlines, dependency count, bureaucratic culture) actually justifies the overhead.
3. Watch for overreach and "starting too big" — Gall's Law says complex systems that work evolve from simple ones that worked, not from all-encompassing initial designs.
4. Build a bottom-up roadmap (KTLO + mandates + system improvements + product roadmap) once delivery or operational pressure appears; cap KTLO at ~40% and use 70/20/10 as a lens, not a budget.
5. Only merge roadmaps one level up (skip-manager); further rollups sacrifice fidelity and invite headcount politics.
6. Avoid innersourcing as a substitute for real prioritization conversations with customers — the platform team still owns the operational risk.
7. Run biweekly Wins and Challenges, structured as Situation→Action→Result, and always include genuine Challenges — they build trust and surface blockers that pure Wins-only reporting hides.

## Connects To
- **Ch 2**: paved path vs. railway commitment failure underlies the "unclear problem space" anti-pattern.
- **Ch 4**: "specialist as evangelist" trap recurs in the performance-engineering hiring discussion.
- **Ch 5**: product roadmap is one of the four inputs to the bottom-up roadmap; "boring parts first" advice reapplied to scoping proposals.
- **Ch 6**: KTLO estimation builds directly on the on-call/support rotation data from operating platforms.
- **Ch 8**: system-improvement projects too large for a single stack-rank item become rearchitecture projects, covered next.
