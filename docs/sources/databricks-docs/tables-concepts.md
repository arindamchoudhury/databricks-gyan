# Databricks tables concepts

> **Source:** [docs.databricks.com/aws/en/tables/tables-concepts](https://docs.databricks.com/aws/en/tables/tables-concepts)
> **Added:** 2026-06-22
> **Source updated:** 2026-06-17
> **Tags:** tables, unity-catalog, managed, external, foreign, temporary, delta, iceberg, three-level-namespace, permissions, B4
> **Type:** documentation

Databricks defines tables along two axes: **table type** (managed, external, foreign — plus session-scoped temporary) and **storage format** (Delta Lake, Apache Iceberg). The **type** is set by *which catalog owns the data files*; the **format** sets *how data is physically tracked*. The default — and Databricks' recommendation for every new table — is a **Unity Catalog managed Delta table**. A table lives at the third level of the UC three-level namespace (`catalog.schema.table`).

The quick test for table type: *"If I drop this table, who deletes the data?"* — **Unity Catalog → managed**, **nobody (files stay in your bucket) → external**, **another system → foreign**. Type is about *who controls the files' lifecycle* (create, delete, location, layout, optimize), not the file format and not where the files physically sit.

> 📌 Corrects the DCDE-SG Ch 3 book (DBR 13.3-era): the book frames tables as **managed vs external on `hive_metastore`**. The current model is **three types under Unity Catalog**, managed is the recommended default (the book leans external), and Iceberg is a first-class format. There's no `hive_metastore` on this page at all. See the [Ch 3 reading notes](../dcde-sg/ch03-mastering-relational-entities/).

## Example managed table

`prod.people_ops_employees` — a managed table; its data files sit in UC's managed storage location in cloud storage.

[![Example table containing employee data](assets/tables-concepts/01-example-table.png)](assets/tables-concepts/01-example-table.png)

## Storage formats

How data is physically structured and tracked in object storage. Both formats add a transactional layer = ACID + time travel.

| Format | Supported on | Notes |
|---|---|---|
| **Delta Lake** | managed, external, foreign | **Default** for managed + external. |
| **Apache Iceberg** | managed, foreign | Use when integrating with the Iceberg ecosystem. |

> Note the asymmetry: **external tables = Delta only** (no Iceberg); **Iceberg has no external variant** on this page. Foreign supports both.

## Table types

Type = how data is **owned and accessed**, set by the managing catalog:

| Type | Managing catalog | Read/write | Perf optimization | Storage-cost optimization |
|---|---|---|---|---|
| **Managed** | Unity Catalog | Yes | Yes | Yes |
| **Temporary** | None (session-scoped managed table) | Yes | Yes | Yes |
| **External** | None (files only) | Yes | Manual only | Manual only |
| **Foreign** | An external system / catalog service | **Read only** | No | No |

- **Managed** — UC manages **both data files and metadata**; files live in UC's managed storage location. Default + recommended: auto-optimization, lower cost, external-system access (e.g. Trino). → [[managed-tables]]
- **External** (aka *unmanaged*) — references data in external cloud object storage. Databricks registers **metadata only** and does not manage the files. Multiple formats incl. Delta → readable by external systems. Optimization is **manual only**. → [[external-tables]]
- **Foreign** — data in external systems connected via **Lakehouse Federation**. **Read-only** on Databricks (learning-path I8). → [[foreign-tables]]
- **Temporary** — session-scoped; store intermediate results without a permanent table. **Auto-dropped at session end**, and **no catalog/schema privileges needed** to create. → [[temporary-tables]]

## Permissions

A table is the third level of the UC namespace (`catalog.schema.table`):

[![Unity Catalog object model, focused on table](assets/tables-concepts/02-object-model-table.png)](assets/tables-concepts/02-object-model-table.png)

Most table operations require **`USE CATALOG`** + **`USE SCHEMA`** on the containing catalog/schema, plus:

| Operation | Additional permission |
|---|---|
| Create a table | `CREATE TABLE` on the schema |
| Query a table | `SELECT` on the table |
| Update / delete / merge / insert | `SELECT` + `MODIFY` on the table |
| Drop a table | `MANAGE` on the table |
| Replace a table | `MANAGE` on the table + `CREATE TABLE` on the schema |

SQL syntax refs: `CREATE TABLE [USING]`, `ALTER TABLE`, `DROP TABLE`, `SHOW TABLES`.

Related: [[managed-tables]], [[external-tables]], [[foreign-tables]], [[temporary-tables]], [DCDE-SG Ch 3 notes](../dcde-sg/ch03-mastering-relational-entities/).
