# Chapter 8: Evolve Team Structures with Organizational Sensing

## Core Idea
The most important design decision is not the current team shape but the *rules for changing it* — organizations must treat operations as high-fidelity sensory input and deliberately evolve interaction modes (collaboration → X-as-a-Service) as discovery gives way to predictable delivery.

## Frameworks Introduced
- **Organizational Sensing**: teams and their communication act as the organization's "senses" (Peter Drucker's "synthetic sense organs for the outside"); well-defined, stable communication pathways between teams are what make sensing possible at all.
  - When to use: continuously — ask whether team-interaction modes still fit reality, whether a build-vs-buy decision should change, whether an X-as-a-Service boundary is drifting back into needed collaboration.
  - How: use concrete questions (have we misunderstood user needs? should Team A/B still collaborate or move to X-as-a-Service? does the platform serve teams D–G's real needs?) as a recurring organizational check, not a one-time exercise.
- **Explore / Exploit / Sustain / Retire via Evolving Team Topologies**: team interaction modes are expected to evolve over months (not days) — close collaboration (discovery) → limited collaboration → X-as-a-Service (established, predictable delivery) — with different parts of a large organization at different stages simultaneously.
  - When to use: whenever a team pairing has been static for a long period, or a new technology/domain is being explored.
  - How: start new/uncertain work in collaboration mode; deliberately transition to X-as-a-Service once a boundary or API proves stable; expect multiple such transitions running concurrently across an enterprise (Figure 8.7's multi-team pattern).

## Key Concepts
- **Triggers for topology evolution**: named, recognizable symptom clusters that should prompt a redesign — (1) software has grown too large for one team (Dunbar's-number-scale growth, routine bottleneck assignees, documentation complaints), (2) delivery cadence is slowing (velocity trending down, growing WIP waiting on other teams), (3) many business services depend on a large set of underlying services (poor end-to-end visibility, hard reuse).
- **Platform wrapper**: a thin "platformizing" layer over multiple lower-level services/APIs that gives stream-aligned teams a consistent DevEx (correlation IDs, health checks, diagnostics) even when the underlying services are heterogeneous or externally supplied.
- **Cybernetic feedback / self-steering**: treating live operations output as a direct, high-fidelity input back into design and development decisions, rather than as a separate downstream phase.
- **Continuity of care**: one stream-aligned team owning both new-feature work and "business as usual" (BAU) maintenance of the same system side by side, so learning from operations feeds directly back into design (contrasted with separate new-service/BAU teams, which block this feedback loop).
- **The Three Ways of DevOps** (Kim et al., cited): systems thinking (optimize the whole flow), feedback loops (Ops informs Dev), and a culture of continual experimentation/learning — all three require the sensing infrastructure this chapter describes.

## Mental Models
- Treat "how much collaboration is right?" as a live, ongoing question per team pair, not a one-time org-design decision — Team A/B might need close collaboration this quarter and near-zero interaction next year.
- Model organizational change like an organism: separate "sensing organs" (teams close to signals) and "response capacity" (teams/structures that can act on those signals) both need to exist and stay connected.
- Staff IT operations/service-desk roles with experienced engineers, not the most junior staff — the signal quality flowing back to Dev depends on the triage skill of whoever is closest to the live system.

## Anti-patterns
- **Separate "new stuff" and BAU teams**: splits the team that builds from the team that lives with the consequences, breaking the feedback loop and leaving the BAU team unable to apply newer telemetry techniques to older systems (a "non-cybernetic" structure, in the book's own words).
- **Cost-optimizing maintenance work with cheaper/separate staff**: Sriram Narayan's warning that this is "false economy" — it hurts business outcomes and reduces IT agility by starving the feedback loop.
- **Freezing an interaction mode past its useful life**: keeping two teams in expensive collaboration mode long after a boundary has stabilized, or forcing X-as-a-Service prematurely before a boundary is actually proven, both waste the mode's intended benefit.
- **Ignoring the "software too large" symptom cluster**: letting routine changes keep landing on the same specialist(s) — a reinforcing local optimization that hides a topology problem until it becomes a serious bottleneck.

## Reference Tables
<!-- omitted: this chapter's content (trigger symptom lists, case-study timelines) is presented as prose/bulleted lists, not a formal comparison table -->

## Worked Example
uSwitch (Paul Ingles, Head of Engineering) explicitly used a *technology* decision to force an *organizational* change: "We didn't change our organization because we wanted to use Kubernetes; we used Kubernetes because we wanted to change our organization." Dev teams had been forced to understand too much of the underlying stack (excess cognitive load); adopting a platform abstraction was the lever to reduce that load and shift team interaction back toward the intended X-as-a-Service pattern with a platform team. Separately, TransUnion's System-Build/Platform-Build teams (started 2014) evolved over roughly four years — from close collaboration, to a merged enabling-style function, to finally dissolving back into Dev and Ops once the platform relationship had stabilized — illustrating that topology evolution properly takes months to years, driven by named triggers and observed outcomes, not a single reorg event.

## Key Takeaways
1. Design the *rules* for evolving team structure, not just a single target structure — the organization's context will keep changing.
2. Recognize the three named trigger clusters (software too large, delivery cadence slowing, many services underlying a business capability) as signals to redesign topology, not as things to individually patch around.
3. Never separate the team that builds a system from the team that operates it long-term — continuity of care is what makes operational feedback usable for design.
4. Deliberately transition team-interaction modes over time (collaboration for discovery, then X-as-a-Service for stable delivery) rather than treating the initial choice as permanent.
5. Staff sensing points (service desk, on-call, first response) with experienced people — the fidelity of the signal reaching Dev depends on it.
6. Use a platform wrapper to give stream-aligned teams a consistent DevEx over a heterogeneous set of underlying/external services, rather than exposing every inconsistency directly.

## Connects To
- **Ch 7**: the collaboration → X-as-a-Service evolution described here is the same three modes from that chapter, applied over time.
- **Ch 4**: the TransUnion and Sky Betting & Gaming case studies begun there are resolved/continued here.
- **Ch 2**: the reverse Conway maneuver reappears here as an ongoing, iterative practice rather than a one-time move.
