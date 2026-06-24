# Partition discovery for external tables

> **Source:** [docs.databricks.com/aws/en/tables/external-partition-discovery](https://docs.databricks.com/aws/en/tables/external-partition-discovery)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-17
> **Tags:** tables, unity-catalog, external, partitioning, partition-metadata, msck-repair, hive-style, B4
> **Type:** documentation

## Summary

How Unity Catalog finds the partitions of an **external** table. Default behavior: UC recursively lists every directory under the table `LOCATION` to discover partitions — correct but slow for large partition counts. Since **DBR 13.3 LTS**, you can opt into **partition metadata logging** (`partitionMetadataEnabled=true`): UC stops auto-scanning and instead reads only partitions registered in metadata (Hive-metastore-style behavior), trading automatic discovery for faster reads. With logging on, you take ownership of keeping metadata in sync — via `MSCK REPAIR` (Hive-style layouts) or `ALTER TABLE … ADD PARTITION` (non-Hive layouts). Only affects **non-Delta** external tables (Parquet, ORC, CSV, Avro, JSON); Databricks recommends [[liquid-clustering]] over partitioning in general.

## Key points

- **Default strategy** = recursive directory listing of the table `LOCATION` on every operation → high latency for tables with many partition directories.
- **Partition metadata logging** (DBR 13.3 LTS+, opt-in) → UC reads only registered partition metadata, matching Hive metastore behavior. Recommended for read speed/query perf on partitioned external tables.
- Applies **only** to UC external tables that are **partitioned** and use **Parquet, ORC, CSV, Avro, or JSON** (i.e. non-Delta).
- **Trade-off:** with logging enabled, auto-discovery is **off** — new partitions written out-of-band (external systems, path-based writes) won't be seen until you manually repair metadata.
- **Runtime floor:** tables with logging enabled are readable/writable only on **DBR 13.3 LTS+**. To read on 12.2 LTS you must drop + recreate with the property disabled.
- **Always use table names**, not paths, for reads/writes — path-based access can skip partition registration. This is why path-based access is an anti-pattern here (mirrors the out-of-band warning in [[external-tables]]).
- This is the feature behind the `MSCK REPAIR TABLE … SYNC METADATA` line name-dropped in [[external-tables]] — now explained in full.

## Notes

### Enabling partition metadata logging

Set the table property at create time:

```sql
CREATE OR REPLACE TABLE <catalog>.<schema>.<table-name>
USING <format>
PARTITIONED BY (<partition-column-list>)
TBLPROPERTIES ('partitionMetadataEnabled' = 'true')
LOCATION 's3://<bucket-path>/<table-directory>';
```

After creation, UC uses the metadata for all subsequent reads.

**Session-level enable** — a Spark config makes every external table created in the session default to logging on (off by default globally):

```sql
SET spark.databricks.nonDelta.partitionLog.enabled = true;
```

The explicit `TBLPROPERTIES` value at create time overrides the session config.

**Upgrading an existing table** — because external tables don't delete data on drop, use `CREATE OR REPLACE` to flip an existing table to logging (no `TBLPROPERTIES` line in this example because the goal shown is re-registering; add the property to turn it on):

```sql
CREATE OR REPLACE TABLE <catalog>.<schema>.<table-name>
USING <format>
PARTITIONED BY (<partition-column-list>)
LOCATION 's3://<bucket-path>/<table-directory>';
```

**Verify** it's on: `DESCRIBE EXTENDED table_name` (or Catalog Explorer) → table properties contains `partitionMetadataEnabled=true`.

> UC enforces path-overlap rules: you cannot register a new table on a file collection if a table already exists at that location.

### Listing partitions

```sql
SHOW PARTITIONS <table-name>
```

Check a single partition:

```sql
SHOW PARTITIONS <table-name>
PARTITION (<partition-column-name> = <partition-column-value>)
```

### Manually add / drop / repair metadata

With logging on, auto-discovery is disabled — so out-of-band or path-based writes require a manual repair.

**Hive-style layouts** (key=value directories, e.g. `year=2021/month=01/`) backed by Parquet/ORC/CSV/JSON → use `MSCK REPAIR`:

```sql
-- Add and remove partition metadata to match directories in table location
MSCK REPAIR TABLE <table_name> SYNC PARTITIONS;

-- Add partitions in the table location that are not registered as partition metadata
MSCK REPAIR TABLE <table_name> ADD PARTITIONS;

-- Drop partitions registered as partition metadata that are not in the table location
MSCK REPAIR TABLE <table_name> DROP PARTITIONS;
```

> All partitions must live inside the directory registered via `LOCATION`.

**Non-Hive layouts** → you must specify partition paths explicitly. This can also be **faster than `MSCK REPAIR`** for tables with many partitions:

```sql
ALTER TABLE <table-name>
ADD PARTITION (<partition-column-name> = <partition-column-value>)
LOCATION 's3://<bucket-path>/<table-directory>/<partition-directory>';
```

`ALTER TABLE … PARTITION` also drops, renames, recovers, and sets locations for partitions.

### Limitations

- Reading the table **by directory path** returns **all** partitions — including ones manually added or dropped (path reads bypass the metadata).
- Insert/overwrite **by path** instead of table name → partition metadata is **not** recorded.

## Quotes worth keeping

> "Tables with partition metadata logging enabled have different behavior for partition discovery. Instead of automatically scanning the table location for partitions, Unity Catalog only respects partitions registered in the partition metadata." (Use partition metadata logging)

> "Using path-based patterns for reads or writes can result in partitions being ignored or not registered to the Unity Catalog metastore." (Work with tables with partition metadata)

## Open questions

- Does enabling logging retroactively backfill existing partition directories, or must you run `MSCK REPAIR … ADD PARTITIONS` after the `CREATE OR REPLACE` upgrade? Page implies a repair is needed for anything written out-of-band.

## Related sources

- [[external-tables]] — parent concept; this page details the partition-discovery mechanics behind its `MSCK REPAIR TABLE … SYNC METADATA` mention.
- [[liquid-clustering]] — Databricks' recommended alternative to partitioning altogether (the page's lead recommendation).
- [[managed-tables]] — managed tables don't expose this; UC owns their layout.
