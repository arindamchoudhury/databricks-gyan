# Ch 3 — Getting Started with the Databricks Data Intelligence Platform

> **Source:** Kaplan & Kara, *The Data Intelligence Platform For Dummies* (Wiley, 2nd Databricks Special Ed., © 2026) — Chapter 3, PDF pp. 29–38.
> **Added:** 2026-06-20
> **Tags:** platform-components, unity-catalog, lakeflow, spark-declarative-pipelines, lakebase, databricks-sql, ai-bi, databricks-apps, B1
> **Type:** book

> *The component tour — the one chapter with real product names. How Databricks delivers data intelligence (learning your business semantics), then a bottom-up walk through the platform stack: Open Data Lake, Unity Catalog, Agent Bricks, Lakeflow, Databricks SQL, Lakebase, AI/BI, Databricks Apps, data collaboration, and Databricks Assistant.*

> 📌 **This is the chapter to keep.** It's the current (2026) Databricks component map. One rename to apply: the book says **Delta Sharing** → use **OpenSharing**. The book also slips and writes "DLT pipelines"; the current name is **Lakeflow Spark Declarative Pipelines**.

---

## 1. Delivering data intelligence with Databricks

- Combines GenAI + lakehouse into one end-to-end platform that **continually learns the nuances of your business and data**.
- Intelligence is sourced from signals across the estate: **centralized business semantics, table/column descriptions, dashboards, notebooks, pipelines, usage, and human feedback**. Because the platform is unified end-to-end, it sees how data is actually used.
- The pitch vs. generic LLMs: purpose-built agents on *your* data beat internet-trained LLMs that don't know that "did a customer churn?" or "when does our fiscal year start?" vary by company.

### Privacy & governance
- Unified governance/security spans **MLOps + LLMOps** and AI development; keeps IP private.
- **MLOps** = ML-engineering discipline of taking models to production and monitoring them as data changes.

---

## 2. The platform stack (Figure 3-1, bottom → top)

> The booklet walks the architecture diagram from the storage floor upward. This is the most useful single artifact in the book — a labeled component inventory.

### Open Data Lake
- Data stays under your control, open formats, no lock-in. Stores structured/semi/unstructured, batch or streaming.
- Two open table formats: **Delta Lake** and **Apache Iceberg** — pick either, no repeated copying or format lock-in.
- AI auto-optimizes storage (no manual table/volume tuning as data changes).

### Unity Catalog (UC)
- **Unified governance layer for data *and* AI** — governs structured + unstructured data, ML models, notebooks, dashboards, files, on any cloud.
- Centralized catalog of **business semantics and metrics**; auto-generates descriptions/tags (optionally human-guided), making the platform aware of jargon, acronyms, rules, metrics.
- Powers **contextual search** (not keyword) — e.g. disambiguating `sales_NE` = Nebraska vs. New England vs. Netherlands; finding "last week's" table.

### Agent Bricks
- Environment to **build, productionize, monitor, evaluate** composable agents. Ships pre-built agents + lets you create custom ones starting from the business problem.
- Does orchestration behind the scenes (data pulling, judging) while maintaining governance and balancing cost vs. quality. → full detail in Ch 4.

### Lakeflow + Spark Declarative Pipelines
- **Databricks Lakeflow** = the declarative ETL framework for batch + streaming, three components:
  - **Lakeflow Connect** — scalable data ingestion (ETL/ELT).
  - **Spark Declarative Pipelines (SDP)** — simplified, reliable transformation. *(Book also calls these "DLT pipelines" — legacy name; current = Lakeflow Spark Declarative Pipelines.)*
  - **Lakeflow Jobs** — orchestrate/schedule pipelines as workflows with monitoring/observability.
- Define transformations; the platform auto-manages task orchestration, cluster management, monitoring, data quality, error handling — on **serverless compute** that starts nearly instantly.

> 💭 (mine): the booklet conflates "Databricks Workflows" and "Lakeflow Jobs" in the same breath — they're the orchestration layer. Current branding is **Lakeflow Jobs**.

### Databricks SQL (DBSQL)
- A leading **serverless data warehouse**. Runs ETL + BI with UC governance, open-source foundation, AI-built, advanced data-access acceleration (Photon below).

### Photon
- Next-gen **vectorized query engine** — very fast queries at low cost; lets Databricks handle the largest workloads. (Mentioned here as the perf enhancement under DBSQL.)

### Lakebase
- A **new category of OLTP database for the agentic era**:
  - **Open-source Postgres foundation** — avoids lock-in, full community-extension support.
  - **Compute/storage separation** — very low latency, high QPS (ms/query), production SLAs.
  - **Built for AI** — instances launch in <1 s, pay only for compute used.
- Contrast: legacy DBs are 40+ years old, sticky/lock-in, expensive, admin-heavy, on-prem, not built for AI.

### AI/BI
- **AI/BI Dashboards** — anyone self-serves visualizations; NL to create datasets/reports, NL or point-and-click to build visuals.
- **AI/BI Genie** — a chatbot to "talk with your data"; translates NL questions → analytical SQL, responds with tables/visuals, adheres to UC governance, learns from feedback. No code; near-instant Genie Space.

### Databricks Apps
- Build/deploy secure data + AI apps **directly on Databricks** — no separate infra; bring the app to the data. Governed via UC, open ecosystem. → more in Ch 4.

### Data collaboration
- **Databricks Marketplace** — open third-party marketplace for data, analytics, AI.
- **Clean Rooms** — secure, privacy-centric collaboration with partners on any cloud.
- ~~**Delta Sharing**~~ **OpenSharing** — the widely-adopted **open protocol** for secure live data/AI sharing across platforms/clouds; powers Marketplace + Clean Rooms. ⚠️ Book says "Delta Sharing"; renamed **OpenSharing** (June 2026). "Databricks-to-Databricks" remains the term for the DB↔DB sub-protocol.
- **Lakehouse Federation** — query external sources (Snowflake, MySQL, Oracle, Hive) in place via UC, zero copy; expose data to Salesforce, Palantir, SAP.
- UC secures/governs all of the above.

---

## 3. Databricks Assistant

- Context-aware AI assistant **native in notebooks, SQL editor, file editor**.
- Generate SQL from English, document complex code, debug. Uses **UC metadata** (tables, columns, descriptions, popular assets) for personalized responses.

---

## Summary

The platform stack, floor to ceiling: **Open Data Lake** (Delta/Iceberg) → **Unity Catalog** (governance + semantics) → compute/dev surfaces (**Lakeflow/SDP**, **Databricks SQL**+**Photon**, **Lakebase** OLTP) → intelligence surfaces (**Agent Bricks**, **AI/BI Genie/Dashboards**, **Databricks Apps**, **Assistant**) → sharing (**Marketplace, Clean Rooms, OpenSharing, Lakehouse Federation**). UC is the through-line tying governance across all of it.

## References

- Source: PDF pp. 29–38. Figure 3-1 (platform architecture) not reproduced.
- Related: [[ch04-building-ai-applications]] (Agent Bricks deep dive), [[ch01-getting-started-with-databricks]] (DCDE-SG architecture), personal book [[ch01-databricks-platform-workspace]].
