# Chapter 7: Building End-to-End Lineage

## Core Idea
Field-level (not just table-level) data lineage is the technology that turns "something broke" into "here's exactly what broke, why, and who's affected" — and building it at scale requires a SQL-parsing pipeline plus a data model expressive enough to capture arbitrarily nested queries.

## Frameworks Introduced
- **Table-level vs. field-level lineage**: table-level shows "table A feeds table B"; field-level shows exactly which upstream *columns* produce which downstream *columns* — necessary for real root cause analysis and impact analysis, not just a nice visualization.
  - When to use: table-level is enough for a first pass / macro view; field-level is required once you need to answer "if I change this column, what breaks?"
- **Selected vs. non-selected fields**: selected fields define the values in the result table (`SELECT` clause); non-selected fields (e.g., in `WHERE`/`JOIN`) affect *which rows* appear but not the field values themselves — separating these keeps the lineage UI from being noise.
- **Basic lineage requirements checklist**: fast time-to-value, secure architecture (metadata only, never raw PII), automation (not manual upkeep), integration with the existing stack, column-level extraction.

## Key Concepts
- **Data lineage**: a map of a data set's journey from ingestion to the analytics layer — "how did data get from point A to point B," down to the column level in modern tooling.
- **mcon (table ID)**: a stable identifier for a table used as the anchor of a lineage edge, paired with a hashed lineage-object ID so multiple queries updating the same destination table can all be captured.
- **ANTLR-based query parsing**: parses SQL into a grammar tree so column-level relationships (not just table names) can be extracted programmatically.

## Anti-patterns
- **Building lineage that touches raw user data/PII**: lineage should be built from metadata, logs, and parsed queries — never by reading the actual data out of the customer's environment.
- **Table-level-only lineage for RCA**: too coarse to explain *why* a metric is wrong; field-level is the level at which root cause actually becomes visible.
- **Lineage without a curated UI**: showing every possible SQL-clause relationship at once produces a "spider web" that buries the two layers people actually care about — the most-upstream source and the most-downstream BI report.

## Worked Example
The chapter walks through parsing a real, deeply nested SQL query (nine chained CTEs in a `WITH` clause, e.g. `usage_stuck_to_be_processed`, `usage_subscription_state_updated`, `usage_subscription_state_change_actions`, ending in a final `SELECT` joining multiple of these plus a `LEFT JOIN`). Rather than treating this as one opaque blob, the field-level lineage model decomposes it into a JSON edge object:
```json
{
  "edge_id": "37d65dc5c943cab124398b2c43f0d8f2c0ff5e76a2ba3052",
  "destination_table_mcon": "",
  "source_table_mcons": ["mcon1", "mcon2"],
  "sources": [{"table_mcon": "", "field_name": ""}],
  "destination_field": "new field name",
  "parsed_query": ""
}
```
This lets a UI show, for one destination field, exactly which upstream table.column pairs feed it — collapsing a nine-CTE query into a small number of resolvable edges, which is what makes "which report breaks if I change this column?" answerable in seconds instead of a manual SQL read-through.

## Code Examples
```sql
-- Illustrative fragment of the kind of nested CTE lineage must resolve
WITH usage_stuck_to_be_processed AS (
  SELECT s.usage_id, s.created_date
  FROM 'decom.processed.subscriptions' s
  JOIN 'decom.processed.usages' u ON s.usage_id = u.id
  WHERE (s.state = 'to_be_processed' AND u.activated_at IS NOT NULL)
),
usage_subscription_state_updated AS (
  SELECT *, rank() OVER (PARTITION BY usage_id ORDER BY created_at DESC) AS sub_update_no_desc
  FROM 'decom.usage_timelines.usage_subscription_states'
)
-- ... 7 more CTEs, then a final SELECT joining several of them.
```

## Reference Tables
| Lineage requirement | Why it matters |
|---|---|
| Fast time-to-value | Column-level abstraction needed for quick remediation, table-level is too broad |
| Secure architecture | Metadata/logs only — never raw data or PII |
| Automation | Manual lineage upkeep doesn't survive schema churn |
| Stack integration | Must span warehouse/lake, transformation (dbt/Airflow), and BI (Looker/Tableau/Mode) |
| Column-level extraction | Query-log parsing alone (table-level) can't power real RCA |

| Lineage use case | What it answers |
|---|---|
| Reviewing a suspicious revenue number | Which upstream table/model produced this field? |
| Reducing data debt | Is this column still used downstream, or safe to deprecate? |
| Managing PII | Which downstream dashboards inherit a PII column? |

## Key Takeaways
1. Table-level lineage is a good first pass, but field-level lineage is what makes root cause analysis and impact analysis actually fast.
2. Lineage should be built from metadata/query parsing, never from reading raw data — this is both a security requirement and a scalability one.
3. A recursive, nested-CTE-aware SQL parser (e.g., via ANTLR) is the hard engineering problem — expect ~70% coverage on a first pass, with the remaining 30% requiring iterative grammar fixes.
4. The most useful lineage UI shows only the most-upstream source and most-downstream BI asset by default — full graphs are for power users, not the default view.

## Connects To
- **Ch 2**: extends the ANTLR SQL-parsing example introduced there into a full lineage system.
- **Ch 4**: lineage is what turns an anomaly ("habitability average dropped") into a root cause ("schema change in an upstream table on the same date").
- **Ch 6**: lineage is explicitly step 1 of the five-step RCA sequence.
