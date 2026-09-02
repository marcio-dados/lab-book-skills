# Glossary

**API (application programming interface)** — a description and specification for how to interact programmatically with software; extended in this book to "team API," the full surface by which other teams interact with a team (Ch 3).

**Application monolith** — a single, large deployable application with many dependencies and responsibilities, possibly exposing many services/user journeys (Ch 6).

**Bounded context** — a unit for partitioning a larger domain model into smaller, internally consistent parts, each with its own unified model and ubiquitous language (Eric Evans, DDD) (Ch 6).

**Brooks's Law** — adding people to a team doesn't immediately increase its capacity, and may reduce it during ramp-up (Fred Brooks) (Ch 3).

**Cognitive load** — the total amount of mental effort used in working memory; the book distinguishes intrinsic, extraneous, and germane cognitive load (Ch 1, Ch 3).

**Collaboration mode** — team interaction mode where two teams work closely together, sharing responsibility and blurring boundaries, for a defined period (Ch 7).

**Complicated-subsystem team** — a team responsible for a part of the system that depends heavily on specialist knowledge, formed to offload cognitive load from stream-aligned teams (Ch 5).

**Continuity of care** — a team's ongoing responsibility for a system across exploration, exploitation, and maintenance horizons, without hand-off to a separate team (Ch 3, Ch 8).

**Conway's Law** — organizations which design systems are constrained to produce designs that copy their own communication structures (Mel Conway, 1968) (Ch 1, Ch 2).

**Distributed monolith** — a system split into separately deployable services that remain coupled at test/release time, giving none of microservices' independence (Ch 6).

**Domain complexity** — how complex the business problem is that software is solving; used (instead of lines of code) to gauge team cognitive load (Ch 3).

**Dunbar's Number** — anthropological limits on group trust/cognition (~5 close, ~15 deep trust, ~50 mutual trust, ~150 remembered capability), applied to team and grouping size (Ch 3).

**Enabling team** — a team of specialists in a technical/product domain that helps stream-aligned teams close a capability gap, operating mainly in facilitating mode, for a limited time (Ch 5).

**Extraneous cognitive load** — mental effort related to the environment in which a task is done (e.g., deployment steps, tool configuration) — should be minimized/eliminated (Ch 3).

**Facilitating mode** — team interaction mode where one team helps (or is helped by) another to clear impediments or learn a new approach, time-boxed (Ch 7).

**Fracture plane** — a natural seam in a software system that allows it to split cleanly into team-sized parts (Ch 6).

**Germane cognitive load** — mental effort on the aspects of a task requiring special attention for learning or high performance (the "value-add" thinking) (Ch 3).

**Homomorphic force** — Allan Kelly's term for Conway's law's pull toward matching shapes between organizational structure and software architecture (Ch 1, Ch 2).

**Intrinsic cognitive load** — mental effort fundamental to the problem space itself (e.g., language syntax, core algorithms) (Ch 3).

**Joined-at-the-database monolith** — several applications/services coupled to the same database schema, hard to change, test, or deploy separately (Ch 6).

**Monolithic build** — one gigantic CI build required to produce a new version of any component (Ch 6).

**Monolithic model** — software forcing a single domain language/representation across many different contexts (Ch 6).

**Monolithic release** — a set of independently buildable components bundled together and deployed as one release (Ch 6).

**Monolithic thinking** — "one-size-fits-all" standardization across teams that removes freedom to pick the right tool for the job (Ch 6).

**Monolithic workplace** — a single, uniform office-layout pattern imposed on all teams regardless of their actual collaboration needs (Ch 3, Ch 6).

**Organizational sensing** — teams and their internal/external communication acting as the organization's "senses," enabling it to detect and respond to change (Ch 8).

**Platform team** — a team providing self-service internal services (APIs, tools, knowledge, support) that reduce cognitive load for stream-aligned teams (Ch 5).

**Platform wrapper** — a thin layer that "platformizes" multiple lower-level/external services into a consistent developer experience for stream-aligned teams (Ch 8).

**Promise theory** — Mark Burgess's framing of inter-team/inter-system relationships as voluntary promises (e.g., SemVer) rather than commands or enforceable contracts (Ch 7).

**Reverse Conway Maneuver** (inverse Conway maneuver) — deliberately evolving team/organizational structure to achieve a desired software architecture, ahead of building the system (Ch 2, Ch 7, Ch 8).

**Stream** — a continuous flow of work aligned to a business domain, product, service, user journey, or persona (Ch 5).

**Stream-aligned team** — a team aligned to a single, valuable stream of work, empowered to deliver end-to-end with minimal hand-offs; the primary/default team type (Ch 5).

**Team (book's definition)** — a stable grouping of 5–9 people working toward a shared goal as a unit; the smallest entity to which work should be assigned (never an individual) (Ch 3).

**Team API** — the full surface (code, versioning, docs, practices, communication channels, visible priorities) by which other teams interact with a team (Ch 3).

**Team Topologies (the model)** — an organizational-design model using four fundamental team types and three team interaction modes, informed by Conway's law and cognitive load, to enable fast flow and organizational sensing (whole book).

**Team-toxic (individual)** — a person who consistently puts personal goals above team goals, damaging or destroying team cohesion if not coached or removed (Ch 3).

**Thinnest Viable Platform (TVP)** — the smallest platform that still meaningfully accelerates delivery for its consuming teams; grown only as complexity genuinely demands (Ch 5).

**X-as-a-Service mode** — team interaction mode where one team consumes something (API, library, platform) provided by another with minimal ongoing collaboration (Ch 7).
