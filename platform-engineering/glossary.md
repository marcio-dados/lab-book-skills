# Glossary

**Accidental complexity** — complexity created by a platform "solution" that just relocates the underlying problem (often onto humans), rather than actually reducing it (Ch 13).

**Adoption drag** — the combination of onboarding cost, migration work, and limited near-term need for new applications that delays adoption even of genuinely wanted platform offerings (Ch 5).

**Away team model** (Amazon) — a contract-driven arrangement where a blocked application team builds the platform feature they need themselves and hands the code to the platform team to own long-term; high management overhead, best used sparingly in early-stage platforms (Ch 9).

**Batteries included vs. building blocks** — two product philosophies for platforms: deeply integrated, workflow-level offerings (batteries included) vs. composable, well-defined APIs that can be swapped out incrementally (building blocks); internal platforms should generally favor building blocks (Ch 12).

**Benevolent dictator (anti-pattern)** — a single leader personally negotiating trust with every stakeholder instead of building institutional/team-level trust; efficient short-term, brittle at scale (Ch 12).

**Bike shed and the nuclear plant** — bikeshedding: small, visible decisions (e.g. UI details) attract disproportionate stakeholder attention relative to invisible, higher-leverage architecture (Ch 3).

**Bottom-up roadmap** — a second, higher-fidelity roadmap built from four pools: KTLO, mandates, system improvements (reliability/efficiency/security), and the product roadmap (Ch 7).

**Building blocks** — see Batteries included.

**Captive audience (internal customers)** — internal customers can't go elsewhere, but that doesn't excuse building the wrong thing; a key characteristic distinguishing platform product management from consumer product management (Ch 5).

**Change budget** — the finite amount of platform/infrastructure change an organization can absorb in a period; competing platform teams all draw on the same customer attention (Ch 5).

**Change management** — mandatory documentation, review, and pre-production testing of production changes; a precursor to full CI/CD for stateful, complex platforms (Ch 6).

**Curated product approach** — the first pillar of platform engineering: balancing customer responsiveness (product) with an opinionated scope (curation) (Ch 2).

**Customer empathy** (vs. user empathy) — appreciating that you're building for other humans with obligations, not just "users"; an explicit interview and culture trait (Ch 4, Ch 5).

**Data reliability engineering (DRE)** — an operational model for teams owning OSS data systems (Postgres, Kafka, Cassandra), focused on automation for resilience/autoscaling (Ch 13).

**Dunbar's number** — ~50-250 people, the point past which a cooperative group can no longer informally know all its members, triggering the need for formal ownership/platform teams (Ch 3, Ch 10).

**Error budget** — a contractual framing (from the SRE book) treating SLO compliance as a release gate; the authors consider it optional and often us-vs-them-inducing rather than necessary (Ch 6).

**Feature Shop Trap** — a platform team perpetually triaging individual customer feature requests instead of pursuing a strategic roadmap (Ch 5).

**FinOps** — financial operations discipline for cloud cost accountability (tagging, spend reports, rightsizing, vendor negotiation); distinct from performance engineering (Ch 7).

**Full encapsulation** — hiding an underlying OSS/vendor system entirely behind a custom API; often reduces application-engineer productivity versus allowing direct access (Ch 2, Ch 13).

**Gall's Law** — "a complex system that works is invariably found to have evolved from a simple system that worked... a complex system designed from scratch never works" (Ch 7).

**Glue** — code, automation, configuration, and management tools that stitch primitives together; the core source of complexity a platform aims to reduce (Ch 1).

**Guardrails** — default limits/protections that prevent costly misconfiguration by non-expert users of a broad platform (Ch 2).

**Haunted graveyard** (Carla Geisser) — a legacy system a development-focused team treats as a curiosity, not something to understand and own; leads to operational neglect (Ch 4).

**Human glue** (Tanya Reilly, "Being Glue") — manual workarounds, documentation, and coordination that bridge gaps a platform hasn't automated; a hidden form of complexity distinct from technical glue (Ch 13).

**Hyrum's Law** — all observable behaviors of a system will eventually be depended on by somebody, regardless of what the contract promises; relevant to innersourcing risk (Ch 7).

**IaaS vs. PaaS** — IaaS gives vendor APIs to provision virtualized infrastructure (still ties apps to infra); PaaS has the vendor own the app's infrastructure entirely (Ch 1).

