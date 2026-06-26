# Convert an external Delta table to a managed UC table

> **Source:** [docs.databricks.com/aws/en/tables/convert-external-managed](https://docs.databricks.com/aws/en/tables/convert-external-managed?language=SQL)
> **Added:** 2026-06-23
> **Source updated:** 2026-06-17
> **Tags:** tables, unity-catalog, managed, external, set-managed, unset-managed, migration, uniform, path-based-redirect, streaming, B4
> **Type:** documentation

Migrate an **external Delta table → UC managed table** in place via `ALTER TABLE … SET MANAGED` (or Catalog Explorer, Beta). It's preferred over CTAS / DEEP CLONE because it minimizes downtime, handles concurrent writes, **retains history/permissions/views**, **redirects path-based reads/writes** so legacy code keeps working, and is **reversible within 14 days** (`UNSET MANAGED`). This is the operation [[managed-tables]] links to.

**Prerequisites:** DBR **17.3 LTS+** or Serverless (for SET/UNSET MANAGED and TRUNCATE UNIFORM HISTORY); the table must be **Delta**; readers/writers on DBR **15.4 LTS+** (14.3 and below = degraded, see below). Conversion is a **two-phase copy**: (1) copy data + log — no downtime; (2) switch metadata to the managed location — brief **writer** downtime (readers on DBR 16.4 LTS+ none). Before converting, cancel/pause OPTIMIZE jobs (liquid clustering, compaction, ZORDER) and never run concurrent `SET MANAGED` on the same table.

## SET MANAGED command

```sql
-- External table WITHOUT Iceberg reads (UniForm)
ALTER TABLE catalog.schema.my_external_table SET MANAGED;

-- External table WITH Iceberg reads (UniForm) already enabled
ALTER TABLE catalog.schema.my_external_table SET MANAGED TRUNCATE UNIFORM HISTORY;
```

- `TRUNCATE UNIFORM HISTORY` truncates **UniForm Iceberg history only** (not Delta history); causes a short Iceberg read+write downtime after truncation but keeps performance + compatibility. Without UniForm, you can enable Iceberg reads on the managed table afterward, no concern.
- **Resumable**: if interrupted while copying, just rerun — it resumes from where it left off.
- ⚠️ A table with `minReaderVersion=2`, `minWriterVersion=7`, `tableFeatures={…, columnMapping}` fails with `DELTA_TRUNCATED_TRANSACTION_LOG`. Check via `DESCRIBE DETAIL`.

> **Cancel existing `OPTIMIZE` jobs** (liquid clustering, compaction, ZORDER) and don't schedule jobs during conversion, to avoid conflicts. Avoid concurrent `SET MANAGED` on the same table.

## Catalog Explorer path (Beta)

Name-based access is used automatically; you can convert multiple external tables in a schema at once.

[![Why migrate to Unity Catalog managed tables dialog](assets/convert-external-managed/01-why-migrate-dialog.png)](assets/convert-external-managed/01-why-migrate-dialog.png)
*Table/schema detail → About this table → "Explore optimizations" → this dialog → Continue.*

[![Table selection screen — pre-selected external table, managed table unavailable](assets/convert-external-managed/02-table-selection.png)](assets/convert-external-managed/02-table-selection.png)
*Select external tables to convert; managed tables are not selectable.*

[![Create conversion notebook dialog](assets/convert-external-managed/03-create-notebook.png)](assets/convert-external-managed/03-create-notebook.png)
*"Create conversion notebook" → review prereqs → run the SET MANAGED Queries cell. Type then shows MANAGED.*

## After conversion

- **Streams fail**: existing read/write streams stop. Restart with the same config → auto path-based redirect.
- **Predictive optimization auto-enabled** unless manually off.
- **Old external data cleanup**: with PO on, Databricks deletes the external-location data after **14 days**; with PO off, run `VACUUM my_converted_table` after 14 days (DBR 17.3 LTS+ / Serverless). Even with PO on, small/infrequently-used tables may not get cleaned — `VACUUM` manually. Only the **data** in the external location is deleted; the Delta log + UC table reference are kept.

Verify: `DESCRIBE EXTENDED catalog_name.schema_name.table_name` → `Type = MANAGED`.

## Readers/writers on DBR 14.3 LTS or below

Recommended: upgrade all readers/writers to DBR 15.4 LTS+. If you don't:

- After conversion, time travel to historical commits is **by version only, not by timestamp**.
- Roll back within 14 days → pre-conversion timestamp time travel is re-enabled.
- Timestamp time travel never works for commits made **between conversion and rollback**.
- Writing post-conversion on DBR 15.4 LTS or below requires dropping a feature: `ALTER TABLE <table_name> DROP FEATURE inCommitTimestamp;`

## Path-based redirect (Public Preview, opt-in)

On DBR **18.1+**, after conversion, path-based reads/writes to the old external location **auto-redirect** to the managed location — legacy path-based code keeps working without refactor.

> "Path-based redirect only has backward compatibility for the migration process and does not enable new path-based access to Unity Catalog managed tables."

- Adds **several hundred ms** overhead per path-based op and requires old Delta logs stay active in the external location. Migrate to **name-based** access for low latency.
- **Streaming with redirect**: reads supported DBR 18.1+, writes DBR 18.2+; must restart streams post-conversion. Read interruption (`DELTA_STREAMING_INTERRUPTED_BY_MANAGED_TABLE_CONVERSION`) and the first-micro-batch write error (`Operation not allowed: STREAMING WRITE cannot be performed on a table with redirect feature`) are both fixed by restarting the stream with the same config.

## Roll back to external (within 14 days)

```sql
ALTER TABLE catalog.schema.my_managed_table UNSET MANAGED;   -- needs DBR 17.3 LTS+ / Serverless
```

- Metadata points back to the original external location; **writes made to the managed location after conversion are preserved**.
- Commits between conversion and rollback → version time travel only, not timestamp.
- **7 days after rollback**, managed-location data is auto-deleted.
- Restart streaming jobs after rollback too; rerun if interrupted. Verify: `DESCRIBE EXTENDED` → `Type = EXTERNAL`.

## Downtime & data-copy estimates

Throughput ~0.5–2 GB/CPU-core/min; step 1 (copy) no downtime, step 2 (switch) brief writer downtime.

| Table size | Recommended cluster | Data copy | Reader+writer downtime |
|---|---|---|---|
| ≤ 100 GB | 32-core / X-Large SQL warehouse | ~6 min or less | ~1–2 min or less |
| 1 TB | 64-core / 2X-Large SQL warehouse | ~30 min | ~1–2 min |
| 10 TB | 256-core / 4X-Large SQL warehouse | ~1.5 hrs | ~1–5 min |

## Troubleshooting

- **Runtime version consistency** — don't retry the same conversion on a *different* DBR version (`VERSIONED_CLONE_INTERNAL_ERROR.EXISTING_FILE_VALIDATION_FAILED`). Always retry with the same DBR.
- **Cluster shutdown mid-conversion** → `DELTA_ALTER_TABLE_SET_MANAGED_INTERNAL_ERROR`; retry to resume.
- **Corrupted source table** → `DELTA_TRUNCATED_TRANSACTION_LOG` / `DELTA_TXN_LOG_FAILED_INTEGRITY` / `DELTA_STATE_RECOVER_ERRORS`. Verify `DESCRIBE DETAIL` works first.
- **File validation failure** → `DELTA_ALTER_TABLE_SET_MANAGED_FAILED.FILE_VALIDATION_FAILED` (some snapshot files not copied). Check driver logs for missing files, verify they exist + are accessible at source, retry; persists → contact support.

## Limitations

- Must restart streaming jobs after conversion; post-conversion-pre-rollback commits get version time travel only, not timestamp.
- **OpenSharing not fully compatible**: open OpenSharing works, but **Databricks-to-Databricks** sharing does *not* auto-update the recipient's managed location — the recipient reads the old location until you reshare:

```sql
ALTER SHARE <share_name> REMOVE TABLE <table_name>;
ALTER SHARE <share_name> ADD TABLE <table_name> AS <table_share_name> WITH HISTORY;
```

- **Cross-region cost**: if the UC metastore/catalog/schema default managed location is in a different region from the external storage, expect cross-region transfer charges. Verify with `DESC SCHEMA EXTENDED`, `DESC CATALOG EXTENDED`, and `SELECT * FROM system.information_schema.metastores`.

Related: [[managed-tables]], [[tables-concepts]], [[convert-foreign-managed]].
