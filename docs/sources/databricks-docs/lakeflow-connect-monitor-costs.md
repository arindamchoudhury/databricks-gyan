# Monitor managed ingestion pipeline cost

> **Source:** [docs.databricks.com/aws/en/ingestion/lakeflow-connect/monitor-costs](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/monitor-costs)
> **Added:** 2026-06-30
> **Source updated:** 2026-05-20
> **Tags:** lakeflow-connect, managed-connectors, cost-monitoring, system-tables, billing, dbu, A3, A6
> **Type:** documentation

**Applies to:** SaaS connectors · Database connectors · Query-based connectors

Cost data lives in `system.billing.usage`. Filter on `billing_origin_product = 'LAKEFLOW_CONNECT'`.

## Billing parameters

| Parameter | Value |
|---|---|
| `billing_origin_product` | `LAKEFLOW_CONNECT` for all managed connector usage |
| `usage_type` | `COMPUTE_TIME` |
| `usage_unit` | `MILLISECOND` (raw compute time) and `DBU` (pricing unit) |

**`usage_metadata` struct fields:**

| Field | Description |
|---|---|
| `dlt_pipeline_id` | Unique identifier for the ingestion pipeline |
| `uc_table_catalog` | Destination table catalog |
| `uc_table_schema` | Destination table schema |
| `uc_table_name` | Destination table name |

## Pipeline maintenance charges

Managed ingestion pipelines incur **maintenance charges** even when not actively ingesting data — similar to Lakeflow Spark Declarative Pipelines. These cover pipeline infrastructure, metadata management, and change tracking between runs.

Separate maintenance from processing costs by analyzing hourly usage patterns (see query below; threshold: 0.1 DBU/hour).

## Operationalize billing data

Databricks recommends **AI/BI dashboards** for cost monitoring. Account admins can import a pre-built customizable cost monitoring dashboard. Alerts can be added to queries. See *Usage dashboards* and *Create an alert* in Databricks docs.

## Sample queries

All queries filter on `billing_origin_product = 'LAKEFLOW_CONNECT'`.

**Monthly total DBU consumption:**

```sql
SELECT
  usage_date,
  SUM(usage_quantity) AS total_dbus
FROM system.billing.usage
WHERE
  billing_origin_product = 'LAKEFLOW_CONNECT'
  AND MONTH(usage_date) = MONTH(NOW())
  AND YEAR(usage_date) = YEAR(NOW())
GROUP BY usage_date
ORDER BY usage_date DESC
```

**Most expensive pipelines (last 30 days):**

Joins `system.lakeflow.pipelines` to resolve pipeline names.

```sql
WITH ranked_pipelines AS (
  SELECT
    u.usage_metadata.dlt_pipeline_id AS pipeline_id,
    p.name AS pipeline_name,
    SUM(u.usage_quantity) AS total_dbus,
    COUNT(DISTINCT u.usage_date) AS days_active
  FROM system.billing.usage u
  JOIN system.lakeflow.pipelines p
    ON u.usage_metadata.dlt_pipeline_id = p.pipeline_id
  WHERE
    u.billing_origin_product = 'LAKEFLOW_CONNECT'
    AND u.usage_date >= DATE_SUB(NOW(), 30)
  GROUP BY pipeline_id, pipeline_name
)
SELECT
  pipeline_name,
  pipeline_id,
  total_dbus,
  days_active,
  ROUND(total_dbus / days_active, 2) AS avg_daily_dbus
FROM ranked_pipelines
ORDER BY total_dbus DESC
LIMIT 20
```

**Cost trend for a specific pipeline (last 90 days):**

Pipeline ID found on the Pipeline Details tab in the Lakeflow Pipelines UI.

```sql
SELECT
  usage_date,
  SUM(usage_quantity) AS daily_dbus,
  COUNT(*) AS usage_events
FROM system.billing.usage
WHERE
  usage_metadata.dlt_pipeline_id = :dlt_pipeline_id
  AND billing_origin_product = 'LAKEFLOW_CONNECT'
  AND usage_date >= DATE_SUB(NOW(), 90)
GROUP BY usage_date
ORDER BY usage_date ASC
```

**Per-pipeline dollar cost (last 30 days):**

Joins `system.billing.list_prices` to compute estimated dollar cost.

```sql
SELECT
  u.usage_date,
  p.name AS pipeline_name,
  SUM(u.usage_quantity) AS daily_dbus,
  SUM(u.usage_quantity * lp.pricing.effective_list.default) AS estimated_cost
FROM system.billing.usage u
JOIN system.lakeflow.pipelines p
  ON u.usage_metadata.dlt_pipeline_id = p.pipeline_id
JOIN system.billing.list_prices lp
  ON lp.sku_name = u.sku_name
WHERE
  u.usage_metadata.dlt_pipeline_id = :pipeline_id
  AND u.billing_origin_product = 'LAKEFLOW_CONNECT'
  AND u.usage_end_time >= lp.price_start_time
  AND (lp.price_end_time IS NULL OR u.usage_end_time < lp.price_end_time)
  AND u.usage_date >= DATE_SUB(NOW(), 30)
GROUP BY u.usage_date, pipeline_name
ORDER BY u.usage_date DESC
```

