# DCDE-SG Ch 2 — verified facts

Last verified: **2026-06-21** against Databricks platform docs (Delta Lake / OPTIMIZE / Deletion Vectors / Predictive Optimization / Liquid Clustering). Current stable: DBR 18 (Spark 4.1), DBR 17.3 LTS (Spark 4.0).

Working file for Chapter 2 of Derar Alhussein's *DCDE-SG* (O'Reilly, 1st Ed., Feb 2025). The book targets DBR 13.3 LTS; these facts capture what changed by mid-2026.

| Book claim (2025) | Current value (2026) | Notes |
|---|---|---|
| Z-Order recommended for data skipping | **Liquid Clustering** is now the Databricks-recommended approach for all new tables | Databricks docs: "use liquid clustering instead of partitions, ZORDER, or other data layout approaches" |
| UPDATE/DELETE copies files (immutability) | **Deletion Vectors** (default-enabled at workspace level for DBR 14.0+) mark stale rows as a bitmap without file copying | Book's NOTE already mentions the DBR 14 behavior change; row-level concurrency added in DBR 14.2 |
| Book uses `hive_metastore` for demos | **Unity Catalog is the default** in all new 2026 workspaces; `DESCRIBE DETAIL` location shows `__unitystorage` | The book includes a WARNING about this; still valid to use `hive_metastore` for local practice |
| `%fs ls dbfs:/user/hive/warehouse/<table>` | Doesn't work on UC-managed tables (restricted `__unitystorage`) | Use `hive_metastore` catalog when practicing file-level commands |
| VACUUM default retention: 7 days | Still 7 days | Set via `delta.deletedFileRetentionDuration`; raise before enabling Predictive Optimization to keep longer time travel |
| Manual `OPTIMIZE` / `VACUUM` / `ANALYZE` | **Predictive Optimization** auto-runs all three on UC managed tables (serverless, billed) | Default-on for accounts created ≥ 2024-11-11; existing-account rollout completing ~Aug 2026. PO's `OPTIMIZE` never runs `ZORDER` and ignores Z-ordered files |
| Liquid Clustering "use it for new tables" | GA on **DBR 15.4 LTS+** (14.3 LTS = DataFrame/DeltaTable API only) | `CLUSTER BY AUTO` (GA 15.4 LTS+, UC managed only) lets predictive optimization pick + adapt keys; `ALTER TABLE … CLUSTER BY AUTO` on existing tables |
| Converting partitioned → liquid clustering | `ALTER TABLE … REPLACE PARTITIONED BY WITH CLUSTER BY [AUTO]` (DBR 18.1+) | Minimizes reader/writer downtime; external + managed tables |

## Sources

- Liquid Clustering GA: <https://www.databricks.com/blog/announcing-general-availability-liquid-clustering>
- Liquid Clustering docs: <https://docs.databricks.com/aws/en/tables/clustering>
- OPTIMIZE docs: <https://docs.databricks.com/aws/en/sql/language-manual/delta-optimize>
- Deletion vectors: <https://docs.databricks.com/aws/en/delta/deletion-vectors>
- Auto-enable deletion vectors (workspace setting): <https://docs.databricks.com/aws/en/admin/workspace-settings/deletion-vectors>
- Row-level concurrency: <https://docs.databricks.com/aws/en/optimizations/isolation/row-level-concurrency>
- Predictive optimization: <https://docs.databricks.com/aws/en/optimizations/predictive-optimization>
- Liquid clustering (incl. CLUSTER BY AUTO): <https://docs.databricks.com/aws/en/tables/clustering>
