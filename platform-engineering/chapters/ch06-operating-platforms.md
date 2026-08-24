# Chapter 6: Operating Platforms

## Core Idea
Platform teams must routinely invest in three operational practices — on-call, user support, and operational feedback — even in good times, because "rare things become common at scale" and neglected operational debt turns into "operational hell" that stalls all feature work.

## Frameworks Introduced
- **Practices, not processes**: practices (on-call, support, operational feedback) are the fixed framework; the specific process implementing each is situational and should change as your problems change. Don't import a process wholesale from SRE/DevOps literature or a previous job without checking fit.
- **Merged DevOps on-call model**: platform teams should staff their own 24x7 on-call rotation with a mixed team of software + systems engineers, rather than splitting off a separate SRE/DevOps team.
  - Why: platform teams are usually too small to sustain a fully separate on-call specialist team (SRE literature: nobody stays if on-call >25% of time, so a split rotation alone needs 4-5 dedicated SREs) — and a split team spread across many platforms loses the deep expertise needed to diagnose complex issues, recreating the Ops-vs-Dev finger-pointing divide (Ch 1).
  - When to use: virtually always, unless you're FAANG-scale with 10+ dedicated engineers per platform justifying a true specialist split.
- **Sustainable on-call load target: <5 business-impacting pages/week**: derived from Amazon-internal survey data — <2 pages/week correlated with happy engineers, 2–5 with some unhappiness but no attrition-intent signal, >5 with both unhappiness and negative "will I be here in 12 months" signal.
  - How to get there: no one on-call more than 1 week in 4 (ideally 1 in 6–8); eliminate false alarms (root cause: usually workday-correlated deployment noise vs. genuine after-hours failures — provide dashboards as an alternative "pulse" for engineers who use false alarms as a heartbeat); prioritize stability work over features once you're above the threshold; use another platform team purely for secondary/fall-through paging (should be rare); don't try to fix unsustainable load with on-call pay — it subsidizes bad management and creates fairness/gamesmanship problems.
- **Four-stage support-load escalation ladder**: Stage 1 — formalize support levels/SLA (categorize ticket types, define what counts as "critical enough to page," invest in postmortem follow-through, observability/synthetic monitoring, and pushing back on unreasonable stakeholder expectations). Stage 2 — separate a business-hours support rotation from on-call once noncritical load stacks up (but keep combined ops load under ~50% of team capacity). Stage 3 — hire a support specialist only once truly overloaded, preferring internal/external "quick learners" on a 12–24 month growth path (T1→T2→full platform engineer) over a career T1 hire who will quickly want to leave, or a permanent contractor. Stage 4 — at large scale, build a company-wide T1 Engineering Support Organization (ESO) with platform teams handling T2, tiered application SLAs, mandatory application-team on-call for Tier 0/1, hiring systems engineers to keep the merged-DevOps culture alive, an embedded "expert network" of advanced customers as first-line peer support, and a biweekly ESO↔platform feedback review.

## Key Concepts
- **Customer-facing vs. internal SLOs (opposite rules)**: customer-facing SLOs/error budgets should be few, minimize false positives (tolerate occasional false negatives with follow-up), and used to trigger a trade-off conversation — not an automatic feature-freeze contract. Internal SLOs should be numerous, tolerate false positives (missing a real issue is worse), and both false positives/negatives need explanation.
- **Error budgets are optional, not free**: SLIs/SLOs/SLAs are essential; the "hard contractual stop on releases when budget is exceeded" framing from the SRE book creates us-vs-them dynamics and is only worth the cost for teams with chronic availability problems or a customer-expectation mismatch to correct.
- **Change management as a precursor to CI/CD, not a substitute**: platforms are often too stateful/complex for full automated CI/CD immediately (e.g. a cache-clearing deploy causing latency spikes); mandatory documentation + review + pre-production testing surfaces where automation investment is actually needed before the one engineer who "just knows" the sharp edges leaves. Reference: the 2017 AWS S3 outage caused by one mistyped command-line parameter.
- **Synthetic (active) monitoring**: simulating real user/API interactions against production to catch correctness (not just latency/availability) issues before customers report them; benefits include end-to-end monitoring, forced "customer understanding" (dogfooding-like), operational-system understanding (lowers MTTR), and triangulation (isolating platform-wide vs. customer-specific issues). Ian's AWS estimate: budget ~25% of ongoing dev time and ~10% of platform resource cost for doing this well.
- **Operational reviews**: regular (usually weekly team-level, monthly org-level) blameless meetings reviewing pages, support issues, postmortems, production changes, and SLO trends — the mechanism that closes the feedback loop between operational data and where engineering time actually goes. Curated by whoever just came off on-call; org-level reviews often best driven by reliability engineers (Ch 4).

