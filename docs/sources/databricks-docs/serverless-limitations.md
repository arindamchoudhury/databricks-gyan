# Serverless compute limitations

> **Source:** [docs.databricks.com/aws/en/compute/serverless/limitations](https://docs.databricks.com/aws/en/compute/serverless/limitations)
> **Added:** 2026-06-16
> **Source updated:** 2026-05-20
> **Tags:** serverless, limitations, streaming, caching, udfs, notebooks, jobs, pipelines, B1, I5, I6
> **Type:** documentation

## Summary

Central reference for all serverless compute limitations across notebooks, jobs, and pipelines. Key themes: no RDD/R/Scala in notebooks, no Spark UI/logs (client-side only), no `df.cache()` family, streaming restricted to `AvailableNow`/`Once` triggers, Unity Catalog required for all external data access.

## Key points

- **No R.** No Scala in notebooks (Scala JAR tasks in jobs are supported).
- **Spark Connect only** — RDD APIs unsupported. Code relying on RDD may behave differently.
- **No Spark UI, no Spark logs** — only client-side application logs; use query profile instead.
- **No `df.cache()` / `df.persist()` / CACHE TABLE** — entire caching API is unsupported.
- **Streaming**: only `Trigger.AvailableNow()` and `Trigger.Once()`. `ProcessingTime` and `Continuous` triggers raise `INFINITE_STREAMING_TRIGGER_NOT_SUPPORTED`.
- **No Maven coordinates, no global temp views, no Databricks Container Services.**
- **No compute policies, no init scripts, no instance pools, no environment variables.**
- ANSI SQL is on by default; opt out with `spark.sql.ansi.enabled = false`.

## Notes

### Language and API

- **R** — not supported anywhere in serverless.
- **Spark RDD APIs** — unsupported; only Spark Connect APIs work.
  - Spark Connect defers analysis/name resolution to execution time — can change code behaviour.
- **ANSI SQL** — enabled by default. Opt out: `spark.sql.ansi.enabled = false`.
- `spark.createDataFrame` rows cannot exceed **128 MB**.

### Data access and storage

- **Unity Catalog required** for all external data source connections — consistent with [[serverless-notebooks]], [[serverless-jobs]], [[serverless-pipelines]].
- **DBFS access limited** — use UC Volumes or workspace files.
- **DBFS mounts with AWS instance profiles** — not supported.
- **Maven coordinates** — unsupported.
- **Global temp views** — unsupported; use session temp views or tables.

### User-defined functions (UDFs)

- UDFs **cannot access the internet**.
- `CREATE FUNCTION (External)` — unsupported. Use `CREATE FUNCTION (SQL and Python)`.
- Custom code **memory cap: 1 GB**.
- **Scala UDFs inside higher-order functions** — unsupported.

### UI and logging

- **Spark UI** — unavailable. Use the **query profile** for Spark query details.
- **Spark logs** — not available. Only **client-side application logs** are accessible.

> 💡 This is the sharpest observability gap vs. classic clusters. [[serverless-notebooks]] replaces Spark UI with query insights; [[serverless-jobs]] uses timeline view + query history. Neither gives you raw Spark logs.

### Networking

- **Cross-workspace access** restricted to same-region workspaces (no IP ACL or front-end PrivateLink configs).
- **Databricks Container Services** — not supported.

### Streaming

Only two triggers supported:

| Trigger | Status |
|---|---|
| `Trigger.AvailableNow()` | ✅ Recommended |
| `Trigger.Once()` | ✅ Deprecated but supported |
| `Trigger.ProcessingTime(interval)` | ❌ Raises `INFINITE_STREAMING_TRIGGER_NOT_SUPPORTED` |
| `Trigger.Continuous(interval)` | ❌ Same error |

> ⚠️ Default Spark behavior uses `Trigger.ProcessingTime("0 seconds")` — **must be overridden** on serverless. Use `Trigger.AvailableNow()` instead. For continuous workloads: use triggered pipeline mode or `AvailableNow` with continuous job execution.

All standard access mode streaming limitations also apply.

### Notebooks

- **Scala and R** — not supported.
- **JAR libraries** — unsupported in notebooks (JAR *tasks* in jobs are supported).
- **Notebook-scoped libraries** — not cached across development sessions.
- **Sharing TEMP tables/views among users** — unsupported.
- **Autocomplete and Variable Explorer for DataFrames** — not supported.
- New notebooks default to `.ipynb` format; source format notebooks may not capture serverless metadata correctly.
- **Notebook tags** — unsupported; use serverless usage policies for billing attribution instead.

### Jobs

- **Task logs not isolated** — logs contain output from multiple tasks, not per-task-run.
- **Task libraries unsupported for notebook tasks** — use notebook-scoped libraries.
- **No default execution timeout** for serverless jobs. Set one explicitly:
  ```python
  spark.conf.set("spark.databricks.execution.timeout", <seconds>)
  ```
  (Compare: serverless *notebooks* default to 2.5 hr timeout — see [[serverless-notebooks]].)

### Compute

These are all unsupported on serverless:

- Compute policies
- Compute-scoped init scripts
- Compute-scoped libraries (custom data sources, Spark extensions)
- Instance pools
- Compute event logs
- Most Apache Spark compute configurations
- **Environment variables** — use widgets for job/task parameters instead

### Caching

**Unsupported DataFrame/SQL cache APIs:**

```python
df.cache()
df.persist()
df.unpersist()
df.checkpoint()
spark.catalog.cacheTable()
spark.catalog.uncacheTable()
spark.catalog.clearCache()
```

**Unsupported SQL commands:** `CACHE TABLE`, `UNCACHE TABLE`, `REFRESH TABLE`, `CLEAR CACHE`

> ⚠️ Metadata *is* cached in serverless sessions — session context may not fully reset when switching catalogs.

### Hive

- **Hive SerDe tables** and `LOAD DATA` command — unsupported.
- **Hive variables** (`${env:var}`, `${configName}`, `${system:var}`, `spark.sql.variable`) — unsupported.
- Use `DECLARE VARIABLE` / `SET VARIABLE` / `IDENTIFIER` clause for parameterisation instead.

### Supported data sources

**DML (write/update/delete):**
CSV, JSON, AVRO, DELTA, KAFKA, PARQUET, ORC, TEXT, UNITY_CATALOG, BINARYFILE, XML, SIMPLESCAN, ICEBERG

**Read-only additions:**
MYSQL, POSTGRESQL, SQLSERVER, REDSHIFT, SNOWFLAKE, SQLDW, DATABRICKS, BIGQUERY, ORACLE, SALESFORCE, SALESFORCE_DATA_CLOUD, TERADATA, WORKDAY_RAAS, MONGODB

## Open questions

- ❓ Do streaming limitations apply equally to notebooks, jobs, and pipelines, or are there differences per compute type?
- ❓ Is there a list of which Spark compute configurations *are* supported (the page says "most" are unsupported)?
- ❓ Does the 1 GB UDF memory cap apply per UDF or total across a session?

## Related sources

- [[serverless-notebooks]] — notebook-specific serverless page; query insights replace Spark UI; 2.5 hr execution timeout by default (jobs have *no* default timeout per this page).
- [[serverless-jobs]] — job-specific serverless page; references this limitations page; JAR tasks supported even though JAR libs in notebooks are not.
- [[serverless-pipelines]] — pipeline-specific serverless page; references this limitations page; stream pipelining and vertical autoscaling are exclusive serverless pipeline features.
