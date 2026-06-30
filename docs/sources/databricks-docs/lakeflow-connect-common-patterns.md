# Common patterns for managed ingestion pipelines

> **Source:** [docs.databricks.com/aws/en/ingestion/lakeflow-connect/common-patterns](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/common-patterns)
> **Added:** 2026-06-30
> **Source updated:** 2026-05-08
> **Tags:** lakeflow-connect, managed-connectors, ingestion, CDC, SCD2, column-selection, row-filtering, cost-monitoring, A3
> **Type:** documentation

Index page for advanced configuration techniques for Lakeflow Connect managed connector pipelines. Each pattern links to a dedicated sub-page.

> **Note:** Not all connectors support every pattern listed here. Check the connector-specific docs.

## Pattern index

| Pattern | Purpose |
|---|---|
| **Column selection** | Select or exclude specific columns during ingestion to reduce data volume and improve performance. |
| **Full refresh** | Force a complete reload of all data from the source system — use when schema changes or data corruption require re-sync. |
| **History tracking** | Track historical changes using Slowly Changing Dimension (SCD) Type 2 — maintains a full record of row-level changes over time. |
| **Monitor costs** | Use system tables to track pipeline costs and monitor usage patterns. |
| **Multi-destination pipelines** | Ingest data from a single source to multiple destination tables or catalogs in one pipeline. |
| **Pipeline maintenance** | Manage pipeline updates, pauses, and troubleshooting workflows. |
| **Pipeline tagging** | Apply tags for resource organization, ownership tracking, and cost attribution. |
| **Row filtering** | Filter rows during ingestion using SQL-like conditions — useful for excluding test data or restricting scope. |
| **Configure the Run as identity** | Set which identity's permissions the pipeline uses at runtime — important for UC access control. |
| **Source data lineage** | Track source table lineage so that source tables appear in UC end-to-end lineage views. |
| **Name destination tables** | Override the default destination table name (defaults to the source table name). Required when ingesting the same source object twice into the same schema, since duplicate names are not allowed. Also useful for naming conventions. |
| **TLS server certificate validation** | Configure TLS certificate validation for database connector pipelines to verify the source server's identity and prevent PITM attacks. |

## Key patterns for A3

**Column selection + row filtering** — reduce egress/compute early in the pipeline; filter at source rather than in downstream transforms.

**SCD Type 2 (history tracking)** — Lakeflow Connect's managed CDC can be configured to materialise full history, not just the current state.

**Multi-destination** — fan-out to multiple schemas/catalogs from one pipeline — avoids redundant source queries.

**Run as identity** — determines which user's UC privileges are checked when the pipeline reads/writes tables; must have READ on the source connection and WRITE on the destination schema.

**Source data lineage** — enables end-to-end UC lineage from the operational database through to the lakehouse. Requires the connector to be configured to emit lineage metadata.

[[lakeflow-connect-managed]] · [[lakeflow-connect-overview]]
