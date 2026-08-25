# Chapter 6: Fixing Data Quality Issues at Scale

## Core Idea
Once you can detect data incidents, you need a repeatable, DevOps-inspired incident management lifecycle — detect, respond, root-cause, resolve, postmortem — instead of ad hoc firefighting, or the same class of incident will keep recurring.

## Frameworks Introduced
- **Data reliability life cycle** (adapted from the DevOps life cycle: plan/code/build/test/release/deploy/operate/monitor): **Detect → Respond → Root-cause → Resolve → Postmortem (prevent)**.
  - When to use: as the default runbook shape for any data incident, regardless of root cause.
  - How: each stage has a clear owner and exit criterion; skipping the postmortem is the most common — and most costly — shortcut teams take.
- **Five Whys** (Amazon's RCA framework): identify the problem → ask why → decide if root cause → could it have been prevented/detected → if human error, why was it possible → repeat on the new "why" until confident.
- **Five-step Root Cause Analysis (RCA) sequence**: (1) look at lineage, (2) look at the code, (3) look at the data, (4) look at the operational environment, (5) leverage your peers.
  - When to use: as the default triage order when a data incident's cause isn't obvious — cheapest/most-likely-to-resolve checks first.

## Key Concepts
- **Incident commander**: the role (borrowed from SRE) responsible for flagging incidents, maintaining a working record, coordinating response, and assessing severity — distinct from whoever fixes the bug.
- **Runbooks vs. playbooks**: runbooks = "how to use this service"; playbooks = "step-by-step process for handling incident type X."
- **Blameless postmortem**: "the system is at fault, not the person" — postmortems that assign blame reduce future reporting of near-misses.
- **Phantom data**: incidents traced back to data nobody actually uses anymore — wasted RCA effort on deprecated assets.
- **Alert noise suppression**: grouping related alerts into one incident (vs. one alert per symptom) to avoid alert fatigue.

## Mental Models
- Incidents rarely have exactly one root cause — they're usually a confluence of an upstream data change, a logic change, and/or an operational failure (job stuck, permission issue, schedule change). Look for all three before declaring "solved."
- "My data is not refreshed" and "my metric shows an abnormal trend" are different incident classes requiring different detection AND different response paths — don't lump them into one alert channel.

## Anti-patterns
- **Relying on anomaly detection as the whole incident management strategy**: detection is one of five stages; without response/RCA/resolution/postmortem processes it's a false sense of "solved."
- **Skipping the postmortem**: without it, runbooks never improve and the same class of incident recurs indefinitely.
- **No clear incident commander**: ambiguity about "who's driving this incident" adds hours to TTR even after the right people are in the room.
- **Not accounting for phantom/deprecated data** in severity triage: teams burn hours firefighting data nobody consumes.

## Worked Example
The chapter walks a full RCA on a broken customer dashboard, step by step:
1. **Lineage**: trace to the most upstream node exhibiting the issue — this is where the actual root cause usually lives, not at the dashboard layer.
2. **Code**: ask what code last updated the table, how relevant fields are calculated, whether logic changed recently, whether there were ad hoc writes/backfills.
3. **Data**: slice by segment/time/subset — e.g. a spike in `user_interests = null` correlated with `source = Twitter` could mean either (a) Twitter volume grew (seasonality, no action) or (b) Twitter's null rate specifically increased (real processing bug) — same symptom, opposite fix, distinguishable only by looking at the joint distribution.
4. **Operational environment**: check ETL/orchestration logs (Airflow) for errors, delays, permission/infra changes, schedule changes.
5. **Peers**: ask who owns/uses the asset and what's happened before — tacit knowledge is often faster than re-deriving from scratch.

**Case study — PagerDuty's "DataDuty" team**: uses PagerDuty (their own product) + Snowflake + observability tooling; three best practices: (1) cover the *entire* data life cycle in incident management, not just pipeline-level checks (metric-trend issues aren't caught by pipeline quality checks alone); (2) suppress noise by grouping related alerts into one incident; (3) route alerts by criticality — executive/financial-reporting assets get escalation policies, routine tables don't.

## Code Examples
```text
# Five Whys template (Amazon):
1. Identify the problem.
2. Ask why it happened; record the reason.
3. Is the reason the root cause?
4. Could it have been prevented? Could it have been detected earlier?
5. If human error — why was it possible?
6. Repeat using the reason as the new problem, until confident.
```

## Reference Tables
| RCA step | Question it answers | Tooling |
|---|---|---|
| Lineage | Where did this start? | Data lineage graph (Ch. 7) |
| Code | What logic produced this? | Git blame / model history |
| Data | Which segment/time is affected? | Ad hoc SQL slicing |
| Operational environment | Did the job itself fail? | Airflow / orchestration logs |
| Peers | Has this happened before? | Tacit knowledge, incident history |

| Incident lifecycle stage | Primary owner | Key artifact |
|---|---|---|
| Detect | Automated monitoring / anomaly detection | Alert |
| Respond | Incident commander | Runbook / status channel |
| Root-cause | Data engineer / on-call | Five-step RCA |
| Resolve | Data engineer | Initial + final resolution |
| Postmortem | Whole team | Blameless postmortem doc |

## Key Takeaways
1. Detection is one of five stages — teams that stop at "we have anomaly detection" haven't actually solved incident management.
2. Use the five-step RCA order (lineage → code → data → operational environment → peers) as a default triage sequence; it's cheapest-first, not exhaustive-first.
3. Blameless postmortems and updated runbooks are what prevent repeat incidents — skipping them is the most common false economy.
4. Route and suppress alerts intelligently (group by incident, escalate by asset criticality) or the on-call rotation will drown in noise.

## Connects To
- **Ch 4**: anomaly detection here is explicitly framed as stage 1 of 5, not the whole solution.
- **Ch 7**: lineage, step 1 of the RCA sequence, is built out in full detail in the next chapter.
- **Ch 8**: severity triage ("is this data actually used?") connects to the data-certification/ownership model.
