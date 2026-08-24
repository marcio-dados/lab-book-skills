# Chapter 5: Driving Data Products with Data Contracts

## Core Idea
Trust — built through relationship, demonstrated expertise, and consistency — is the actual value Data Mesh delivers, and the data contract (following the Open Data Contract Standard, ODCS) plus Data QoS (Data Quality + Service-Level Agreements) are the concrete mechanisms that make that trust auditable and enforceable.

## Frameworks Introduced
- **The Three Elements of Trust** (via Harvard Business Review): positive relationship, expertise, consistency.
  - When to use: whenever justifying *why* a data contract matters to a non-technical stakeholder — trust, not schema enforcement, is the business case.
  - How: relationship = ongoing engagement with consumers; expertise = the contract itself as demonstrated authority; consistency = data quality results + service-level indicators (SLIs) delivered reliably over time.
- **Open Data Contract Standard (ODCS)**: a YAML-based contract format (Bitol project, Linux Foundation AI & Data) covering 8 categories: Fundamentals & demographics, Dataset & schema, Data quality, Pricing, Stakeholders, Roles, Service-level agreement, Custom properties.
  - When to use: as the default schema whenever standardizing data contracts across an organization instead of inventing a bespoke format.
  - How: one contract per dataset/version pair; a data product can have multiple contracts (one per dataset+version combination); use YAML for human+machine readability and Git-based traceability.
- **Data QoS (Data Quality of Service)**: DQ + SLA combined into a single, periodic-table-like classification of measurable elements, organized by group (Data at rest, Data in motion, Performance, Lifecycle, Behavior, Time) and by time/period axis.
  - When to use: whenever "data quality" alone feels insufficient — Data QoS adds the temporal/operational dimensions (retention, end-of-life, latency, time-to-repair) that pure DQ dimensions miss.
  - How: classify every measurable data attribute along the group axis and the time axis, then attach concrete thresholds via SLA/SLO.
- **Semantic Versioning for Data Contracts**: patch (bug fix / metadata / stakeholder change), minor (backward-compatible addition), major (breaking change).
  - When to use: every time a data contract or its underlying schema changes.
  - How: table-based rule — column addition = minor; column type/name change or removal = major; metadata/stakeholder update = patch (see Reference Table below).

## Key Concepts
- **Data contract**: a formal agreement between producer and consumer(s) covering schema, access/usage, quality, security/privacy, versioning, lineage, and error handling.
- **Data QoS**: the union of the seven EDM Council data-quality dimensions with an extensible set of service-level indicators.
- **Human lineage**: tracking the *people* (stakeholders/DPOs) responsible for a data product over time inside the contract itself, not just data lineage.
- **Tribal knowledge**: informal, oral, hard-to-scale knowledge that data contracts help surface and formalize via documentation + authoritative definitions.
- **Postel's Law (Robustness Principle)**: "Be conservative in what you do, be liberal in what you accept from others" — applied here to argue that strict contracts don't require uncompromising consumption.

## Mental Models
- Use the "buying a used car" analogy for every data contract conversation: schema = the car's features; SLA/NFR = fuel economy and pickup date; hard constraints (dealbreakers) = excess duplicate records or NULLs, exactly like excess NOx emissions.
- Think of Data QoS as Mendeleev's periodic table: each "element" (an SLI or DQ dimension) has a name, abbreviation, group, and sequential order — some elements are strictly chronological (general availability before end-of-support before end-of-life), others merely sequential in practice (accuracy checked before consistency, before uniqueness).

## Anti-patterns
- **Confusing data quality with trust**: data quality is necessary but explicitly called out as "not enough" — retention, end-of-life, and time-to-repair live outside DQ and must be captured via service levels.
- **Retrofitting contracts after building the product**: reiterates Ch 4's warning — this chapter treats the contract as foundational, introduced explicitly because delaying it is expensive.
- **Uncompromising strict consumption of a strict contract**: contradicts Postel's Law — a rigorous producer-side contract does not require zero tolerance on the consumer side.
- **Conflating currency/localization formats with a consistency bug**: the author's own date-format example (05/10/1971 read as May 10 in the US vs. October 5 in Europe) — a reminder that consistency issues are about representation drift across stores, not about "being wrong."

