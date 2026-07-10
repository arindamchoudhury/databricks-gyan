# Schedule refreshes (standalone pipelines)

> **Source:** [docs.databricks.com — Schedule refreshes](https://docs.databricks.com/aws/en/ldp/dbsql/schedule-refreshes)
> **Added:** 2026-07-10
> **Source updated:** 2026-07-07
> **Tags:** lakeflow, declarative-pipelines, sdp, standalone-pipelines, materialized-view, streaming-table, trigger-on-update, schedule-cron, refresh, statement-timeout, serverless, performance-mode, I3, E8
> **Type:** documentation

Breadcrumb: Data engineering › Lakeflow Spark Declarative Pipelines › Standalone pipelines › Schedule refreshes. Expands the four-line trigger snippet in [[materialized-views]] into the full refresh-scheduling story for standalone MVs and streaming tables — limits, `ALTER`, timeout capture, notifications, and compute mode.

## Create a schedule

Four ways to drive a standalone pipeline's refresh:

| Method | Description | Example use case |
|---|---|---|
| Manual | On-demand refresh via a SQL `REFRESH` statement, or the workspace UI. | Development, testing, ad-hoc updates. |
| `TRIGGER ON UPDATE` | Refresh automatically when upstream data changes. | Production workloads with data-freshness SLAs or unpredictable refresh periods. |
| `SCHEDULE` | Refresh at defined time intervals. | Predictable, time-based refresh requirements. |
| SQL task in a job | Refresh orchestrated through Lakeflow Jobs. | Complex pipelines with cross-system dependencies. |

A schedule never blocks a manual refresh — you can always run one on demand.

## Manual refresh

```sql
REFRESH MATERIALIZED VIEW <table-name>;
```

For streaming tables, `REFRESH STREAMING TABLE`. In the UI: **Jobs & Pipelines** → select the pipeline → **Start**.

## Trigger on update

`TRIGGER ON UPDATE` refreshes the pipeline when upstream source data changes. It removes the need to coordinate schedules across pipelines — the pipeline monitors its source tables itself, so you don't need to know when upstream jobs finish. **This is the recommended approach for production workloads**, especially when upstream dependencies don't run on predictable schedules.

**Limitations — new, not captured anywhere before**

- **Upstream dependency limit:** max **10 upstream tables** and **30 upstream views** per pipeline. More than that → split the logic across multiple pipelines.
- **Workspace limit:** max **1,000 pipelines with `TRIGGER ON UPDATE`** per workspace. Contact support to raise.
- **Minimum trigger interval:** 1 minute.

```sql
CREATE OR REFRESH STREAMING TABLE catalog.schema.customer_orders
  TRIGGER ON UPDATE
AS SELECT
    o.customer_id,
    o.name,
    o.order_id
FROM catalog.schema.orders o;
```

**Throttle refresh frequency.** When sources update more often than consumers need, cap refresh rate with `AT MOST EVERY`. The `INTERVAL` keyword is required before the time value.

```sql
CREATE OR REFRESH STREAMING TABLE catalog.schema.customer_orders
  TRIGGER ON UPDATE AT MOST EVERY INTERVAL 5 MINUTES
AS SELECT
    o.customer_id,
    o.name,
    o.order_id
FROM catalog.schema.orders o;
```

## Scheduled refresh

Two syntaxes: `SCHEDULE EVERY` (simple intervals) and `SCHEDULE CRON` (precise). `SCHEDULE` and `SCHEDULE REFRESH` are semantically equivalent keywords.

**When a schedule is created, a Databricks job is automatically configured to process the update.** View it with `DESCRIBE EXTENDED`, or in Catalog Explorer under **Overview → Refresh status**.

`EVERY` supports **hour, day, and week** intervals only. Sub-hourly → use `SCHEDULE CRON`.

```sql
CREATE OR REPLACE MATERIALIZED VIEW catalog.schema.hourly_metrics
  SCHEDULE EVERY 1 HOUR
AS SELECT
    date_trunc('hour', event_time) AS hour,
    count(*) AS events
FROM catalog.schema.raw_events
GROUP BY 1;
```

```sql
CREATE OR REPLACE MATERIALIZED VIEW catalog.schema.regular_metrics
  SCHEDULE CRON '0 */15 * * * ?' AT TIME ZONE 'UTC'
AS SELECT
    date_trunc('minute', event_time) AS minute,
    count(*) AS events
FROM catalog.schema.raw_events
WHERE event_time > current_timestamp() - INTERVAL 1 HOUR
GROUP BY 1;
```

## SQL task in a job

Orchestrate the refresh from Lakeflow Jobs by putting a `REFRESH` command in a SQL task. Create it from the SQL Editor (write the command, click **Schedule**) or from the Jobs UI (new job → SQL task → attach a query or notebook).

```sql
REFRESH STREAMING TABLE catalog.schema.sales;
```

Use this when multi-step pipelines have cross-system dependencies, when it must integrate with existing job orchestration, or when job-level alerting/monitoring is needed.

**Cost note:** a SQL task uses **both** the SQL warehouse attached to the job **and** the serverless compute that executes the refresh. If definition-based scheduling would meet the requirement, `TRIGGER ON UPDATE` or `SCHEDULE` is the simpler (and cheaper) path.

## Add, modify, drop a schedule

```sql
-- Add a trigger to an existing table
ALTER STREAMING TABLE sales
  ADD TRIGGER ON UPDATE;

-- Change an existing schedule (EVERY has no minute interval → CRON for sub-hourly)
ALTER STREAMING TABLE catalog.schema.my_table
  ALTER SCHEDULE CRON '0 */5 * * * ?';

-- Remove it
ALTER STREAMING TABLE catalog.schema.my_table
  DROP SCHEDULE;
```

`ALTER SCHEDULE` / `ALTER TRIGGER ON UPDATE` covers every transition: schedule→schedule, trigger→trigger, and switching between a schedule and a trigger.

## Track, stop, and inspect refreshes

Status: the Pipelines UI, `DESCRIBE TABLE EXTENDED <table-name>` (Refresh Information), or Catalog Explorer. The dataset's tabs in Catalog Explorer show refresh status/history, schema, sample data (needs active compute), permissions, lineage, usage insights, and monitors.

Stop an active refresh: **Stop** on the Pipeline details page, the Databricks CLI, or `POST /api/2.0/pipelines/{pipeline_id}/stop`.

Run history: in Catalog Explorer, clicking the **Refresh schedule** link (e.g. "Every 1 hour") opens the **system-managed job** that runs the schedule — including a graph of the last 48 hours of runs. **You can't edit this job.** Change the schedule by editing the pipeline definition with `CREATE OR REFRESH` or `ALTER`.

## Timeouts for refreshes

**New — a real production gotcha.** For standalone pipelines created/updated **on or after 2025-08-14**, the timeout is *captured at the moment you run `CREATE OR REFRESH`*, resolved in this order:

1. `STATEMENT_TIMEOUT`, if set.
2. Otherwise, the timeout of the SQL warehouse that ran the command.
3. Otherwise, a default of **2 days**.

Streaming tables last updated **before 2025-08-14** are fixed at a 2-day timeout.

```sql
SET STATEMENT_TIMEOUT = '6h';

CREATE OR REFRESH MATERIALIZED VIEW my_catalog.my_schema.my_mv
  SCHEDULE EVERY 12 HOURS
AS SELECT * FROM large_source_table;
```

Refreshes every 12 hours; a refresh exceeding 6 hours times out and waits for the next scheduled run.

**How scheduled refreshes handle timeouts.** Timeouts sync **only** on an explicit `CREATE OR REFRESH`. Scheduled refreshes keep using the timeout captured at the most recent `CREATE OR REFRESH`, and **changing the warehouse timeout alone does not affect existing scheduled refreshes**. After changing a warehouse timeout, re-run `CREATE OR REFRESH` to apply it.

## Notifications for scheduled refreshes (Beta)

> 🧪 **Beta.** Workspace admins opt in via **Previews → System-Managed Job for Materialized Views & Streaming Tables**.

How you get notifications depends on how you scheduled:

- **Scheduled with a job** — edit the SQL task and add notifications (full Lakeflow Jobs notification options).
- **Scheduled with a `SCHEDULE` clause** — Catalog Explorer → dataset → **Overview → Refresh schedule** → edit → **More options** → notifications. Email on start, success, or failure. **Default: owner notified on failure only.** The email links to the run history of the system-managed job.

## Performance mode for scheduled refreshes (Beta)

> 🧪 **Beta**, same preview opt-in as notifications.

The compute mode of the underlying serverless pipeline depends on *how the refresh was invoked*:

| Invocation | Default performance mode |
|---|---|
| Interactively in the UI | Performance-optimized |
| Scheduled via a SQL task in a job | The job's **Performance optimized** setting |
| Scheduled via a `SCHEDULE` clause | **Standard** |

Standard mode reduces cost and accepts higher launch latency — serverless workloads typically start **within four to six minutes** of being triggered. Performance-optimized gives faster startup and execution. **Both modes use the same SKU; standard consumes fewer DBUs.**

To change it for `SCHEDULE`-clause pipelines: Catalog Explorer → dataset → **Overview → Refresh schedule** → edit → check **Performance optimized**.

> This is the same Standard vs Performance-Optimized DBU trade-off documented in [[serverless-pipelines]] — here it surfaces per-schedule, and the *default flips to Standard* the moment a refresh runs on a schedule rather than in the UI.

---
Related: [[materialized-views]] — its compact `TRIGGER ON UPDATE` / `SCHEDULE CRON` snippet is what this page expands; [[ldp-concepts-streaming-tables]] — the standalone streaming tables being scheduled here (and their auto-created `MV/ST` pipeline); [[ldp-concepts-pipelines]] — the `MV/ST` / `DBSQL` pipeline type that a standalone pipeline surfaces as; [[serverless-pipelines]] — the Standard vs Performance-Optimized compute modes this page exposes per-schedule.
