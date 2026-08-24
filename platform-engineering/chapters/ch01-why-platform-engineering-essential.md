# Chapter 1: Why Platform Engineering Is Becoming Essential

## Core Idea
Software organizations are stuck in an "over-general swamp" of exploding OSS/cloud primitives and the custom "glue" needed to hold them together; platform engineering exists to clear that swamp by curating a small set of abstractions that reduce total glue and give teams leverage.

## Frameworks Introduced
- **Platform (Evan Bottcher's definition, updated)**: a foundation of self-service APIs, tools, services, knowledge, and support arranged as a compelling internal product, so autonomous application teams can deliver features faster with less coordination.
  - When to use: to decide whether something is "a platform" at all — a wiki page isn't (no engineering), and "the cloud" isn't (too broad/incoherent).
  - How: curate a limited, opinionated set of OSS/cloud choices behind APIs; treat it as a product, not a shared-services dumping ground.
- **The Over-General Swamp**: architecture that forms as each application team independently glues together general-purpose cloud/OSS primitives to ship fast, producing a sticky mess that's slow and costly to change.
  - When to use: diagnosing why "everything works but nothing moves" — the symptom is glue smeared everywhere, so trivial upgrades (e.g. a security patch) require org-wide integration/testing.
  - How: apply "more boxes, fewer lines" — constrain the number of primitives and encapsulate them behind platform abstractions to shrink the glue surface.
- **Leverage**: the core value metric of platform engineering — a few platform engineers' work reduces work for the whole org, via (1) making application engineers more productive and (2) eliminating duplicate work across teams.

## Key Concepts
- **Glue**: integration code, one-off automation, configuration, and management tools that stitch primitives together; holds systems together but makes change harder.
- **IaaS vs PaaS**: IaaS gives vendor APIs to provision a virtualized environment (still ties apps to infra); PaaS has the vendor own the app's infrastructure entirely. Most companies ended up on IaaS despite PaaS's promise.
- **Kubernetes as leaky abstraction**: reduces some glue (YAML vs Terraform) but is not a complexity win — too much detailed configuration leaks through.
- **Split vs Merged DevOps**: Split keeps separate dev/ops teams where ops does some glue-building (DevOps engineers); Merged fuses them ("you build it, you run it").
- **SRE (Google-style)**: heavyweight reliability practice that mostly succeeded only inside Google's specific cultural/organizational context — not a broadly portable silver bullet.
- **Platform-adjacent teams**: Infrastructure, DevTools, DevOps, SRE — each brings valuable skills but is organizationally scoped too narrowly to build true platforms (Table 1-1).
- **Shadow platforms**: the platform-engineering analogue of "shadow IT" — teams building their own alternatives when the platform doesn't fit their needs.

## Mental Models
- Think of the swamp as a trap you walk deeper into with every greenfield project: each new choice adds glue, and the bog gets harder to move through over time.
- Use "more boxes, fewer lines" as a north star for any architecture review — fewer coupling points beats more features.
- Standardization via authority ("I'm the CTO, so I decide") fails; standardization via a customer-focused, product-curated platform succeeds because it earns adoption instead of mandating it.

## Anti-patterns
- **Centralized "Terraform-writing team"**: centralizing engineers without a product mission turns them into a feature-shop team that produces a spaghetti codebase — centralization only helps if it's building a platform, not just pooling glue-writers.
- **Fighting all exceptions to platform use**: refusing any team the right to go off-platform to prove out a new idea both makes the platform too general and stifles healthy innovation.
- **Full centralization by authority**: appeals to authority ("I'm the architect/DBA/CTO") to force standardization ignore business needs and cause application-team suffering.

## Key Takeaways
1. A platform must be an engineered, curated product — not just "the cloud," a wiki, or a centralized glue-writing team.
2. The real cost of software is maintenance (60–75% of lifetime cost), not initial development; platforms pay off by cutting migration and glue-maintenance costs.
3. Reduce glue two ways: fewer primitives in use, and API encapsulation of the primitives you keep.
4. "You build it, you run it" only works sustainably when the platform absorbs the operational complexity of the underlying infrastructure — otherwise on-call burns out application teams.
5. Platforms enable business innovation within existing tech, but genuinely new tech directions will legitimately bypass the platform at first; let those prove out before merging them in.

## Connects To
- **Ch 2**: elaborates the definition of platform engineering as a discipline and its pillars.
- **Ch 10**: revisits the tension between central offerings and letting teams build shadow platforms.
