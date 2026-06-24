# Specify a managed storage location in Unity Catalog

> **Source:** [docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/managed-storage](https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/managed-storage)
> **Added:** 2026-06-23
> **Source updated:** 2026-05-20
> **Tags:** unity-catalog, managed-storage, storage-location, external-location, catalog, schema, metastore, volumes, B1, B4
> **Type:** documentation

## Summary

Where managed-table and managed-volume **data + metadata files physically land** in cloud object storage. A managed storage location attaches to a **metastore, catalog, or schema**; lower levels override higher. This is the "managed storage location" referenced by [[managed-tables]] — this page is the *where*, that page is the *what*. Databricks recommends setting it at the **catalog level** for logical data isolation.

## Key points

- Managed storage holds data **and metadata** for managed tables + managed volumes.
- **Resolution order (most-specific wins)**: schema location → else catalog location → else metastore location.
- Managed storage **cannot overlap** external tables/volumes (UC prevents location-governance overlap).
- New UC-enabled workspaces are created **without** a metastore-level managed location; auto-enabled workspaces get a **workspace catalog** with one.
- Catalog/schema `MANAGED LOCATION` must be **contained within an external location**; the metastore one cannot overlap an external location.
- `ALTER ... SET MANAGED LOCATION` (DBR **18.1+**) affects **only new** managed objects — existing ones are **not moved**.

## Notes

### Hierarchy & resolution

Attach managed storage to metastore, catalog, or schema. Lower levels override higher when a managed table/volume is created.

| UC object | How to set | Relation to external location |
|---|---|---|
| **Metastore** | Account admin, at metastore creation | Cannot overlap an external location |
| **Standard catalog** | `MANAGED LOCATION` at create, or `ALTER CATALOG SET MANAGED LOCATION` | Must be **contained within** an external location |
| **Foreign catalog** | After creation, via Catalog Explorer only | Must be contained within an external location |
| **Schema** | `MANAGED LOCATION` at create, or `ALTER SCHEMA SET MANAGED LOCATION` | Must be contained within an external location |

Resolution rules when creating a managed table/volume:

1. Schema has a managed location → use it.
2. Else catalog has one → use it.
3. Else → metastore managed location.

Databricks recommends **catalog-level** for logical data isolation (metastore + schema are options).

### Storage root vs storage location

When you give a `MANAGED LOCATION`, UC records it as the **Storage Root**. To guarantee uniqueness, UC appends hashed subdirs:

| Object | Path |
|---|---|
| Schema | `<storage-root>/__unitystorage/schemas/00000000-0000-0000-0000-000000000000` |
| Catalog | `<storage-root>/__unitystorage/catalogs/00000000-0000-0000-0000-000000000000` |

The fully-qualified path is tracked as the **Storage Location**. The same managed storage location can be specified for multiple schemas/catalogs.

### Required privileges

- **Set at create** (catalog/schema): `CREATE MANAGED STORAGE` on the external location.
- **Metastore-level**: account admin (optional).
- **Foreign catalog**: `MANAGE` + `USE CATALOG`, or catalog owner.
- **Alter** (standard catalog/schema): owner or `MANAGE` on the object **and** `CREATE MANAGED STORAGE` on the target external location.

### SQL

```sql
-- Catalog at creation
CREATE CATALOG <catalog-name>
MANAGED LOCATION 's3://<external-location-bucket-path>/<directory>';

-- Alter catalog (DBR 18.1+; new objects only, existing not moved)
ALTER CATALOG <catalog-name>
SET MANAGED LOCATION 's3://<external-location-bucket-path>/<directory>';

-- Schema at creation
CREATE SCHEMA <catalog>.<schema-name>
MANAGED LOCATION 's3://<external-location-bucket-path>/<directory>';

-- Alter schema (DBR 18.1+; new objects only)
ALTER SCHEMA <catalog>.<schema-name>
SET MANAGED LOCATION 's3://<external-location-bucket-path>/<directory>';
```

- `MANAGED LOCATION` string (URI scheme + path) must be **≤ 150 characters**.
- **Cloud-agnostic.** The page is identical across clouds — only the URI scheme changes: AWS `s3://…`, GCP `gcs://…`, Azure `abfss://…`. All rules, privileges, hierarchy, and `ALTER` semantics are the same. (Verified by diffing the [AWS](https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/managed-storage) and [GCP](https://docs.databricks.com/gcp/en/connect/unity-catalog/cloud-storage/managed-storage) pages, 2026-06-23 — only the example URI scheme differs.)
- Foreign catalog: Catalog Explorer only — Catalog → catalog name → Storage location → **Add storage location** → pick/create external location → Save.

> ⚠️ **`ALTER ... SET MANAGED LOCATION` does not migrate existing data.** Only managed tables/volumes created *after* the change use the new location. Existing managed objects stay where they are.

## Open questions

- The page says catalog/schema managed locations "must be contained within an external location," but [[managed-tables]] frames managed storage as UC-controlled and external locations as the basis for *external* tables. The relationship — managed storage carved out of an external-location-governed path — isn't spelled out here beyond the containment rule.

## Related sources

- [[managed-tables]] — managed tables store their files here; "Data files for managed tables are stored in the schema or catalog containing them" points to this page.
- [[tables-concepts]] — managed vs external types; this is the storage side of the managed type.

## References

- [Specify a managed storage location in Unity Catalog](https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/managed-storage) — this page
- Learning path: **B1 — Databricks Platform & Architecture**, **B4 — Spark SQL & Relational Entities**
