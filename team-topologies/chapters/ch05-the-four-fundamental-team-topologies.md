# Chapter 5: The Four Fundamental Team Topologies

## Core Idea
Reducing all team variation to four fundamental types — stream-aligned, enabling, complicated-subsystem, platform — removes ambiguity about purpose and interaction, and every other team type in an organization should be converted toward one of these four "magnetic poles."

## Frameworks Introduced
- **The Four Fundamental Team Topologies**: stream-aligned (primary type, aligned to a single valuable flow of work, delivers end-to-end with minimal hand-offs), enabling (specialists who close a stream-aligned team's capability gap, temporarily, via a facilitating relationship), complicated-subsystem (owns a part of the system needing deep specialist knowledge that would overload a stream-aligned team), platform (provides self-service internal services that reduce stream-aligned teams' cognitive load).
  - When to use: as the target shape for every team in the organization; the stream-aligned:other ratio in successful organizations runs roughly 6:1 to 9:1 (about one in seven to one in ten teams is non-stream-aligned).
  - How: map every existing team to whichever of the four it should become, then adopt that type's expected behaviors (see Key Concepts) rather than inventing new hybrid team types.
- **Thinnest Viable Platform (TVP)**: the smallest platform that still meaningfully accelerates and simplifies delivery for the teams that build on it — anything from a wiki list of components to a full custom in-house solution.
  - When to use: whenever standing up or growing a platform team.
  - How: start as thin as possible (even just documentation) and grow the platform's scope only as the underlying substrate's complexity genuinely demands it; resist the pull ("software developers love building platforms") toward building bigger than needed.

## Key Concepts
- **Stream**: a continuous flow of work aligned to a business domain, product, service, user journey, or persona — the unit that stream-aligned teams own end-to-end.
- **Fractal / nested (inner) topologies**: a large platform is itself composed of stream-aligned, enabling, complicated-subsystem, and (lower-level) platform teams — the same four types recur at every scale ("turtles all the way down").
- **Ivory tower (enabling-team failure mode)**: an enabling team that dictates technical choices rather than growing the served team's own capability; the correct end-state is the enabling relationship becoming unnecessary within weeks or months.
- **Complicated-subsystem vs. component team**: a complicated-subsystem team exists because of required specialist knowledge (cognitive load), not because of a perceived opportunity to "share" a component — this is the key test that should keep such teams rare.
- **Internal pricing**: Don Reinertsen's technique of charging teams (e.g., cloud cost tracking) for platform services to regulate demand for "premium" service levels a platform team can't sustainably provide to everyone.
- **"Built on an underlying platform"**: every application sits on some platform, explicit or hidden; an unstable lower-level platform destabilizes everything built on it (Stafford Beer's viable-systems-model parallel).

## Mental Models
- Use the "magnet" metaphor: don't try to invent new team types — pull every team toward whichever of the four fundamental types matches its actual purpose.
- Treat a platform as a live product, not a one-off build: it needs a roadmap, user personas for its Dev-team customers, SLAs/on-call, and UX/DevEx investment, exactly like an external-facing product.
- Convert legacy team types by asking what they're really for: an infrastructure team becomes a platform team; a DBA team becomes an enabling team (if advisory) or platform team (if operating a Database-as-a-Service); a tooling team becomes an enabling team (short-lived) or folds into the platform; an architecture team becomes a part-time enabling team that shapes team-to-team APIs, never a mandate-issuing authority.

## Anti-patterns
- **Ops/support as a separate team type**: there is deliberately no "Ops team" or "support team" among the four — support should align to streams, escalating to dynamic cross-team "swarms" only for incidents that cross stream boundaries.
- **Cloud team as rebranded infrastructure team**: if a "cloud team" still owns and gates every change to application infrastructure the way an old infra team did, the organization gets none of the cloud's speed benefits.
- **Platform without product management**: a platform built and run by former sysadmins without product-management discipline, or one so underfunded it never keeps pace with consumer needs, becomes a hindrance rather than an accelerant.
- **Platform trying to serve everyone at "premium" tier**: if every stream-aligned team demands zero-downtime/auto-scaling/self-healing service, the platform team cannot cope — use internal pricing or tiered service levels instead.

## Reference Tables
<!-- omitted: the chapter's tables (e.g., stream-aligned capability list) are prose lists, not formal comparison tables in the author's original -->

## Worked Example
Auto Trader's transition (Dave Whyte, Andy Humphrey) from a print business to 100% digital: they first stood up a temporary continuous-delivery *enabling* team to help squads adopt CD practices (pipelines, test automation, monitoring). As that team's understanding deepened, it evolved into a full **platform team** ("Infrastructure Engineering") whose remit shifted from teaching to providing the underlying substrate — freeing product squads to own their own operational concerns without embedding Ops people in every squad. Instead, an Ops "squad buddy" attends each Dev squad's standups, providing glue without permanent headcount inside the squad. The company also eliminated the CapEx/OpEx split that had forced Dev to only "build new things," moving everyone to OpEx so all work — features, fixes, operability — could be prioritized by actual customer needs rather than an accounting category.

## Key Takeaways
1. Restrict every team in the organization to one of four types — stream-aligned, enabling, complicated-subsystem, platform — and expect roughly 6:1 to 9:1 stream-aligned-to-other ratio.
2. Stream-aligned teams are the default and the reason the other three exist: enabling, platform, and complicated-subsystem teams all exist purely to reduce a stream-aligned team's cognitive load.
3. An enabling team's job is done, by design, when the stream-aligned team no longer needs it — treat any enabling relationship lasting much longer than weeks/months as a warning sign.
4. Build the thinnest viable platform, not the biggest one your platform engineers can imagine; grow scope only as real complexity demands it.
5. Manage a platform as a live product: roadmap, personas, DevEx, SLAs — never as a side project maintained by whoever has time.
6. Reserve complicated-subsystem teams for genuine specialist-knowledge cognitive-load problems, not for "this could be shared" component thinking.

## Connects To
- **Ch 3**: cognitive load, defined there, is the organizing rationale for all four topologies here.
- **Ch 6**: choosing where to draw the boundaries (fracture planes) for these team types.
- **Ch 7**: the three interaction modes describe *how* these four team types actually work together.
