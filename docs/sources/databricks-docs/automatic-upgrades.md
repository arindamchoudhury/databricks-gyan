# Automatic upgrades for managed tables

> **Source:** [docs.databricks.com/aws/en/tables/automatic-upgrades](https://docs.databricks.com/aws/en/tables/automatic-upgrades)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-18
> **Tags:** tables, unity-catalog, managed, automatic-upgrades, table-features, observation-window, verified-workloads, row-tracking, catalog-commits, checkpoint-v2, column-mapping, change-data-feed, B4, A2
> **Type:** documentation

## Summary

Databricks **automatically turns on GA recommended table features** on Unity Catalog managed tables — no `ALTER TABLE`, no code changes — **after verifying workload compatibility** through an observation window. Runs in the background on serverless compute. New-schema upgrades are **GA**; existing-schema upgrades are **Public Preview** (enroll via form with account ID). The point: stop hand-validating feature-vs-runtime compatibility across thousands of tables; the platform watches access patterns and only flips a feature on when every workload that touched the table is on a new-enough runtime.

> Breadcrumb: Tables › Table types › Managed tables › Automatic upgrades. Managed-table-only; external tables, MVs, streaming tables, and shared tables are excluded.

## Key points

- **Only flips on a feature after an observation window** of compatible access: **50 days** for Public Preview features, **100 days** for GA features.
- Compatibility verified via **verified workloads** — a workload is verified for a feature if it accessed the table from a cluster on DBR **≥ the feature's minimum required version**.
- **One unverified access poisons the whole schema** for that feature — if any table in a schema was accessed within the window by a too-old DBR or an external client, the feature is turned on for *no* table in that schema.
- GA features auto-enable; **Public Preview features only enable if you enrolled** in the preview.
- Detect it: a `SET TBLPROPERTIES` op in table History where the username is a **hash** (e.g. `4d137f29-62`) instead of a real user.
- Reversible: `RESTORE` the table to a prior version, or `ALTER TABLE … DROP FEATURE` (won't be re-enabled after manual drop).
- **Excluded:** external tables, MVs, streaming tables, OpenSharing-shared tables (D2O + D2D), path-based-access workloads.

## Notes

### How it works

Monitors UC access patterns at **table and schema level**, uses an **observation window** to confirm compatibility before enabling anything. Window length by feature maturity:

- **Public Preview feature** → 50-day window
- **GA feature** → 100-day window

Upgrades run in the background on **serverless compute**.

### Behavior by schema/table age

| Schema | Table | Behavior |
|---|---|---|
| New | New | Schema-level defaults set at creation → tables **inherit all supported features immediately, no observation period**. |
| Existing | New | Feature turned on **only if every workload** that accessed the table within the window is verified. A single unverified access → table ignored. |
| Existing | Existing | Feature turned on only when **all** hold: (1) only verified workloads in the window; (2) table's **first recorded access predates** the window; (3) table **accessed within last 30 days** (inactive tables skipped). |

### Verified workloads

Verified = accessed from a Databricks cluster running DBR **≥ the feature's minimum version**.

**Unverified:**

- External clients / third-party engines (Flink, Presto — UC integrations).
- Databricks services with direct/kernel-level access that bypass standard DBR access patterns (e.g. **Zerobus** ingest).

Schema-poisoning rule: if **any** table in the schema was accessed in the window by a sub-minimum DBR or an external client, the feature is enabled on **no** table in that schema.

### Supported features

GA features auto-enable; Public Preview features require enrollment.

| Feature | What it does | Status | Min DBR |
|---|---|---|---|
| **Automatic change data feed** | Row-level change data for Delta + managed Iceberg, no config; needs row tracking on | PP (all tables, all schemas) | 18 |
| **Automatic liquid clustering** | Auto-organizes data by frequently-queried columns | GA new tables/new schemas; PP new tables/existing schemas; **ignores existing tables** | 13.3 LTS |
| **Catalog commits** | Centralizes commits in UC → multi-table txns, external-write interop, cross-engine governance | PP (all tables, all schemas) | 16.4 LTS |
| **Checkpoint V2** | More concurrent writers, fewer write conflicts on large/hot tables | GA new tables/new schemas; PP all tables/existing schemas | 13.3 LTS |
| **Column mapping** | Rename/drop columns without rewriting data | PP (all tables, all schemas) | 15.4 LTS |
| **Row tracking** | Hidden row IDs for incremental processing; enables automatic CDF | GA new tables/new schemas; PP all tables/existing schemas | 14.3 LTS |

> Feature availability may differ by region.

### Requirements

- Serverless compute available in your region.
- Tables must be **UC managed tables**, Delta Lake or Apache Iceberg format.

### Observe enabled features

- Look for a `SET TBLPROPERTIES` op in the **History** tab (Catalog Explorer) or `DESCRIBE HISTORY <table_name>`. Automatic-upgrade ops show a **hash** in the username field instead of a username.
- For new schemas, schema defaults appear in the **Properties** tab, e.g. `catalog.schema.enableRowTracking: "true"`. Existing schemas don't get observability properties.

### Manage / revert

```sql
-- revert table data + metadata to before the feature was enabled
RESTORE TABLE <table_name> TO VERSION AS OF <version>;
RESTORE TABLE <table_name> TO TIMESTAMP AS OF <timestamp>;

-- turn a feature off on one table (not re-enabled automatically afterward)
ALTER TABLE <table_name> DROP FEATURE <feature_name>;
```

### Limitations

- **OpenSharing-shared tables excluded** (Databricks-to-Open and Databricks-to-Databricks).
- **No batch rollback** — can't turn a feature off across all tables in an account at once.
- **Materialized views and streaming tables not supported.**
- **Path-based-access workloads not tracked** — contact account team to discuss compatibility.
- **External tables excluded** — typically file-path-accessed, bypassing UC, with unverified external-client access → UC can't reliably track them (see [[external-tables]]).

## Quotes worth keeping

> "If any table in a schema was accessed within the observation window by a Databricks Runtime version below the feature's minimum required version or by an external client, automatic upgrades don't turn on the corresponding feature on any table in that schema." (Verified workloads)

## Open questions

- "Automatic liquid clustering" *ignores existing tables* entirely — so existing tables never get auto-LC even with compatible workloads? Reads that way.
- Enrollment is per-account-ID via form; no self-serve toggle documented for existing-schema preview.

## Related sources

- [[managed-tables]] — the feature set this silently enables; automatic-upgrades is the delivery mechanism for those GA features.
- [[catalog-commits]] — one of the upgraded features (PP, min DBR 16.4 LTS).
- [[predictive-optimization]] — sibling under Managed tables; PO runs maintenance, automatic-upgrades flips on table features. Both serverless, background, managed-only.
- [[liquid-clustering]] — automatic liquid clustering is the auto-enabled form.
- [[external-tables]] — explicitly excluded; explains why (path access, unverified clients).
- [[external-access]] — external clients (Flink/Presto) and credential-vended access count as unverified workloads here.
