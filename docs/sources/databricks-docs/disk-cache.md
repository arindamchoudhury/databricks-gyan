# Optimize performance with caching (disk cache)

> **Source:** [docs.databricks.com/aws/en/optimizations/disk-cache](https://docs.databricks.com/aws/en/optimizations/disk-cache)
> **Added:** 2026-06-24
> **Source updated:** 2024-05-01
> **Tags:** optimization, performance, disk-cache, delta-cache, dbio-cache, caching, ssd, spark-cache, A1
> **Type:** documentation

> "The data is cached automatically whenever a file has to be fetched from a remote location. Successive reads of the same data are then performed locally…"

Disk caching accelerates reads by copying remote Parquet files (incl. Delta) to a node's **local SSD** in a fast intermediate format. It's **automatic on first read** and auto-invalidates/evicts when files change — no manual cache busting. It was "formerly referred to as the Delta cache and the DBIO cache" (renamed to avoid implying it's part of the Delta protocol — it's a proprietary Databricks feature), and is distinct from Apache Spark caching.

## Disk cache vs Apache Spark cache

| Feature | Disk cache | Spark cache |
|---|---|---|
| Stored as | Local files on worker node | In-memory blocks |
| Applied to | Any Parquet table (S3/ABFS/…) | Any DataFrame or RDD |
| Triggered | Automatically, on first read | Manually, requires code changes |
| Evaluated | Lazily | Lazily |
| Availability | Config flags; default-on certain node types | Always available |
| Evicted | Auto LRU or on file change; manually on restart | Auto LRU; manually with `unpersist` |

Databricks recommends **automatic disk caching** over Spark cache. Disk cache auto-detects when files are created/deleted/modified/overwritten — you can write/modify/delete with no explicit invalidation.

## Instance types & configuration

Easiest path: choose an **SSD-backed (cache-accelerated) worker type** — those are enabled and configured for disk caching, using **at most half** the local SSD.

```ini
spark.databricks.io.cache.maxDiskUsage 50g          # disk per node for cached data
spark.databricks.io.cache.maxMetaDataCache 1g       # disk per node for cached metadata
spark.databricks.io.cache.compression.enabled false # store cached data compressed?
```

```scala
spark.conf.get("spark.databricks.io.cache.enabled")
spark.conf.set("spark.databricks.io.cache.enabled", "[true | false]")
```

Disabling does **not** drop already-cached data — it just stops adding to / reading from the cache. Note: `CACHE SELECT` is **ignored** on SQL warehouses + DBR 14.2+ (an enhanced algorithm is used instead), and on autoscaling, a decommissioned worker loses its cache (re-read from source).

Related: [[optimization-recommendations]], [[sql-warehouse-types]], [[long-spark-stage-io]].
