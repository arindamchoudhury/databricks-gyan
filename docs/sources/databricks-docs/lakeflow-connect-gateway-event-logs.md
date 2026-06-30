# Monitor ingestion gateway progress with event logs

> **Source:** [docs.databricks.com/aws/en/ingestion/lakeflow-connect/gateway-event-logs](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/gateway-event-logs)
> **Added:** 2026-06-30
> **Source updated:** 2026-05-27
> **Tags:** lakeflow-connect, managed-connectors, ingestion, gateway, event-log, monitoring, cdc, snapshot, A3, A6
> **Type:** documentation

**Applies to:** SaaS connectors · Database connectors

Gateway event logs provide per-table metrics for both snapshot and CDC phases. Emitted at a configurable interval (default: every 5 minutes) for each table.

## How progress events work

Two event types, both at `level = 'METRICS'`:

| Event type | Applies to | What it reports |
|---|---|---|
| `flow_progress` | Snapshot + CDC flows | Row + byte **deltas** since last emission; resets to zero after each event. CDC flows also include latency metrics. |
| `operation_progress` | Snapshot flows only | Snapshot completion **%** (cumulative 0→100) + estimated time remaining. |

Flow name format encodes the phase:
- `{catalog}.{schema}.{table}_snapshot_flow` — initial load
- `{catalog}.{schema}.{table}_cdc_flow` — incremental CDC

Events are emitted even when no data changes occur — zero-update events serve as **liveness signals** distinguishing idle tables from unprocessed ones.

Events are available via the event log table only (not public APIs).

## Access

- UI: navigate to gateway → **Event log** tab
- SQL: `event_log('<pipeline-id>')`

## Key event fields

| Field | Type | Description |
|---|---|---|
| `event_type` | String | `flow_progress` or `operation_progress` |
| `level` | String | Always `METRICS` for progress events |
| `timestamp` | String | ISO 8601 emission time |
| `origin.pipeline_type` | String | Always `INGESTION_GATEWAY` |
| `origin.pipeline_name` | String | Gateway name |
| `origin.dataset_name` | String | Table being ingested |
| `origin.catalog_name` | String | UC catalog |
| `origin.schema_name` | String | UC schema |
| `origin.flow_name` | String | Phase identifier (`_snapshot_flow` or `_cdc_flow`) |
| `origin.ingestion_source_type` | String | e.g. `SQLSERVER`, `MYSQL`, `POSTGRESQL`, `ORACLE` |
| `details:flow_progress.metrics.num_upserted_rows` | Integer | Rows inserted/updated **since last event** (delta) |
| `details:flow_progress.metrics.num_deleted_rows` | Integer | Rows deleted **since last event** (delta); `null` for snapshot |
| `details:flow_progress.metrics.num_output_bytes` | Integer | Compressed bytes uploaded to volume **since last event** (delta) |
| `details:flow_progress.streaming_metrics.discovery_latency_ms` | Integer | Source commit → event emission latency (CDC only) |
| `details:flow_progress.streaming_metrics.batch_processing_time_ms` | Integer | Gateway read + upload time for last batch (CDC only; excludes source lag) |
| `details:flow_progress.streaming_metrics.event_time.max` | String | Most recent source change timestamp read by gateway (CDC only) |
| `details:operation_progress.status` | String | `IN_PROGRESS`, `COMPLETED`, `STARTED`, `CANCELED`, `FAILED` |
| `details:operation_progress.progress_percent` | Double | Snapshot completion % (0.0–100.0; cumulative, not delta) |
| `details:operation_progress.estimated_completion_ms` | Integer | Estimated ms remaining; decreases as snapshot progresses; `null` until enough data processed |
| `details:operation_progress.cdc_snapshot.target_table_name` | String | Fully qualified table being snapshotted |
| `maturity_level` | String | Always `STABLE` |

## Metric behavior

**Delta metrics** (`num_upserted_rows`, `num_deleted_rows`, `num_output_bytes`):
- Represent changes since last event — not cumulative totals
- Reset to zero after each emission
- Emitted even with zero updates (liveness signal)
- `num_deleted_rows` is `null` for snapshot flows

**Cumulative metric** (`progress_percent`):
- Accumulates 0.0 → 100.0 over snapshot lifetime
- Small tables may jump 0.0 → 100.0 in one emission (single chunk)
- Does not survive pipeline restart or refresh — resumes from last checkpoint

**Point-in-time metrics** (`discovery_latency_ms`, `batch_processing_time_ms`, `event_time.max`, `estimated_completion_ms`):
- Reflect state at emission time
- CDC flows only: `discovery_latency_ms`, `batch_processing_time_ms`, `event_time.max`
- Snapshot flows only: `estimated_completion_ms`
- Values reported as `0` if result would be negative

