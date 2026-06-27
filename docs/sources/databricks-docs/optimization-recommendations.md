# Optimization recommendations on Databricks

> **Source:** [docs.databricks.com/aws/en/optimizations](https://docs.databricks.com/aws/en/optimizations)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-11
> **Tags:** optimization, performance, databricks-runtime, disk-cache, dynamic-file-pruning, low-shuffle-merge, cbo, range-join, isolation, bloom-filter, A1
> **Type:** documentation

The hub/landing page for Databricks Runtime optimizations. Most take effect **automatically** — "you get their benefits simply by using Databricks" — and most DBR features require Delta Lake (the default format). Defaults are tuned for most workloads; some settings can be changed for extra performance. Everything listed is **enabled by default in DBR 10.4 LTS+**, so use the **latest DBR** to get the newest enhancements.

## Runtime performance enhancements (auto-on)

- **Disk caching** — accelerates repeated reads of Parquet by loading data to disk volumes on compute. → [[disk-cache]]
- **Dynamic file pruning** — skips files without data matching query predicates. → [[dynamic-file-pruning]]
- **Low shuffle merge** — reduces files rewritten by `MERGE` and the need to re-`OPTIMIZE` after merges. → [[low-shuffle-merge]]
- **Adaptive query execution (AQE)** — Spark 3.0+ runtime replanning. → [[aqe]]

## Recommendations for enhanced performance

- **Clone** tables (deep or shallow copies) → [[managed-tables]]
- **Cost-based optimizer (CBO)** — uses table statistics to accelerate query plans → [[cost-based-optimizer]]
- **Spark SQL on JSON strings**; **higher-order functions** (optimized array/map ops, faster than UDFs); **complex-type operators**.
- **Range join optimization** — manual tuning for range joins → [[range-join]]

## Opt-in behaviors

- **Isolation level** — `WriteSerializable` by default; switching to `Serializable` can reduce throughput for concurrent ops but may be needed when read-serializability is required → [[isolation-levels]]

> "Databricks has deprecated bloom filter indexes. Use predictive I/O or liquid clustering instead."

Related: [[disk-cache]], [[dynamic-file-pruning]], [[low-shuffle-merge]], [[cost-based-optimizer]], [[range-join]], [[isolation-levels]], [[aqe]], [[liquid-clustering]], [[predictive-optimization]].
