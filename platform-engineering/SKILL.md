---
name: platform-engineering
description: "Knowledge base from \"Platform Engineering: A Guide for Technical, Product, and People Leaders\" by Camille Fournier and Ian Nowland. Use when applying the authors' frameworks for platform team design, product-as-platform strategy, operating platforms sustainably, rearchitecting/migrating live systems, stakeholder management, or evaluating platform success (alignment, trust, complexity, love), studying the book, or referencing its concepts."
origem: publico-terceiro
classificacao: nao-corporativo
tipo: livro-tecnico
idioma: en
titulo_pt: "Platform Engineering"
proveniencia:
  titulo: "Platform Engineering: A Guide for Technical, Product, and People Leaders"
  autor: ["Camille Fournier", "Ian Nowland"]
  editora: "O'Reilly"
  fonte_sha256: "4ecc0eda6715e711f4637c958973e295839cd2b62178075ca66555f8e5867d3a"
  convertido_em: "2026-08-24"
  ferramenta_sha: "7bcfcd5262329f8d57a385903f18a98bc6705e4e"
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Platform Engineering: A Guide for Technical, Product, and People Leaders
**Authors**: Camille Fournier and Ian Nowland | **Pages**: ~330 | **Chapters**: 14 | **Generated**: 2026-08-24

## How to Use This Skill

- **Without arguments** — load core frameworks for reference
- **With a topic** — ask about `on-call`, `rearchitecture`, `stakeholder mapping`, or another indexed topic; I find and read the relevant chapter
- **With chapter** — ask for `ch08`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not covered in Core Frameworks below, I will read
the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**The Four Pillars of Platform Engineering** (Ch 2): Product (curated product approach), Development (software-based abstractions), Breadth (serving a broad base of application developers), Operations (operating as foundations for the business). Missing any pillar means you're doing something else — ops with empathy, a feature shop, a niche tool, or an unreliable system.

**Platform** (Evan Bottcher, updated): a foundation of self-service APIs, tools, services, knowledge, and support arranged as a compelling internal product. A wiki isn't a platform (no engineering); "the cloud" isn't a platform (too broad, incoherent).

**The Over-General Swamp** (Ch 1): the architecture that forms as application teams independently glue together general-purpose cloud/OSS primitives to ship fast. Platforms clear it by constraining primitives and encapsulating them, following "more boxes, fewer lines."

**Paved Path vs. Railway** (Ch 2): paved path smooths existing offerings into an opinionated ~80%-case workflow (Pareto); railway builds genuinely new infrastructure for a gap no offering covers, usually generalized from an application team's own prototype.

**Four Engineer Roles** (Ch 4): Software engineer (writes code, wants systems understanding, comfortable on business-critical on-call), Systems engineer (broad generalist), Reliability engineer (deep reliability focus), Systems specialist (deep single-domain expert). Keep title, level-matrix, and interview process as three independent, not automatically bundled, dials.

**Product Management ≠ Stakeholder Management** (Ch 5, Ch 10): product management figures out what customers/company actually need via evidence and revealed preferences; stakeholder management is about convincing leaders you made the right call. Both are necessary; neither substitutes for the other. Map stakeholders on power × interest and prioritize high-power/high-interest even when they're disengaged until unhappy.

**Merged DevOps On-Call, <5 pages/week** (Ch 6): staff a single rotation of software + systems engineers; target fewer than 5 business-impacting pages/week (the threshold correlated with retention in Amazon survey data). Eliminate false alarms before assuming the load is truly unsustainable.

**KTLO + Mandates + System Improvements + Product Roadmap** (Ch 7): the four pools that make up a bottom-up roadmap once a team is under delivery/operational pressure. Cap KTLO at ~40%; use Google's 70/20/10 (core/adjacent/transformational) as a lens, not a budget; merge roadmaps only one level up (skip-manager).

**Rearchitecture over v2 Rewrite** (Ch 8): iteratively reimplement a live system's architecture within existing boundaries rather than building a from-scratch replacement — avoids the second-system effect and matches most mature teams' settler/town-planner mindset (not the pioneer agility a v2 demands). Four-step planning: think big on goals (all of features/efficiency/reliability/security) → factor in migration cost → determine 12-month wins (3 fallback goals) → get leadership buy-in for the 3-5 year horizon.

**Migrations as an Opportunity** (Ch 9): engineer for transparency first (minimize glue/variation, multi-version deployment, ownership/usage metadata tracking, automation over clipboards), then coordinate (scope/limit/prioritize overlapping changes, communicate early), and reserve mandates/sunsetting for last resort. True sunsetting only for very-low-adoption, high-cost, or focus-redirecting cases.

**Yes / No / Not-Yet Framework** (Ch 10): prefer "yes, with compromises" (narrower scope now) over binary responses; distinguish priority-based "not yet," technical "not yet," strategic "no" (mission creep), and technical "no" (infeasible) — always leave an alternative path.

