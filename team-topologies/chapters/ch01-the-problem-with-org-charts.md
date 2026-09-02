# Chapter 1: The Problem with Org Charts

## Core Idea
The org chart (formal structure) is not how work actually gets done; organizations need a dynamic, adaptive model of team design — Team Topologies — grounded in Conway's law and team cognitive load, rather than a static chart.

## Frameworks Introduced
- **Conway's Law**: "Organizations which design systems... are constrained to produce designs which are copies of the communication structures of these organizations" (Mel Conway, 1968).
  - When to use: whenever evaluating why a system architecture looks the way it does, or when planning a new architecture.
  - How: map real communication paths (not the org chart) and expect the resulting software to mirror them; if the desired architecture doesn't fit the organization, one of the two must change.
- **Three Organizational Structures (Niels Pflaeging)**: every organization actually has (1) formal structure (org chart, facilitates compliance), (2) informal structure (realm of influence between individuals), (3) value creation structure (how work actually gets done via inter-personal/inter-team reputation).
  - When to use: whenever using the org chart as the primary tool for allocating work or diagnosing delivery problems.
  - How: success comes from the interaction between informal and value-creation structures — design teams and interaction modes to strengthen those, not just the formal chart.

## Key Concepts
- **Org chart**: formal hierarchical reporting structure; useful for compliance, misleading as a map of real communication.
- **Systems thinking**: optimizing for the whole flow of work, finding the biggest bottleneck, eliminating it, repeating — rather than local optimization of one team/stage.
- **Homomorphic force**: Allan Kelly's term for the pull that makes software architecture and team structure converge in shape.
- **Cognitive load**: the finite amount of information a person (and by extension a team) can hold and process at once; ignored by most organizations when assigning responsibilities.
- **Team Topologies (the model)**: four fundamental team types (stream-aligned, enabling, complicated-subsystem, platform) plus three team interaction modes (collaboration, X-as-a-Service, facilitating), combined with Conway's law and cognitive load awareness.

## Mental Models
- Think of the org chart as a "software architecture document" for people: it goes stale the moment real work starts, so never treat it as ground truth for how teams actually collaborate.
- Use systems thinking, not local optimization: fast infrastructure provisioning is worthless if a weekly change-approval board still gates every release — find the real bottleneck first.
- Treat team structure and software architecture as two sides of one coin: a decision about team boundaries is implicitly a decision about system architecture (and vice versa).

## Anti-patterns
- **Org-chart-as-work-allocator**: splitting and assigning work strictly along formal reporting lines ignores lateral, cross-line communication that actually gets things done, producing unrealistic expectations and misaligned systems.
- **Static re-orgs (e.g., matrix management)**: introducing a new "final" structure without dynamic/sensing capability — it's outdated the moment business or technology shifts, and repeated re-orgs erode trust and momentum.
- **Ignoring cognitive load when assigning work**: assuming a team can absorb unlimited extra responsibility "because it's expected to adapt" leads to bottlenecks, quality issues, and demotivation.

## Worked Example
OutSystems' Engineering Productivity team (five years old, eight people) was responsible for build efficiency, CI/CD, and infrastructure automation. As responsibilities accumulated, sprint planning became a scramble across unrelated domains; constant context switching undermined all three of Dan Pink's intrinsic-motivation drivers — autonomy (priorities constantly hijacked), mastery (jack of all trades), and purpose (too many disconnected domains). The team looked healthy from the org chart (one team, one manager, clear mission statement) but the value-creation structure had quietly broken down: cognitive load had exceeded capacity without anyone naming it as the cause. (The book resolves this case later — Chapter 3 — by splitting into domain-focused microteams.)

## Key Takeaways
1. Never use the org chart as the primary mechanism for allocating work in a highly collaborative, uncertain context — it optimizes for compliance, not flow.
2. Look for the biggest bottleneck in the whole flow of work before improving any single team's local process.
3. Cognitive load is a real, if hard-to-quantify, constraint — treat it as a first-class factor when assigning team responsibilities.
4. Conway's law means organization design and software architecture design are inseparable; whoever decides team shape is implicitly deciding system architecture.
5. Expect and design for evolution — a single static structure (org chart or matrix) cannot keep pace with technology and business change.

## Connects To
- **Ch 2**: expands Conway's Law into the Reverse Conway Maneuver and practical team-design consequences.
- **Ch 3**: gives the detailed treatment of team cognitive load introduced here.
- **Ch 5**: introduces the four fundamental team topologies previewed in this chapter's summary.
