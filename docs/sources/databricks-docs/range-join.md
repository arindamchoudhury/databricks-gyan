# Range join optimization

> **Source:** [docs.databricks.com/aws/en/optimizations/range-join](https://docs.databricks.com/aws/en/optimizations/range-join)
> **Added:** 2026-06-24
> **Source updated:** 2026-05-21
> **Tags:** optimization, performance, range-join, join, bin-size, range-join-hint, databricks-sql, timestamp, interval, A1
> **Type:** documentation

A range join occurs when two relations join on a **point-in-interval** or **interval-overlap** condition (`BETWEEN`, inequalities) — otherwise run as a slow nested loop. The optimization splits the value domain into equal **bins** so only candidates in overlapping bins are compared. "In Databricks SQL, Databricks automatically optimizes range joins without any manual configuration" (bin size derived by sampling); on other compute you tune it via a `RANGE_JOIN` hint or session config. Bin-size units: `DATE` = days, `TIMESTAMP` = seconds (fractions allowed, e.g. `0.1` = 100 ms).

## What qualifies

A point-in-interval or interval-overlap condition where all values are numeric / `DATE` / `TIMESTAMP`, **all the same type** (decimals: same scale + precision), in an `INNER JOIN` (or `LEFT OUTER` with point on left / `RIGHT OUTER` with point on right), with a bin size.

```sql
-- point-in-interval
SELECT * FROM points JOIN ranges ON points.p BETWEEN ranges.start AND ranges.end;
-- interval-overlap
SELECT * FROM r1 JOIN r2 ON r1.start < r2.end AND r2.start < r1.end;
```

## Bin size

Splits the domain into equal bins; with bin size 10 and `p BETWEEN 8 AND 22`, only points in bins [0,10), [10,20), [20,30) are candidates. Small bins filter better but become inefficient if much smaller than typical intervals. Choose from the interval-length distribution:

```sql
SELECT map_from_arrays(
  ARRAY(0.5, 0.9, 0.99, 0.999, 0.9999),
  APPROX_PERCENTILE(end::DOUBLE - start::DOUBLE, ARRAY(0.5, 0.9, 0.99, 0.999, 0.9999))
) AS bin_sizes FROM ranges;
```

Recommended start: max of (90th-percentile length, 99th/10, 99.9th/100, …) — at the 90th-percentile bin size only 10% of intervals span >2 bins. A starting point only; fine-tune per workload.

## Numeric-equality-key pitfall

If a join has both an equality on a numeric column and a range condition, the optimizer may bin the equality column → degraded perf.

> "To ensure the range join optimization applies only to the intended range condition, cast the numeric equality columns to STRING."

```sql
SELECT /*+ RANGE_JOIN(reference, 3306084) */ reference.*, position.*
FROM position INNER JOIN reference
  ON CAST(position.parent_index AS STRING) = CAST(reference.parent_index AS STRING)
  AND position.child_index BETWEEN reference.min_child_index AND reference.max_child_index;
```

## Specifying the hint

```sql
SELECT /*+ RANGE_JOIN(points, 10) */ * FROM points JOIN ranges ON points.p >= ranges.start AND points.p < ranges.end;
SET spark.databricks.optimizer.rangeJoin.binSize=5;          -- session config (hint overrides)
SET spark.databricks.optimizer.autoRangeJoin.enabled=false;  -- disable auto in Databricks SQL
```

The hint relation is a table/view/subquery alias from the join; with left-associative joins `(a JOIN b) JOIN c`, a hint for the `a`–`c` range must name `c`. Python/Scala: `.hint("range_join", binSize)` on a DataFrame.

Related: [[sql-join-hints]], [[optimization-recommendations]].
