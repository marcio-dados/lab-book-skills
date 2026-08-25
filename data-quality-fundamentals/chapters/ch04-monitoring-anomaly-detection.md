# Chapter 4: Monitoring and Anomaly Detection for Your Data Pipelines

## Core Idea
Testing only catches "known unknowns"; monitoring and anomaly detection across the five pillars of data observability (freshness, distribution, volume, schema, lineage) are what catch the "unknown unknowns" that testing structurally cannot anticipate.

## Frameworks Introduced
- **Known unknowns vs. unknown unknowns**: predictable issues (nulls, expected freshness cadence) vs. issues no test was written for (a JSON schema change turning 6 columns into 600, silent data drift).
  - When to use: to decide whether you need more tests (known unknowns) or monitoring/anomaly detection (unknown unknowns).
- **The five pillars of data observability**: freshness, distribution, volume, schema, lineage.
  - How: build a detector per pillar — freshness via `DAYS_SINCE_LAST_UPDATE`, distribution via null/zero rate queries, schema via a versioned columns table, lineage via a dependency graph.
- **Precision/Recall/F-score framework** for tuning detectors.
  - When to use: any time you set a threshold parameter on a detector and need to justify *where* to set it.
  - How: Precision = TP/(TP+FP); Recall = TP/(TP+FN); Fβ weighs recall as β times more important than precision — use β>1 (e.g., missile alerts) when false negatives are catastrophic, β<1 when false alarms are the bigger cost.

## Key Concepts
- **Freshness**: is the data recent? Measured via `DAYS_SINCE_LAST_UPDATE` per table.
- **Distribution**: are values within expected ranges (null rate, zero rate, quantiles)?
- **Volume**: did all the expected data arrive?
- **Schema**: has the table's structure changed, and when?
- **Lineage**: what upstream/downstream dependencies explain an anomaly's root cause?
- **Seasonality**: predictable fluctuation over time (e.g., a table that never updates on Sundays) — naive z-score thresholds misfire on seasonal data.
- **Central Limit Theorem**: justifies (with caveats) using Gaussian z-scores for anomaly scoring, but fails when observations are correlated (business data usually is).
- **True/False Positive/Negative**: the four detector outcomes — sleeping-guard-dog detectors (never alert) vs. boy-who-cried-wolf detectors (always alert) are the two failure extremes.

## Anti-patterns
- **Relying on anomaly detection alone**: it's necessary but not sufficient — without lineage/root-cause tooling, "there's a problem" doesn't tell you *what* to fix (the "car mechanic" analogy: "something is wrong with my car" vs. specific symptoms).
- **Optimizing for "accuracy"**: a detector that always says "not anomalous" scores 99.6% "accuracy" on rare-event data (AIDS-diagnosis example) while being useless — always prefer precision/recall/F-score.
- **Using ABS() on a null-rate delta indiscriminately**: a null rate *increase* is alarming; a null rate *decrease* usually isn't — don't blindly symmetrize your anomaly signal.

## Worked Example
Full tutorial using a mock `EXOPLANETS` SQLite table (`_id, distance, g, orbital_period, avg_temp, date_added`):

1. **Freshness detector** — start from counting rows per day, then compute a lag-based gap:
```sql
WITH UPDATES AS (
  SELECT DATE_ADDED, COUNT(*) AS ROWS_ADDED FROM EXOPLANETS GROUP BY DATE_ADDED
)
SELECT DATE_ADDED,
  JULIANDAY(DATE_ADDED) - JULIANDAY(LAG(DATE_ADDED) OVER (ORDER BY DATE_ADDED)) AS DAYS_SINCE_LAST_UPDATE
FROM UPDATES;
-- turn into a detector by adding a threshold:
-- ... WHERE DAYS_SINCE_LAST_UPDATE > 1;
```
Six outages surfaced (e.g. 2020-05-14 was 8 days stale). Raising the threshold from 1→3→7 days trades recall for precision — fewer false alarms, but smaller outages go undetected.

