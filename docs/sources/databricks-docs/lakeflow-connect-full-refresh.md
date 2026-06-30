# Fully refresh target tables (Lakeflow Connect)

> **Source:** [docs.databricks.com/aws/en/ingestion/lakeflow-connect/full-refresh](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/full-refresh)
> **Added:** 2026-06-30
> **Source updated:** 2026-05-27
> **Tags:** lakeflow-connect, managed-connectors, full-refresh, cdc, ingestion, A3
> **Type:** documentation

**Applies to:** SaaS connectors · Database connectors · Query-based connectors

A full refresh clears data and state of target tables, then reprocesses all records from source. Can target all tables in the pipeline or a selected subset.

## Triggering a full refresh

| Interface | How |
|---|---|
| Lakehouse UI | Manually trigger a pipeline update |
| Pipelines API | `POST /api/2.0/pipelines/{pipeline_id}/updates` |
| Databricks CLI | `databricks pipelines start-update` |

> **IMPORTANT:** If a pipeline update fails during the Initializing or Resetting tables phase, Lakeflow Connect retries automatically. If you interrupt retries or they fail fatally, start a new update manually using the **same table refresh selection**. Otherwise target tables end up in an inconsistent state with partial data. If manual retries also fail, create a support ticket.

## Full refresh behavior (CDC)

**Applies to:** SaaS connectors · Database connectors

Databricks optimizes full refresh to minimize downtime:

1. **Snapshot request** — when you request a full refresh, the ingestion gateway immediately begins creating a snapshot of the source table. The destination streaming table is excluded from the refresh selection until the snapshot completes.
2. **Continued availability** — during the snapshot, the destination table retains existing data and remains queryable. No updates, appends, or deletes are applied while the snapshot is in progress.
3. **Atomic refresh** — after the snapshot completes, Databricks applies the full refresh in a single atomic update. This update applies all snapshot data plus any CDC records accumulated since the snapshot was requested.

**Example:** table has 50 records at end of update 15; full refresh requested in update 16:
- Gateway begins snapshot during update 16
- Table continues showing 50 records until snapshot completes
- When snapshot completes (update 16 or later, depending on source size), full refresh is applied atomically

This approach significantly reduces PENDING_RESET and timeout errors.

> **IMPORTANT:** Gateway snapshots can't be resumed. If you update the pipeline while a snapshot is in progress (e.g. adding new tables), the current snapshot is canceled and a new one starts. The new snapshot covers the union of tables from the canceled snapshot plus any newly added tables. Wait for the current snapshot to complete before updating the pipeline.

## Configure full refresh behavior for database connectors

**Applies to:** SaaS connectors · Database connectors

### Full refresh window

Schedule when snapshot operations for full refresh occur. When a full refresh is requested (manually or automatically), the snapshot waits until the next available time in the configured window.

**Scheduling behavior:**

| Request time | Window | Snapshot starts | Notes |
|---|---|---|---|
| Mon 2025-10-20 10:00 UTC | start_hour: 20, days: Tuesday, tz: UTC | Tue 2025-10-21 20:00 UTC | Deferred to next window day |
| Mon 2025-10-20 09:30 UTC | start_hour: 9, days: Monday, tz: UTC | Mon 2025-10-20 09:30 UTC | Request time within window |
| Mon 2025-10-20 10:00 UTC | start_hour: 9, days: Monday, tz: UTC | Mon 2025-10-27 09:00 UTC | Past window; deferred to next week |

**Parameters** (set in `ingestion_definition.full_refresh_window`):

| Parameter | Type | Description | Required |
|---|---|---|---|
| `start_hour` | Integer | Start hour for window (0-23, 24h) | Yes |
| `days_of_week` | Array | Days window is active. Valid: MONDAY…SUNDAY. Defaults to all days | No |
| `time_zone_id` | String | Time zone for window. Defaults to UTC | No |

**DABs (YAML)**

