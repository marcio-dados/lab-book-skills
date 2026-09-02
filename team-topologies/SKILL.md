---
origem: publico-terceiro
classificacao: nao-corporativo
tipo: livro-tecnico
idioma: en
titulo_pt: "Team Topologies"
proveniencia:
  titulo: "Team Topologies: Organizing Business and Technology Teams for Fast Flow"
  autor: ["Matthew Skelton", "Manuel Pais"]
  editora: "IT Revolution"
  fonte_sha256: "0bfd72c33f51a6c360abf740df4a5c25427d312d994acac7d52ff805c3d038c8"
  convertido_em: "2026-09-01"
  ferramenta_sha: "7bcfcd5262329f8d57a385903f18a98bc6705e4e"
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Team Topologies: Organizing Business and Technology Teams for Fast Flow
**Authors**: Matthew Skelton and Manuel Pais | **Pages**: ~43 (spine sections) | **Chapters**: 8 | **Generated**: 2026-09-01

## How to Use This Skill

- **Without arguments** — load core frameworks for reference
- **With a topic** — ask about `conway's law`, `team interaction modes`, `cognitive load`, or another indexed topic; I find and read the relevant chapter
- **With chapter** — ask for `ch05`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not covered in Core Frameworks below, I will read
the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**Conway's Law** (Ch 1–2): "Organizations which design systems... are constrained to produce designs which are copies of the communication structures of these organizations" (Mel Conway, 1968). Team structure and software architecture are two sides of one coin — never design one without the other.

**Reverse Conway Maneuver** (Ch 2, 7, 8): deliberately evolve team/communication structure to *achieve* a desired architecture, before the system is built, rather than mandating an architecture and hoping teams follow it. Expect the old architecture to "push back" temporarily; hold new boundaries with explicit collaboration + facilitating support until they stabilize.

**Team Cognitive Load** (Ch 1, 3): a team's finite capacity for intrinsic (fundamental to the problem), extraneous (environment/tooling friction — eliminate this), and germane (valuable domain knowledge — protect this) load. Match software/domain responsibility to team capacity, never the reverse. Domain-count rule: 2–3 simple domains OK; one complex domain gets no others; never two complicated domains on one team.

**The Team (definition)** (Ch 3): a stable group of 5–9 people (Dunbar's number-derived; up to ~15 only in high-trust orgs) working toward a shared goal. Assign work to teams, never individuals. Teams take 2 weeks to 3 months to become effective — protect that stability; reassign people at most ~once a year.

**The Four Fundamental Team Topologies** (Ch 5): **Stream-aligned** (default type, owns one flow of work end-to-end), **Enabling** (specialists closing a capability gap, temporary/facilitating), **Complicated-subsystem** (owns a part needing deep specialist knowledge — rare, driven by cognitive load not "shareability"), **Platform** (self-service internal product reducing stream-aligned teams' cognitive load). Target ratio: 6:1 to 9:1 stream-aligned to other types.

**The Three Team Interaction Modes** (Ch 7): **Collaboration** (close joint work, ≤1 partner team at a time, for discovery — expensive, boundary-blurring), **X-as-a-Service** (consume/provide with minimal collaboration, scales to many partners, needs strong service-management discipline), **Facilitating** (time-boxed help clearing impediments/capability gaps, the enabling team's main mode). Use collaboration to *discover* a viable X-as-a-Service boundary, then transition deliberately.

**Fracture Planes** (Ch 6): natural seams for splitting software into team-sized parts. Default to business-domain **Bounded Context** (DDD); layer in regulatory compliance, change cadence, risk, performance isolation, team location, technology, or user-persona planes only as secondary considerations. Test: "could we, as a team, consume or provide this as a service?"

**Thinnest Viable Platform** (Ch 5): start as thin as possible (even a wiki page); grow platform scope only as real complexity demands. Manage it as a live product — roadmap, user personas, DevEx, SLAs — never a side project.

**Organizational Sensing** (Ch 8): teams and their communication are the organization's senses. Watch three named triggers for topology redesign — software too large for one team, delivery cadence slowing, many services underlying a business capability — and treat operations as high-fidelity input to design (never split "new work" and "BAU" into separate teams; that breaks the feedback loop).

**Six Kinds of Hidden Monolith** (Ch 6): application, joined-at-the-database, monolithic build, monolithic release, monolithic model, monolithic thinking. A "distributed monolith" — services still requiring combined end-to-end release testing — means the split didn't achieve real independence.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-the-problem-with-org-charts.md) | The Problem with Org Charts | Conway's Law (intro), Pflaeging's three structures, systems thinking |
| [ch02](chapters/ch02-conways-law-and-why-it-matters.md) | Conway's Law and Why It Matters | Reverse Conway Maneuver, restrict unnecessary communication, tool-driven communication |
| [ch03](chapters/ch03-team-first-thinking.md) | Team-First Thinking | Dunbar's Number, Team Cognitive Load, Team API |
| [ch04](chapters/ch04-static-team-topologies.md) | Static Team Topologies | DevOps Topologies catalog, SRE dynamic relationship, non-blocking dependencies |
| [ch05](chapters/ch05-the-four-fundamental-team-topologies.md) | The Four Fundamental Team Topologies | Stream-aligned/Enabling/Complicated-subsystem/Platform, Thinnest Viable Platform |
| [ch06](chapters/ch06-choose-team-first-boundaries.md) | Choose Team-First Boundaries | Bounded Context, Fracture Planes, hidden monoliths |
| [ch07](chapters/ch07-team-interaction-modes.md) | Team Interaction Modes | Collaboration / X-as-a-Service / Facilitating, promise theory |
| [ch08](chapters/ch08-evolve-team-structures-with-organizational-sensing.md) | Evolve Team Structures with Organizational Sensing | Organizational sensing, topology-evolution triggers, continuity of care |

## Topic Index

- **Bounded Context** → ch06
- **Cognitive load (team)** → ch01, ch03, ch05
- **Collaboration mode** → ch07, ch08
- **Complicated-subsystem team** → ch05, ch07
- **Continuity of care** → ch03, ch08
- **Conway's Law** → ch01, ch02
- **DevOps Topologies catalog** → ch04
- **Distributed monolith / hidden monoliths** → ch06
- **Dunbar's Number** → ch03
- **Enabling team** → ch05, ch07
- **Facilitating mode** → ch07, ch08
- **Fracture planes** → ch06
- **Organizational sensing** → ch08
- **Platform team / Thinnest Viable Platform** → ch05
- **Promise theory** → ch07
- **Reverse Conway Maneuver** → ch02, ch07, ch08
- **SRE (Site Reliability Engineering)** → ch04, ch05
- **Stream-aligned team** → ch05, ch07
- **Team API** → ch03
- **Team interaction modes (overview)** → ch07, ch08
- **Topology evolution triggers** → ch08
- **X-as-a-Service mode** → ch07, ch08

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns
- [cheatsheet.md](cheatsheet.md) — quick reference tables and decision guides

---

## Scope & Limits

This skill covers the book content only. For hands-on implementation in your codebase,
combine with project-specific tools. For topics beyond this book, check related skills
or ask the agent directly.
