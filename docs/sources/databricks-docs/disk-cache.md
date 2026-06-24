# Optimize performance with caching (disk cache)

> **Source:** [docs.databricks.com/aws/en/optimizations/disk-cache](https://docs.databricks.com/aws/en/optimizations/disk-cache)
> **Added:** 2026-06-24
> **Source updated:** 2024-05-01
> **Tags:** optimization, performance, disk-cache, delta-cache, dbio-cache, caching, ssd, spark-cache, A1
> **Type:** documentation

## Summary
Disk caching accelerates data reads by copying remote Parquet files (incl. Delta) to a node's **local SSD storage** in a fast intermediate format. Caching is **automatic on first read**; successive reads of the same data are served locally. Works for all Parquet files on S3/ABFS/etc. Formerly called **Delta cache / DBIO cache** (renamed to avoid implying it's part of the Delta Lake protocol — it's a proprietary Databricks feature). Distinct from Apache Spark caching.

## Key points

- Auto-caches on first read; auto-invalidates/evicts when files change → no manual cache busting needed.
- Best enabled by choosing an **SSD-backed (cache-accelerated) worker type** — auto-configured, uses ≤ half the local SSD.
- `CACHE SELECT` is **ignored** on SQL warehouses + DBR 14.2+ (enhanced algorithm used instead).
- Disk cache ≠ Spark cache (`.cache()`/`.persist()`).
- Autoscaling caveat: a decommissioned worker loses its cache → re-read from source.

## Notes

### Disk cache vs Apache Spark cache

| Feature | Disk cache | Spark cache |
|---|---|---|
| Stored as | Local files on worker node | In-memory blocks (depends on storage level) |
| Applied to | Any Parquet table (S3/ABFS/…) | Any DataFrame or RDD |
| Triggered | Automatically, on first read (if enabled) | Manually, requires code changes |
| Evaluated | Lazily | Lazily |
| Availability | Config flags; enabled by default on certain node types | Always available |
| Evicted | Auto LRU or on file change; manually on cluster restart | Auto LRU; manually with `unpersist` |

Databricks recommends **automatic disk caching** over Spark cache.

### Consistency

Disk cache auto-detects when files are created/deleted/modified/overwritten and updates accordingly. You can write/modify/delete table data with no explicit invalidation — stale entries are auto-evicted.

### Instance types & configuration

Easiest path: choose a worker type with SSD volumes — those are enabled + configured for disk caching. Cache uses **at most half** the local SSD space.

```ini
spark.databricks.io.cache.maxDiskUsage 50g          # disk per node for cached data
spark.databricks.io.cache.maxMetaDataCache 1g       # disk per node for cached metadata
spark.databricks.io.cache.compression.enabled false # store cached data compressed?
```

Check / toggle:

```scala
spark.conf.get("spark.databricks.io.cache.enabled")
spark.conf.set("spark.databricks.io.cache.enabled", "[true | false]")
```

Disabling does **not** drop already-cached data — it just stops adding to / reading from the cache.

## Quotes worth keeping

> "The data is cached automatically whenever a file has to be fetched from a remote location. Successive reads of the same data are then performed locally…" (intro)

> "Disk caching on Databricks was formerly referred to as the Delta cache and the DBIO cache." (rename note)

## Open questions

- Page last updated 2024-05-01 — older than its siblings; verify config flag names still current on DBR 18.

## Related sources

- [[optimization-recommendations]] — parent hub listing this as a runtime enhancement.
- [[sql-warehouse-types]] — disk cache is part of why warehouses serve repeated BI queries fast.
- [[long-spark-stage-io]] — Spark-UI note that flags delta-cache hit/miss when diagnosing I/O-bound stages.