## Mental Models
- Treat a page count above 5/week not as a personnel problem but as a business-priority signal: stop feature work and restore stability.
- When engineers resist eliminating "useful" false alarms, satisfy the underlying need (a sense of system "pulse") with dashboards instead of leaving noisy pages in place.
- Judge whether a support specialist hire is temporary (documentation/training/platform fixes could eliminate the need — use a contractor) or permanent (build a growth pipeline for nontraditional-background "quick learners" instead of a revolving door of short-term hires).
- A platform team building its own full shadow deployment platform (instead of investing proportionately in release engineering) signals distrust of the company's own platforms and is a political, not just technical, problem — cap around 12 developer-months/year as a warning sign of overbuilding.

## Reference Tables
| On-call weekly pages | Engagement signal (Amazon survey) |
|---|---|
| < 2 | Happy team members |
| 2–5 | Some unhappiness, no attrition intent |
| > 5 | Consistent unhappiness + attrition intent |

| Support escalation stage | Trigger | Action |
|---|---|---|
| 1 — Formalize support levels | Support noise not yet separated from on-call | Categorize tickets, define SLA/paging criteria, invest in postmortems + observability |
| 2 — Separate support rotation | Noncritical load stacking up, backlog growing | Dedicated business-hours support rotation (keep total ops load <~50%) |
| 3 — Hire a specialist | Team still overloaded after Stage 2 | Growth-path hire (T1→T2→platform engineer) or contractor if temporary |
| 4 — Org-level ESO | Multiple platform teams need T1 | Company-wide T1 org, tiered SLAs, mandatory app-team on-call for Tier 0/1, expert network, biweekly reviews |

## Anti-patterns
- **Split SRE/DevOps team spread thin across many platforms**: recreates Ops-vs-Dev finger-pointing because no one has deep expertise in any one platform.
- **Paying for on-call to fix an unsustainable load**: subsidizes bad management, creates fairness disputes and metric gamesmanship instead of fixing root causes.
- **Manager/PM absorbing all noncritical support personally**: removes engineers' visibility into real user pain and eventually overloads the one absorbing person too.
- **Treating error budgets as an automatic feature-freeze trigger** rather than a prompt for a trade-off conversation.
- **Platform team building a full shadow deployment platform** instead of proportionate release-engineering investment — a political and technical overreach.
- **Rigid, over-processed operational reviews divorced from the team's actual situational issues** — wastes the time it's meant to protect.

## Worked Example
At Amazon around 2014, Ian's larger organization was in "operational hell": early builders who tolerated growth-phase pain had moved on, leaving second-generation owners with monthly customer-impacting issues and ~25% annual attrition. A new VP correlated engagement-survey data against pager load and found the <2 / 2–5 / >5 pages-per-week breakpoints described above. The organization's response was not to add headcount but to prioritize stability, systematically eliminate false alarms (providing dashboards to preserve the "pulse" some engineers valued), and hold leadership accountable for balancing feature work against the newly visible operational signal — directly informing the "sustainable on-call load" and "eliminate false alarms" practices in this chapter.

## Key Takeaways
1. Invest in on-call, support, and operational feedback as fixed practices even when things look fine — operational debt compounds silently until it's acute.
2. Prefer a merged DevOps on-call rotation over a split model for all but the largest platform teams.
3. Target fewer than 5 business-impacting pages/week; treat exceeding it as a mandate to pause features and fix stability, not a personnel failure.
4. Separate support from on-call once load grows, following the 4-stage ladder, and resist premature or permanent specialist hires when the root cause is fixable.
5. Use customer-facing SLOs sparingly and to start a trade-off conversation, not as an automatic contractual trigger; use many, noisier internal SLOs to actually catch problems.
6. Change management is the necessary precursor to real CI/CD for stateful, complex platforms — skipping it hides risk until the one person who "knows the sharp edges" leaves.
7. Invest meaningfully in synthetic monitoring — it's often more valuable for platforms than for typical application systems.
8. Run regular, blameless operational reviews with engaged leadership to close the loop between operational data and engineering priorities.

## Connects To
- **Ch 1**: revisits the Ops-vs-Dev / split-vs-merged DevOps debate.
- **Ch 2**: user observability and guardrails recur as prerequisites for sane support/SLA definitions.
- **Ch 4**: reliability engineers are the natural drivers of org-level operational reviews.
- **Ch 10**: stakeholder conversations about unreasonable support expectations are developed further.