2. **Distribution detector** — null-rate and zero-rate queries per field per day, then a rolling-average filter to reduce noise:
```sql
WITH NULL_RATES AS (
  SELECT DATE_ADDED,
    CAST(SUM(CASE WHEN AVG_TEMP IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS AVG_TEMP_NULL_RATE
  FROM EXOPLANETS GROUP BY DATE_ADDED
),
NULL_WITH_AVG AS (
  SELECT *, AVG(AVG_TEMP_NULL_RATE) OVER (ORDER BY DATE_ADDED
    ROWS BETWEEN 14 PRECEDING AND CURRENT ROW) AS TWO_WEEK_ROLLING_AVG
  FROM NULL_RATES
)
SELECT * FROM NULL_WITH_AVG WHERE AVG_TEMP_NULL_RATE - TWO_WEEK_ROLLING_AVG > 0.3;
```

3. **Schema + lineage detector** — an `EXOPLANETS_COLUMNS` table versions the schema over time; comparing `LAG(COLUMNS)` finds the exact date two new fields (`eccentricity`, `atmosphere`) were added. Cross-referencing that date against a downstream `HABITABLES` table's `zero_rate` spike shows the schema change is the root cause of a distribution anomaly two tables downstream — demonstrating why lineage context turns "the average dropped" into an actionable root cause.

4. **Precision/recall tuning** — with 6 labeled freshness outages (2 "genuine," per the exercise), setting the threshold at 3 days yields precision 0.75/recall 0.75/F1 0.75; raising to 5 days yields precision 1.0/recall 0.5/F1 0.667. The sweet spot in this example is 4 days.

## Code Examples
```sql
-- Precision/recall bookkeeping for a threshold-based detector
-- TP: predicted anomalous AND genuinely anomalous
-- FP: predicted anomalous BUT not genuinely anomalous
-- FN: not predicted BUT genuinely anomalous
-- Precision = TP / (TP + FP); Recall = TP / (TP + FN)
-- F_beta = (1+beta^2) * (Precision*Recall) / (beta^2*Precision + Recall)
```

## Reference Tables
| Outcome | Predicted anomalous | Predicted not anomalous |
|---|---|---|
| Actually anomalous | True Positive | False Negative |
| Actually fine | False Positive | True Negative |

| Detector type | Personality | Failure mode |
|---|---|---|
| Boy who cried wolf | Alerts on everything | High recall, terrible precision (alert fatigue) |
| Sleeping guard dog | Never alerts | High precision, terrible recall (misses real incidents) |

| ML framework | Use case |
|---|---|
| Facebook Prophet | Seasonality-aware forecasting (daily/weekly/yearly) |
| TensorFlow / Keras | Autoencoder-based anomaly detection, general DL |
| PyTorch | Similar to TensorFlow, more academic adoption |
| scikit-learn | ARIMA, k-NN, isolation forest |
| MLflow | Experiment tracking / model registry / reproducibility |

## Key Takeaways
1. Build one detector per pillar (freshness, distribution, volume, schema, lineage) — they catch different failure classes and none substitutes for another.
2. A detector is only as good as its threshold; always reason explicitly in precision/recall/Fβ terms rather than "does it feel right."
3. Lineage is what turns anomaly detection from "something broke" into "here is the root cause" — pair detection with dependency graphs.
4. "Accuracy" is a misleading metric for rare-event detection; use precision, recall, and Fβ instead.
5. Rule-based thresholds are a legitimate, scalable starting point; autoregression (ARIMA), exponential smoothing (Holt-Winters), clustering (isolation forest/k-NN), and ensembles are the next rungs up when rules stop scaling.

## Connects To
- **Ch 2**: the SQL metadata-pulling patterns from Ch. 2 are the literal input to these detectors.
- **Ch 5**: freshness/volume/distribution/schema/lineage become the five pillars underpinning SLA/SLI/SLO design.
- **Ch 6**: root cause analysis formalizes the "look at lineage → code → data → operational environment → peers" sequence hinted at here.
- **Ch 7**: the lineage graph used informally here (EXOPLANETS → HABITABLES) is built out as a full field-level lineage system.
