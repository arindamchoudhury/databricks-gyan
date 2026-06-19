# SQL Hints: Join, Partition, and Skew

> **Source:** [https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-hints](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-hints)
> **Added:** 2026-06-18
> **Source updated:** (date not shown on page)
> **Tags:** spark, sql, join-hints, broadcast, shuffle, partitioning, performance, optimization, B2, B8
> **Type:** documentation

## Summary

SQL hint syntax for steering Databricks SQL's query planner toward a specific join strategy or output partitioning scheme. Hints are optimizer suggestions — the planner will use them if the join type allows it, but not all hints apply to all join types.

## Key points

- Hint syntax: `/*+ hint1, hint2 */` immediately after `SELECT`.
- Three hint families: **join hints**, **partition hints**, **skew hints**.
- Join hint priority (highest→lowest): `BROADCAST` > `MERGE` > `SHUFFLE_HASH` > `SHUFFLE_REPLICATE_NL`.
- `BROADCAST` bypasses `autoBroadcastJoinThreshold` — forces broadcast regardless of table size.
- `REBALANCE` is a best-effort partition hint; **ignored if AQE is not enabled**.
- When multiple partition hints conflict, the **leftmost** hint wins.
- When a table has an alias, the hint must use the **alias name**, not the original table name.

## Notes

### Join hints

**Syntax**

```sql
/*+ join_hint(table_name) */
```

**Hint types**

| Hint | Aliases | Strategy |
|---|---|---|
| `BROADCAST(t)` | `BROADCASTJOIN`, `MAPJOIN` | Broadcast hash join — sends `t` to every executor |
| `MERGE(t)` | `SHUFFLE_MERGE`, `MERGEJOIN` | Shuffle sort-merge join |
| `SHUFFLE_HASH(t)` | — | Shuffle hash join |
| `SHUFFLE_REPLICATE_NL(t)` | — | Shuffle-and-replicate nested loop join |

**Priority when hints conflict**

When hints are placed on both sides of a join, the optimizer uses the highest-priority hint and emits a warning for the overridden one:

```
org.apache.spark.sql.catalyst.analysis.HintErrorLogger:
Hint (strategy=merge) is overridden by another hint and will not take effect.
```

Priority order: `BROADCAST` > `MERGE` > `SHUFFLE_HASH` > `SHUFFLE_REPLICATE_NL`

**Build side selection**

- `BROADCAST`: if both sides hinted, smaller table (by stats) is broadcast.
- `SHUFFLE_HASH`: if both sides hinted, smaller side becomes the build side.

**Not guaranteed**

> "Because a given strategy might not support all join types, Databricks SQL is not guaranteed to use the join strategy suggested by the hint."

This matters for `BROADCAST` on the outer side of an outer join, or `SHUFFLE_HASH` when the join type requires sorted input.

**Examples**

```sql
-- Broadcast join (three equivalent forms)
SELECT /*+ BROADCAST(t1) */    * FROM t1 INNER JOIN t2 ON t1.key = t2.key;
SELECT /*+ BROADCASTJOIN(t1) */ * FROM t1 LEFT  JOIN t2 ON t1.key = t2.key;
SELECT /*+ MAPJOIN(t2) */       * FROM t1 RIGHT JOIN t2 ON t1.key = t2.key;

-- Sort-merge join
SELECT /*+ MERGE(t1) */         * FROM t1 INNER JOIN t2 ON t1.key = t2.key;

-- Shuffle hash join
SELECT /*+ SHUFFLE_HASH(t1) */  * FROM t1 INNER JOIN t2 ON t1.key = t2.key;

-- Nested loop join
SELECT /*+ SHUFFLE_REPLICATE_NL(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;

-- Conflicting hints — BROADCAST wins; MERGE hint raises a warning
SELECT /*+ BROADCAST(t1), MERGE(t1, t2) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;

-- Alias rule: use alias in hint, not original name
SELECT /*+ BROADCAST(s1), MERGE(s1, s2) */ *
FROM t1 AS s1 INNER JOIN t2 AS s2 ON s1.key = s2.key;
```

### Partition hints

Control the number and layout of output partitions.

| Hint | Effect |
|---|---|
| `COALESCE(n)` | Reduce partition count to `n` (no shuffle) |
| `REPARTITION(n)` / `REPARTITION(col)` / `REPARTITION(n, col)` | Repartition by count, columns, or both |
| `REPARTITION_BY_RANGE(col)` / `REPARTITION_BY_RANGE(n, col)` | Range-based repartition |
| `REBALANCE` / `REBALANCE(col)` | Best-effort rebalance to avoid tiny/huge files; **AQE required** |

When multiple partition hints are written, multiple logical plan nodes are inserted but **only the leftmost hint is applied by the optimizer**.

```sql
SELECT /*+ COALESCE(3) */            * FROM t;
SELECT /*+ REPARTITION(3) */         * FROM t;
SELECT /*+ REPARTITION(c) */         * FROM t;
SELECT /*+ REPARTITION(3, c) */      * FROM t;
SELECT /*+ REPARTITION_BY_RANGE(c) */ * FROM t;
SELECT /*+ REBALANCE */              * FROM t;
SELECT /*+ REBALANCE(c) */           * FROM t;
-- Alias rule applies here too
SELECT /*+ REBALANCE(d) */           * FROM t AS s(d);
```

### Skew hints

The `SKEW` hint is Delta Lake-specific. See the Databricks docs on [Skew join optimization using skew hints](https://docs.databricks.com/aws/en/archive/legacy/skew-join) for details.

### PySpark equivalent — `DataFrame.hint()`

Same hints available via `df.hint(name, *params)`. SQL hint and PySpark hint produce identical logical plan nodes.

```python
# Join hints
df1.hint("broadcast").join(df2, "key")
df1.hint("merge").join(df2, "key")
df1.hint("shuffle_hash").join(df2, "key")
df1.hint("shuffle_replicate_nl").join(df2, "key")

# Partition hints
df.hint("coalesce", 3)
df.hint("repartition", 3)
df.hint("repartition", 3, "col")
df.hint("repartition_by_range", "col")
df.hint("rebalance", "col")
```

Same priority rules and alias support apply. `/*+ BROADCAST(t1) */` and `df1.hint("broadcast")` are two surfaces over the same optimizer mechanism.

## Quotes worth keeping

> "The join side with the hint is broadcast regardless of autoBroadcastJoinThreshold."

> "This hint is ignored if AQE is not enabled." (REBALANCE)

> "When multiple partitioning hints are specified, multiple nodes are inserted into the logical plan, but the leftmost hint is picked by the optimizer."

## Open questions

- What happens when `BROADCAST` hint is applied to the *outer* side of a left/right outer join and the table is large — does it silently fall back to sort-merge, or error?
- Is `SHUFFLE_REPLICATE_NL` ever preferred over a Cartesian product that the optimizer already chose?

## Related sources

- [[optimize-data-workloads-guide]] — broadcast threshold config (`autoBroadcastJoinThreshold`), shuffle hash join toggle (`spark.sql.join.preferSortMergeJoin=false`), hard 8 GB broadcast limit
- [[spark-memory-issues]] — large broadcast as OOM cause; recommendation to lower threshold or switch to sort-merge
- [[slow-spark-stage-low-io]] — `CartesianProduct` / `BroadcastNestedLoopJoin` in DAG as signal of an unintended nested loop join; use hints or equi-join to fix
