# Create or modify a table using file upload

> **Source:** [docs.databricks.com/aws/en/ingestion/create-or-modify-table](https://docs.databricks.com/aws/en/ingestion/create-or-modify-table)
> **Added:** 2026-06-29
> **Source updated:** 2026-03-31
> **Tags:** ingestion, file-upload, add-data-ui, delta, managed-table, csv, json, parquet, avro, unity-catalog, A3
> **Type:** documentation

The **Add data UI** (New → Add or upload data → Create or modify a table) lets you upload small local files to create or overwrite a managed Delta table in UC or the Hive metastore. Intended for ad-hoc/manual ingestion — not for production pipelines.

## Constraints

- Up to **10 files** per upload, max **2 GB** total
- Formats: CSV, TSV (`.tsv`/`.tab`), JSON, Avro, Parquet, text (`.txt`)
- Compressed files (`.zip`, `.tar`) are **not supported**
- Compute required for preview/configure: SQL warehouses, serverless, or dedicated — **not group clusters**
- Workspace admins can disable this UI entirely

## Workflow

1. **New → Add or upload data → Create or modify a table**
2. Browse or drag-drop files onto the drop zone (files go to a secure internal staging area, garbage-collected daily)
3. Select compute to preview up to **50 rows**
4. Choose catalog/schema and table name; pick **Create new** or **Overwrite existing**
5. Configure format options and edit column names/types
6. Click **Create**

## Format options

**CSV/TSV:**
- First row is header (default on)
- Column delimiter (default comma; single character only, no backslash)
- Auto-detect column types (default on; disable → all `STRING`)
- Rows span multiple lines (default off)
- Merge schema across multiple files (default off)

**JSON:**
- Auto-detect column types (default on)
- Rows span multiple lines (default on)
- Allow comments (default on)
- Allow single quotes (default on)
- Infer timestamp strings as `TimestampType` (default on)

## Column names and types

Editable before creating. Restrictions on column names: no commas, backslashes, or unicode characters (including emojis). Column mapping is used under the hood to support special characters. Nested types (`STRUCT`, `ARRAY`) cannot be edited.

Supported types: `BIGINT`, `BOOLEAN`, `DATE`, `DOUBLE`, `STRING`, `TIMESTAMP`, `STRUCT`, `ARRAY`, `DECIMAL(P,S)`.

Type inference is best-effort — mismatches cast to `NULL`. Known issue: casting `BIGINT` to `DATE` can error.

## Multi-file behavior

When uploading multiple files: header settings apply uniformly (inconsistent headers → data loss); files are **appended as rows** — no join or merge logic during upload.

[lakeflow-connect-overview](lakeflow-connect-overview/) · [managed-tables](managed-tables/)
