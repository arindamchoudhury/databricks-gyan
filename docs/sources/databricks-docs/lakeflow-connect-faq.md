# Managed connector FAQs (Lakeflow Connect)

> **Source:** [docs.databricks.com/aws/en/ingestion/lakeflow-connect/faq](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/faq)
> **Added:** 2026-06-30
> **Source updated:** 2026-06-24
> **Tags:** lakeflow-connect, managed-connectors, faq, schema-evolution, pricing, A3
> **Type:** documentation

## Supported connectors

GA managed connectors: Salesforce, SQL Server, ServiceNow, Google Analytics (+ Workday, implied by pricing section). For Private Preview connectors, contact account team.

## Interfaces

All managed connectors support **API** and **DABs**. UI support varies — three entry points where supported:

- Add data page (Data Ingestion)
- Jobs & Pipelines page (Create new → Ingestion pipeline)
- Tasks pane (Add task → + New ingestion pipeline or Type → Pipeline)

## Schema evolution

| Event | Behavior |
|---|---|
| New column appears in source | Auto-ingested on next run; prior rows get NULL |
| Column deleted from source | Set to **inactive** in destination (not dropped) |
| Same-name column appears after deletion | **Pipeline fails** — full refresh or manually drop the inactive column |
| New table (schema ingestion mode) | Auto-ingested unless opted out |
| Table deleted from source | Set to inactive in destination |

**Connector differences:**
- Salesforce column rename = delete + add (automatic, no action needed)
- SQL Server column rename = requires **full refresh** of affected tables

Opt out of automated new-column ingestion: list specific columns via API, or disable "any future columns" in the UI.

## Customization limits

Can customize: ingested objects, destination, schedule, permissions, notifications.

**Cannot** customize the ingestion process itself — it's fully managed. For custom logic: use Lakeflow Spark Declarative Pipelines or Structured Streaming.

## Managed connectors vs Lakehouse Federation vs OpenSharing

| Scenario | Choose |
|---|---|
| Avoid data duplication | OpenSharing |
| Query freshest possible data | OpenSharing |
| Ad hoc reporting / PoC on ETL pipelines | Lakehouse Federation |
| Incremental ingestion from SaaS/DB sources | Managed connectors |

## Managed connectors vs Auto Loader

- **Managed connectors** — SaaS (Salesforce) and DB (SQL Server) sources; fully-managed ingestion pipelines
- **Auto Loader** — cloud object storage (S3/ADLS/GCS); incrementally ingests files as they arrive; works with Structured Streaming + SDP; **not** fully managed (no pipeline management layer)

## Multi-destination and API-only gotcha

Multi-destination pipelines (write to multiple destination schemas) are supported. However: **once a pipeline uses multi-destination, it becomes API-only** — it can no longer be edited in the UI.

See [[lakeflow-connect-multi-destination]].

## Concurrent pipeline updates

If update N is still running when update N+1 is scheduled → N+1 is **skipped**. Next run is N+2 (assuming N completed by then).

## Pipeline deletion

Deleting an ingestion pipeline **drops the destination tables**. Irreversible.

## ALTER on managed-pipeline destination tables

Allowed (`ALTER STREAMING TABLE` / `ALTER MATERIALIZED VIEW`):

```sql
ALTER MATERIALIZED VIEW view_name | ALTER STREAMING TABLE table_name
{
    ALTER COLUMN column_clause |
    SET ROW FILTER clause |
    DROP ROW FILTER |
    SET TAGS clause |
    UNSET TAGS clause
}

column_clause
{
    column_identifier
    COMMENT clause |
    SET MASK clause |
    DROP MASK |
    SET TAGS clause |
    UNSET TAGS clause
}
```

**Not** allowed via ALTER: schedule or trigger — use *Update the pipeline schedule* instead (see [[lakeflow-connect-pipeline-maintenance]]).

## Pricing

| Source type | Compute | DBU type |
|---|---|---|
| SaaS (Salesforce, Workday) | **Serverless only** | Serverless SDP DBUs |
| Database (SQL Server) | Gateway: classic or serverless; pipeline: serverless | Both classic + serverless SDP DBUs possible |

Rates: see Lakeflow Spark Declarative Pipelines pricing page.

## Ingestion gateway + serverless-only workspaces

**No** — gateways require classic compute. Cannot deploy a gateway in a workspace that has no classic compute support. Applies to database (CDC) connectors only.

## CDF on destination tables

Delta Lake change data feed is **enabled automatically** on all destination tables.

[[lakeflow-connect-common-patterns]] · [[lakeflow-connect-managed]] · [[lakeflow-connect-multi-destination]] · [[lakeflow-connect-pipeline-maintenance]] · [[lakeflow-connect-row-filtering]]