## Core queries

**flow_progress — row + byte counters:**

```sql
SELECT
  timestamp,
  CONCAT(origin.catalog_name, '.', origin.schema_name, '.', origin.dataset_name) AS table_name,
  details:flow_progress:metrics:num_upserted_rows::bigint AS rows_upserted,
  COALESCE(details:flow_progress:metrics:num_deleted_rows::bigint, 0) AS rows_deleted,
  details:flow_progress:metrics:num_output_bytes::bigint AS output_bytes,
  CASE
    WHEN origin.flow_name LIKE '%_snapshot_flow' THEN 'snapshot'
    WHEN origin.flow_name LIKE '%_cdc_flow' THEN 'cdc'
    ELSE 'unknown'
  END AS ingestion_phase
FROM event_log('<pipeline-id>')
WHERE event_type = 'flow_progress'
  AND level = 'METRICS'
  AND origin.pipeline_type = 'INGESTION_GATEWAY'
ORDER BY timestamp DESC
```

**operation_progress — snapshot % by table:**

```sql
SELECT
  timestamp,
  origin.flow_name AS flow_name,
  details:operation_progress:status::string AS status,
  details:operation_progress:progress_percent::double AS progress_pct
FROM event_log('<pipeline-id>')
WHERE event_type = 'operation_progress'
  AND level = 'METRICS'
  AND origin.pipeline_type = 'INGESTION_GATEWAY'
ORDER BY timestamp DESC
```

## Configure progress events

Progress events are enabled by default for all new gateways. Existing pipelines adopt the feature on next update or restart.

**Enable/disable:**

```json
"configuration": {
    "pipelines.gateway.progressEventsEnabled": "true"
}
```

**Adjust emission frequency:**

```json
"configuration": {
    "pipelines.gateway.progressEventEmitFrequencySeconds": "300"
}
```

Default: 300 seconds. Valid range: 30–3600 seconds. Controls both `flow_progress` and `operation_progress` cadence.

**Example gateway spec (Python):**

```python
gateway_pipeline_spec = {
   "pipeline_type": "INGESTION_GATEWAY",
   "name": "my_gateway_pipeline",
   "catalog": "main",
   "target": "my_schema",
   "continuous": True,
   "configuration": {
      "pipelines.gateway.progressEventsEnabled": "true",
      "pipelines.gateway.progressEventEmitFrequencySeconds": "300"
   },
}
```

## Metric availability

Snapshot ETA (`estimated_completion_ms`) and CDC latency (`streaming_metrics`) require the **May 2026 gateway image or later**. Databricks selects the image automatically — no manual config. All production regions have it as of May 2026.

**Verify support:**

```sql
SELECT
  MAX(CASE WHEN details:operation_progress:estimated_completion_ms IS NOT NULL
           THEN timestamp END) AS last_snapshot_eta,
  MAX(CASE WHEN details:flow_progress:streaming_metrics IS NOT NULL
           THEN timestamp END) AS last_cdc_latency
FROM event_log('<pipeline-id>')
WHERE event_type IN ('operation_progress', 'flow_progress')
  AND level = 'METRICS'
  AND timestamp >= current_timestamp() - INTERVAL 1 HOUR
```

If both columns have a recent timestamp (within one emission interval after restart), the gateway supports both features.

## CDC latency diagnosis

`discovery_latency_ms` vs `batch_processing_time_ms` tells you where latency is concentrated:

| Pattern | What it means |
|---|---|
| Both small | CDC is running and fresh |
| `discovery_latency_ms` high, `batch_processing_time_ms` low | Source-side lag (replication delay, log backlog, long-running source transactions) |
| Both high | Gateway-side lag (compute, network to UC volume) |
| `discovery_latency_ms` rising on one table only | Per-table source issue (DDL in flight, lock contention, blocked replication slot) |
| `discovery_latency_ms` rising on every table | Gateway-wide issue (resources, volume connectivity, source CDC log backlog) |
| `event_time.max` not advancing across emissions | Source is idle or gateway has lost source connectivity |

**Note:** `discovery_latency_ms` covers source → UC volume. To isolate source-side lag: `discovery_latency_ms - batch_processing_time_ms`. These are gateway latencies only — downstream applier latency (volume → destination table) is observed separately in the applier's event log.

**CDC freshness query (last 30 min, sorted by lag):**

