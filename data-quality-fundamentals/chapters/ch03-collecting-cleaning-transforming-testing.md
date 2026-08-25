# Chapter 3: Collecting, Cleaning, Transforming, and Testing Data

## Core Idea
Data quality has to be actively managed at four distinct stages — collection, cleaning, transformation, and testing — and each stage has its own failure modes, tools, and best practices; treating them as one undifferentiated "ETL blob" is why pipelines break silently.

## Frameworks Introduced
- **Entrypoint taxonomy**: the three main raw data source types — application logs, API responses, sensor data — each with distinct structure, purpose, and failure modes.
  - When to use: when deciding what to validate/monitor for a new data source, start by classifying it into one of these three.
  - How: logs → check structure/timestamps/log levels; API responses → check response codes and structure; sensors → check for noise and silent failure (sensors don't emit "ERROR" logs, they just emit garbage).
- **Circuit breaker pattern**: pipelines stop running when data doesn't meet quality thresholds, borrowed from CI/CD.
  - When to use: to prevent bad data from silently propagating downstream when upstream data fails integrity checks.
  - How: two states — circuit closed (data flows) / circuit open (data blocked) — implemented via Airflow's `catchup=False`, `LatestOnlyOperator`, or custom Python checks.
- **ETL vs. ELT**: ETL transforms in a staging area before loading (safer, slower); ELT loads raw data then transforms in the warehouse (faster, riskier without testing).

## Key Concepts
- **Entrypoint**: the most upstream point where external data enters your pipeline (analogous to Docker's `ENTRYPOINT` or a program's `main`).
- **Type coercion**: automatic/implicit conversion between data types (e.g., float 4.99 → int 4, silently truncating) — a common source of "sinister" bugs.
- **Syntactic ambiguity**: same metric under different field names/types (`clickthrough_annual` vs `clickthrough_rate_yr`).
- **Semantic ambiguity**: same field, different understood meaning across teams (worse than syntactic — causes wrong dashboards, not just friction).
- **SLA (Service-Level Agreement)**: the maximum time a task/pipeline should take before it's flagged.

## Mental Models
- Treat data cleaning as removing "inaccurate or unrepresentative data," not as a one-size list — outlier removal, normalization, reconstruction (interpolation), UTC time-zone conversion, and type coercion are the five recurring moves.
- Batch vs. stream is a data-quality trade-off, not just a latency one: batch has higher data quality margin (more time to validate); streaming trades quality margin for freshness.

## Anti-patterns
- **Test fatigue**: adding tests without clear rationale leads engineers to delete them just to unblock CI — worse than no tests, because it signals false confidence.
- **dbt tests as the only line of defense**: dbt tests catch "known unknowns" (~20% of issues per the authors' interviews) — they cannot catch unknown unknowns (Ch. 4's job).
- **Ignoring time zones**: not normalizing to UTC at collection is a top source of silent bugs (the authors call it doing this "like some kind of maniac").

## Code Examples
```sql
-- dbt singular test: fail if any refund makes total go negative
select order_id, sum(amount) as total_amount
from {{ ref('fct_payments') }}
group by 1
having not(total_amount >= 0)

-- dbt generic test: templated NULL check
{% test not_null(model, column_name) %}
  select * from {{ model }} where {{ column_name }} is null
{% endtest %}
```
```python
# Great Expectations: range check
expect_column_values_to_be_between(
    column="zip_code", min_value=1, max_value=99999
)
```
```scala
// Deequ (Scala): declarative unit tests on a Spark DataFrame
val verificationResult = VerificationSuite()
  .onData(data)
  .addCheck(
    Check(CheckLevel.Error, "unit testing my data")
      .hasSize(_ == 5)
      .isComplete("id")
      .isUnique("id")
      .isContainedIn("priority", Array("high", "low"))
      .isNonNegative("numViews"))
  .run()
```
```python
# Airflow SLA miss callback + circuit-breaker-adjacent SQL check operator
@task(sla=datetime.timedelta(seconds=10))
def sleep_20():
    time.sleep(20)

SQLCheckOperator(
    task_id="orange_carddata_row_quality_check",
    sql="row_quality_blue_bankdata_check.sql",
    params={"dropoff_datetime": "2021-01-01"},
)
```
- **What it demonstrates**: the same "assert this condition, fail if violated" pattern implemented across four different testing ecosystems (dbt/SQL, Great Expectations/Python, Deequ/Scala, Airflow/SQLCheckOperator) — pick based on your stack's dominant language, not on features alone.

## Reference Tables
| Tool | Language | Best for | Key limitation |
|---|---|---|---|
| dbt tests | SQL | Teams already modeling in dbt | Manual upkeep, limited to per-model unit/integration blur |
| Great Expectations | Python | Data science / Python-heavy teams | Separate from transformation/orchestration tooling |
| Deequ / PyDeequ | Scala (Python wrapper) | AWS/Spark-heavy stacks, built-in anomaly detection | Scala learning curve, weak on integration testing |

| Data quality test type | Answers |
|---|---|
| Null values | Are any values unknown? |
| Volume | Did I get any data at all / too much / too little? |
| Distribution | Are values within expected ranges? |
| Uniqueness | Are values duplicated? |
| Known invariants | Do two related fields hold an expected relationship (e.g., profit = revenue − cost)? |

## Worked Example
The chapter builds up an Airflow circuit breaker step by step: start from an `sla_miss_callback` that receives `dag`, `task_list`, `blocking_task_list`, `slas`, `blocking_tis`; wire it into a DAG decorated with `sla_miss_callback=sla_callback`; then layer in a `SQLCheckOperator` that runs a query returning a single boolean row — if any value is `False`, the pipeline halts before propagating bad data downstream. This progression (SLA alert → SQL assertion → hard stop) is the template for building your own circuit breaker without buying a platform.

## Key Takeaways
1. Split your mental model of the pipeline into four stages (collect, clean, transform, test) — each has different tools and different failure signatures.
2. Testing catches ~20% of data quality issues (known unknowns); the rest require monitoring/anomaly detection (Ch. 4) — don't over-invest in tests expecting full coverage.
3. Type coercion and time-zone handling are unglamorous but are disproportionate sources of silent, hard-to-debug bugs.
4. Circuit breakers (stop the pipeline on bad data) are cheap to implement in Airflow and prevent cascading damage — reserve them for high-severity incidents only.

## Connects To
- **Ch 2**: builds directly on the warehouse/lake distinction — ETL vs. ELT risk profiles differ by storage layer.
- **Ch 4**: testing (known unknowns) is explicitly positioned as insufficient; anomaly detection covers what testing misses.
- **Ch 6**: circuit breakers and root cause analysis reappear as part of the full incident management lifecycle.