**Innersourcing** — allowing any internal team to contribute code to a platform like open source; creates operational risk since the platform team gets paged for third-party bugs (Ch 7).

**Internal developer portal (IDP)** — a centralized catalog for platform/API/resource metadata and configuration; optional, not a required component of platform engineering (Ch 2).

**KTLO ("keep the lights on")** — nondiscretionary operational work: on-call, essential support, incident/postmortem remediation (Ch 7).

**Leverage** — the core value metric of platform engineering: a few platform engineers' work reduces work for the whole org (Ch 1).

**Mandates** — top-down executive edicts requiring specific migrations/initiatives; scarce organizational resource, use sparingly (Ch 7, Ch 9).

**Monorepo** — a single repository for all/most company code; helps in-house library changes more than platform migrations broadly, due to service/API versioning needs (Ch 9).

**Multitenancy** — a platform's ability to support different applications within the same runtime components, for engineering-time (not just hardware) efficiency (Ch 2).

**Operational hell** — a state where neglected operational problems have ongoing acute business impact, taking months to remediate and stalling feature delivery (Ch 6, Ch 7).

**Over-general swamp** — the architecture that forms as application teams independently glue together general-purpose cloud/OSS primitives; the central problem platform engineering exists to solve (Ch 1).

**Paved path** — a curated platform layering multiple offerings into an easy, opinionated workflow covering the ~80% common case; users can step off for outlier needs (Ch 2).

**Pierceable abstraction** (Will Larson) — letting trusted/advanced users deliberately break through a workflow-level abstraction to access underlying building blocks when needed (Ch 12, Ch 14).

**Pioneers, Settlers, Town Planners** (Simon Wardley) — three engineering mindsets mapped to platform maturity stages: exploratory/agile (pioneer), productizing/trust-building (settler), industrializing/efficient (town planner) (Ch 8).

**Platform** (Evan Bottcher's definition, updated) — a foundation of self-service APIs, tools, services, knowledge, and support arranged as a compelling internal product (Ch 1).

**Platform engineering** — the discipline of developing and operating platforms to manage system complexity and deliver business leverage via a curated product approach (Ch 1).

**Power-Interest Grid** — a stakeholder-mapping technique plotting power (organizational influence) against interest (engagement) into four management quadrants (Ch 10).

**Product owner vs. product manager** — in internal platform contexts, no need to split these roles absent external marketing needs (Ch 4).

**Railway** — a curated platform built to fill a genuine infrastructure gap not covered by any existing offering, often generalized from an application team's own prototype (Ch 2).

**Rearchitecture** — an iterative process of reimplementing a live system's architecture while it continues serving load, as opposed to a "v2" rewrite (Ch 8).

**Revealed preferences** — what customers actually do, as opposed to what they say they want (stated preferences); a stronger product signal for platform teams (Ch 5).

**Second-system effect** (Fred Brooks) — a team's second system balloons in scope trying to correct every perceived flaw of the first, often failing to ship (Ch 8).

**Shadow platform** — a system application teams build themselves that duplicates a platform's function, using different technology/feature/cost profile; sometimes a source of genuine innovation (Ch 3, Ch 10, Ch 13).

**Single pane of glass** — a unifying UI concept that sounds like complexity reduction but often becomes an extra, worse hop between users and their tools; a success red herring (Ch 13).

**SLI / SLO / SLA** — service level indicator (measured signal), objective (target), agreement (customer-facing commitment); customer-facing and internal SLOs should follow opposite rules on quantity and false-positive tolerance (Ch 6).

**Sunsetting** — turning off a platform/feature without offering a replacement, reserved for very-low-adoption, high-cost, or distracting offerings (Ch 9).

**Synthetic monitoring** (active monitoring) — simulating real user/API interactions against production to catch correctness issues before customers report them (Ch 6).

**Tiering (support/application)** — categorizing support requests (T1/T2) and applications (Tier 0-N) by criticality to define differentiated SLAs (Ch 6).

**Town planners** — see Pioneers, Settlers, Town Planners.

**Wins and Challenges** — a biweekly reporting practice (Situation → Action → Result structure) that rolls team updates up the management chain for transparency (Ch 7).
