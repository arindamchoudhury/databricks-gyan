# Range join optimization

> **Source:** [docs.databricks.com/aws/en/optimizations/range-join](https://docs.databricks.com/aws/en/optimizations/range-join)
> **Added:** 2026-06-24
> **Source updated:** 2026-05-21
> **Tags:** optimization, performance, range-join, join, bin-size, range-join-hint, databricks-sql, timestamp, interval, A1
> **Type:** documentation

## Summary
A range join occurs when two relations join on a **point-in-interval** or **interval-overlap** condition (`BETWEEN`, inequalities) — otherwise run as a slow nested loop. The range join optimization splits the value domain into equal **bins** so only candidates in overlapping bins are compared. In **Databricks SQL it's automatic** (bin size derived by sampling); on other compute you tune it via a `RANGE_JOIN` hint or session config.

## Key points

- Automatic in Databricks SQL (`spark.databricks.optimizer.autoRangeJoin.enabled = true`); manual elsewhere.
- Manual tuning: `/*+ RANGE_JOIN(relation, binSize) */` hint **or** `spark.databricks.optimizer.rangeJoin.binSize`. Hint overrides session config overrides auto.
- Applies to numeric / `DATE` / `TIMESTAMP` columns, **all same type** (decimals same scale+precision), `INNER` join (or specific `OUTER`).
- **Pitfall:** a numeric **equality** key alongside the range condition may get binned and hurt perf → **cast equality keys to `STRING`**.
- Bin size units: `DATE` = days, `TIMESTAMP` = seconds (fractions allowed, e.g. `0.1` = 100 ms).

## Notes

### What qualifies

Range join optimization is performed for joins that:

- Have a point-in-interval or interval-overlap condition.
- All values in the condition are numeric (integral/float/decimal), `DATE`, or `TIMESTAMP`.
- All values are the **same type** (decimals: same scale + precision).
- Are `INNER JOIN`, or a `LEFT OUTER` (point on left) / `RIGHT OUTER` (point on right).
- Have a bin size (auto-derived or manual).

**Point-in-interval** examples:

```sql
SELECT * FROM points JOIN ranges ON points.p BETWEEN ranges.start AND ranges.end;
SELECT * FROM points JOIN ranges ON points.p >= ranges.start AND points.p < ranges.end;
```

**Interval-overlap** example:

```sql
SELECT * FROM r1 JOIN r2 ON r1.start < r2.end AND r2.start < r1.end;
```

### Bin size

A numeric tuning parameter splitting the domain into equal bins. With bin size 10 and condition `p BETWEEN 8 AND 22`, the interval overlaps bins [0,10), [10,20), [20,30) — only points in those 3 bins are candidates. Small bins filter better but become inefficient if much smaller than typical intervals (long intervals span too many bins).

Choose from the interval-length distribution:

```sql
SELECT map_from_arrays(
  ARRAY(0.5, 0.9, 0.99, 0.999, 0.9999),
  APPROX_PERCENTILE(end::DOUBLE - start::DOUBLE, ARRAY(0.5, 0.9, 0.99, 0.999, 0.9999))
) AS bin_sizes
FROM ranges;
```

Recommended starting point: max of (90th-percentile length, 99th/10, 99.9th/100, …). Rationale: at the 90th-percentile bin size, only 10% of intervals span >2 bins; at 99th, only 1% span >11 bins. Starting point only — fine-tune per workload.

### Numeric-equality-key pitfall

If a join has both an equality on a numeric column and a range condition, the optimizer may bin the equality column → degraded perf. Cast it to `STRING` to exclude:

```sql
SELECT /*+ RANGE_JOIN(reference, 3306084) */ reference.*, position.*
FROM position
INNER JOIN reference
  ON CAST(position.parent_index AS STRING) = CAST(reference.parent_index AS STRING)
  AND position.child_index BETWEEN reference.min_child_index AND reference.max_child_index;
```

### Specifying the hint

```sql
SELECT /*+ RANGE_JOIN(points, 10) */ *
FROM points JOIN ranges ON points.p >= ranges.start AND points.p < ranges.end;
```

Hint relation = a table/view/subquery alias from the join. With left-associative joins `(a JOIN b) JOIN c`, a hint for the `a`–`c` range must name `c`, not `a`. Python/Scala: `.hint("range_join", binSize)` on a DataFrame.

Session config (applies to all range joins; hint overrides):

```sql
SET spark.databricks.optimizer.rangeJoin.binSize=5
```

Disable auto in Databricks SQL:

```sql
SET spark.databricks.optimizer.autoRangeJoin.enabled = false;
```

## Quotes worth keeping

> "In Databricks SQL, Databricks automatically optimizes range joins without any manual configuration." (intro)

> "To ensure the range join optimization applies only to the intended range condition, cast the numeric equality columns to STRING." (numeric-equality pitfall)

## Related sources

- [[sql-join-hints]] — join/broadcast/skew hints; `RANGE_JOIN` is the hint for interval joins.
- [[optimization-recommendations]] — parent hub (lists range join under recommendations).
