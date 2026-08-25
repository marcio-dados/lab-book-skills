# Chapter 15: Strategy and Execution

## Core Idea
Data mesh execution must be business-driven (strategic use cases identify and prioritize data products and platform features, not the reverse), end-to-end and iterative, and evolutionary — guided at the macro level by a multiphase adoption S-curve and at the micro level by objective "fitness functions," never by a rigid up-front master plan.

## Frameworks Introduced
- **Seven-Criteria Readiness Self-Assessment**: organizational complexity, data-oriented strategy, executive support, data technology at the core (not outsourced), early-adopter appetite, modern engineering practices, domain-oriented organization, plus long-term commitment. Score medium/high on these to be a good data mesh candidate *now*.
  - When to use: before starting any data mesh initiative — if the organization scores low on data complexity or lacks a domain-oriented structure already, data mesh will not deliver value yet.
- **Strategy-to-Platform Chain** (Fig. 15-2): Data strategy → Strategic business initiatives/use cases → Intelligent applications/touchpoints → Data products → Multiplane platform → Organizational alignment, all connected by continuous feedback loops.
  - How: use as a top-down traceability check — every data product and platform feature should trace back to a business initiative, not exist "just in case."
- **Fitness Functions** (borrowed from evolutionary computing / *Building Evolutionary Architectures*): objective functions measuring how "fit" the mesh implementation is relative to its target outcomes, one set derived per principle (domain ownership, data as a product, self-serve platform, governance) — explicitly preferred over vanity KPIs like "number of data products."
  - How: pick metrics that measure *value delivered through connectivity/usage* (e.g., "number of links to data products," "lead time to adopt a new policy") rather than raw production volume.
- **S-Curve Multiphase Evolution Model** (adapted from Rogers' diffusion of innovation + Kent Beck's Explore/Expand/Extract): Explore (few innovator domains, exploratory tooling, manual policy), Expand (rapid onboarding of the majority, standardized patterns, automated policy coverage), Extract (stabilized count, focus shifts to optimization and legacy laggard onboarding).
  - How: apply this same three-phase lens separately to each of the four principles (domain ownership, data-as-a-product, platform, governance) — each has its own explore/expand/extract characteristics, not one shared timeline.

## Key Concepts
- **Business-driven execution's core tension**: continuous value delivery and fast feedback vs. the risk of building non-reusable "point-in-time solutions," incurring technical debt under deadline pressure, and project-based budgeting starving long-term platform/data-product ownership.
- **Atomic evolutionary migration step**: a legacy migration step is only "complete" when new data products are built, existing consumers are migrated to them, AND the old pipelines/tables are retired — partial completion (new + old coexisting indefinitely) increases entropy rather than reducing it.
- **"No centralized data architecture coexists with data mesh, unless in transition"**: a warehouse/lake feeding a mesh downstream, or a mesh feeding a shrinking warehouse of legacy edge consumers, are acceptable *transitional* states — a permanent architecture with both is explicitly an antipattern.
- **Working Backwards** (Amazon's practice, cited approvingly): start from the customer/business case and work backward to the data products and platform features needed — the discipline underlying "business-driven execution."

## Mental Models
- **"The essence of strategy is choosing to perform activities differently than rivals do" (Porter, epigraph)**: data mesh is framed as a strategic differentiator, not a generic infrastructure upgrade — it only makes sense paired with an actual data-oriented business strategy.
- **"A Big Bang re-architecture guarantees a Big Bang" (Fowler)**: reinforces the anti-big-bang, iterative, atomic-steps posture throughout the chapter.
- **Kinetic vs. potential energy of change**: framing incremental, value-delivering iterations as using "kinetic energy" to keep moving, instead of waiting to accumulate enough "potential energy" (organizational will) for one big transformation push.
- **YAGNI vs. product thinking, balanced**: don't build data products for imagined future use cases (YAGNI), but source-aligned data products *do* need to capture business reality broadly (not narrowly fit to today's one use case) — the balance is achieved through product ownership judgment, not a rule.

## Anti-patterns
- **Linking extrinsic rewards (e.g., year-end bonuses) to vanity metrics like "number of data products"**: produces a rush of low-quality data product creation before review cycles, followed by technical debt cleanup — directly undermines the mesh's actual goal of connected value.
- **Treating "number of data products" as a KPI of success**: the book explicitly names this as the wrong measure; "number of links to/usage of data products" reflects real value generation.
- **Bypassing the source and building data products directly off legacy warehouse/lake tables during migration**: adds another layer of technical debt and increases the distance between source and consumer instead of closing the gap data mesh exists to close — go to the domain source directly instead.
- **Leaving old pipelines/lake files "just in case" after building replacement data products**: an incomplete atomic migration step; architectural entropy accumulates because consumers were never actually migrated off the old system.
- **A rigid, fully up-front transformation plan with fixed milestones**: won't survive contact with a large, volatile business environment — favor lightweight, outcome-driven, continuously-learning execution (e.g., EDGE-style frameworks).

## Reference Tables
| Evolution phase | Domain ownership | Data as a product | Self-serve platform | Governance |
|---|---|---|---|---|
| Explore/Bootstrap | Few innovator domains, dual provider+consumer role | Small set, limited affordances, exploratory patterns | Utility plane basics, manual/script-based self-serve | Few domains, essential policies only, some crowdsourced |
| Expand/Scale | Majority of domains onboard, aggregate domains emerge | Rapid growth, diverse transformations, higher-risk products | Automated data product generation, majority-generalist users | Majority of domains join federation, most policies automated |
| Extract/Sustain | Domain count stabilizes; bottleneck domains split/merge | Count stabilizes; optimization and consolidation focus | Mature observability/self-healing; laggard onboarding | Full automated policy conformance monitoring |

## Key Takeaways
1. Assess readiness against the seven criteria before starting — data mesh is not universally the right choice "right now" for every organization.
2. Every data product and platform capability should trace back through the strategy-to-platform chain to an actual business initiative — this is the discipline against point-solution sprawl.
3. Use fitness functions (value/connectivity-oriented), not vanity KPIs (raw counts), to measure progress — and be skeptical of any single numeric target, per *Accelerate*'s finding that most metrics are vanity measurements.
4. Apply the explore/expand/extract S-curve separately to each of the four principles — they don't mature on the same timeline.
5. Legacy migration must proceed in atomic steps: build the new data product, migrate its consumers, retire the old pipeline/tables — all three, every time, or the step isn't done.
6. A centralized warehouse/lake may coexist with the mesh only transitionally, never as a permanent parallel architecture.

## Connects To
- **Ch 1–5**: the four principles whose fitness functions and adoption phases this chapter operationalizes.
- **Ch 11 (Building Evolutionary Architectures)**: fitness functions concept borrowed directly.
- **Ch 16**: organizational and cultural change (Team Topologies, values, roles) that must accompany this execution framework — the next and final chapter.
