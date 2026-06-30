# Apply tags to managed ingestion pipelines (Lakeflow Connect)

> **Source:** [docs.databricks.com/aws/en/ingestion/lakeflow-connect/pipeline-tags](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/pipeline-tags)
> **Added:** 2026-06-30
> **Source updated:** 2026-05-06
> **Tags:** lakeflow-connect, managed-connectors, pipeline-tags, cost-attribution, A3
> **Type:** documentation

**Status:** Public Preview

**Applies to:** SaaS connectors · Database connectors · Query-based connectors

> **Tags vs serverless usage policies:** pipeline tags = metadata on the pipeline resource. Serverless usage policies = tags applied to serverless **compute billing records**. Two separate mechanisms. See *Attribute usage with serverless usage policies* for the billing side.

## How pipeline tags work

Tags are custom key-value pairs defined in the pipeline specification. Use cases:

- Group pipelines by environment, project, or team
- Identify the owner (team or individual) of a pipeline
- Associate usage with cost centers or budgets
- Filter and automate operations by tag value

Tags **propagate to system tables and billing records**, enabling joins between pipeline metadata and usage data (see [[lakeflow-connect-monitor-costs]] for the `custom_tags[:key]` billing query pattern).

## Add or update pipeline tags

Set a `tags` object in the pipeline spec. API/CLI only — no DABs YAML example in the docs.

```json
{
  "name": "sales-data-pipeline",
  "catalog": "prod",
  "target": "sales",
  "serverless": true,
  "tags": {
    "environment": "production",
    "owner": "data-engineering-team",
    "costcenter": "engineering-analytics",
    "project": "sales-analytics"
  },
  "ingestion_definition": {
    "connection_name": "salesforce-prod",
    "objects": [
      {
        "table": {
          "source_schema": "salesforce",
          "source_table": "Account",
          "destination_catalog": "prod",
          "destination_schema": "sales",
          "table_configuration": {
            "scd_type": "SCD_TYPE_1"
          }
        }
      }
    ]
  }
}
```

## View pipeline tags

Query `system.lakeflow.pipelines` (see Jobs system table reference).

[[lakeflow-connect-common-patterns]] · [[lakeflow-connect-monitor-costs]] · [[lakeflow-connect-pipeline-maintenance]]
