# Adaptive Query Execution (AQE)

> **Source:** [https://docs.databricks.com/aws/en/optimizations/aqe](https://docs.databricks.com/aws/en/optimizations/aqe)
> **Added:** 2026-06-18
> **Source updated:** 2023-10-12
> **Tags:** spark, aqe, performance, optimization, broadcast, skew, shuffle, partitioning, B2, B8, B16
> **Type:** documentation

## Summary

AQE is query re-optimization that runs *during* execution. It collects runtime statistics after shuffle and broadcast exchanges and uses them to dynamically improve join strategies, partition sizes, and skew handling — without any manual tuning.

## Key points

- AQE enabled by default (`spark.databricks.optimizer.adaptive.enabled = true`).
- Applies only to non-streaming queries with at least one exchange (join, aggregate, window) or sub-query.
- Four capabilities: dynamic broadcast join conversion, partition coalescing, skew join splitting, empty relation propagation.
- AQE broadcast threshold (30 MB) is separate from the static broadcast threshold (`autoBroadcastJoinThreshold`, default 10 MB — see [[optimize-data-workloads-guide]]).
- Skew detection requires **both** conditions to be true: partition > 256 MB **AND** partition > 5× median.
- `REBALANCE` hint (see [[sql-join-hints]]) is **ignored if AQE is off**.
- Static broadcast hints beat AQE's dynamic broadcast — AQE may shuffle first, then decide to broadcast.
- AQE does **not** do dynamic join reordering.
- Structured Streaming: `spark.sql.shuffle.partitions` cannot change between restarts from the same checkpoint.
- Not all AQE-applied queries are re-optimized — re-optimization only occurs when runtime stats suggest a better plan.

## Notes

### Four capabilities

**1. Dynamic broadcast join conversion**

At runtime, after shuffle exchange, if one side of a sort-merge join turns out to be ≤ 30 MB, AQE converts it to a broadcast hash join. Avoids a full sort-merge shuffle when data is small in practice.

> Caveat: broadcast is not supported for all join types. E.g., the **left relation of a LEFT OUTER JOIN cannot be broadcast**.

> Caveat 2: AQE also skips the broadcast conversion if the percentage of non-empty partitions is below `spark.sql.adaptive.nonEmptyPartitionRatioForBroadcastJoin` — sort-merge may finish quickly enough on sparse data.

**2. Partition coalescing**

After shuffle, AQE merges small partitions into target-size partitions. "Very small tasks have worse I/O throughput and tend to suffer more from scheduling overhead and task setup overhead. Combining small tasks saves resources and improves cluster throughput."

| Config | Default | Meaning |
|---|---|---|
| `spark.sql.adaptive.coalescePartitions.enabled` | `true` | Enable coalescing |
| `spark.sql.adaptive.advisoryPartitionSizeInBytes` | `64MB` | Target size (upper bound) |
| `spark.sql.adaptive.coalescePartitions.minPartitionSize` | `1MB` | Floor — partitions won't shrink below this |
| `spark.sql.adaptive.coalescePartitions.minPartitionNum` | 2× cores | Minimum count; **not recommended to set explicitly** — overrides `minPartitionSize` |

[![Custom shuffle reader diagram](assets/aqe/07-custom-shuffle-reader.png)](assets/aqe/07-custom-shuffle-reader.png)
*`CustomShuffleReader` node with `Coalesced` property — signals AQE coalesced the partitions.*

[![Custom shuffle reader string](assets/aqe/08-custom-shuffle-reader-string.png)](assets/aqe/08-custom-shuffle-reader-string.png)
*`CustomShuffleReader` as seen in `DataFrame.explain()` string output.*

**3. Skew join handling**

AQE splits (and replicates if needed) skewed partitions in sort-merge and shuffle hash joins.

A partition is considered skewed when **both** are true:

```
partition size > skewedPartitionFactor × median partition size
partition size > skewedPartitionThresholdInBytes
```

| Config | Default | Meaning |
|---|---|---|
| `spark.sql.adaptive.skewJoin.enabled` | `true` | Enable skew handling |
| `spark.sql.adaptive.skewJoin.skewedPartitionFactor` | `5` | Multiplier against median |
| `spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes` | `256MB` | Absolute floor for skew detection |

> Skew handling is limited for some join types. In `LEFT OUTER JOIN`, only skew on the **left side** can be optimized.

[![Skew join plan](assets/aqe/09-skew-join-plan.png)](assets/aqe/09-skew-join-plan.png)
*Skew join plan diagram — `SortMergeJoin` node with `isSkew=true`.*

[![Skew join string](assets/aqe/10-skew-join-string.png)](assets/aqe/10-skew-join-string.png)
*`SortMergeJoin` with `isSkew` field as seen in string output.*

**4. Empty relation propagation**

If a relation turns out empty at runtime, AQE short-circuits joins/aggregations that depend on it. The plan replaces the affected subtree with `LocalTableScan` with an empty relation field.

Config: `spark.databricks.adaptive.emptyRelationPropagation.enabled` (default: `true`)

[![Local table scan](assets/aqe/11-local-table-scan.png)](assets/aqe/11-local-table-scan.png)
*Empty relation propagation — subtree replaced by `LocalTableScan`.*

[![Local table scan string](assets/aqe/12-local-table-scan-string.png)](assets/aqe/12-local-table-scan-string.png)
*`LocalTableScan` with empty relation field in string output.*

### Configuration reference

| Config | Default | Notes |
|---|---|---|
| `spark.databricks.optimizer.adaptive.enabled` | `true` | Master switch |
| `spark.sql.shuffle.partitions` | `200` | Set to `auto` for auto-optimized shuffle (recommended on Databricks) |
| `spark.databricks.adaptive.autoBroadcastJoinThreshold` | `30MB` | AQE-specific runtime broadcast threshold |

### Reading the AQE query plan

AQE-applied queries contain `AdaptiveSparkPlan` nodes, usually as the root of each query/sub-query. The `isFinalPlan` flag is `false` while running, `true` after completion.

**How each tool shows it**

**Spark UI** — plan diagram evolves as stages complete. Completed nodes (with metrics) are frozen; future nodes can still change.

[![Query plan diagram](assets/aqe/01-query-plan-diagram.png)](assets/aqe/01-query-plan-diagram.png)
*Spark UI query plan diagram — nodes evolve as execution progresses.*

**`DataFrame.explain()`** — shows both initial plan and current/final plan. Each shuffle/broadcast stage has statistics with an `isRuntime` flag:

- Before stage: `Statistics(sizeInBytes=1024.0 KiB, rowCount=4, isRuntime=false)` (compile-time estimate)
- After stage: `Statistics(sizeInBytes=658.1 KiB, rowCount=2.81E+4, isRuntime=true)` (actual runtime)

[![Before execution](assets/aqe/02-before-execution.png)](assets/aqe/02-before-execution.png)
*`DataFrame.explain()` before execution — all stats are compile-time estimates.*

[![During execution](assets/aqe/03-during-execution.png)](assets/aqe/03-during-execution.png)
*`DataFrame.explain()` during execution — completed stages show runtime stats; plan may differ from initial.*

[![After execution](assets/aqe/04-after-execution.png)](assets/aqe/04-after-execution.png)
*`DataFrame.explain()` after execution — final plan with all runtime stats.*

**`SQL EXPLAIN`** — does not execute the query; always shows the initial plan. AQE transformations are not reflected.

[![SQL EXPLAIN](assets/aqe/05-sql-explain.png)](assets/aqe/05-sql-explain.png)
*SQL EXPLAIN output — static initial plan only; no AQE transformations.*

**Recognizing AQE transformations in the plan**

| AQE feature | Signal in plan |
|---|---|
| Sort-merge → broadcast hash join | Different physical join node vs initial plan |
| Partition coalescing | `CustomShuffleReader` with `Coalesced` property |
| Skew join | `SortMergeJoin` with `isSkew=true` |
| Empty relation propagation | `LocalTableScan` with empty relation field |

[![Join strategy string](assets/aqe/06-join-strategy-string.png)](assets/aqe/06-join-strategy-string.png)
*Join strategy change visible in plan string — different physical join node vs initial plan.*

### FAQ

**Q: Why didn't AQE broadcast a small table?**

Two reasons:
1. Join type doesn't support it (e.g., left relation of LEFT OUTER JOIN).
2. Too many empty partitions — sort-merge finishes fast anyway, or AQE skips broadcast when non-empty partition ratio falls below `spark.sql.adaptive.nonEmptyPartitionRatioForBroadcastJoin`.

**Q: Should I still use BROADCAST hints with AQE?**

Yes. Static hint is usually faster — AQE may shuffle both sides first before deciding to broadcast. "AQE will respect query hints the same way as static optimization does, but can still apply dynamic optimizations that are not affected by the hints."

**Q: AQE skew handling vs SKEW hint?**

Prefer AQE. Automatic, and generally performs better than the hint.

**Q: Why didn't AQE reorder my joins?**

Dynamic join reordering is not part of AQE.

**Q: Why didn't AQE detect my skew?**

Both size conditions must be met simultaneously. If skew is moderate (e.g., 3× median), AQE won't trigger — lower `skewedPartitionFactor`. Also check join type: LEFT OUTER JOIN only handles left-side skew.

### Legacy note

"Adaptive Execution" existed since Spark 1.6 but only did partition coalescing. The AQE in Spark 3.0 is fundamentally different — a full framework for dynamic planning and replanning based on runtime stats, supporting multiple optimization types and extensible to more.

## Quotes worth keeping

> "A statically planned broadcast join is usually more performant than a dynamically planned one by AQE as AQE might not switch to broadcast join until after performing shuffle for both sides of the join."

> "It is recommended to rely on AQE skew join handling rather than use the skew join hint, because AQE skew join is completely automatic and in general performs better than the hint counterpart."

> "Dynamic join reordering is not part of AQE."

> "For Structured Streaming, this configuration cannot be changed between query restarts from the same checkpoint location."

## Open questions

- What is the interaction between `spark.sql.autoBroadcastJoinThreshold` (static, 10 MB) and `spark.databricks.adaptive.autoBroadcastJoinThreshold` (AQE runtime, 30 MB)? Independent thresholds for different planning stages?
- What is the default value of `spark.sql.adaptive.nonEmptyPartitionRatioForBroadcastJoin`?

## Related sources

- [[sql-join-hints]] — BROADCAST hint beats AQE dynamic broadcast; REBALANCE hint requires AQE enabled
- [[optimize-data-workloads-guide]] — static `autoBroadcastJoinThreshold` (10 MB default, safe up to 200 MB); shuffle partition formula
- [[spark-memory-issues]] — large broadcast as OOM cause; reducing threshold or switching join type
- [[long-spark-stage-page]] — skew detection in Spark UI; AQE skew handling as the remedy
