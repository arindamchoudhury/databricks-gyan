# Select rows to ingest — row filtering (Lakeflow Connect)

> **Source:** [docs.databricks.com/aws/en/ingestion/lakeflow-connect/row-filtering](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/row-filtering)
> **Added:** 2026-06-30
> **Source updated:** 2026-06-15
> **Tags:** lakeflow-connect, managed-connectors, row-filtering, ingestion, A3
> **Type:** documentation

**Status:** Beta — requires `"channel": "PREVIEW"` in pipeline spec.

**Applies to:** SaaS connectors · Database connectors · Query-based connectors

Row filtering ingests only matching rows using a SQL WHERE-like expression in `table_configuration.row_filter`. Improves performance on initial loads with historical data; reduces data duplication in dev environments.

Row filtering applies during **both the initial load and subsequent incremental updates**.

> **Not the same as UC row filters.** UC row filters (A4) restrict access to rows in destination Delta tables. This feature filters which rows are fetched from the source during ingestion — different layer, different purpose.

## Supported connectors

Not all managed connectors support row filtering. Supported:

- **SaaS:** Google Analytics, Salesforce, ServiceNow
- **Query-based:** Oracle, Teradata, SQL Server, MySQL, MariaDB, PostgreSQL

Database connectors (CDC via gateway) are **not** listed as supported.

## Configure row filtering

Add `row_filter` inside `table_configuration` on each `table` object. Pipeline must use `"channel": "PREVIEW"`.

```python
pipeline_spec = """
{
  "name": "...",
  "ingestion_definition": {
    "connection_name": "...",
    "objects": [
      {
        "table": {
          "source_schema": "...",
          "source_table": "...",
          "destination_catalog": "...",
          "destination_schema": "...",
          "destination_table": "...",
          "table_configuration": {
            "row_filter": "..."
          }
        }
      }
    ]
  },
  "channel": "PREVIEW"
}
"""
create_pipeline(pipeline_spec)
```

## Supported operators

| Operator | Supported |
|---|---|
| `AND` | Yes |
| `OR` | Salesforce and Google Analytics only |
| `=` | Yes |
| `!=` | Yes |
| `<` `<=` | Yes |
| `>` `>=` | Yes |
| `LIKE` | No |
| `IN` | No |

## Limitations by connector

**Salesforce**

Row filtering supported on two columns only:
1. Primary key (`ID`, if available)
2. Cursor column — selected in this preference order: `SystemModstamp` → `LastModifiedDate` → `CreatedDate` → `LoginTime`

**ServiceNow**

- `OR` not supported — `AND` only
- Timestamp format in filters must be `YYYY-MM-DD HH:mm:SS` (e.g. `2004-03-02 17:14:59`)
- Reference field filters: compare the `.value` subfield to `sys_id` of the referenced record (e.g. `assigned_to.value = '5137153cc611227c000bbd1bd8cd2005'`). **Applied post-fetch** (not server-side) — source data volume is not reduced by reference field filters

**Timestamp column filters (all connectors)**

- Row filtering only works for **incrementally updated** tables, not batch-updated tables
- Filtering applies **on write only**, not on read

## Edge cases — row/query updates

| Scenario | Behavior | Full refresh needed? |
|---|---|---|
| Row fails to match on initial load → later updated to match | Ingested on next pipeline update | No |
| Row matches on initial load → later updated to not match | **Not deleted** from destination | No |
| Query updated → previously uningested row now matches | **Not ingested** | **Yes** |
| Query updated → previously ingested row no longer matches | **Not deleted** from destination | No |

Key implication: **changing the `row_filter` expression does not retroactively clean up the destination.** Rows that were ingested under an old filter stay in the table even if they no longer match. A full refresh is needed only when you want to capture rows that previously didn't match (and still exist in source).

## Examples

**Salesforce** — ingest after a system timestamp, or a specific row:

```json
"row_filter": "SystemModstamp > '2025-06-10T23:40:11.000-07:00'"
"row_filter": "Id = 'a00Qy00000vps2NIAQ'"
```

**Google Analytics** — numeric columns must use **unquoted** literals; quoted numerics prevent server-side filtering (slow initial load):

```json
"row_filter": "event_timestamp >= 1712224270703246"
"row_filter": "event_date = '2025-01-01'"
"row_filter": "is_active_user = TRUE"
"row_filter": "platform != 'WEB'"
"row_filter": "event_timestamp >= 1712224270703246 AND (platform != 'WEB' OR is_active_user = FALSE)"
```

**ServiceNow** — timestamps quoted; reference field via `.value`:

```json
"row_filter": "sys_updated_on > '2004-03-02 17:14:59'"
"row_filter": "u_active = TRUE AND u_name = 'johnsmith'"
"row_filter": "assigned_to.value = '5137153cc611227c000bbd1bd8cd2005'"
```

[[lakeflow-connect-common-patterns]] · [[lakeflow-connect-column-selection]] · [[lakeflow-connect-full-refresh]]
