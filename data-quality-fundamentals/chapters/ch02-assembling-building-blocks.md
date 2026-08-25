# Chapter 2: Assembling the Building Blocks of a Reliable Data System

## Core Idea
Reliable data quality starts with understanding the infrastructure primitives — operational vs. analytical data, warehouses vs. lakes, and the metadata (query logs, catalogs) each one exposes — because you can only measure and monitor what your storage layer makes visible.

## Frameworks Introduced
- **Operational vs. analytical data**: operational data runs the business (inventory snapshots, transactions); analytical data manages the business (churn, clickthrough rates). Same split as OLTP vs. OLAP (see *Designing Data-Intensive Applications*).
  - When to use: to decide where to invest in reliability tooling — this book focuses on analytical data.
  - How: operational data usually sits upstream and optimizes for low latency; analytical data sits downstream and optimizes for high throughput.
- **Throughput vs. latency trade-off**: for any system with fixed computational power, you cannot maximize both. High latency-optimization (transactional DBs) vs. high throughput-optimization (analytical DBs, e.g., Snowflake/Redshift) are different architectural bets.
  - When to use: when picking or justifying a database technology for a workload.
  - How: ask whether the workload needs single-record speed (optimize latency) or large-aggregation speed (optimize throughput) — you cannot cheaply do both.
- **Schema-on-write vs. schema-on-read**: warehouses enforce structure at ingestion (schema-on-write); lakes infer it at read time (schema-on-read).
  - When to use: schema-on-write for governed, BI-ready data; schema-on-read for flexible, exploratory/ML workloads.

## Key Concepts
- **Data warehouse**: structured (row-column), schema-on-write, e.g. Redshift, BigQuery, Snowflake — great for SQL analytics, poor for semi/unstructured data.
- **Data lake**: schema-on-read, stores structured/semi-structured/unstructured data at the file level — flexible but prone to "swampification."
- **Swampification**: a data lake accruing so much undocumented technical debt that only a few tacit-knowledge holders can navigate it.
- **Data lakehouse**: hybrid adding warehouse features (SQL, schema, ACID via Delta Lake/Hudi) on top of lake flexibility.
- **Data catalog**: an inventory of metadata (location, ownership, health) — traditionally manual/spreadsheet-based, increasingly automated.
- **Data discovery**: a more dynamic alternative to catalogs that surfaces the *current* state of data (not the "cataloged/ideal" state), inspired by data mesh.

## Anti-patterns
- **"Blind ETL"**: transforming lake data assuming a schema without verifying it — breaks silently on any upstream change.
- **Manual data cataloging via spreadsheet**: does not scale past a handful of tables; becomes stale immediately.
- **SQL-only warehouse workflows for ML**: forces movement of data out of the warehouse, which is exactly where volume/freshness/schema anomalies tend to appear.

## Code Examples
Four SQL steps to pull data quality metrics from Snowflake (generalizes to other warehouses):
```sql
-- Step 1: map inventory
SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, TABLE_OWNER, TABLE_TYPE,
       IS_TRANSIENT, RETENTION_TIME, AUTO_CLUSTERING_ON, COMMENT
FROM "ANALYTICS".information_schema.tables
WHERE table_schema NOT IN ('INFORMATION_SCHEMA')
  AND TABLE_TYPE NOT IN ('VIEW', 'EXTERNAL TABLE')
ORDER BY TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME;

-- Step 2: freshness & volume
SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, ROW_COUNT, BYTES,
       CONVERT_TIMEZONE('UTC', CREATED) AS CREATED,
       CONVERT_TIMEZONE('UTC', LAST_ALTERED) AS LAST_ALTERED
FROM "ANALYTICS".information_schema.tables
WHERE table_schema NOT IN ('INFORMATION_SCHEMA')
  AND TABLE_TYPE NOT IN ('VIEW', 'EXTERNAL TABLE');

-- Step 3: query history (who/what/when)
SELECT QUERY_TEXT, DATABASE_NAME, SCHEMA_NAME, QUERY_TYPE, USER_NAME,
       ROLE_NAME, EXECUTION_STATUS, START_TIME, END_TIME, TOTAL_ELAPSED_TIME,
       BYTES_SCANNED, ROWS_PRODUCED
FROM snowflake.account_usage.query_history
WHERE QUERY_TYPE NOT IN ('DESCRIBE', 'SHOW') AND ERROR_CODE IS NULL
ORDER BY start_time DESC;

-- Step 4: health check (completeness, distinctness, distribution)
SELECT
  COUNT(account_id) / CAST(COUNT(*) AS NUMERIC) AS account_id___completeness,
  COUNT(DISTINCT account_id) / CAST(COUNT(*) AS NUMERIC) AS account_id___approx_distinctness,
  SUM(IFF(num_of_users = 0, 1, 0)) / CAST(COUNT(*) AS NUMERIC) AS num_of_users___zero_rate
FROM analytics.prod.client_hub
GROUP BY bucket_start, bucket_end;
```
- **What it demonstrates**: the four-step metadata-pull pattern (inventory → freshness/volume → query logs → per-field health check) that recurs throughout the book as the basis for anomaly detectors (Ch. 4).

## Reference Tables
| Data Warehouse | Notes |
|---|---|
| Amazon Redshift | First popular cloud DW, columnar, AWS-native |
| Google BigQuery | Serverless, GCP-native, scales by usage |
| Snowflake | Cloud-agnostic (AWS/GCP/Azure), separate compute/storage billing |

| Warehouse drawback | Why it matters for data quality |
|---|---|
| Limited flexibility | Semi-structured data (JSON) often unsupported, bad data slips through |
| SQL-only | ML workflows must export data via SQL — a common breakage point |
| Frictional workflows | Fast-iterating teams find schema-on-write too rigid |

## Worked Example
The chapter walks a "basic, rough-and-dirty data catalog" (Table 2-1): a spreadsheet with columns `Table name | Dashboard/report | Last updated | Owner | Notes`, e.g. `RYANS_DATA.csv | Marketing Model (Looker) | March 3, 2022 | Ryan Kearns | For demand generation models`. It then shows parsing a SQL query with ANTLR into a syntax tree (`dmlStatement → selectStatement → ...`) so the parsed structure — not just raw SQL text — can be indexed into a catalog automatically. This is the conceptual seed for the field-level lineage parser built in Ch. 7.

## Key Takeaways
1. Know whether you're managing operational or analytical data — the reliability playbook differs (this book is about analytical data).
2. Warehouses and lakes fail in different ways: warehouses break on rigid schema/SQL-only constraints; lakes break on ungoverned "blind ETL" and swampification.
3. Query logs (who, what, when, how often) are an underused, already-available source of data quality metadata — mine them before building new tooling.
4. Manual data catalogs don't scale; automated parsing (SQL parsers, ANTLR) is the path to catalogs that stay current.

## Connects To
- **Ch 3**: takes the warehouse/lake building blocks here and shows how data is collected, cleaned, transformed, and tested as it flows through them.
- **Ch 4**: the metadata pulled here (freshness, volume, query logs) becomes the raw material for anomaly detectors.
- **Ch 7**: the ANTLR SQL-parsing example here is the starting point for full field-level lineage.
