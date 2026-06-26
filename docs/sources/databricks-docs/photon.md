# Photon

> **Source:** [docs.databricks.com/aws/en/compute/photon](https://docs.databricks.com/aws/en/compute/photon)
> **Added:** 2026-06-16
> **Source updated:** 2026-06-16
> **Tags:** compute, photon, performance, vectorized, sql-warehouse, B1
> **Type:** documentation

> "The Databricks-native vectorized query engine that accelerates your SQL workloads, DataFrame API calls, ETL pipelines, and stateless streaming workloads."

Photon replaces the JVM-based Spark SQL execution engine with a native **C++ runtime** for supported operations, processing data **in columnar batches** rather than row by row so SIMD instructions operate across thousands of rows at once. Databricks claims up to **5× better price/performance** (TPC-DS vs competing cloud warehouses). It's **enabled by default on serverless compute and SQL warehouses** (a toggle on classic compute), and **Predictive IO** and **dynamic file pruning** (MERGE/UPDATE/DELETE) both *require* it.

## How Photon works (fallback)

> "When Photon encounters an unsupported operation during query execution, it transparently falls back to the Spark runtime for the remainder of that operation."

So a single query can have some stages accelerated by Photon and others run by Spark — no manual intervention.

## Performance optimisations

- **Hash joins** replace sort-merge joins.
- **Native Parquet writer** accelerates Delta Lake, Iceberg, and Parquet writes — applies to `UPDATE`, `DELETE`, `MERGE INTO`, `INSERT`, and `CREATE TABLE AS SELECT`.
- **Filter pushdown** and **dictionary pruning** reduce storage reads.

Supported **operators**: Scan, Filter, Project, Hash Aggregate, Hash Join, Hash Shuffle, Window Functions, Sorts. Supported **data types**: numeric, string, date/timestamp, struct, array, map, geometry, geography.

## Features that require Photon

- **Predictive IO** (read and write) — see [[sql-warehouse-types]].
- **Dynamic file pruning** in `MERGE`, `UPDATE`, and `DELETE` ([[dynamic-file-pruning]]).

## Enabling Photon

- **Classic compute (UI):** "Use Photon Acceleration" checkbox under Performance (default on DBR 9.1 LTS+).
- **API — clusters/jobs:** set `runtime_engine` to `PHOTON`.
- **API — pipelines:** set `photon` to `true`.
- **SQL warehouses and serverless compute:** enabled by default, no toggle.

## Monitoring Photon usage

- **Spark UI:** Photon operators appear in **orange** in the query DAG.
- **Query profile** (SQL warehouses / serverless): Photon operators **purple**, standard Spark operators **grey**.

## Limitations

| Limitation | Detail |
|---|---|
| Sub-2-second queries | No meaningful improvement |
| UDFs | Not supported — falls back to Spark |
| RDD APIs | Not supported |
| Dataset APIs | Not supported |
| Stateful streaming | Not supported (stateless streaming: OK) |
| Graviton + Photon | No Databricks Container Services; no SQL warehouses |

Photon instance types consume DBUs at a **different rate** from standard instances (check the pricing page) — typically cost-positive, as the price/performance uplift outweighs the higher DBU rate.

Related: [[sql-warehouse-types]], [[dynamic-file-pruning]], [[classic-compute-configure]], [[serverless-limitations]].
