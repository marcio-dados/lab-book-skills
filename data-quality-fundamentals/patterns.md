# Patterns — Data Quality Fundamentals

## Freshness Detector
**When to use**: any table with an expected update cadence, to catch stale/missing loads.
**How**: compute `JULIANDAY(date) - JULIANDAY(LAG(date) OVER (ORDER BY date))` per update, then threshold (`> N days`). Tune the threshold via precision/recall (lower = higher recall/more false alarms, higher = higher precision/misses smaller outages).
**Trade-offs**: a single global threshold is cheap but blunt; per-table thresholds (or ML-based seasonal baselines) scale better but cost more to maintain. (Ch 4)

## Distribution/Null-Rate Detector
**When to use**: catching silent data corruption (nulls, zeros, out-of-range values) that doesn't break the pipeline but corrupts downstream metrics.
**How**: compute a per-field, per-day rate (e.g., `null_count / total_count`), smooth with a rolling average (e.g., 14-day window), and alert when the current value deviates from the rolling average by a threshold — not on the raw value alone, to reduce seasonality-driven false positives.
**Trade-offs**: rolling-average smoothing reduces noise but adds detection lag; don't apply `ABS()` indiscriminately — an increase and a decrease in null rate are often not equally alarming. (Ch 4)

## Schema Versioning Table
**When to use**: detecting and dating schema changes without native DB version history.
**How**: maintain a side table (`date, columns`) snapshotting the schema on each check; compare `LAG(columns)` to the current row to find the exact date of change.
**Trade-offs**: cheap and DB-agnostic, but only as fine-grained as your check frequency (daily checks miss intra-day changes). (Ch 4)

## Field-Level Lineage Edge Model
**When to use**: whenever you need to answer "what does this column feed, and where did it come from" — root cause analysis, impact analysis, PII tracing.
**How**: parse each query (via ANTLR or similar) into destination table/field + source table/field edges, distinguishing selected fields (define values) from non-selected fields (affect row filtering only); key documents by a hashed lineage-object ID plus the destination table's stable ID (mcon) so multiple queries updating one table are all captured.
**Trade-offs**: expect ~70% SQL-clause coverage on a first implementation pass; full coverage requires iteratively testing every clause combination against your stack's actual query patterns. (Ch 7)

## Circuit Breaker
**When to use**: preventing bad data from propagating downstream once detected, for high-severity assets only.
**How**: two states (closed = flowing, open = blocked); implement via `catchup=False`, `LatestOnlyOperator`, or a custom Python/SQL check (`SQLCheckOperator`) that halts the DAG on failure.
**Trade-offs**: powerful but blunt — overuse blocks unrelated, perfectly good jobs sharing the same DAG; reserve for incidents with serious business ramifications. (Ch 3)

## Five-Step Root Cause Analysis
**When to use**: any data incident where the cause isn't immediately obvious.
**How**: check in this order — (1) lineage (find the most upstream affected node), (2) code (what logic/model last changed?), (3) data (slice by segment/time to isolate the anomaly), (4) operational environment (orchestration/ETL logs), (5) peers (tacit knowledge, prior incidents). Cheapest/most-informative checks first.
**Trade-offs**: sequential and mostly manual; lineage tooling (previous pattern) short-circuits step 1 dramatically. (Ch 6)

## SLA / SLI / SLO Definition Loop
**When to use**: formalizing "what does reliable mean" for a data asset before an incident forces the conversation.
**How**: (1) define reliability via stakeholder interviews and historical baseline, (2) pick SLIs that are specific and measurable (e.g., "% of days updated by 8am"), (3) set SLOs as target values (e.g., "99%"), (4) build dashboards tracking the SLI against the SLO.
**Trade-offs**: SLAs without a defined response protocol ("Team Z will verify within 2 hours...") are unenforceable; vague SLAs ("reliable data at all times") are non-falsifiable and worthless. (Ch 5, Ch 8)

## Seven-Step Data Certification Program
**When to use**: scaling data trust across an organization instead of table-by-table, ad hoc firefighting.
**How**: (1) build observability baseline, (2) assign owners per table/life-cycle stage, (3) define "good" via stakeholder KPIs per pillar, (4) set SLAs/SLOs/SLIs, (5) build communication/incident processes, (6) tag certified assets (consider bronze/silver/gold tiers), (7) train the team and downstream consumers.
**Trade-offs**: don't certify everything at once — start with the most-queried, highest-dependency tables and certify in waves. (Ch 8)

## Data Downtime Cost Calculation
**When to use**: building a budget/headcount case for data quality investment.
**How**: `DDT = N × (TTD + TTR)`; convert to dollars via `(engineering time as % of downtime hours × headcount × avg wage) + (analyst idle time) + compliance risk + opportunity cost`.
**Trade-offs**: the book's default percentages (50%/35%/20% of engineer time by maturity level) are survey-based anchors — recalibrate with your own incident history once you have one. (Ch 5, Ch 10)

## Data Mesh Readiness Score
**When to use**: deciding whether a data mesh migration is worth the organizational cost, before starting one.
**How**: sum five factors — # data sources, data team size, # data domains, engineering-bottleneck severity (1–10), governance priority (1–10). Score 1–15 = not yet; 15–30 = adopt mesh concepts now; 30+ = sweet spot for a full mesh.
**Trade-offs**: a mesh missing any of Dehghani's four defining elements (distributed ownership, long-term accountability, self-serve infra, federated governance) is "just overengineering a centralized team's distribution," not a real mesh. (Ch 9)
