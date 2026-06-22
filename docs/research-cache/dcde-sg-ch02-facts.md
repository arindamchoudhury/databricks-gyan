# DCDE-SG Ch 2 — verified facts

Last verified: **2026-06-21** against Databricks platform docs (Delta Lake / OPTIMIZE / Deletion Vectors / Predictive Optimization / Liquid Clustering). Current stable: DBR 18 (Spark 4.1), DBR 17.3 LTS (Spark 4.0).

Working file for Chapter 2 of Derar Alhussein's *DCDE-SG* (O'Reilly, 1st Ed., Feb 2025). The book targets DBR 13.3 LTS; these facts capture what changed by mid-2026.

| Book claim (2025) | Current value (2026) | Notes |
|---|---|---|
| Z-Order recommended for data skipping | **Liquid Clustering** is now the Databricks-recommended approach for all new tables | Databricks docs: "use liquid clustering instead of partitions, ZORDER, or other data layout approaches" |
| UPDATE/DELETE copies files (immutability) | **Deletion Vectors** (merge-on-read): mark old rows stale in a bitmap (RoaringBitmap) on the existing file, write changed rows to a new small file; reads merge. UPDATE ≈ soft-delete + insert | NOT a blanket default: enable per-table `delta.enableDeletionVectors` or region-dependent workspace auto-enable (SQL warehouse / DBR 14.3 LTS+). Iceberg v3 = on by default; MV/streaming in HMS = off. Row-level concurrency DBR 14.2+. Soft-deletes physical only via OPTIMIZE / auto-compact / REORG…APPLY(PURGE), then VACUUM |
| Book uses `hive_metastore` for demos | **Unity Catalog is the default** in all new 2026 workspaces; managed tables land in UC managed storage `s3://<bucket>/__unity_storage/catalogs/<catalog_id>/tables/<table_id>` (AWS) | Token is `__unity_storage` (underscore) on AWS; `__unitystorage` is the Azure container name. Organized by GUIDs, not table name. Still valid to use `hive_metastore` for local practice |
| `%fs ls dbfs:/user/hive/warehouse/<table>` | Not the access model on UC managed tables — UC governs by full cloud-URI grants, not friendly-path browsing | Use `hive_metastore` catalog when practicing file-level commands; for ad-hoc files use UC volumes |
| VACUUM default retention: 7 days | Still 7 days | Set via `delta.deletedFileRetentionDuration`; raise before enabling Predictive Optimization to keep longer time travel |
| Manual `OPTIMIZE` / `VACUUM` / `ANALYZE` | **Predictive Optimization** auto-runs all three on UC managed tables (serverless, billed) | Default-on for accounts created ≥ 2024-11-11; existing-account rollout completing ~Aug 2026. PO's `OPTIMIZE` never runs `ZORDER` and ignores Z-ordered files |
| Liquid Clustering "use it for new tables" | GA on **DBR 15.4 LTS+** (14.3 LTS = DataFrame/DeltaTable API only) | `CLUSTER BY AUTO` (GA 15.4 LTS+, UC managed only) lets predictive optimization pick + adapt keys; `ALTER TABLE … CLUSTER BY AUTO` on existing tables |
| Converting partitioned → liquid clustering | `ALTER TABLE … REPLACE PARTITIONED BY WITH CLUSTER BY [AUTO]` (DBR 18.1+) | Minimizes reader/writer downtime; external + managed tables |
| HMS / DBFS available in new workspaces | **Accounts created after 2025-12-19 have legacy features OFF by default, no opt-out**: Hive Metastore, DBFS root + mounts, no-isolation shared clusters, DBR < 13.3 LTS | Earlier accounts use the "Disable legacy features" account setting; workspace admin can re-enable per-workspace. New 2026 account = UC-only out of the box |

## Sources

- Liquid Clustering GA: <https://www.databricks.com/blog/announcing-general-availability-liquid-clustering>
- Liquid Clustering docs: <https://docs.databricks.com/aws/en/tables/clustering>
- OPTIMIZE docs: <https://docs.databricks.com/aws/en/sql/language-manual/delta-optimize>
- Deletion vectors (merge-on-read, enablement, REORG PURGE): <https://docs.databricks.com/aws/en/delta/deletion-vectors>
- Auto-enable deletion vectors (workspace setting): <https://docs.databricks.com/aws/en/admin/workspace-settings/deletion-vectors>
- Row-level concurrency: <https://docs.databricks.com/aws/en/optimizations/isolation/row-level-concurrency>
- UC managed storage path / `__unity_storage`: <https://docs.databricks.com/aws/en/data-governance/unity-catalog/storage-conflicts>
- DBFS + Unity Catalog best practices: <https://docs.databricks.com/aws/en/dbfs/unity-catalog>
- Disable legacy features in new workspaces (2025-12-19 cutoff): <https://docs.databricks.com/aws/en/admin/account-settings/legacy-features>
- Work with legacy Hive metastore alongside UC: <https://docs.databricks.com/aws/en/data-governance/unity-catalog/hive-metastore>
- Predictive optimization: <https://docs.databricks.com/aws/en/optimizations/predictive-optimization>
- Liquid clustering (incl. CLUSTER BY AUTO): <https://docs.databricks.com/aws/en/tables/clustering>
