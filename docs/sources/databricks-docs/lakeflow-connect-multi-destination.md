# Create multi-destination pipelines (Lakeflow Connect)

> **Source:** [docs.databricks.com/aws/en/ingestion/lakeflow-connect/multi-destination-pipeline](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/multi-destination-pipeline)
> **Added:** 2026-06-30
> **Source updated:** 2026-05-06
> **Tags:** lakeflow-connect, managed-connectors, ingestion, multi-destination, fan-out, destination-table, A3
> **Type:** documentation

**Applies to:** SaaS connectors · Database connectors · Query-based connectors

One pipeline can write to **multiple destination catalogs and schemas** — and ingest the same object multiple times to different targets. Constraint: duplicate table names in the **same** destination schema are not allowed; use `destination_table` to give one of them a unique name.

> **Key distinction:** the top-level `catalog`/`schema` on the pipeline resource is the **event log location**, not the default destination. Each `table`/`report` object must specify its own `destination_catalog` and `destination_schema`.

## Example 1: Two objects into different schemas

### Google Analytics (SaaS)

```yaml
resources:
  pipelines:
    pipeline_ga4:
      name: <pipeline-name>
      catalog: <target-catalog-1>   # event log location
      schema: <target-schema-1>     # event log location
      ingestion_definition:
        connection_name: <connection-name>
        objects:
          - table:
              source_url: <project-1-id>
              source_schema: <property-name>
              destination_catalog: <target-catalog-1>
              destination_schema: <target-schema-1>
          - table:
              source_url: <project-2-id>
              source_schema: <property-name>
              destination_catalog: <target-catalog-2>
              destination_schema: <target-schema-2>
```

### MySQL (database connector — requires gateway)

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

    pipeline_mysql:
      name: <pipeline-name>
      catalog: <target-catalog-1>   # event log location
      schema: <target-schema-1>     # event log location
      ingestion_definition:
        ingestion_gateway_id: ${resources.pipelines.gateway.id}
        objects:
          - table:
              source_schema: <source-schema-1>
              source_table: <source-table-1>
              destination_catalog: <target-catalog-1>
              destination_schema: <target-schema-1>
          - table:
              source_schema: <source-schema-2>
              source_table: <source-table-2>
              destination_catalog: <target-catalog-2>
              destination_schema: <target-schema-2>
```

### Salesforce / SQL Server / Workday

Same pattern — list multiple `table` (or `report` for Workday) objects, each with its own `destination_catalog` / `destination_schema`.

## Example 2: One object ingested three times

When the third copy lands in the **same schema** as another copy, a duplicate table name would result. Specify `destination_table` to rename it.

### Google Analytics

```yaml
      ingestion_definition:
        connection_name: <connection-name>
        objects:
          - table:
              source_url: <project-id>
              source_schema: <property-name>
              destination_catalog: <target-catalog-1>
              destination_schema: <target-schema-1>    # first copy
          - table:
              source_url: <project-id>
              source_schema: <property-name>
              destination_catalog: <target-catalog-2>
              destination_schema: <target-schema-2>    # second copy
          - table:
              source_url: <project-id>
              source_schema: <property-name>
              destination_catalog: <target-catalog-2>
              destination_schema: <target-schema-2>    # third copy — same schema as second
              destination_table: <custom-target-table-name>   # required to avoid duplicate
```

### MySQL

```yaml
      ingestion_definition:
        ingestion_gateway_id: ${resources.pipelines.gateway.id}
        objects:
          - table:
              source_catalog: <source-catalog>
              source_schema: <source-schema>
              source_table: <source-table>
              destination_catalog: <destination-catalog-1>
              destination_schema: <destination-schema-1>    # first copy
          - table:
              source_catalog: <source-catalog>
              source_schema: <source-schema>
              source_table: <source-table>
              destination_catalog: <destination-catalog-2>
              destination_schema: <destination-schema-2>    # second copy
          - table:
              source_catalog: <source-catalog>
              source_schema: <source-schema>
              source_table: <source-table>
              destination_catalog: <destination-catalog-2>
              destination_schema: <destination-schema-2>    # third copy — same schema
              destination_table: <custom-destination-table-name>   # required
```

[[lakeflow-connect-common-patterns]] · [[lakeflow-connect-managed]]
