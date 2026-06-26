# Serverless compute limitations

> **Source:** [docs.databricks.com/aws/en/compute/serverless/limitations](https://docs.databricks.com/aws/en/compute/serverless/limitations)
> **Added:** 2026-06-16
> **Source updated:** 2026-06-18
> **Tags:** serverless, limitations, streaming, caching, udfs, notebooks, jobs, pipelines, B1, I5, I6
> **Type:** documentation

The central reference for all serverless compute limitations across notebooks, jobs, and pipelines. The recurring themes: no RDD/R/Scala in notebooks, no Spark UI/logs (client-side only), no `df.cache()` family, streaming restricted to `AvailableNow`/`Once` triggers, Unity Catalog required for all external data access, and a hard **7-day max runtime**.

## Language and API

- **R** — not supported anywhere in serverless. **Scala** — not in notebooks (Scala JAR *tasks* in jobs are supported).
- **Spark RDD APIs** — unsupported; only **Spark Connect** APIs work, and Spark Connect defers analysis/name resolution to execution time (can change code behaviour).
- **ANSI SQL** — enabled by default; opt out with `spark.sql.ansi.enabled = false`.
- `spark.createDataFrame` rows cannot exceed **128 MB**.

## Data access and storage

- **Unity Catalog required** for all external data source connections.
- **DBFS access limited** — use UC Volumes or workspace files; DBFS mounts with AWS instance profiles aren't supported.
- **Maven coordinates** — unsupported. **Global temp views** — unsupported (use session temp views or tables).

## User-defined functions (UDFs)

- UDFs **cannot access the internet**.
- `CREATE FUNCTION (External)` unsupported — use `CREATE FUNCTION (SQL and Python)`.
- Custom-code **memory cap: 1 GB**. **Scala UDFs inside higher-order functions** unsupported.

## UI and logging

- **Spark UI** — unavailable; use the **query profile** for Spark query details.
- **Spark logs** — not available; only **client-side application logs**.

> 💡 The sharpest observability gap vs classic clusters. [[serverless-notebooks]] replaces Spark UI with query insights; [[serverless-jobs]] uses timeline view + query history. Neither gives raw Spark logs.

## Networking

- **Cross-workspace access** restricted to same-region workspaces (no IP ACL or front-end PrivateLink configs).
- **Databricks Container Services** — not supported.

## Streaming

| Trigger | Status |
|---|---|
| `Trigger.AvailableNow()` | ✅ Recommended |
| `Trigger.Once()` | ✅ Deprecated but supported |
| `Trigger.ProcessingTime(interval)` | ❌ `INFINITE_STREAMING_TRIGGER_NOT_SUPPORTED` |
| `Trigger.Continuous(interval)` | ❌ Same error |

> ⚠️ Default Spark behavior uses `Trigger.ProcessingTime("0 seconds")` — **must be overridden** on serverless. For continuous workloads use triggered pipeline mode or `AvailableNow` with continuous job execution. All standard-access-mode streaming limitations also apply.

## Notebooks

- **Scala and R** not supported. **JAR libraries** unsupported in notebooks (JAR *tasks* in jobs are supported).
- Notebook-scoped libraries not cached across dev sessions; sharing TEMP tables/views among users unsupported; autocomplete + Variable Explorer for DataFrames not supported.
- New notebooks default to `.ipynb`; **notebook tags** unsupported (use serverless usage policies for billing attribution).

## Jobs

- **Task logs not isolated** (contain output from multiple tasks). Task libraries unsupported for notebook tasks — use notebook-scoped libraries.
- **No default execution timeout** — set one: `spark.conf.set("spark.databricks.execution.timeout", <seconds>)`. (Serverless *notebooks* default to a 2.5 hr timeout — see [[serverless-notebooks]].)
- **Max runtime 7 days** — runs exceeding 7 days are terminated and **not retried**; break long workloads up or use classic compute.

## Compute

Unsupported on serverless: compute policies; compute-scoped init scripts; compute-scoped libraries (custom data sources, Spark extensions); instance pools; compute event logs; most Apache Spark compute configurations; **environment variables** (use widgets for job/task parameters).

## Caching

```python
df.cache(); df.persist(); df.unpersist(); df.checkpoint()
spark.catalog.cacheTable(); spark.catalog.uncacheTable(); spark.catalog.clearCache()
```

…are all unsupported, as are the SQL commands `CACHE TABLE`, `UNCACHE TABLE`, `REFRESH TABLE`, `CLEAR CACHE`.

> ⚠️ Metadata *is* cached in serverless sessions — session context may not fully reset when switching catalogs.

## Hive

- **Hive SerDe tables** and `LOAD DATA` unsupported.
- **Hive variables** (`${env:var}`, `${configName}`, `${system:var}`, `spark.sql.variable`) unsupported — use `DECLARE VARIABLE` / `SET VARIABLE` / `IDENTIFIER` clause instead.

## Supported data sources

- **DML (write/update/delete):** CSV, JSON, AVRO, DELTA, KAFKA, PARQUET, ORC, TEXT, UNITY_CATALOG, BINARYFILE, XML, SIMPLESCAN, ICEBERG.
- **Read-only additions:** MYSQL, POSTGRESQL, SQLSERVER, REDSHIFT, SNOWFLAKE, SQLDW, DATABRICKS, BIGQUERY, ORACLE, SALESFORCE, SALESFORCE_DATA_CLOUD, TERADATA, WORKDAY_RAAS, MONGODB.

Related: [[serverless-notebooks]], [[serverless-jobs]], [[serverless-pipelines]], [[lakeguard]].
