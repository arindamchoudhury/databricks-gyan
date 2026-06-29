# Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics

> **Source:** [Armbrust, Ghodsi, Xin, Zaharia — CIDR 2021 (paper 17)](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf)
> **Added:** 2026-06-21
> **Source updated:** 2021-01 (CIDR '21, Jan 11–15, Online)
> **Tags:** lakehouse, architecture, data-warehouse, data-lake, delta-lake, metadata-layer, parquet, tpc-ds, foundations, research-paper, B1
> **Type:** paper
> **Authors:** Michael Armbrust (Databricks), Ali Ghodsi (Databricks / UC Berkeley), Reynold Xin (Databricks), Matei Zaharia (Databricks / Stanford)

## Summary

The peer-reviewed paper that lays out the **Lakehouse** thesis: the classic data-warehouse architecture will wane and be replaced by a system built on **open, direct-access formats** (Parquet/ORC), with **first-class ML/data-science support** and **state-of-the-art SQL performance**. It traces three generations of data platforms (warehouse → two-tier lake+warehouse → lakehouse), names four concrete problems with the dominant two-tier model (reliability, staleness, limited advanced-analytics support, total cost of ownership), and proposes a concrete design centered on a **transactional metadata layer** (Delta Lake / Iceberg) over object storage, plus **caching, auxiliary data structures, and data-layout optimizations** for performance and **declarative DataFrame APIs** for ML. It backs the feasibility claim with **TPC-DS** results where the Databricks **Delta Engine** beats four cloud warehouses on both time and cost. This is the academic, mechanism-level companion to the [[what-is-a-lakehouse]] blog post.

## Key points

- **Three platform generations:**
    1. **1st gen — data warehouses**: schema-on-write, coupled compute+storage (on-prem appliances), great for structured BI but couldn't hold unstructured data or scale cost-effectively.
    2. **2nd gen — two-tier lake + warehouse**: offload raw data to a cheap **data lake** (HDFS, then S3/ADLS/GCS) in open formats (schema-on-read), then ETL a subset into a downstream warehouse (Teradata/Redshift/Snowflake). Now dominant — "used at virtually all Fortune 500 enterprises."
    3. **3rd gen — lakehouse**: management + performance features applied **directly** on the open-format data lake, removing the warehouse tier.
- **Four problems with the two-tier model:** **reliability** (keeping lake & warehouse consistent needs continuous, bug-prone ETL), **data staleness** (warehouse lags the lake by days — 86% of analysts use out-of-date data), **limited advanced-analytics support** (TensorFlow/PyTorch/XGBoost can't run efficiently over warehouses via ODBC/JDBC; exporting adds a *third* ETL hop), **total cost of ownership** (double storage cost + proprietary-format lock-in).
- **Lakehouse definition:** "a data management system based on low-cost and directly-accessible storage that *also* provides traditional analytical DBMS management and performance features such as ACID transactions, data versioning, auditing, indexing, caching, and query optimization."
- **The trade-off:** lakehouses give up some **data independence** (the storage format becomes part of the public API to allow direct access) — the opposite of a traditional DBMS.
- **Three enabling technical ideas:** (1) a **transactional metadata layer** over object storage, (2) **format-independent performance optimizations** (caching, auxiliary data, data layout), (3) **declarative DataFrame APIs** that fold ML data-prep into optimizable query plans.
- **Proof of feasibility:** Delta Engine (C++ engine for Spark) on **TPC-DS @ scale factor 30,000**, 960 vCPUs, beats four cloud warehouses (DW1–DW4) on both **power-test duration** and **customer cost**.
- **The straw-man rejected:** "just put everything in a warehouse with separated compute/storage" — limited adoption because it still can't handle video/audio/text or fast direct ML access.

## Notes

### Evolution of data platform architectures (Fig. 1)

The paper's framing diagram, three panels:

- **(a) First-generation** — operational DBs → **ETL** → structured data in **data warehouses** → BI/reports.
- **(b) Current two-tier** — structured/semi/unstructured data → **data lake** → **ETL** → **warehouses** → BI/reports, with data science & ML reading the lake directly. Two tiers, multiple ETL hops.
- **(c) Lakehouse** — one **data lake** of open-format files with a **Metadata, Caching, and Indexing layer** on top serving BI, data science, ML, and reports directly. One tier.

> 💡 This is the same warehouse→lake→lakehouse story told in [[what-is-a-lakehouse]] and personal book [[ch01-databricks-platform-workspace]] — but the paper is precise about *why each generation existed* (schema-on-write vs schema-on-read) and *what specifically breaks* in the two-tier model.

### Why the two-tier architecture is "accidental complexity"

Drawing on Brooks' *No Silver Bullet*, the authors argue much of the pain is **accidental** (from how platforms are wired) rather than **intrinsic**:

- **Reliability/quality** is the #1 reported problem. Lake and warehouse differ in data types, SQL dialects, and schemas (e.g. denormalized in one); more ETL jobs across more systems → more failure surface.
- **Staleness** comes from the staging-area + periodic-ETL design. Streaming pipelines could help but are harder to operate than batch. First-gen warehouses ironically had *fresher* raw data because it lived in the same environment.
- **Unstructured data** (images, sensors, documents) is now a large fraction of enterprise data; SQL warehouses don't support it well.
- **ML/DS** need large non-SQL reads; ODBC/JDBC streaming is inefficient, and direct access to proprietary warehouse formats is impossible. Open formats are judged the most effective long-term answer. ML/DS also suffer the *same* data-management problems (quality, consistency, isolation) — so DBMS features have "immense value" for them.

**Existing half-steps (evidence of dissatisfaction):** every major warehouse added **external-table** support for Parquet/ORC (but it doesn't add management features or remove ETL/staleness, and connectors perform poorly); and there's broad investment in direct-on-lake SQL engines (Spark SQL, Presto, Hive, Athena) — but those alone lack ACID and indexes to match warehouse performance.

### The Lakehouse design — three components

#### 1. Metadata layers for data management (§3.2)

A transactional metadata layer raises a raw object store (S3/HDFS, where even multi-file updates aren't atomic) to DBMS-level abstractions:

- **Lineage of designs:** Apache **Hive ACID** (tracks files per table version via an OLTP DBMS) → **Delta Lake** (2016, Databricks) which stores the set of objects as a **transaction log in Parquet inside the data lake itself**, scaling to billions of objects per table → **Apache Iceberg** (Netflix; Parquet + ORC) with a similar design → **Apache Hudi** (Uber; focused on streaming ingest, *no concurrent writers*).
- **Adoption signal:** Delta Lake grew to **half of Databricks' compute-hours in three years**; zero-copy conversion of an existing Parquet directory into a Delta table by writing an initial log entry referencing all files.
- Metadata layers add **data-quality enforcement** (Delta schema enforcement + constraints API → reject/quarantine violating records) and are the natural home for **governance** (access control, audit logging — check permission before issuing object-store read credentials).
- **Open question:** Delta stores its log in the same (high-latency) object store → simple + highly available but caps transactions/sec; a faster metadata store may be better. Also: only single-table transactions today; cross-table txns and log-format/object-size tuning are open.

#### 2. SQL performance — format-independent optimizations (§3.3)

The hard problem: state-of-the-art SQL performance when **the storage format is part of the public API** (can't be hidden/changed like a closed-world DBMS). Three optimizations that leave the data files unchanged:

- **Caching** — with a transactional layer, it's safe to cache hot files on SSD/RAM (transactions know when a cached file is still valid); cache can be **transcoded** to an engine-friendlier form (Databricks' cache partially decompresses Parquet).
- **Auxiliary data** — maintain extra files the system fully controls: per-file **column min/max statistics** (stored in the same Parquet as the transaction log) enabling **data skipping**, plus a Bloom-filter index.
- **Data layout** — record ordering to cluster co-accessed data: single-dimension ordering or **space-filling curves (Z-order, Hilbert)** for multi-dimensional locality.

These combine well: cache the hot subset like a closed-world warehouse; for cold data, layout + zone maps minimize I/O against the open format.

#### 3. Efficient access for advanced analytics (§3.4)

ML libraries use imperative non-SQL code but need big reads. The successful approach: **declarative DataFrame APIs** (Spark DataFrames, Koalas) that lazily evaluate and compile data-prep into Spark SQL query plans, so caching/data-skipping/layout optimizations (§3.3) accelerate ML I/O. Spark pushes selections/projections into the Delta Lake data-source plugin (Fig. 4). Caveat: some APIs (TensorFlow `tf.data`) don't push query semantics down and focus on CPU↔GPU overlap — keeping accelerators well-utilized is an open challenge. Delta integrates with **MLflow** for reproducible table-version tracking; **feature stores** could be built on Lakehouse transactions/versioning instead of bespoke systems.

### TPC-DS results (Fig. 3)

Delta Engine vs four cloud warehouses (DW1–DW4) at **SF 30,000**, 960 vCPUs each, local SSD, AWS/Azure/GCP:

| System | Power-test duration (s) | Cost ($) |
|---|---|---|
| DW1 | 2996 | $153 |
| DW2 | 7143 | $286 |
| DW3 | 5793 | $206 |
| DW4 | 37283 | $570 |
| **Delta Engine (on-demand)** | **3302** | **$104** |
| **Delta Engine (spot)** | **3252** | **$56** |

Delta Engine is **comparable-or-better on time and cheapest on cost**. Footnote: systems started with data cached on SSD (some warehouses only support node-attached storage); Delta Engine was only **18% slower from a cold cache**.

### Research implications (§4)

- **Are there other ways?** A massively-parallel serving layer over a warehouse (e.g. Hive LLAP) is judged more expensive, harder to manage, less performant than direct object-store access — and hasn't seen broad deployment. **Governance/regulatory** pressure (search/delete old data, avoid vendor blocking) further favors open formats; the long-term industry trend is toward open formats.
- **Polystores** — many cross-engine queries could run directly against open-format lake data.
- **HTAP** could be a "bolt-on" archiving into a Lakehouse for consistent-snapshot queries.
- **Data mesh** — lakehouses suit distributed/decentralized team ownership because every dataset is directly accessible from the object store without onboarding users onto shared compute.

## Quotes worth keeping

> "We define a Lakehouse as a data management system based on low-cost and directly-accessible storage that also provides traditional analytical DBMS management and performance features such as ACID transactions, data versioning, auditing, indexing, caching, and query optimization." (§3)

> "Lakehouses' support for direct access means that they give up some aspects of data independence, which has been a cornerstone of relational DBMS design." (§3)

> "Delta Lake grew to cover half the compute-hours on Databricks in three years." (§3.2)

## Version note

> 📌 Point-in-time (Jan 2021). Several named pieces have since evolved: **Delta Engine** is now productized as **Photon** (the C++ vectorized engine); Z-order layout is now superseded for new tables by **Liquid Clustering**; **Koalas** became the `pyspark.pandas` API in Spark 3.2+. The architectural argument and the metadata-layer design are unchanged and now realized as **Delta Lake + Unity Catalog + Photon** on the Databricks Data Intelligence Platform.

## Open questions

- The paper's open metadata questions (cross-table transactions, faster metadata store than the object store) — how much has Delta/UC closed since 2021? (Unity Catalog now centralizes governance the paper sketched.)
- TPC-DS DW1–DW4 are anonymized — the relative standings are vendor-era-specific; the durable claim is *feasibility*, not a current leaderboard.

## Related sources

- [what-is-a-lakehouse](../databricks-blog/what-is-a-lakehouse/) — the 2020 Databricks blog post; same thesis for a general audience. This paper is its peer-reviewed, mechanism-level version (metadata layer internals, TPC-DS numbers, research agenda). Stonebraker's "data swamp" critique cited here (ref \[48\]) is the lake's failure mode the blog also names.
- [ch01-databricks-platform-workspace](../../book/ch01-databricks-platform-workspace/) — personal book Ch 1 builds its warehouse→lake→lakehouse narrative and Delta-transaction-log explanation directly on this paper's framing.
- [[02-explaining-lakehouses]] — Lakehouse-Dummies Ch 2 restates the same defining features for a business audience.
