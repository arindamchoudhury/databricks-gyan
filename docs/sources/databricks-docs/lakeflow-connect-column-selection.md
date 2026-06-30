# Select columns to ingest (Lakeflow Connect)

> **Source:** [docs.databricks.com/aws/en/ingestion/lakeflow-connect/column-selection](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/column-selection)
> **Added:** 2026-06-30
> **Source updated:** 2026-05-06
> **Tags:** lakeflow-connect, managed-connectors, ingestion, column-selection, table-configuration, A3
> **Type:** documentation

**Applies to:** SaaS connectors · Database connectors · Query-based connectors

By default, managed connectors ingest **all current and future columns**. Use `table_configuration` to narrow that.

## Properties

| Property | Effect on future columns |
|---|---|
| `include_columns` | **Opt-in list.** Future source columns are **excluded** automatically — must be added manually to ingest them. |
| `exclude_columns` | **Opt-out list.** Future source columns are **included** automatically. |

Set these inside the `table_configuration` block of a `table` (or `report`) object in the `ingestion_definition`.

## Key distinction

`include_columns` freezes the schema at definition time — safer for strict schema control but requires maintenance when source adds columns.

`exclude_columns` is schema-forward — new source columns flow through automatically, only named columns are suppressed.

## DABs YAML pattern (applicable to all SaaS/DB connectors)

```yaml
resources:
  pipelines:
    my_pipeline:
      name: <pipeline-name>
      catalog: <target-catalog>
      schema: <target-schema>
      ingestion_definition:
        connection_name: <connection-name>
        objects:
          - table:
              source_schema: <source-schema>
              source_table: <source-table>
              destination_catalog: <destination-catalog>
              destination_schema: <destination-schema>
              table_configuration:
                include_columns:       # or exclude_columns
                  - <column_a>
                  - <column_b>
                  - <column_c>
```

For Workday (report-based), replace `table:` with `report:` and use `source_url` instead of `source_schema`/`source_table`.

## Connector differences

- **SaaS (Salesforce, Google Analytics, Workday, etc.)** — supported; examples on the page.
- **Database connectors** — supported.
- **Query-based connectors** — supported.
- Not all connectors support this pattern — check connector-specific docs.

[[lakeflow-connect-common-patterns]] · [[lakeflow-connect-managed]]