```yaml
resources:
  pipelines:
    gateway:
      name: <gateway-name>
      gateway_definition:
        connection_id: <connection-id>
        gateway_storage_catalog: <destination-catalog>
        gateway_storage_schema: <destination-schema>
        gateway_storage_name: <destination-schema>
      target: <destination-schema>
      catalog: <destination-catalog>

    pipeline_sqlserver:
      name: <pipeline-name>
      catalog: <destination-catalog>
      schema: <destination-schema>
      ingestion_definition:
        ingestion_gateway_id: <gateway-id>
        objects:
          - table:
              source_schema: <source-schema>
              source_table: <source-table>
              destination_catalog: <destination-catalog>
              destination_schema: <destination-schema>
        full_refresh_window:
          start_hour: 20
          days_of_week:
            - MONDAY
            - TUESDAY
          time_zone_id: 'America/Los_Angeles'
```

**Databricks notebook (Python)**

```python
gateway_pipeline_spec = {
  "pipeline_type": "INGESTION_GATEWAY",
  "name": "<gateway-name>",
  "catalog": "<destination-catalog>",
  "target": "<destination-schema>",
  "gateway_definition": {
    "connection_id": "<connection-id>",
    "gateway_storage_catalog": "<destination-catalog>",
    "gateway_storage_schema": "<destination-schema>",
    "gateway_storage_name": "<destination-schema>"
  }
}

ingestion_pipeline_spec = {
  "pipeline_type": "MANAGED_INGESTION",
  "name": "<pipeline-name>",
  "catalog": "<destination-catalog>",
  "schema": "<destination-schema>",
  "ingestion_definition": {
    "ingestion_gateway_id": "<gateway-pipeline-id>",
    "source_type": "SQLSERVER",
    "objects": [
      {
        "table": {
          "source_schema": "<source-schema>",
          "source_table": "<source-table>",
          "destination_catalog": "<destination-catalog>",
          "destination_schema": "<destination-schema>"
        }
      }
    ],
    "full_refresh_window": {
      "start_hour": 20,
      "days_of_week": ["MONDAY", "TUESDAY"],
      "time_zone_id": "America/Los_Angeles"
    }
  }
}
```

### Auto full refresh policy

Automatically triggers a full refresh when the pipeline encounters unsupported DDL operations:

- Table truncate
- Incompatible schema changes (e.g. data type changes)
- Column renames
- Column additions with default values

Without this enabled, you must manually trigger a full refresh for these cases.

**Parameters** (set in `table_configuration.auto_full_refresh_policy`):

| Parameter | Type | Description | Default |
|---|---|---|---|
| `enabled` | Boolean | Whether auto full refresh is enabled | `false` |
| `min_interval_hours` | Integer | Minimum wait between full refreshes (hours since last snapshot) | `24` |

Configure at pipeline level (`ingestion_definition.table_configuration`) or table level (`ingestion_definition.objects[].table.table_configuration`). Table-level overrides pipeline-level.

**Example: pipeline-level (all tables)**

DABs (YAML):

```yaml
        table_configuration:
          auto_full_refresh_policy:
            enabled: true
            min_interval_hours: 24
```

Notebook (Python) — inside `ingestion_definition`:

```python
    "table_configuration": {
      "auto_full_refresh_policy": {
        "enabled": True,
        "min_interval_hours": 24
      }
    }
```

**Example: mixed — pipeline enabled, one table disabled**

```yaml
        objects:
          - table:
              source_table: table_1
              # inherits pipeline-level policy (enabled)
          - table:
              source_table: table_2
              table_configuration:
                auto_full_refresh_policy:
                  enabled: false   # overrides pipeline-level
                  min_interval_hours: 24
        table_configuration:
          auto_full_refresh_policy:
            enabled: true
            min_interval_hours: 24
```

`table_1` uses the pipeline-level policy (enabled). `table_2` overrides with table-level config (disabled).

[[lakeflow-connect-common-patterns]] · [[lakeflow-connect-managed]]
