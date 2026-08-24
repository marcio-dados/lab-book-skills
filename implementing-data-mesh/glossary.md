# Glossary

**ANSI/ASA governance analogy** — the recurring model for federated governance: a central body sets standards; data product owners self-certify against them, like manufacturers certifying products against ANSI standards. (Ch 1, Ch 4, Ch 15)

**Artifact** — any object a data product owner makes available to consumers beyond raw data: programs, AI/ML models, queries, streams, bundles. (Ch 2, Ch 4)

**Certification (data product)** — a data product owner's public declaration that their product meets governance standards, queryable via governance interfaces. (Ch 1, Ch 4, Ch 15)

**Climate Quantum Inc.** — the book's fictional case-study firm applying Data Mesh to climate data. (Ch 3)

**Composable Component (GenAI)** — a reusable GenAI capability (summarization/tagging, taxonomy/knowledge graphs, code/document generation, natural language search) assembled into higher-value use cases. (Ch 9)

**Conway's Law** — an organization's systems mirror its communication/organizational structure; used to predict and design Data Mesh architecture fit. (Ch 15)

**Data as a Product** — one of Dehghani's four foundational Data Mesh principles: data is treated with product discipline (ownership, lifecycle, consumer focus), not as a system byproduct. (Ch 1)

**Data contract** — a formal agreement between producer and consumer(s) defining schema, access/usage rules, quality, security/privacy, versioning, lineage, and error handling. (Ch 4, Ch 5)

**Data Enabling team** — a short-term, consultative team that helps Data Product teams overcome specific obstacles without owning their work. (Ch 14)

**Data Mesh** — a decentralized data architecture treating data as a product, with domain-oriented ownership, self-serve infrastructure, and federated governance. (Ch 1)

**Data Mesh Console** — the CLI counterpart to the Marketplace, used for scripted/admin interaction with the mesh. (Ch 4)

**Data Mesh Fabric** — the shared infrastructure layer (compute/network/storage, interaction/communication services, data access services, DevSecOps, data platforms, collaboration services) supporting the mesh. (Ch 4)

**Data Mesh Marketplace** — the user-facing hub for finding, consuming, sharing, and trusting data products, with distinct UX for consumers, producers, owners, and admins. (Ch 4)

**Data Mesh Registry** — a DNS-like directory of data product summaries/tags for fast, low-friction discovery. (Ch 4)

**Data Platform team** — a team providing shared "X-as-a-Service" infrastructure/tooling to Data Product teams. (Ch 14)

**Data Product** — a self-contained, self-descriptive package oriented to a business purpose: data + tools + documentation + metadata. (Ch 2)

**Data Product Actors** — the five roles in a Data Mesh ecosystem: Data Product Owners, Data Producers, Data Consumers, Data Mesh Administrators, Data Governance Professionals. (Ch 4)

**Data Product Harness** — the consistent implementation layer exposing standardized interfaces (`/ingest`, `/consume`, `/discover`, `/observe`, `/control`) for a data product, and the integration point for contract/policy enforcement. (Ch 4)

**Data Product Owner (DPO)** — the accountable, empowered decision-maker for a data product's strategy, funding, and lifecycle. (Ch 2, Ch 4, Ch 14)

**Data Product team** — a self-contained, autonomous team responsible end-to-end for a specific data product's lifecycle. (Ch 14)

**Data QoS (Data Quality of Service)** — Data Quality (7 EDM Council dimensions) combined with Service-Level Agreements/Indicators, organized like a periodic table by group and time axis. (Ch 5)

**Decentralized Domain Ownership** — one of Dehghani's four foundational principles: responsibility for data is distributed to domain-specific teams. (Ch 1)

**Distributed organization** — a fully decentralized, self-governing organizational model (e.g., Apache Software Foundation); maps to a microservices data architecture. (Ch 15)

**Embedding** — a compact vector representation capturing the semantic essence of content, enabling similarity ("nearest neighbor") search. (Ch 9)

**FAIR (data products)** — Findable, Accessible, Interoperable, Reusable — a data-quality-of-usability framework. (Ch 2)

**Federated Computational Governance** — one of Dehghani's four foundational principles: governance responsibility distributed to domain owners, aligned with (not replaced by) enterprise policy. (Ch 1)

**Federated organization** — an organizational model with tiered governance and local autonomy bound by common policy (e.g., the EU); the natural fit for Data Mesh. (Ch 15)

**Human lineage** — tracking the people (stakeholders/DPOs) responsible for a data product over time, inside the contract itself. (Ch 5)

**LLM (Large Language Model)** — an AI system trained on massive text corpora to process/generate language; has a training cutoff and no access to private enterprise data by default. (Ch 9)

**Matrixed organization** — an organizational model with dual reporting lines (functional + project); maps naturally to a data lake architecture. (Ch 15)

**Nearest-neighbor search** — finding the vectors most semantically similar to a query vector, the core capability of a vector database. (Ch 9)

**ODCS (Open Data Contract Standard)** — the YAML-based data contract standard from the Bitol project (Linux Foundation AI & Data), covering 8 categories from fundamentals to custom properties. (Ch 5)

**Operating model** — the blueprint aligning people, process, and technology to deliver strategic goals; for Data Mesh, governs how data is managed, shared, and utilized. (Ch 15)

**Physical Risk data product** — Climate Quantum's flagship product, synthesizing temperature, precipitation, and sea-level products via AI/ML. (Ch 3, Ch 4)

**Postel's Law (Robustness Principle)** — "Be conservative in what you do, be liberal in what you accept" — applied to data-contract consumption. (Ch 5)

**Regionalization** — the Conway's-Law-driven tendency of a Data Mesh to fragment into regional ecosystems unless proactively counteracted. (Ch 15)

**Release Manager** — the Data Product team role responsible for release planning, versioning, and communicating changes. (Ch 14)

**Self-Serve Data Infrastructure** — one of Dehghani's four foundational principles: a framework letting domain teams manage their data independently. (Ch 1)

**Semantic versioning (data contracts)** — patch/minor/major classification of contract changes, based on backward compatibility impact. (Ch 5)

**Sponsor** — a senior executive who champions a data product, secures funding, and removes organizational obstacles. (Ch 2)

**Target state / roadmap** — the defined end-goal vision for a data product and the strategic plan to reach it. (Ch 2)

**Team Topologies** — Skelton & Pais's framework (stream-aligned, platform, enabling teams) adapted here as Data Product, Data Platform, and Data Enabling teams. (Ch 14)

**Tribal knowledge** — informal, oral, hard-to-scale organizational knowledge that data contracts help surface via documentation and human lineage. (Ch 5)

**Vector database** — a database of embeddings enabling efficient nearest-neighbor (semantic similarity) search. (Ch 9)
