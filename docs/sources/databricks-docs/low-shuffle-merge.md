# Low shuffle merge

> **Source:** [docs.databricks.com/aws/en/optimizations/low-shuffle-merge](https://docs.databricks.com/aws/en/optimizations/low-shuffle-merge)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-11
> **Tags:** optimization, performance, merge, low-shuffle-merge, delta, shuffle, liquid-clustering, zorder, optimize, A1, I5
> **Type:** documentation

## Summary
Low shuffle merge is Databricks' optimized `MERGE` implementation that processes **unmodified rows** in a separate, streamlined, shuffle-free path instead of running them through the same shuffles + expensive calculations as modified rows. Result: far less shuffled data, faster MERGE, and **preserved data layout** (incl. liquid clustering / Z-order) on unmodified rows — reducing the need to re-`OPTIMIZE` after a merge. GA + default-on in **DBR 10.4 LTS+**.

## Key points

- Default-on DBR 10.4 LTS+ — the `spark.databricks.delta.merge.enableLowShuffle` flag is a **no-op** there (it only mattered on older runtimes).
- Why MERGE is costly: Delta updates are **per-file**, so changing a few rows forces rewriting all other rows in that file. Low shuffle merge handles those unmodified rows cheaply.
- Preserves existing layout (liquid clustering / Z-order) on unmodified data **best-effort**.
- Still: newly inserted/updated rows may not be optimally laid out → may still need `OPTIMIZE` (or `OPTIMIZE ZORDER BY` on legacy Z-order tables).

## Notes

### Optimized performance

Many MERGE workloads update only a small fraction of rows, but Delta can only update per file — so the old implementation reprocessed all unmodified rows in the same file through shuffles + expensive processing. Low shuffle merge routes unmodified rows through a path with **no shuffles or added overhead**.

### Optimized data layout

The earlier MERGE implementation changed the layout of unmodified data entirely, degrading later operations. Low shuffle merge **preserves** the layout of unmodified records (incl. liquid clustering) best-effort, so performance degrades more slowly across repeated merges.

> **Caveat:** updated/newly inserted data may not be optimally laid out → you may still need `OPTIMIZE` on liquid-clustered tables (or `OPTIMIZE ZORDER BY` on Z-ordered tables).

### Availability

Default-on DBR 10.4+. Legacy: set `spark.databricks.delta.merge.enableLowShuffle = true` on older runtimes; no effect on 10.4+. Databricks recommends liquid clustering for all new tables (Z-order is legacy).

## Quotes worth keeping

> "Low shuffle merge also reduces the need for users to re-run OPTIMIZE after performing a MERGE operation." (intro)

## Related sources

- [[liquid-clustering]] — layout low shuffle merge preserves on unmodified rows.
- [[ch02-managing-data-with-delta-lake]] / I5 — manual `MERGE INTO` / `OPTIMIZE` mechanics this optimizes.
- [[optimization-recommendations]] — parent hub.
