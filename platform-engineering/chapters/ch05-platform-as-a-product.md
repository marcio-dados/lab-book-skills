# Chapter 5: Platform as a Product

## Core Idea
Treating a platform as a product means understanding internal customers deeply (their revealed preferences, not just requests), discovering products through partnership and incremental proofs of concept, and executing through a vision→strategy→goals→milestones roadmap — product management for platforms is not the same thing as stakeholder management.

## Frameworks Introduced
- **Revealed preferences over stated preferences**: what customers actually do (how they use systems, what tasks they perform) is a better product signal than what they say they want, because engineers are bad at predicting their own future needs and will agree to "best/fastest/most scalable" if asked leadingly.
  - How: ask specific, bounded questions ("how quickly do you need X") instead of open-ended ones ("do you want it real-time") to avoid over-building.
- **Product management vs. Stakeholder management**: stakeholder management is political — power structure appreciation, horse-trading, protecting the requester's interests; product management is figuring out what the company/customers actually need via evidence and impact metrics. Both are necessary, but conflating them lets you build "crappy products" while keeping stakeholders nominally happy.
- **Feature Shop Trap**: a platform team ends up perpetually triaging individual customer feature requests (often via ad hoc "fair share" allocation schemes) instead of pursuing a strategic roadmap — caused by (1) scaling adoption before the architecture supports self-service, and (2) treating precise customer requests as the correct response.
  - How to escape: find the pattern behind requests and build the platform so *categories* of features become self-serviceable by customers, rather than building bespoke one-offs forever.
- **Smoothing the edges vs. rethinking the problem**: a diagnostic for scoping platform investment.
  - Smooth the edges when a human-in-the-loop, multi-party workflow needs coordination (e.g. a dev-experience platform aggregating build/test/review status) — humans must stay involved.
  - Rethink the problem when supporting machine processes/data, or when a human doesn't actually need to be in the loop (e.g. dependency upgrades) — aim to remove the task from the user entirely via a real operated abstraction (e.g. moving auth logic into a sidecar the platform manages), not just a better tool for doing it manually.