**Cost by usage policy / budget tag:**

Usage policy tagging for managed ingestion pipelines is **API-only**.

```sql
SELECT
  custom_tags[:key] AS tag_value,
  usage_date,
  SUM(usage_quantity) AS daily_dbus
FROM system.billing.usage
WHERE
  billing_origin_product = 'LAKEFLOW_CONNECT'
  AND custom_tags[:key] = :value
  AND usage_date >= DATE_SUB(NOW(), 30)
GROUP BY tag_value, usage_date
ORDER BY usage_date DESC
```

**Maintenance vs processing cost:**

Threshold of 0.1 DBU/hour distinguishes maintenance from active processing. Adjust per pipeline characteristics.

```sql
WITH hourly_usage AS (
  SELECT
    usage_metadata.dlt_pipeline_id AS pipeline_id,
    DATE_TRUNC('hour', usage_start_time) AS usage_hour,
    SUM(usage_quantity) AS hourly_dbus
  FROM system.billing.usage
  WHERE
    billing_origin_product = 'LAKEFLOW_CONNECT'
    AND usage_date >= DATE_SUB(NOW(), 30)
  GROUP BY pipeline_id, usage_hour
)
SELECT
  pipeline_id,
  SUM(CASE WHEN hourly_dbus > 0.1 THEN hourly_dbus ELSE 0 END) AS processing_dbus,
  SUM(CASE WHEN hourly_dbus <= 0.1 THEN hourly_dbus ELSE 0 END) AS maintenance_dbus,
  SUM(hourly_dbus) AS total_dbus
FROM hourly_usage
GROUP BY pipeline_id
ORDER BY total_dbus DESC
```

**Month-over-month cost growth:**

```sql
SELECT
  after.pipeline_id,
  after.pipeline_name,
  before_dbus,
  after_dbus,
  ROUND(((after_dbus - before_dbus) / NULLIF(before_dbus, 0) * 100), 2) AS growth_rate
FROM
  (SELECT u.usage_metadata.dlt_pipeline_id AS pipeline_id, p.name AS pipeline_name,
          SUM(u.usage_quantity) AS before_dbus
   FROM system.billing.usage u
   JOIN system.lakeflow.pipelines p ON u.usage_metadata.dlt_pipeline_id = p.pipeline_id
   WHERE u.billing_origin_product = 'LAKEFLOW_CONNECT'
     AND u.usage_date BETWEEN DATE_SUB(NOW(), 60) AND DATE_SUB(NOW(), 30)
   GROUP BY pipeline_id, pipeline_name) AS before
JOIN
  (SELECT u.usage_metadata.dlt_pipeline_id AS pipeline_id, p.name AS pipeline_name,
          SUM(u.usage_quantity) AS after_dbus
   FROM system.billing.usage u
   JOIN system.lakeflow.pipelines p ON u.usage_metadata.dlt_pipeline_id = p.pipeline_id
   WHERE u.billing_origin_product = 'LAKEFLOW_CONNECT'
     AND u.usage_date >= DATE_SUB(NOW(), 30)
   GROUP BY pipeline_id, pipeline_name) AS after
  ON before.pipeline_id = after.pipeline_id
WHERE after_dbus > before_dbus
ORDER BY growth_rate DESC
```

**Dollar cost for previous month:**

```sql
SELECT
  DATE_TRUNC('day', u.usage_date) AS usage_day,
  SUM(u.usage_quantity * lp.pricing.effective_list.default) AS estimated_cost
FROM system.billing.usage u
JOIN system.billing.list_prices lp ON lp.sku_name = u.sku_name
WHERE
  u.billing_origin_product = 'LAKEFLOW_CONNECT'
  AND u.usage_end_time >= lp.price_start_time
  AND (lp.price_end_time IS NULL OR u.usage_end_time < lp.price_end_time)
  AND u.usage_date >= ADD_MONTHS(DATE_TRUNC('month', CURRENT_DATE), -1)
  AND u.usage_date < DATE_TRUNC('month', CURRENT_DATE)
GROUP BY usage_day
ORDER BY usage_day ASC
```

**Cost by destination catalog/schema:**

```sql
SELECT
  usage_metadata.uc_table_catalog AS catalog_name,
  usage_metadata.uc_table_schema AS schema_name,
  COUNT(DISTINCT usage_metadata.dlt_pipeline_id) AS pipeline_count,
  SUM(usage_quantity) AS total_dbus
FROM system.billing.usage
WHERE
  billing_origin_product = 'LAKEFLOW_CONNECT'
  AND usage_metadata.uc_table_catalog IS NOT NULL
  AND usage_date >= DATE_SUB(NOW(), 30)
GROUP BY catalog_name, schema_name
ORDER BY total_dbus DESC
```

[[lakeflow-connect-common-patterns]] · [[lakeflow-connect-managed]]