## Code Examples
```yaml
# Conformity rule: enforce a minimum value on a numeric identifier
- table: Air_Quality
  description: Air quality of the city of New York
  dataGranularity: Raw records
  columns:
  - column: UniqueID
    isPrimary: true
    businessName: Unique identifier
    logicalType: number
    physicalType: int
    quality:
    - templateName: RangeCheck
      toolName: ClimateQuantumDataQualityPackage
      description: 'This column should not contain values under 100000'
      dimension: conformity
      severity: error
      businessImpact: operational
      customProperties:
        - property: min
          value: 100000
```
- **What it demonstrates**: how a single data-quality dimension (conformity) is expressed as a declarative rule inside an ODCS-style contract, tied to a specific tool (`toolName`) and business-impact classification.

```yaml
# Service levels apply to the whole data product, not per-table
slaDefaultColumn: StartDate
slaProperties:
- property: endOfSupport
  value: 2030-01-01T00:00:00-04:00
- property: retention
  value: 100
  unit: y
- property: generalAvailability
  value: 2014-10-23T00:00:00-04:00
- property: latency
  value: -1
  unit: As needed
```
- **What it demonstrates**: SLIs are expressed as extensible property/value pairs, not a fixed schema — new indicators can be added without a contract format version bump.

## Reference Tables
### Severity of Changes (Table 5-1, condensed)
| Artifact | Patch | Minor | Major |
|---|---|---|---|
| Table | logic change to existing column | adding a new column | column type/name change; column removal |
| API | bug fix (non-breaking) | new optional field/param; required→optional | changing request/response format or data type; removing a resource; new *required* field |
| Data contract | metadata/description/stakeholder updates | new optional/defaulted key; custom property | changing a key's type or name; removing a key |

### The Seven Data Quality Dimensions (EDM Council)
| Dimension | Abbrev. | Question it answers |
|---|---|---|
| Accuracy | Ac | Does the value match the authoritative source? |
| Completeness | Cp | Is a required value populated (not null)? |
| Conformity | Cf | Does the value match required format/standard? |
| Consistency | Cs | Do values/formats/definitions match across stores? |
| Coverage | Cv | Are all expected records present? |
| Timeliness | Tm | Does data reflect current conditions? |
| Uniqueness | Uq | Is each record/attribute one-of-a-kind? |

### Key Service-Level Indicators
| Indicator | Abbrev. | Measures |
|---|---|---|
| Availability | Av | Is the source accessible? |
| Throughput | Th | Access speed (bytes/records per unit time) |
| Error rate | Er | Frequency/tolerance of errors |
| General availability | Ga | Date the product is publicly ready |
| End of support | Es | Date after which no fixes are offered |
| End of life | El | Date after which the product/data is gone entirely |
| Retention | Re | How long records are kept |
| Frequency of update | Fy | Update cadence |
| Latency | Ly | Time between data production and availability |
| Time to detect | Td | Speed of problem detection |
| Time to notify | Tn | Speed of notifying users after detection |
| Time to repair | Tr | Speed of fixing once detected |

## Worked Example
The chapter's "human lineage" scenario: a data contract tracks Data Product Owners as stakeholders with `dateIn`/`dateOut`/`replacedByUsername` fields, so that when a DPO goes on leave (or the chain of successors is several links deep — Clint → John → Calamity → Billy), anyone can trace back through the contract itself to find who last held accountability, without relying on institutional memory. This is "human lineage" as a first-class, versioned artifact inside the same contract that already tracks schema and quality — solving the tribal-knowledge problem structurally rather than procedurally.

## Key Takeaways
1. Trust, not data quality, is the actual deliverable of a Data Mesh — the contract is the vehicle, not the goal.
2. Adopt an existing standard (ODCS/Bitol) rather than inventing your own YAML contract format — it buys ecosystem tooling and shared vocabulary for free.
3. Data QoS = 7 EDM Council quality dimensions + an open-ended set of service-level indicators, organized like a periodic table (group axis + time axis) — this is broader than "data quality" alone.
4. Use semantic versioning (patch/minor/major) for contract changes, and use the severity table to classify any given change before deciding how to version it.
5. Track human lineage (stakeholder succession) inside the contract, not just data lineage — it directly solves the tribal-knowledge problem.
6. Postel's Law applies to contract consumption: strict on what you produce, liberal on what you accept.

## Connects To
- **Ch 2**: the FAIR/enterprise-grade data product criteria are made concrete and enforceable through the contract mechanisms in this chapter.
- **Ch 3**: uses the Climate Quantum NYC Air Quality dataset as the running example for every contract snippet.
- **Ch 4**: previewed data contracts as an architectural concern; this chapter is the deep dive it promised.
