# Partition discovery for external tables

> **Source:** [docs.databricks.com/aws/en/tables/external-partition-discovery](https://docs.databricks.com/aws/en/tables/external-partition-discovery)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-17
> **Tags:** tables, unity-catalog, external, partitioning, partition-metadata, msck-repair, hive-style, B4
> **Type:** documentation

How Unity Catalog finds the partitions of an **external** table. By default, UC **recursively lists every directory** under the table `LOCATION` to discover partitions — correct but slow for large partition counts. Since **DBR 13.3 LTS**, you can opt into **partition metadata logging** (`partitionMetadataEnabled=true`): UC stops auto-scanning and instead reads only partitions registered in metadata (Hive-metastore-style behavior), trading automatic discovery for faster reads. With logging on, you own keeping metadata in sync — via `MSCK REPAIR` (Hive-style layouts) or `ALTER TABLE … ADD PARTITION` (non-Hive). This applies **only to non-Delta** external tables (Parquet, ORC, CSV, Avro, JSON); Databricks recommends [[liquid-clustering]] over partitioning in general. It's the feature behind the `MSCK REPAIR TABLE … SYNC METADATA` line name-dropped in [[external-tables]].

> "Tables with partition metadata logging enabled have different behavior for partition discovery. Instead of automatically scanning the table location for partitions, Unity Catalog only respects partitions registered in the partition metadata."

The trade-off: with logging on, auto-discovery is off, so new partitions written out-of-band won't be seen until you manually repair. Tables with logging enabled are readable/writable only on **DBR 13.3 LTS+** (to read on 12.2 LTS, drop + recreate with the property disabled). **Always use table names, not paths** — path-based access can skip partition registration.

## Enabling partition metadata logging

At create time:

```sql
CREATE OR REPLACE TABLE <catalog>.<schema>.<table-name>
USING <format>
PARTITIONED BY (<partition-column-list>)
TBLPROPERTIES ('partitionMetadataEnabled' = 'true')
LOCATION 's3://<bucket-path>/<table-directory>';
```

Session-level default (the explicit `TBLPROPERTIES` value overrides it): `SET spark.databricks.nonDelta.partitionLog.enabled = true;`. To upgrade an existing table, use `CREATE OR REPLACE` with the property (external tables don't delete data on drop). Verify with `DESCRIBE EXTENDED table_name` → properties contain `partitionMetadataEnabled=true`.

> UC enforces path-overlap rules: you cannot register a new table on a file collection if a table already exists at that location.

## Listing partitions

```sql
SHOW PARTITIONS <table-name>;
SHOW PARTITIONS <table-name> PARTITION (<partition-column-name> = <partition-column-value>);
```

## Manually add / drop / repair metadata

With logging on, auto-discovery is disabled — out-of-band or path-based writes require a manual repair.

**Hive-style layouts** (`year=2021/month=01/`) backed by Parquet/ORC/CSV/JSON → `MSCK REPAIR`:

```sql
MSCK REPAIR TABLE <table_name> SYNC PARTITIONS;   -- add + remove to match directories
MSCK REPAIR TABLE <table_name> ADD PARTITIONS;    -- add directories not yet registered
MSCK REPAIR TABLE <table_name> DROP PARTITIONS;   -- drop registered metadata not in the location
```

All partitions must live inside the directory registered via `LOCATION`.

**Non-Hive layouts** → specify partition paths explicitly (also faster than `MSCK REPAIR` for many partitions):

```sql
ALTER TABLE <table-name>
ADD PARTITION (<partition-column-name> = <partition-column-value>)
LOCATION 's3://<bucket-path>/<table-directory>/<partition-directory>';
```

`ALTER TABLE … PARTITION` also drops, renames, recovers, and sets locations for partitions.

## Limitations

> "Using path-based patterns for reads or writes can result in partitions being ignored or not registered to the Unity Catalog metastore."

- Reading the table **by directory path** returns **all** partitions — including ones manually added or dropped (path reads bypass the metadata).
- Insert/overwrite **by path** instead of table name → partition metadata is **not** recorded.

Related: [[external-tables]], [[liquid-clustering]], [[managed-tables]].
