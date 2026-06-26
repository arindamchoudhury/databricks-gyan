# Automatic upgrades for managed tables

> **Source:** [docs.databricks.com/aws/en/tables/automatic-upgrades](https://docs.databricks.com/aws/en/tables/automatic-upgrades)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-18
> **Tags:** tables, unity-catalog, managed, automatic-upgrades, table-features, observation-window, verified-workloads, row-tracking, catalog-commits, checkpoint-v2, column-mapping, change-data-feed, B4, A2
> **Type:** documentation

Databricks **automatically turns on GA recommended table features** on Unity Catalog managed tables — no `ALTER TABLE`, no code changes — **after verifying workload compatibility** through an observation window, running in the background on serverless compute. The point: stop hand-validating feature-vs-runtime compatibility across thousands of tables; the platform watches access patterns and only flips a feature on when every workload that touched the table is on a new-enough runtime. New-schema upgrades are **GA**; existing-schema upgrades are **Public Preview** (enroll via form with account ID). Managed-table-only — external tables, MVs, streaming tables, and shared tables are excluded.

## How it works

Monitors UC access patterns at **table and schema level**, using an **observation window** to confirm compatibility before enabling anything: **50 days** for Public Preview features, **100 days** for GA features. GA features auto-enable; **Public Preview features only enable if you enrolled**.

| Schema | Table | Behavior |
|---|---|---|
| New | New | Schema-level defaults set at creation → tables **inherit all supported features immediately, no observation period**. |
| Existing | New | Feature on **only if every workload** that accessed the table within the window is verified. A single unverified access → table ignored. |
| Existing | Existing | Feature on only when all hold: (1) only verified workloads in the window; (2) table's **first recorded access predates** the window; (3) table **accessed within last 30 days** (inactive tables skipped). |

## Verified workloads

Verified = accessed from a Databricks cluster running DBR **≥ the feature's minimum version**. **Unverified:** external clients / third-party engines (Flink, Presto), and Databricks services with direct/kernel-level access that bypass standard DBR patterns (e.g. **Zerobus** ingest).

> "If any table in a schema was accessed within the observation window by a Databricks Runtime version below the feature's minimum required version or by an external client, automatic upgrades don't turn on the corresponding feature on any table in that schema."

So **one unverified access poisons the whole schema** for that feature.

## Supported features

| Feature | What it does | Status | Min DBR |
|---|---|---|---|
| **Automatic change data feed** | Row-level change data for Delta + managed Iceberg, no config; needs row tracking on | PP (all tables, all schemas) | 18 |
| **Automatic liquid clustering** | Auto-organizes data by frequently-queried columns | GA new tables/new schemas; PP new tables/existing schemas; **ignores existing tables** | 13.3 LTS |
| **Catalog commits** | Centralizes commits in UC → multi-table txns, external-write interop, cross-engine governance | PP (all tables, all schemas) | 16.4 LTS |
| **Checkpoint V2** | More concurrent writers, fewer write conflicts on large/hot tables | GA new tables/new schemas; PP all tables/existing schemas | 13.3 LTS |
| **Column mapping** | Rename/drop columns without rewriting data | PP (all tables, all schemas) | 15.4 LTS |
| **Row tracking** | Hidden row IDs for incremental processing; enables automatic CDF | GA new tables/new schemas; PP all tables/existing schemas | 14.3 LTS |

Feature availability may differ by region. Requirements: serverless compute available in your region, and tables must be **UC managed** (Delta or Iceberg).

## Observe enabled features

- Look for a `SET TBLPROPERTIES` op in the **History** tab (Catalog Explorer) or `DESCRIBE HISTORY <table_name>` — automatic-upgrade ops show a **hash** in the username field (e.g. `4d137f29-62`) instead of a username.
- For new schemas, schema defaults appear in the **Properties** tab, e.g. `catalog.schema.enableRowTracking: "true"`. Existing schemas don't get observability properties.

## Manage / revert

```sql
RESTORE TABLE <table_name> TO VERSION AS OF <version>;       -- revert before the feature was enabled
RESTORE TABLE <table_name> TO TIMESTAMP AS OF <timestamp>;
ALTER TABLE <table_name> DROP FEATURE <feature_name>;        -- turn off on one table (not re-enabled after manual drop)
```

## Limitations

- **OpenSharing-shared tables excluded** (Databricks-to-Open and Databricks-to-Databricks).
- **No batch rollback** — can't turn a feature off across all tables in an account at once.
- **Materialized views and streaming tables not supported.**
- **Path-based-access workloads not tracked** — contact account team to discuss compatibility.
- **External tables excluded** — typically file-path-accessed, bypassing UC, with unverified external-client access → UC can't reliably track them ([[external-tables]]).

Related: [[managed-tables]], [[catalog-commits]], [[predictive-optimization]], [[liquid-clustering]], [[row-tracking]], [[change-data-feed]], [[external-tables]], [[external-access]].
