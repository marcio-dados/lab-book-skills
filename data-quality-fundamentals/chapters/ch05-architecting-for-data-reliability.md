# Chapter 5: Architecting for Data Reliability

## Core Idea
Data reliability must be engineered deliberately — via testing at ingestion, observability in the pipeline, and formal SLAs/SLIs/SLOs downstream — using the same three-part discipline (process, technology, people) that software SRE developed for application uptime.

## Frameworks Introduced
- **SLA / SLI / SLO framework** (borrowed from SRE), applied to data:
  - **SLA**: the promise ("table X updates by 8 a.m. daily"), including remedy if missed.
  - **SLI**: the specific number measured (e.g., % of days table X updated on time).
  - **SLO**: the target value for the SLI (e.g., "99% of days").
  - When to use: any time you need to formalize "what does reliable mean here" with stakeholders instead of relying on vibes.
  - How: (1) define reliability via stakeholder interviews, (2) measure via SLIs, (3) track via SLOs and dashboards.
- **Three application observability pillars → five data observability pillars**: metrics/logs/traces (software) map to freshness/distribution/volume/schema/lineage (data).
- **Cost-of-data-downtime equation**: `(TTD hours + TTR hours) × Downtime hourly cost = Cost of data downtime`.
  - When to use: to build a business case for investing in data quality tooling/headcount.
  - How: estimate engineering time as a fraction of downtime hours, add analyst idle-time cost, multiply by monthly downtime hours.

## Key Concepts
- **Time to Detection (TTD)**: how long until a data quality issue is noticed — often days/weeks/months without observability tooling.
- **Time to Resolution (TTR)**: how long from alert to fix.
- **Data platform's six layers**: ingestion, storage/processing, transformation/modeling, BI/analytics, discovery/governance, and quality/observability (interconnected, not strictly sequential).
- **DAMA UK's six data quality dimensions**: completeness, timeliness, validity, accuracy, consistency, uniqueness (traditional data-steward framing — the authors note "accuracy" is hard for engineers to operationalize directly).
- **Net promoter score for data**: a subjective trust metric to complement objective SLIs.

## Mental Models
- Think of TTD × TTR as the two levers you can pull to reduce downtime cost — observability tooling primarily reduces TTD; lineage/runbooks primarily reduce TTR.
- SLAs are meaningless without accountability: define them WITH consumers, not FOR them, or they become theater.

## Anti-patterns
- **Setting SLAs no one measures**: "having reliable data at all times" is not an SLA — it's not falsifiable. A good SLA names the table, the deadline, the response window, and the escalation ("Team Z will verify within 2 hours...").
- **Boiling the ocean on certification**: trying to formalize SLAs for every table at once instead of starting with the most-queried, highest-dependency tables.
- **Ignoring the analytics-layer discovery gap**: most teams don't realize data is bad until it reaches a dashboard — by then the cost of TTD has already compounded.

## Reference Tables
| Data platform layer | Core question it answers |
|---|---|
| Ingestion | How does data enter the system? |
| Storage & processing | Where does it live, structured or not? |
| Transformation & modeling | How is it shaped into business logic? |
| BI & analytics | How is it made actionable for humans? |
| Discovery & governance | Who can find it, and who's allowed to? |
| Quality & observability | Is it healthy, and do we know when it isn't? |

## Worked Example
**Cost-of-downtime calculation** (illustrative, from the book): a data engineer spends ~¼ of every downtime hour on it, at ~$59/hr fully loaded → ~$14.75/downtime-hour in engineering cost. Add analyst idle time: 10 analysts × $75/hr, with only 4 realistically blocked and at 60% engagement → ~$300/hour analyst cost. At ~100 downtime hours/month, that's `100 × $300 × 12 = $420,000/year` — and this excludes lost-opportunity cost. The equation generalizes: `Labor cost + Compliance risk + Opportunity cost = Annual cost of broken data`, with compliance risk estimated at ~4% of annual revenue and labor cost as `# data engineers × annual salary × 30%`.

**Case study — Blinkist**: real-time behavioral data (Facebook/Google ad optimization) broke down when COVID-19 invalidated historical patterns; the team was spending 50% of engineering time firefighting. Fix: SLAs/SLIs on critical tables + observability tooling → 120 hours/week saved across a 6-person team. Key lesson from the case: setting SLOs/SLIs alone doesn't improve anything — the team's real win was *prioritizing execution* against the metrics, not just measuring them.

## Key Takeaways
1. Borrow SRE's SLA/SLI/SLO triad wholesale for data — it forces specificity that "we want good data" never achieves.
2. TTD and TTR are the two numbers that actually matter for downtime cost; instrument for both separately.
3. Build the business case for data quality investment with a dollar figure (labor + compliance + opportunity cost), not a vague appeal to "data trust."
4. A data platform has six interconnected layers — quality/observability is one of them, not a bolt-on afterthought.

## Connects To
- **Ch 4**: the five pillars measured here (freshness, distribution, volume, schema, lineage) are exactly what the anomaly detectors from Ch. 4 monitor.
- **Ch 6**: TTD/TTR are the core metrics the incident management lifecycle in Ch. 6 is built to minimize.
- **Ch 8**: SLAs reappear as the backbone of the "data certification" program.
