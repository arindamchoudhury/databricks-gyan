# Managed connectors in Lakeflow Connect

> **Source:** [docs.databricks.com/aws/en/ingestion/lakeflow-connect](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/)
> **Added:** 2026-06-29
> **Source updated:** 2026-06-09
> **Tags:** ingestion, lakeflow-connect, managed-connectors, cdc, saas, database, kafka, streaming, query-based, file-connectors, serverless, A3
> **Type:** documentation

Managed connectors are fully-managed ingestion pipelines governed by Unity Catalog and powered by serverless compute + Lakeflow Spark Declarative Pipelines. They handle incremental reads/writes, automated retries, schema evolution, and source-specific edge cases so you don't have to.

## Connector types

| Type | Sources | CDC required? |
|---|---|---|
| **Database connectors (CDC)** | MySQL, PostgreSQL, SQL Server | Yes — requires gateway + staging storage |
| **Query-based connectors** | Databases (schedule-based queries) | No — queries source directly on a schedule |
| **SaaS connectors** | Salesforce, HubSpot, Jira, Workday, and more | No — cursor-column or API-based |
| **File source connectors** | Google Drive, SharePoint | No |
| **Streaming connectors** | RabbitMQ and other message buses | No — continuous reads |
| **Community connectors** | Community-built, no Databricks SLA | Varies |

## Architecture by connector type

**SaaS / Query-based / Streaming / File connectors:**
- **Connection** — UC securable object storing auth credentials
- **Ingestion pipeline** — SDP pipeline on serverless compute
- **Destination tables** — streaming tables in UC

**Database connectors (CDC):**
- All of the above, plus:
- **Ingestion gateway** — runs as a continuous-task Lakeflow Job; captures changes from the source
- **Staging storage** — holds change events between gateway and pipeline

The gateway runs in its own dedicated job separate from the ingestion pipeline job.

## Orchestration

Custom schedules on the ingestion pipeline auto-create Lakeflow Jobs. The ingestion pipeline is a task within that job; you can add more tasks. Database connector gateways run in a separate continuous-task job.

## Incremental ingestion

First run: full load. Subsequent runs: only changed data. The mechanism depends on the source:
- SQL Server: change tracking and/or CDC
- Salesforce: cursor column from a fixed set of options
- Some sources/tables don't yet support incremental ingestion

## Networking

- SaaS connectors: reach source APIs directly; compatible with serverless egress controls
- Cloud databases: Private Link, or VNet/VPC peering
- On-premises databases: AWS Direct Connect / Azure ExpressRoute

## Deployment

Deploy with **Declarative Automation Bundles (DABs)** via the Databricks CLI — enables source control, CI/CD, and multi-environment (dev/staging/prod) deployment.

## Failure recovery and monitoring

Automatic retries with exponential backoff. On errors requiring manual intervention (e.g. expired credentials), the connector stores the last cursor position and resumes from there on the next run.

Monitoring: event logs, cluster logs, pipeline health/quality metrics. Track costs via `system.billing.usage`. Database gateway progress visible via event logs.

## Dependency disclaimer

Databricks may discontinue a connector if the underlying external service changes in ways that make maintenance impractical.

[lakeflow-connect-overview](lakeflow-connect-overview/) · [serverless-pipelines](serverless-pipelines/) · [what-is-cdc](what-is-cdc/)