**Four Success Criteria (not metrics)** (Part III, Ch 11-14): your platforms are **Aligned** (purpose, product strategy, plans across teams), **Trusted** (operations, big-investment buy-in, not a bottleneck), manage **Complexity** (never eliminate it, manage accidental complexity/human glue/shadow platforms/growth/product discovery), and are **Loved** (friction elimination, not a vanity metric — CSAT needs rigor, and "boring but useful" is a legitimate win).

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-why-platform-engineering-essential.md) | Why Platform Engineering Is Becoming Essential | Platform definition, Over-general swamp, Leverage |
| [ch02](chapters/ch02-pillars-of-platform-engineering.md) | The Pillars of Platform Engineering | Four pillars, Paved paths vs. railways, Guardrails |
| [ch03](chapters/ch03-how-and-when-to-get-started.md) | How and When to Get Started | Startup maturity stages, Dunbar's number, Leverage-vs-coordination test |
| [ch04](chapters/ch04-building-great-platform-teams.md) | Building Great Platform Teams | Four engineer roles, Single-focus failure archetypes, Title/ladder/interview separation |
| [ch05](chapters/ch05-platform-as-a-product.md) | Platform as a Product | Revealed preferences, Feature Shop Trap, Vision→Strategy→Goals→Milestones |
| [ch06](chapters/ch06-operating-platforms.md) | Operating Platforms | Merged DevOps on-call, Sustainable pager load, Support escalation ladder, Synthetic monitoring |
| [ch07](chapters/ch07-planning-and-delivery.md) | Planning and Delivery | Five-part proposal, Bottom-up roadmap, Wins and Challenges |
| [ch08](chapters/ch08-rearchitecting-platforms.md) | Rearchitecting Platforms | Pioneers/Settlers/Town Planners, Rearchitecture vs. v2, Security by design |
| [ch09](chapters/ch09-migrations-and-sunsetting.md) | Migrations and Sunsetting of Platforms | Transparent migrations, Automation over clipboards, Sunsetting criteria |
| [ch10](chapters/ch10-managing-stakeholder-relationships.md) | Managing Stakeholder Relationships | Power-Interest Grid, Calibrated transparency, Budget-defense process |
| [ch11](chapters/ch11-your-platforms-are-aligned.md) | Your Platforms Are Aligned | Purpose/strategy/plan misalignment, Adoption as red herring, Alignment resolution process |
| [ch12](chapters/ch12-your-platforms-are-trusted.md) | Your Platforms Are Trusted | Benevolent dictator anti-pattern, Accelerate/optimize trust curve, Building blocks vs. batteries included |
| [ch13](chapters/ch13-your-platforms-manage-complexity.md) | Your Platforms Manage Complexity | Single pane of glass red herring, Human glue, Controlled growth, Product discovery |
| [ch14](chapters/ch14-your-platforms-are-loved.md) | Your Platforms Are Loved | CSAT rigor, Awareness/compatibility/quality/time-to-market, Progressive disclosure |

## Topic Index

- **Adoption metrics** → ch11
- **Architecture (rearchitecture, v2, security)** → ch08
- **Batteries included vs. building blocks** → ch12
- **Bottom-up roadmap** → ch07
- **Budget cuts / cost defense** → ch10
- **Change management** → ch06
- **Complexity (accidental, human glue)** → ch13
- **CSAT / customer surveys** → ch14
- **Curated product approach** → ch02
- **DevOps / on-call model** → ch06
- **Dunbar's number** → ch03, ch10
- **Engineer roles / hiring** → ch04
- **FinOps / efficiency** → ch07
- **Four pillars** → ch02
- **Glue (technical and human)** → ch01, ch13
- **Guardrails** → ch02, ch08
- **Innersourcing** → ch07
- **KTLO** → ch07, ch13
- **Love (as success metric)** → ch14
- **Mandates** → ch07, ch09
- **Metadata (ownership, usage)** → ch02, ch09
- **Migrations** → ch09
- **Over-general swamp** → ch01
- **Paved path / railway** → ch02
- **Pioneers / Settlers / Town Planners** → ch08
- **Planning (proposals, milestones)** → ch07
- **Platform as a product** → ch05
- **Power-Interest Grid** → ch10
- **Product discovery** → ch05, ch13
- **Rearchitecture** → ch08
- **Sunsetting** → ch09
- **Shadow platforms** → ch03, ch10, ch13
- **SLOs / SLAs / error budgets** → ch06
- **Stakeholder management** → ch10
- **Startup maturity stages** → ch03
- **Support tiers (T1/T2)** → ch06
- **Synthetic monitoring** → ch06
- **Trust** → ch12
- **Wins and Challenges** → ch07

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns
- [cheatsheet.md](cheatsheet.md) — quick reference tables and decision guides

---

## Scope & Limits

This skill covers the book content only. For hands-on implementation in your codebase,
combine with project-specific tools. For topics beyond this book, check related skills
or ask the agent directly.
