# DCDE-SG Ch 3 — verified facts

Last verified: **2026-06-22** against Databricks platform docs (Unity Catalog tables / views / constraints / clone / serverless limitations). Current stable: DBR 18 (Spark 4.1), DBR 17.3 LTS (Spark 4.0).

Working file for Chapter 3 of Derar Alhussein's *DCDE-SG* (O'Reilly, 1st Ed., Feb 2025). The book targets DBR 13.3 LTS and demos everything against `hive_metastore` + `dbfs:` paths; these facts capture what changed by mid-2026.

| Book claim (2025) | Current value (2026) | Notes |
|---|---|---|
| "A database = a schema in `hive_metastore`" | In UC the same concept is a **schema** inside the **3-level namespace** `catalog.schema.table`. `DATABASE` and `SCHEMA` keywords still interchangeable. | Book's `USE CATALOG hive_metastore` works only where HMS is enabled |
| Managed table data → `dbfs:/user/hive/warehouse` | UC managed tables → UC **managed storage** (`s3://…/__unity_storage/catalogs/<catalog_id>/tables/<table_id>`), addressed by GUID | DROP still deletes data + metadata |
| External table = `CREATE TABLE … LOCATION '<any dbfs path>'` | UC external table requires the `LOCATION` to fall under a **registered external location** (storage path + storage credential / IAM role); plain `dbfs:/mnt/...` mount paths are gone | UC also needs `CREATE EXTERNAL TABLE` + `CREATE MANAGED STORAGE`/external-location grants. DROP removes metadata only; data persists |
| Custom-location DB via `CREATE SCHEMA … LOCATION 'dbfs:/...'` | UC schema/catalog **managed location** must also be a registered external location; `dbfs:/Shared/...` won't work on UC-only workspaces | Managed location set at catalog or schema level |
| `/mnt/demo`, `dbfs:/Shared/...` mount paths | DBFS **mounts + root deprecated**; accounts created after 2025-12-19 have them OFF (no opt-out). Use **UC Volumes** / external locations | Same shift flagged in Ch 1–2 |
| Constraints: only `NOT NULL` + `CHECK` | Still the only **enforced** constraints. UC adds **informational** `PRIMARY KEY` / `FOREIGN KEY` (not enforced; used for query optimization + ER diagrams) | `CHECK` validated against existing + new rows; PK/FK metadata in `INFORMATION_SCHEMA.TABLE_CONSTRAINTS` |
| Deep clone / shallow clone | Both still valid. **Shallow clone for UC managed tables: DBR 13.3+**. Can only clone managed→managed, external→external. Cannot nest shallow clones | UC shallow clone gives independent access control without copying data; VACUUM on source can delete files referenced by a shallow clone of a managed table |
| Global temporary view (`global_temp`, tied to cluster) | **Not supported on serverless compute** (Spark Connect). Considered legacy; Databricks recommends session temp views or tables | Temp + stored views still fully supported. New 2026 default compute = serverless → global temp views unavailable there |
| `PARTITIONED BY` for performance | Discouraged for new tables; use **liquid clustering** (Ch 2 §7) | Small-files problem the book warns about is real |
| `SELECT * FROM DELTA.\`path\`` direct path query | Still works for paths you can access; on UC, path access is governed by external-location grants | |
| Two table types: managed + external | **Three primary types: managed, external, foreign** (+ session-scoped temporary tables). Foreign = Lakehouse Federation, **read-only**. | tables-concepts (Jun 2026) |
| All tables are Delta | **Delta = default**, but **Apache Iceberg** also supported (managed + foreign) | Both add ACID/time-travel |
| External = "flexible" choice | Databricks **recommends managed for every new table** (auto-optimization, lower cost, Trino-readable); external only when files must outlive UC lifecycle | tables-concepts |
| (HMS had no grants) | UC table-op permissions: `CREATE TABLE` (create), `SELECT` (query), `SELECT`+`MODIFY` (write), **`MANAGE`** (DROP/REPLACE), plus `USE CATALOG`+`USE SCHEMA` | tables-concepts |
| `hive_metastore` always visible as a catalog | Visible **only where HMS enabled**; on "Disable legacy features" workspaces (default for accounts after 2025-12-19) it does **not appear at all** — Catalog Explorer shows UC catalogs only | Confirmed against user's own UC-only workspace 2026-06-22 |

## Sources

- Tables concepts (3 types + 2 formats + permissions): <https://docs.databricks.com/aws/en/tables/tables-concepts>
- Managed vs external tables (UC): <https://docs.databricks.com/aws/en/tables/external>
- External locations: <https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-external-locations>
- UC managed storage: <https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/managed-storage>
- ADD CONSTRAINT (NOT NULL / CHECK / PK / FK): <https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-syntax-ddl-alter-table-add-constraint>
- Query optimization with PK/UNIQUE constraints: <https://docs.databricks.com/aws/en/sql/user/queries/query-optimization-constraints>
- CREATE TABLE CLONE: <https://docs.databricks.com/aws/en/sql/language-manual/delta-clone>
- Shallow clone for UC tables: <https://docs.databricks.com/aws/en/delta/clone-unity-catalog>
- Views overview (stored / temp / global temp): <https://docs.databricks.com/aws/en/views/>
- Serverless compute limitations (global temp views unsupported): <https://docs.databricks.com/aws/en/compute/serverless/limitations>
