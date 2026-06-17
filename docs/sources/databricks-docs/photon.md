# Photon

> **Source:** [docs.databricks.com/aws/en/compute/photon](https://docs.databricks.com/aws/en/compute/photon)
> **Added:** 2026-06-16
> **Source updated:** 2026-06-16
> **Tags:** compute, photon, performance, vectorized, sql-warehouse, B1
> **Type:** documentation

## Summary

Photon is Databricks' native C++ vectorized query engine that replaces the JVM-based Spark SQL execution engine for supported operations. It processes data in columnar batches instead of row-by-row, enabling SIMD parallelism. Transparent fallback to Spark for unsupported operations. Enabled by default on serverless compute and SQL warehouses. Key limitations: no UDFs, no RDD/Dataset APIs, no stateful streaming, no benefit for sub-2-second queries.

## Key points

- **C++ vectorised engine** replacing JVM Spark SQL; columnar batch processing via SIMD.
- **Transparent fallback**: unsupported operations silently hand off to Spark mid-query.
- **Default-on**: serverless compute and SQL warehouses. Toggle on classic compute.
- **Predictive IO** and **dynamic file pruning** (MERGE/UPDATE/DELETE) both *require* Photon.
- **No UDFs, no RDD APIs, no Dataset APIs, no stateful streaming**.
- **Graviton + Photon**: no Databricks Container Services, no SQL warehouses.
- **Sub-2-second queries** see no meaningful improvement.
- DBU rate differs for Photon instance types — check pricing page.
- Monitor: Spark UI (orange operators); Query profile (purple = Photon, grey = standard).

## Notes

### What Photon is

"The Databricks-native vectorized query engine that accelerates your SQL workloads, DataFrame API calls, ETL pipelines, and stateless streaming workloads."

Replaces "the JVM-based Spark SQL execution engine with a native C++ runtime" for supported operations. Processes "data in columnar batches rather than row by row" — SIMD instructions operate across thousands of rows simultaneously instead of one at a time.

Performance claim: up to **5× better price/performance** for data and analytics workloads (TPC-DS benchmarks vs competing cloud warehouses).

### How Photon works (fallback)

"When Photon encounters an unsupported operation during query execution, it transparently falls back to the Spark runtime for the remainder of that operation."

This means a single query can have some stages accelerated by Photon and others run by Spark — no manual intervention needed.

### Performance optimisations

- **Hash joins** replace sort-merge joins.
- **Native Parquet writer** accelerates Delta Lake, Apache Iceberg, and Parquet writes — applies to `UPDATE`, `DELETE`, `MERGE INTO`, `INSERT`, and `CREATE TABLE AS SELECT`.
- **Filter pushdown** and **dictionary pruning** reduce storage reads.

### Supported operators and data types

**Operators**: Scan, Filter, Project, Hash Aggregate, Hash Join, Hash Shuffle, Window Functions, Sorts.

**Data types**: numeric, string, date/timestamp, struct, array, map, geometry, geography.

### Features that require Photon

Two Databricks SQL features are gated on Photon being enabled:

- **Predictive IO** (read and write) — see [[sql-warehouse-types]] for context.
- **Dynamic file pruning** in `MERGE`, `UPDATE`, and `DELETE` statements.

### Enabling Photon

**Classic compute (UI)**: Use Photon Acceleration checkbox under Performance (enabled by default on DBR 9.1 LTS+).

**API — clusters/jobs**: set `runtime_engine` to `PHOTON`.

**API — pipelines**: set `photon` to `true`.

**SQL warehouses and serverless compute**: enabled by default; no manual toggle.

### Monitoring Photon usage

**Spark UI**: Photon operators appear in **orange** in the query DAG.

**Query profile** (SQL warehouses / serverless): Photon operators shown in **purple**; standard Spark operators in **grey**.

### Limitations

| Limitation | Detail |
|---|---|
| Sub-2-second queries | No meaningful improvement |
| UDFs | Not supported — falls back to Spark |
| RDD APIs | Not supported |
| Dataset APIs | Not supported |
| Stateful streaming | Not supported (stateless streaming: OK) |
| Graviton + Photon | No Databricks Container Services; no SQL warehouses |

> 💡 Photon on Graviton is supported (see [[classic-compute-configure]] §Graviton) but loses two capabilities: DCS and SQL warehouses.

### DBU billing

Photon instance types consume DBUs at a **different rate** from standard instances. Check the Databricks pricing page for exact rates. The trade-off is typically cost-positive — the price/performance uplift outweighs the higher DBU rate.

## Open questions

- ❓ What is the exact DBU rate multiplier for Photon vs non-Photon instances?
- ❓ What specific window functions and aggregations are supported vs fall back?

## Related sources

- [[sql-warehouse-types]] — Photon is present on all three warehouse types; Predictive IO and IWM are layered on top.
- [[classic-compute-configure]] — how to enable/disable Photon checkbox; Graviton + Photon interaction.
- [[serverless-limitations]] — serverless compute; Photon is on by default there too.
