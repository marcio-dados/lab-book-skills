# Cheatsheet — Data Quality Fundamentals

## Decision rules

- **Choosing warehouse vs. lake**: need SQL-first, governed, BI-ready data → warehouse (schema-on-write). Need flexible, ML-friendly, semi/unstructured ingestion → lake (schema-on-read). Need both → lakehouse, because forcing one to do the other's job is where quality breaks (Ch 2).
- **Testing vs. monitoring**: if you can name the failure mode in advance, write a test (dbt/Great Expectations/Deequ). If you can't, you need anomaly detection/observability — testing only covers ~20% of real-world issues (Ch 3, Ch 4).
- **Detector threshold too aggressive?** If alert fatigue is reported ("boy who cried wolf"), raise the threshold (trade recall for precision). If real incidents are being missed ("sleeping guard dog"), lower it (Ch 4).
- **Fβ weighting**: recall matters more than precision (β>1) when false negatives are catastrophic (e.g., missile alerts, fraud). Precision matters more (β<1) when false alarms burn trust faster than a missed issue would (Ch 4).
- **Null-rate change direction**: an *increase* in null rate is usually the alarming direction; don't symmetrize with `ABS()` by default — check which direction matters for the specific field (Ch 4).
- **Data mesh or not**: score < 15 → no. 15–30 → adopt mesh concepts, don't fully migrate. 30+ → migrate. A mesh without distributed ownership + accountability + self-serve infra + federated governance isn't a mesh (Ch 9).
- **Should this data quality effort be a test, a monitor, or a circuit breaker?** Known failure mode + cheap check → test. Unknown/statistical failure mode → monitor/anomaly detector. High-severity, must-not-propagate → circuit breaker (blocks the whole pipeline) (Ch 3, Ch 4).
- **RCA order**: always check lineage → code → data → operational environment → peers, in that order — cheapest and most likely to resolve first (Ch 6).
- **Build vs. buy**: build only if (a) data is too sensitive/regulated to hand a vendor, (b) you need niche customization a vendor won't prioritize, or (c) building is itself a strategic/competitive advantage. Otherwise buy (Ch 8).

## Decision tree: is my data "broken"?

1. Did a known assertion fail (null check, uniqueness, range)? → **Yes**: it's a test failure — known unknown, fix per Ch 3.
2. No test fired, but a stakeholder / dashboard looks wrong? → **Unknown unknown** — go to anomaly detection (Ch 4): check freshness, distribution, volume, schema, lineage in that order.
3. Anomaly confirmed — what's upstream? → Run the 5-step RCA (Ch 6): lineage → code → data → operational environment → peers.
4. Root cause found — is this asset certified / high blast radius? → **Yes**: circuit-break if still propagating, notify per SLA, escalate to incident commander. **No**: fix, log, consider whether it should be certified going forward (Ch 8).
5. After resolution → blameless postmortem, update runbook, re-check SLA/SLO validity (Ch 5, Ch 6, Ch 8).

## Trade-off matrices

| Testing framework | Language | Strength | Weakness |
|---|---|---|---|
| dbt tests | SQL | Native to transformation layer | Manual upkeep, blurred unit/integration |
| Great Expectations | Python | Rich test library, Data Docs | Disconnected from orchestration |
| Deequ/PyDeequ | Scala/Python | Scale via Spark, built-in anomaly detection | Scala learning curve, weak integration testing |

| Detector personality | Precision | Recall | Failure mode |
|---|---|---|---|
| Boy who cried wolf (low threshold) | Low | High | Alert fatigue |
| Sleeping guard dog (high threshold) | High | Low | Misses real incidents |
| Tuned (Fβ-optimized) | Balanced per use case | Balanced per use case | Requires labeled ground truth to tune |

| Catalog approach | Scales to lake/mesh? | Maintenance |
|---|---|---|
| Manual spreadsheet catalog | No | High, immediately stale |
| Traditional data catalog (UI-driven) | Poorly | Medium, still manual entry |
| Data discovery (automated, ML-based) | Yes | Low, self-updating |

## Thresholds & defaults (book's stated numbers — recalibrate with your own data)

- Freshness anomaly threshold: start at "> 1 day since last update," then tune (book's worked example finds the F1-optimal threshold at 4 days for that data set).
- Null-rate spike default: alert when null rate > 90% *or* deviates from a 2-week rolling average by > 0.3 (30 percentage points).
- Data quality maturity → % of engineer time on quality issues: low = 50%, average = 35%, high = 20%.
- 1 in 15 tables affected by a data incident per year (empirical anchor across ~150 companies surveyed).
- Average TTD+TTR: ~8h (low maturity), ~6h (average), ~4h (high maturity).
- Data mesh readiness score bands: <15 no, 15–30 adopt concepts, 30+ migrate.
- ~50+ tables is a rough threshold where observability tooling starts paying for itself, regardless of severity.

## Tells & smells

- "We keep getting Slack messages asking which table is good to use" → you need a data catalog/certification program, not more engineers (Ch 8).
- A detector alert doesn't change what anyone does → the detector lacks lineage/context; pair it with lineage before adding more alerts (Ch 6, Ch 7, Ch 9).
- Postmortems keep getting skipped → the same incident class will recur; missing postmortems is the single most common false economy in incident management (Ch 6).
- A table that "should be null-free" starts showing 90%+ nulls right after a schema change elsewhere → check lineage first, it's very likely a same-day upstream schema change (Ch 4, Ch 7).
- Your SLA says "reliable data at all times" → it's not a real SLA; it has no falsifiable measurement or response protocol (Ch 5, Ch 8).
- A team is scoring high on the data mesh rubric but hasn't distributed *accountability*, only *infrastructure* → they're building a distributed monolith, not a mesh (Ch 9).
