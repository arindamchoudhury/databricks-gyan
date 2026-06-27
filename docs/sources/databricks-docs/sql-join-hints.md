# SQL Hints: Join, Partition, and Skew

> **Source:** [docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-hints](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-hints)
> **Added:** 2026-06-18
> **Source updated:** 2026-06-18
> **Tags:** spark, sql, join-hints, broadcast, shuffle, partitioning, performance, optimization, B2, B8
> **Type:** documentation

SQL hint syntax (`/*+ hint1, hint2 */` immediately after `SELECT`) for steering the planner toward a specific join strategy or output partitioning. Hints are optimizer *suggestions* — used if the join type allows, but not all hints apply to all join types. Three families: **join hints**, **partition hints**, **skew hints**. When a table has an alias, hints must use the **alias name**.

## Join hints

| Hint | Aliases | Strategy |
|---|---|---|
| `BROADCAST(t)` | `BROADCASTJOIN`, `MAPJOIN` | Broadcast hash join — sends `t` to every executor |
| `MERGE(t)` | `SHUFFLE_MERGE`, `MERGEJOIN` | Shuffle sort-merge join |
| `SHUFFLE_HASH(t)` | — | Shuffle hash join |
| `SHUFFLE_REPLICATE_NL(t)` | — | Shuffle-and-replicate nested loop join |

When hints conflict (both sides hinted), priority is **`BROADCAST` > `MERGE` > `SHUFFLE_HASH` > `SHUFFLE_REPLICATE_NL`** and a warning is emitted for the overridden one. Build side: for `BROADCAST` / `SHUFFLE_HASH` with both sides hinted, the smaller table (by stats) is broadcast / becomes the build side.

> "The join side with the hint is broadcast regardless of autoBroadcastJoinThreshold." But: "Because a given strategy might not support all join types, Databricks SQL is not guaranteed to use the join strategy suggested by the hint" (e.g. `BROADCAST` on the outer side of an outer join).

```sql
SELECT /*+ BROADCAST(t1) */    * FROM t1 INNER JOIN t2 ON t1.key = t2.key;
SELECT /*+ MERGE(t1) */        * FROM t1 INNER JOIN t2 ON t1.key = t2.key;
SELECT /*+ SHUFFLE_HASH(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;
SELECT /*+ BROADCAST(t1), MERGE(t1, t2) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;  -- BROADCAST wins; MERGE warns
SELECT /*+ BROADCAST(s1) */ * FROM t1 AS s1 INNER JOIN t2 AS s2 ON s1.key = s2.key;     -- use alias in hint
```

## Partition hints

| Hint | Effect |
|---|---|
| `COALESCE(n)` | Reduce partition count to `n` (no shuffle) |
| `REPARTITION(n)` / `REPARTITION(col)` / `REPARTITION(n, col)` | Repartition by count, columns, or both |
| `REPARTITION_BY_RANGE(col)` / `REPARTITION_BY_RANGE(n, col)` | Range-based repartition |
| `REBALANCE` / `REBALANCE(col)` | Best-effort rebalance to avoid tiny/huge files; **AQE required** |

> "This hint is ignored if AQE is not enabled." (REBALANCE) · "When multiple partitioning hints are specified… the leftmost hint is picked by the optimizer."

## Skew hints

The `SKEW` hint is Delta Lake-specific — see "Skew join optimization using skew hints". (Prefer AQE skew handling — see [[aqe]].)

## PySpark equivalent — `DataFrame.hint()`

Same hints via `df.hint(name, *params)`, producing identical logical plan nodes:

```python
df1.hint("broadcast").join(df2, "key")
df1.hint("merge").join(df2, "key")
df.hint("coalesce", 3)
df.hint("repartition", 3, "col")
df.hint("rebalance", "col")
```

`/*+ BROADCAST(t1) */` and `df1.hint("broadcast")` are two surfaces over the same optimizer mechanism.

Related: [[aqe]], [[optimize-data-workloads-guide]], [[spark-memory-issues]], [[slow-spark-stage-low-io]], [[range-join]].
