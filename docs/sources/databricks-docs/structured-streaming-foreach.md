# Use foreachBatch to write to arbitrary data sinks

> **Source:** [docs.databricks.com/aws/en/structured-streaming/foreach](https://docs.databricks.com/aws/en/structured-streaming/foreach)
> **Added:** 2026-06-30
> **Source updated:** 2026-06-29
> **Tags:** structured-streaming, foreach-batch, streaming, idempotency, dead-letter-queue, I2, I5
> **Type:** documentation

`streamingDF.writeStream.foreachBatch(fn)` applies a **batch function** to each micro-batch output of a streaming query. Function signature: `(batch_df: DataFrame, batch_id: int/long)`.

Required for **Delta MERGE operations** in Structured Streaming — see [[merge]].

## Delivery guarantee

**At-least-once** by default. For exactly-once: use `batchId` to deduplicate output (e.g. `txnAppId`/`txnVersion` for Delta).

## Key constraints

- Does **not** work with **continuous processing mode** — use `foreach()` instead
- With **stateful operators** (e.g. `dropDuplicatesWithinWatermark`): must completely consume each batch DataFrame or the query fails on the next batch

## Handle empty DataFrames

`foreachBatch()` can receive an empty DataFrame. Code must handle `isEmpty()` or the query may fail.

Two Delta sources of empty batches:
- `OPTIMIZE` runs on source with no files to process → empty micro-batch at sink
- Predicate pushdown / file pruning eliminates all records at physical plan level

```python
def process_batch(output_df, batch_id):
    if not output_df.isEmpty():
        # business logic
        pass

streamingDF.writeStream.foreachBatch(process_batch).start()
```

## DBR 14.0 behavior changes (Standard access mode)

- `print()` writes to driver logs (not notebook output)
- `dbutils.widgets` unavailable inside the function
- All files/modules/objects referenced must be serializable and available on Spark

## Write to multiple locations

Prefer **multiple Structured Streaming writers** (better parallelism/throughput). Using `foreachBatch` for multiple sinks serializes writes → increases micro-batch latency.

If using `foreachBatch` for multiple Delta tables, use `txnAppId`/`txnVersion` for idempotent writes.

## Completely consume each batch (stateful operators)

When using stateful operators, the entire batch DataFrame must be consumed. Partial consumption fails the query on the next batch.

Pattern — silently consume remainder after partial processing:

```python
def do_nothing(row):
    pass

def partial_func(batch_df, batch_id):
    batch_df.show(2)
    batch_df.foreach(do_nothing)  # consume remainder
```

## Error handling

**Recommended approach:** let errors propagate to the orchestration layer (Lakeflow Jobs, Apache Airflow) for retry. Complex retry logic inside `foreachBatch` risks data loss.

| Target | Guidance |
|---|---|
| Delta tables | Use `txnAppId` + `txnVersion` bound to `batchId`; do **not** catch/retry locally; let errors propagate so Spark metrics stay accurate |
| External destinations (APIs, OLTP, queues) | Implement own idempotency; assume any operation may be retried; safest = let errors propagate |

| Exception type | Examples | Action |
|---|---|---|
| Transient sink errors | `SQLTransientConnectionException`, HTTP 429, timeouts | Catch: retry or send to DLQ |
| Idempotent duplicate/key violations | `SQLIntegrityConstraintViolationException` | Catch: log and suppress |
| Custom retryable | Wrapped socket exceptions | Catch: increment metrics |
| Logic/schema errors | `NullPointerException`, `AttributeError`, schema mismatch | Propagate: fail the query |
| Non-retryable / uncaught bugs | `ValueError`, `PermissionError` | Propagate: fail the query |
| Critical failures | `OutOfMemoryError`, corrupted state | Propagate: fail the query |

## Dead-letter queue (DLQ) pattern

Split each micro-batch into valid and invalid records; route each to its own Delta table. Both writes use `txnVersion`/`txnAppId` for idempotency.

```python
from pyspark.sql.functions import current_timestamp, lit

main_table = "catalog.schema.orders"
dlq_table = "catalog.schema.orders_dlq"
app_id = "orders-streaming-job"

def process_orders(batch_df, batch_id):
    if batch_df.isEmpty():
        return

    valid_condition = "order_amount > 0 AND customer_id IS NOT NULL"

    batch_df.filter(valid_condition).write \
        .format("delta").mode("append") \
        .option("txnVersion", batch_id) \
        .option("txnAppId", app_id) \
        .saveAsTable(main_table)

    invalid_df = batch_df.filter(f"NOT ({valid_condition})")
    if not invalid_df.isEmpty():
        invalid_df \
            .withColumn("dlq_batch_id", lit(batch_id)) \
            .withColumn("dlq_ingest_time", current_timestamp()) \
            .write.format("delta").mode("append") \
            .option("txnVersion", batch_id) \
            .option("txnAppId", app_id) \
            .saveAsTable(dlq_table)

spark.readStream.format("delta").table("catalog.schema.raw_orders") \
    .writeStream.foreachBatch(process_orders) \
    .option("checkpointLocation", "/path/to/checkpoint") \
    .start()
```

[[merge]] · [[batch-vs-streaming]] · [[aggregation]]
