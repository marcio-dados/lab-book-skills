# Chapter 1: Why Data Quality Deserves Attention—Now

## Core Idea
"Data downtime" — periods where data is missing, inaccurate, or otherwise erroneous — is one of the biggest hidden costs in modern companies, and it is a direct analog of software downtime in the SRE/DevOps world.

## Frameworks Introduced
- **Data downtime**: periods of time where data is missing, inaccurate, or otherwise erroneous, manifesting as stale dashboards, inaccurate reports, and poor decision making.
  - When to use: as the master metric for "is my data healthy" — replaces vague complaints ("the data feels off") with a measurable state.
  - How: track it the same way SREs track application uptime/downtime, aiming toward a "five nines"-style reliability target for critical data assets.
- **DataOps**: the process of improving the reliability and performance of data through automation, borrowed directly from DevOps.
  - When to use: whenever a data team is scaling past ad hoc, manual data hygiene.
  - How: apply CI/CD-style discipline, monitoring, and automation to data pipelines instead of treating each pipeline as a one-off script.

## Key Concepts
- **Data downtime**: any period data is wrong, missing, or late.
- **Operational vs. analytical framing** (previewed here, detailed in Ch. 2): the split between data that runs the business vs. data that explains the business.
- **Data mesh**: a domain-oriented, self-serve data architecture (Zhamak Dehghani) — introduced here as a trend, built out in Ch. 9.
- **Data lakehouse**: a hybrid combining warehouse structure with lake flexibility.
- **DataOps**: DevOps practices applied to data pipelines.
- **"No data is better than bad data"**: a common but often impractical maxim — bad data is usually unavoidable at scale, so the real goal is detecting and bounding it, not eliminating it.

## Mental Models
- Think of data quality the way SRE thinks of application uptime: not a binary "works/broken" state, but a continuously measured SLA.
- Treat "throughput vs. latency" tension (detailed in Ch. 2) as the same trade-off data infra faces that transactional vs. analytical systems have always faced.

## Anti-patterns
- **Waiting for a stakeholder to report broken data**: by the time your CEO notices a wrong number in a board deck, the cost (trust, decisions made on bad data) is already sunk.
- **Treating data quality as a "nice to have"**: teams that don't invest lose ~40% of their time firefighting instead of building.

## Key Takeaways
1. Data downtime is not rare — it is a normal, recurring cost of running any data-driven company, and it should be measured, not just complained about.
2. The rise of the cloud, more data sources, more complex pipelines, more specialized teams, and decentralized data ownership are the five structural forces driving *more* data downtime, not less, as companies mature.
3. Treating data reliability with the same rigor as software reliability (via DataOps, data mesh, and observability, covered in later chapters) is the strategic response, not a one-off fix.

## Connects To
- **Ch 2**: operational vs. analytical data, and the technology building blocks that generate the data quality metrics referenced here.
- **Ch 5**: SLAs/SLIs/SLOs formalize the "uptime" analogy introduced in this chapter.
- **Ch 9**: the data mesh concept introduced here is explored in full, including a scoring rubric to decide if you need one.
