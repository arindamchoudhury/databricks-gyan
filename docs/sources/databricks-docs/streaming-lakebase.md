# Connect to Lakebase (Streaming Sink)

> **Source:** [docs.databricks.com/aws/en/structured-streaming/lakebase](https://docs.databricks.com/aws/en/structured-streaming/lakebase)
> **Added:** 2026-06-30
> **Source updated:** 2026-06-29
> **Tags:** structured-streaming, lakebase, postgresql, streaming-sink, ltap, E8, I2
> **Type:** documentation

**Status:** Public Preview

Structured Streaming sink for writing to Lakebase (PostgreSQL-compatible). Built-in batching, automatic retries, workspace-managed authentication — no custom `foreachBatch` needed.

**Reverse direction** (Lakebase → Delta): see Lakebase Change Data Feed.

## Requirements

- DBR 18+
- Classic compute (dedicated or standard access mode)
- **No serverless; no Lakeflow Spark Declarative Pipelines**

## Connection methods

### UC-registered Lakebase tables

Connector auto-manages credentials using the identity of the running user or service principal. Creates the table if it doesn't exist.

```python
df.writeStream \
    .outputMode("update") \
    .option("upsertkey", "<primary-key-column>")  # optional; inferred from PK if omitted
    .option("checkpointLocation", "/Volumes/<catalog>/<schema>/<volume>/<checkpoint-name>") \
    .toTable("<catalog>.<schema>.<table>")
```

### Non-UC Lakebase tables

Use `format("postgresql")` with explicit `endpoint` and `dbtable`. Also auto-manages credentials; creates table if not exists.

```python
df.writeStream \
    .format("postgresql") \
    .outputMode("update") \
    .option("endpoint", "<project-id>.<branch-id>.<endpoint-id>") \
    .option("database", "<database>")          # optional; defaults to databricks_postgres
    .option("dbtable", "<schema>.<table>") \
    .option("upsertkey", "<primary-key-column>")  # optional
    .option("checkpointLocation", "/Volumes/<catalog>/<schema>/<volume>/<checkpoint-name>") \
    .start()
```

`endpoint` format: `project_id.branch_id` or `project_id.branch_id.endpoint_id` (endpoint_id optional if branch has a single read-write endpoint).

## Configuration options

| Option | Default | Notes |
|---|---|---|
| `checkpointLocation` | — | **Required.** UC Volume path or cloud URI; unique per query |
| `batchsize` | 1000 | Max rows per database transaction |
| `batchinterval` | 100ms | Max time to buffer rows before flushing |
| `upsertkey` | (inferred) | Comma-separated PK columns; must match table's PRIMARY KEY exactly |
| `database` | `databricks_postgres` | Non-UC only; target PostgreSQL database |
| `dbtable` | — | Non-UC only; required; `schema.table` format |
| `endpoint` | — | Non-UC only; required |

Unrecognized options raise `JDBC_STREAMING_SINK_INVALID_OPTIONS`.

## Upsert behavior

- **Upsert key exists** (via `upsertkey` or inferred from PK): uses `INSERT INTO ... ON CONFLICT (...) DO UPDATE SET ...`
- **No upsert key**: plain inserts; output mode has no effect on behavior

**Upsert key constraints:**
- Must be a non-empty subset of DataFrame columns
- Must match the table's PRIMARY KEY exactly — mismatch fails the query
- Must be comparable types (numeric/string); complex/struct types not supported
- Sink sorts rows by upsert key within each batch to prevent deadlocks

**Table/schema naming:** simple identifiers only — letters, digits, underscores; no quoted identifiers, no hyphens.

## Performance tuning

**Flush triggers:** either `batchsize` reached or `batchinterval` exceeded (whichever comes first).

- Low-latency (real-time mode): decrease `batchinterval`
- High-throughput: increase `batchsize`

**Connection pooling:** 1 task per connection by default. Increasing `spark.databricks.sql.streaming.jdbc.tasksPerConnection` risks connection contention. If DB has a low connection limit, reduce shuffle partitions or increase `tasksPerConnection`.

**Auto-retry:** transient JDBC errors (connection failures, deadlocks, rate limiting). Exhausting retries fails the query.

**Backpressure:** propagated upstream when the database can't keep up.

## Supported triggers and output modes

**Triggers:** realTime ✓ · ProcessingTime ✓ · AvailableNow ✓ · Once ✓

**Output modes:** update ✓ · append ✓ (same behavior as update) · complete ✗

## Limitations

- Serverless compute not supported
- Lakeflow Spark Declarative Pipelines not supported
- Only Lakebase supported as write target — external PostgreSQL-compatible databases are **not** supported

[[structured-streaming-delta-lake]] · [[structured-streaming-foreach]]
