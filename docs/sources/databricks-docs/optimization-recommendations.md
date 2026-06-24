# Optimization recommendations on Databricks

> **Source:** [docs.databricks.com/aws/en/optimizations](https://docs.databricks.com/aws/en/optimizations)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-11
> **Tags:** optimization, performance, databricks-runtime, disk-cache, dynamic-file-pruning, low-shuffle-merge, cbo, range-join, isolation, bloom-filter, A1
> **Type:** documentation

## Summary
Hub/landing page for Databricks Runtime optimizations. Most take effect **automatically** — you benefit just by using Databricks — and most DBR features require Delta Lake (the default table format). Defaults are tuned for most workloads; some settings can be changed for extra performance. Page groups features into auto-on runtime enhancements, opt-in recommendations, and deprecated behaviors. All listed behaviors are **enabled by default in DBR 10.4 LTS+**.

## Key points

- Three buckets: **Runtime performance enhancements** (auto-on), **recommendations for enhanced performance**, **opt-in behaviors**.
- Use the **latest DBR** to get the newest enhancements.
- **Bloom filter indexes are deprecated** → use predictive I/O or liquid clustering.

## Notes

### Databricks Runtime performance enhancements (auto-on, DBR 10.4 LTS+)

- **Disk caching** — accelerates repeated reads of Parquet by loading data to disk volumes on compute. See [[disk-cache]].
- **Dynamic file pruning** — skips directories/files without data matching query predicates. See [[dynamic-file-pruning]].
- **Low shuffle merge** — reduces files rewritten by `MERGE`, reduces need to re-`OPTIMIZE` after merges. See [[low-shuffle-merge]].
- **Adaptive query execution (AQE)** — Spark 3.0+ runtime replanning. See [[aqe]].

### Recommendations for enhanced performance

- **Clone** tables (deep or shallow copies) — see [[managed-tables]].
- **Cost-based optimizer (CBO)** — uses table statistics to accelerate query plans. See [[cost-based-optimizer]].
- **Spark SQL on JSON strings** — interact with JSON without parsing strings.
- **Higher-order functions** — built-in optimized ops for arrays/maps, faster than UDFs.
- **Complex-type operators** — built-in syntax for arrays, structs, JSON strings.
- **Range join optimization** — manual tuning for range joins. See [[range-join]].

### Opt-in behaviors

- **Isolation level** — `WriteSerializable` by default; switching to `Serializable` can reduce throughput for concurrent ops but may be needed when read-serializability is required. See [[isolation-levels]].
- **Bloom filter indexes — DEPRECATED.** Use predictive I/O or liquid clustering instead.

## Quotes worth keeping

> "Many of these optimizations take place automatically. You get their benefits simply by using Databricks." (intro)

> "Databricks has deprecated bloom filter indexes. Use predictive I/O or liquid clustering instead." (Opt-in behaviors)

## Related sources

- [[disk-cache]], [[dynamic-file-pruning]], [[low-shuffle-merge]], [[cost-based-optimizer]], [[range-join]], [[isolation-levels]] — the per-feature deep dives this hub links.
- [[aqe]] — the fourth auto-on runtime enhancement, already captured.
- [[liquid-clustering]], [[predictive-optimization]] — the layout/maintenance optimizations this hub points to (and the replacements for deprecated bloom filters).