- **Vision → Strategy → Goals/Metrics → Milestones roadmap cascade**: Vision (aspirational long-term picture, may never fully complete) → Strategy (mid-term — what's blocking the vision, translated into high-level product requirements) → Goals/Metrics (this year, OKR-style) → Milestones (quarterly, technical delivery pieces). Share only user-visible milestones externally; keep internal technical milestones internal to avoid "engineering built what's cool, not what matters" perception.
- **Product discovery patterns**: "Assimilate and expand" (take over a system a single team already built and validated for themselves, generalize it — you inherit a satisfied customer base and a pre-validated problem) and "Partner to prototype" (embed with a partner team to build a narrow solution, then extract the general pattern) — avoid sliding into a pure solutions-engineering team that never generalizes what it builds.

## Key Concepts
- **Internal customer characteristics**: small customer base (metrics-driven A/B testing often doesn't apply at your scale), captive audience (can't go elsewhere, but that doesn't excuse building the wrong thing), conflicting incentives (customers may also fund your team's budget), moving-target happiness (improvements are quickly taken for granted), customers-as-competitors (engineers build their own alternative if you're too slow).
- **Adoption drag**: the combination of onboarding cost, required migration work, and limited near-term need for new applications that delays customer adoption even of genuinely wanted offerings.
- **Impact metrics vs. guardrail metrics vs. product health metrics**: impact metrics justify strategy upward (built on a causal "impact theory" graph linking inputs like storage throughput to business KPIs like revenue); guardrail metrics prevent tunnel vision (e.g. DORA's change failure rate as a guardrail on deployment frequency); health/consumer-style metrics (acquisition, conversion, retention) find opportunities and at-risk products.
- **Change budget**: the finite amount of platform/infrastructure change an organization can absorb in a period — competing platform teams all clamor for the same customer attention, so plan realistically for how much adoption you can actually drive.
- **"You aren't Google" caution**: big-company OSS/practices (e.g. monorepos, Bazel) encode undocumented ecosystem and cultural context; adopting them without that context can fail even when the technology itself is sound.

## Mental Models
- Ask "am I supporting a human-in-the-loop workflow (smooth edges) or a machine/data process (rethink and remove the human)?" before scoping a new platform investment.
- When evaluating a new product idea, run it through: does the tech-stack context match? Will it need a culture/process change the company is willing to make? Who exactly benefits, and how many? Is there real appetite for near-term adoption?
- Treat "we could build this ourselves" pitches from your own engineers (inspired by blog posts/conference talks) with the same market-validation rigor as any other product bet — sounding good on a conference stage often hides the internal pain and context that made it work elsewhere.
- When stability is poor, that IS the product priority — new features on an unstable base burn the trust needed for any future adoption.

## Anti-patterns
- **Pure relationship-model product decisions**: building exactly what a customer team asks for to preserve the relationship — sets both sides up for failure because engineering teams are bad at predicting what they'll actually want/adopt.
- **Feature Shop Trap** (see above): perpetual triage instead of strategic roadmap.
- **Underestimating migration cost**: a "reasonably straightforward" migration (e.g. a new code-search tool) can take years once link redirection, edge cases, and user retraining are accounted for — always model migration cost as part of the product decision, not an afterthought.
- **Overestimating users' change budget**: pushing adoption of a nice-to-have when customers have no bandwidth, especially under budget/deadline pressure.
- **Too many PMs for the engineering team's size**: PMs end up doing project-management busywork, and engineers "shut off their brains" on prioritization, hiding technical debt behind "PM didn't prioritize it."
- **Collapsing product management into product ownership**: treating PM as just backlog grooming/short-term prioritization neglects the harder, more ambiguous strategic work.
- **"You aren't Google" mimicry**: adopting a big-company practice (monorepo, Bazel-style tooling) without the surrounding ecosystem/context that made it work there.

## Worked Example
A compute platform team wants to bring "fast compute provisioning for containerized environments" to developers. **Vision**: provision any environment (on-prem, cloud, DMZ) in two hours. **Strategy**: research reveals the highest-leverage intermediate target is containerized workloads specifically — "reduce provisioning time for new containerized environments to minutes" — rather than trying to fix provisioning time everywhere at once. **Goals (OKR, this year)**: Objective — "Bring fast compute provisioning for containerized environments to the user's development context." Key Results — enable provisioning from IDE/CLI for 50% of supported compute types; reduce provisioning request-to-completion time by 25%; drive down legacy VM platform usage by 20%. **Milestones**: quarterly technical delivery pieces feeding those KRs, tracked internally but only user-visible milestones are shared externally with customers.

## Key Takeaways
1. Understand customers via revealed preferences (what they do) more than stated preferences (what they ask for), especially for other engineering teams who are bad at predicting their own future needs.
2. Product management and stakeholder management are different disciplines — you need both, but neither substitutes for the other.
3. Escape the Feature Shop Trap by finding the pattern behind one-off requests and making categories of features self-serviceable.
4. Diagnose "smooth the edges" vs. "rethink the problem" before scoping any platform investment — the highest leverage often comes from removing the human from the loop entirely, not making their task easier.
5. Build a roadmap that cascades Vision → Strategy → Goals/OKRs → Milestones, and share only user-visible milestones with customers.
6. Always model migration cost and change budget as first-class parts of a product decision — underestimating either is a top platform product failure mode.
7. When stability is poor, fix stability before shipping new features — it's a prerequisite for adoption trust, not a competing priority.

## Connects To
- **Ch 2**: revisits paved paths and railways as product-growth strategies.
- **Ch 4**: the customer-empathy culture required from engineers to make product management work.
- **Ch 7**: expands on merging technical roadmap milestones with other platform work into an overall prioritized roadmap.
- **Ch 8**: incremental POC-driven delivery connects to incremental rearchitecture practices.
- **Ch 9**: migration cost, only touched on here, gets full treatment.
- **Ch 10**: the stakeholder-management side of the product/stakeholder split is developed further.
