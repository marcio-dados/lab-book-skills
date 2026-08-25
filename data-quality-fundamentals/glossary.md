# Glossary — Data Quality Fundamentals

**Analytical data** — data used to drive decisions (churn, clickthrough rate); contrast with operational data. (Ch 2)

**Anomaly detection** — identifying observations that deviate from historical norms across the five pillars of data observability. (Ch 4)

**Blameless postmortem** — a post-incident review that treats the system, not the individual, as the point of failure. (Ch 6)

**Blast radius** — the extent of downstream impact when a data asset breaks. (Ch 8)

**Central Limit Theorem** — statistical basis for Gaussian z-score anomaly detection; breaks down when observations are correlated (common in business data). (Ch 4)

**Circuit breaker** — a pattern that halts a pipeline when data fails a quality threshold, preventing bad data from propagating. (Ch 3)

**Data catalog** — an inventory of metadata giving visibility into data location, ownership, and health. (Ch 2)

**Data certification** — approving a data asset for org-wide use after it meets agreed SLAs for quality, ownership, and communication. (Ch 8)

**Data discovery** — a dynamic, automated alternative to data catalogs that reflects the *current* (not "ideal/cataloged") state of data, native to distributed/mesh architectures. (Ch 2, Ch 9)

**Data downtime** — periods where data is missing, inaccurate, or otherwise erroneous. (Ch 1)

**Data Downtime Total (DDT)** — `N × (TTD + TTR)`; the master cost equation for data unreliability. (Ch 10)

**Data lake** — schema-on-read storage for structured/semi-structured/unstructured data at the file level. (Ch 2)

**Data lakehouse** — hybrid architecture adding warehouse features (SQL, schema, ACID) to lake flexibility. (Ch 2)

**Data literacy** — the ability to read, write, and communicate about data across an organization, not just within the data team. (Ch 8)

**Data mesh** — a domain-oriented, self-serve data architecture with federated governance (Zhamak Dehghani). (Ch 1, Ch 9)

**Data warehouse** — schema-on-write, structured storage optimized for SQL analytics (e.g., Snowflake, Redshift, BigQuery). (Ch 2)

**DataOps** — DevOps practices (automation, monitoring, CI/CD discipline) applied to data pipelines. (Ch 1)

**Entrypoint** — the most upstream point where external data enters a pipeline (logs, API responses, sensor data). (Ch 3)

**Five pillars of data observability** — freshness, distribution, volume, schema, lineage. (Ch 4, Ch 5)

**Five Whys** — Amazon's iterative root-cause-analysis technique. (Ch 6)

**Fβ-score** — weighted harmonic mean of precision and recall; β>1 weighs recall more, β<1 weighs precision more. (Ch 4)

**Incident commander** — the role responsible for coordinating, communicating, and assessing severity during a data incident. (Ch 6)

**Known unknowns / unknown unknowns** — predictable issues testing can catch vs. issues no test anticipated, requiring monitoring instead. (Ch 4)

**Lineage (field-level)** — a map of exactly which upstream columns produce which downstream columns, enabling real root cause and impact analysis. (Ch 7)

**Phantom data** — data nobody actually uses anymore, wastefully investigated during incident triage. (Ch 6)

**Precision / Recall** — Precision = TP/(TP+FP) (how often an alert is right); Recall = TP/(TP+FN) (how many real anomalies are caught). (Ch 4)

**RACI matrix** — Responsible/Accountable/Consulted/Informed framework for assigning data quality ownership. (Ch 8)

**Runbook / playbook** — runbooks explain how to use a service; playbooks give step-by-step incident-handling processes. (Ch 6)

**Schema-on-read / schema-on-write** — lakes infer structure at read time; warehouses enforce it at ingestion. (Ch 2)

**Semantic ambiguity** — a field whose *meaning* is understood differently across teams (worse than syntactic ambiguity). (Ch 3)

**Service-Level Agreement / Indicator / Objective (SLA/SLI/SLO)** — the promise, the measured number, and the target value for data reliability. (Ch 5)

**Swampification** — a data lake accruing so much undocumented technical debt that only tacit-knowledge holders can navigate it. (Ch 2)

**Syntactic ambiguity** — the same metric appearing under different field names/types. (Ch 3)

**Time to Detection (TTD) / Time to Resolution (TTR)** — how long until an issue is noticed, and how long from alert to fix. (Ch 5)

**Type coercion** — automatic/implicit conversion between data types, a common silent source of bugs. (Ch 3)
