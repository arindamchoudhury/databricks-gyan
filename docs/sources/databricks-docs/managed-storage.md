# Specify a managed storage location in Unity Catalog

> **Source:** [docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/managed-storage](https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/managed-storage)
> **Added:** 2026-06-23
> **Source updated:** 2026-05-20
> **Tags:** unity-catalog, managed-storage, storage-location, external-location, catalog, schema, metastore, volumes, B1, B4
> **Type:** documentation

Where managed-table and managed-volume **data + metadata files physically land** in cloud object storage. A managed storage location attaches to a **metastore, catalog, or schema**, and lower levels override higher. This is the "managed storage location" referenced by [[managed-tables]] — that page is the *what*, this is the *where*. Databricks recommends setting it at the **catalog level** for logical data isolation. Managed storage **cannot overlap** external tables/volumes, and new UC-enabled workspaces are created **without** a metastore-level managed location (auto-enabled workspaces get a workspace catalog with one).

## Hierarchy & resolution

Attach managed storage to a metastore, catalog, or schema; lower levels override higher when a managed table/volume is created.

| UC object | How to set | Relation to external location |
|---|---|---|
| **Metastore** | Account admin, at metastore creation | Cannot overlap an external location |
| **Standard catalog** | `MANAGED LOCATION` at create, or `ALTER CATALOG SET MANAGED LOCATION` | Must be **contained within** an external location |
| **Foreign catalog** | After creation, via Catalog Explorer only | Must be contained within an external location |
| **Schema** | `MANAGED LOCATION` at create, or `ALTER SCHEMA SET MANAGED LOCATION` | Must be contained within an external location |

Resolution when creating a managed table/volume: schema location → else catalog location → else metastore location. Databricks recommends **catalog-level**.

## Storage root vs storage location

When you give a `MANAGED LOCATION`, UC records it as the **Storage Root** and appends hashed subdirs to guarantee uniqueness:

| Object | Path |
|---|---|
| Schema | `<storage-root>/__unitystorage/schemas/00000000-0000-0000-0000-000000000000` |
| Catalog | `<storage-root>/__unitystorage/catalogs/00000000-0000-0000-0000-000000000000` |

The fully-qualified path is tracked as the **Storage Location**. The same managed storage location can be specified for multiple schemas/catalogs.

## Required privileges

- **Set at create** (catalog/schema): `CREATE MANAGED STORAGE` on the external location.
- **Metastore-level**: account admin (optional).
- **Foreign catalog**: `MANAGE` + `USE CATALOG`, or catalog owner.
- **Alter** (standard catalog/schema): owner or `MANAGE` on the object **and** `CREATE MANAGED STORAGE` on the target external location.

## SQL

```sql
CREATE CATALOG <catalog-name> MANAGED LOCATION 's3://<external-location-bucket-path>/<directory>';
ALTER CATALOG <catalog-name> SET MANAGED LOCATION 's3://…';   -- DBR 18.1+; new objects only
CREATE SCHEMA <catalog>.<schema-name> MANAGED LOCATION 's3://…';
ALTER SCHEMA <catalog>.<schema-name> SET MANAGED LOCATION 's3://…';  -- DBR 18.1+; new objects only
```

- The `MANAGED LOCATION` string (URI scheme + path) must be **≤ 150 characters**.
- **Cloud-agnostic** — only the URI scheme changes: AWS `s3://…`, GCP `gcs://…`, Azure `abfss://…`. All rules, privileges, hierarchy, and `ALTER` semantics are identical.
- Foreign catalog: Catalog Explorer only — Catalog → catalog name → Storage location → **Add storage location** → pick/create external location → Save.

> ⚠️ **`ALTER … SET MANAGED LOCATION` does not migrate existing data.** Only managed tables/volumes created *after* the change use the new location; existing managed objects stay where they are.

Related: [[managed-tables]], [[tables-concepts]].
