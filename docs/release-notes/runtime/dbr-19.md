# Databricks Runtime 19 (Beta) Release Notes

> **Source:** [docs.databricks.com/aws/en/release-notes/runtime/19](https://docs.databricks.com/aws/en/release-notes/runtime/19)
> **Beta date:** 2026-06-15
> **Added:** 2026-06-30
> **Status:** Beta — not for production. End-of-support determined at LTS transition.

## Core versions

| Component | Version |
|---|---|
| Apache Spark | 4.2.0 |
| Python | 3.12.3 |
| Delta Lake | 4.2.0 |
| Java | Zulu21.48+15-CA (JDK **21** only) |
| Scala | 2.13.16 |
| OS | Ubuntu 24.04.4 LTS |
| R | 4.6.0 |
| PyArrow | 21.0.0 |
| pandas | 2.3.3 |

---

## Breaking changes

> ⚠️ **Review these before testing workloads on DBR 19.**

**JDK 17 fallback removed — JDK 21 only**
DBR 18 still shipped JDK 17 as a fallback selectable via `JNAME`. That fallback is gone. Clusters that set `JNAME=zulu17-ca-amd64` (or the ARM equivalent) must remove the variable before upgrading.

**~90 Python packages removed**
Compared to DBR 18, ~90 standard runtime packages are dropped. Notable removals: `plotly`, `seaborn`, `openai`, `langchain-core`, `langchain-openai`, `huggingface_hub`, `psycopg2`, `pyodbc`. The JupyterLab bundled server is split out (~54 Jupyter packages removed). Workloads depending on these must install them explicitly via cluster library or init script.

**Reserved table property `pipelines.pipelineId`**
Now reserved on all tables. Setting it manually raises an error. Remove explicit `pipelines.pipelineId` assignments from table DDL before upgrading.

**Environment variables restricted in standard access mode** (June 26)
Only a predefined set of env vars (proxy settings, cloud credentials, catalog vars) reaches the Spark engine and init scripts. Other cluster-set variables remain available to user code/UDFs but not to the engine or init scripts. Previously all cluster env vars reached the engine.

**Restricted Spark configs in standard access mode** (June 26)
Setting `spark.driver.extraJavaOptions`, `spark.executor.extraJavaOptions`, `spark.jars`, `spark.files`, `spark.executorEnv.*`, `spark.kubernetes.*` (matched by prefix) now fails cluster create/edit. Remove them before upgrading.

**Real-time mode watermark delay shifted +1 ms**
In RTM streaming, a record whose event time equals the current watermark (when the watermark advances mid-batch) was previously dropped as late; it is now retained. Micro-batch mode unaffected.

**DStream checkpoint class allowlist required**
Spark 4.2.0 adds a security control for DStream checkpoint deserialization. Custom/third-party types in DStream closures require `spark.streaming.checkpoint.allowedClasses` (comma-separated FQCNs or wildcards) before checkpoint recovery. Default allowlist covers standard Spark types only.

---

## New features (Apache Spark 4.2.0)

DBR 19 includes all Spark fixes from DBR 18, plus the following from Spark 4.2.0:

### SQL & Query Processing

- **`is_valid_variant(expr)`** — returns true if input is a well-formed VARIANT
- **`INSERT INTO ... REPLACE ON <cols>` / `REPLACE USING <subquery>`** — upsert-style writes that replace rows by matching column values
- **Batch CDC post-processing with `ChangelogTable`** — read CDC output as a changelog and compute net changes in batch mode
- **`TABLESAMPLE SYSTEM`** block sampling with DSv2 pushdown
- **Scalar UDFs as table-valued function arguments**
- **KLL quantile functions** (Apache DataSketches) — aggregation + CDF
- **Tuple Sketch aggregation functions** — approximate set intersection/union over typed payloads

### Data Source v2 catalogs

- **Transaction management** — atomic multi-table writes, consistent reads
- **`CREATE VIEW` / `ALTER VIEW`** — view DDL parity for non-Hive catalogs
- **`CREATE METRIC VIEW`** on V2 catalogs

### DataFrame / API

- **`withSchemaEvolution()`** in the DataFrame writer API
- **`Dataset.zipWithIndex`** in the Scala API (parity with Python/Java)
- **`DataFrameGroupBy.cov`** and **`SeriesGroupBy.describe`** in pandas API on Spark
- **`pa.ChunkedArray` support** in `createDataFrame()`
- **Codegen for array higher-order functions** (`filter`, `transform`, `aggregate`)
- **Plan download links** (SVG/DOT/TXT) in the Spark UI execution page

### Bug fixes

- `df.dropDuplicates(subset).exceptAll(other)` correctness fixed
- SQL parser no longer drops statements ending with a block comment
- Stream-stream join correctness fixed with RocksDB state format V4 + time-window predicates

---

## Library upgrades

100+ package updates. Highlights: NumPy 2.3.4, pandas 2.3.3, scikit-learn 1.7.2, PyArrow 21.0.0, mlflow-skinny 3.12.0, R 4.6.0, SparkR 4.2.0, Delta Lake 4.2.0.

[[dbr-18]] · [[dbr-17-3-lts]]