```sql
SELECT
  origin.flow_name AS flow_name,
  details:flow_progress:streaming_metrics:event_time:max::string AS latest_source_commit_seen,
  details:flow_progress:streaming_metrics:discovery_latency_ms::bigint AS discovery_latency_ms,
  details:flow_progress:streaming_metrics:batch_processing_time_ms::bigint AS batch_processing_time_ms,
  timestamp AS emission_ts
FROM event_log('<pipeline-id>')
WHERE event_type = 'flow_progress'
  AND level = 'METRICS'
  AND origin.pipeline_type = 'INGESTION_GATEWAY'
  AND origin.flow_name LIKE '%_cdc_flow'
  AND details:flow_progress:streaming_metrics IS NOT NULL
  AND timestamp >= current_timestamp() - INTERVAL 30 MINUTES
ORDER BY discovery_latency_ms DESC NULLS LAST, flow_name, emission_ts DESC
```

## Key monitoring queries (sample)

The page includes a full **Ingestion Gateway Progress Monitor** notebook (import to workspace, specify gateway ID). Key query patterns:

**Overall snapshot progress (single-row summary):**

```sql
WITH latest_per_table AS (
  SELECT
    origin.flow_name AS flow_name,
    details:operation_progress:status::string AS status,
    details:operation_progress:progress_percent::double AS progress_pct,
    ROW_NUMBER() OVER (PARTITION BY origin.flow_name ORDER BY timestamp DESC) AS rn
  FROM event_log('<pipeline-id>')
  WHERE event_type = 'operation_progress'
    AND level = 'METRICS'
    AND origin.pipeline_type = 'INGESTION_GATEWAY'
)
SELECT
  COUNT(*) AS total_tables,
  SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) AS tables_completed,
  SUM(CASE WHEN status = 'IN_PROGRESS' AND progress_pct > 0 AND progress_pct < 100 THEN 1 ELSE 0 END) AS tables_in_progress,
  SUM(CASE WHEN progress_pct = 0 THEN 1 ELSE 0 END) AS tables_not_started,
  ROUND(AVG(progress_pct), 2) AS overall_progress_pct
FROM latest_per_table
WHERE rn = 1
```

**Stalled snapshot detection (no progress_percent change in 30 min):**

```sql
WITH latest_update AS (
  SELECT origin.update_id AS update_id
  FROM event_log('<pipeline-id>')
  WHERE event_type = 'create_update'
  ORDER BY timestamp DESC LIMIT 1
),
recent AS (
  SELECT
    origin.flow_name AS flow_name,
    details:operation_progress:progress_percent::double AS progress_pct,
    details:operation_progress:status::string AS status,
    timestamp
  FROM event_log('<pipeline-id>')
  WHERE event_type = 'operation_progress'
    AND level = 'METRICS'
    AND origin.pipeline_type = 'INGESTION_GATEWAY'
    AND origin.update_id = (SELECT update_id FROM latest_update)
    AND timestamp >= current_timestamp() - INTERVAL 30 MINUTES
)
SELECT
  flow_name,
  ROUND(MAX(progress_pct) - MIN(progress_pct), 2) AS pct_change_30min,
  COUNT(*) AS events_in_window,
  MAX(timestamp) AS last_event_ts
FROM recent
WHERE status = 'IN_PROGRESS'
GROUP BY flow_name
HAVING MAX(progress_pct) - MIN(progress_pct) = 0
   AND MAX(progress_pct) < 100
ORDER BY MAX(progress_pct) ASC
```

Other query patterns available on the page:

- Volume per table (upserts + deletes, last 24 h)
- Silent/stuck tables (zero upserts + deletes in last 60 min)
- Per-table timeline with cumulative totals (window function over `update_id`)
- Bytes per table (MB/GB, last 24 h)
- Throughput trend (MB per minute time series)
- Average bytes per row (LOB / wide-schema detection)
- Snapshot ETA per table (`estimated_completion_ms` from `operation_progress`)
- CDC latency time series (hourly avg `discovery_latency_ms` + `batch_processing_time_ms`)

## Troubleshooting

| Issue | Action |
|---|---|
| No progress events | Check `progressEventsEnabled = "true"`; wait one full interval after start; confirm pipeline is running; use `level = 'METRICS'` filter |
| Wrong frequency | Adjust `progressEventEmitFrequencySeconds` (30–3600 s) |
| Metrics reset to zero after restart | Expected — delta metrics are in-memory; reset on restart/refresh/resume |
| Missing metrics for some tables | Check table not filtered; CDC tables need CDC/change tracking enabled at source |
| Missing `estimated_completion_ms` or `streaming_metrics` | See "Metric availability" section — requires May 2026 gateway image |

[[lakeflow-connect-common-patterns]] · [[lakeflow-connect-managed]] · [[lakeflow-connect-full-refresh]]
