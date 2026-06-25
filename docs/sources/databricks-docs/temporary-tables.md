# Temporary tables

> **Source:** [docs.databricks.com/aws/en/tables/temporary-tables](https://docs.databricks.com/aws/en/tables/temporary-tables)
> **Added:** 2026-06-25
> **Source updated:** 2026-06-23
> **Tags:** tables, table-types, temporary, session-scoped, delta, sql, dbr-18.1, no-privileges
> **Type:** documentation

## Summary

The fourth table type alongside [[managed-tables]], [[external-tables]], and [[foreign-tables]] — but a different beast: a **temporary table** stores data **only for the duration of a Databricks session** and lives **outside the catalog namespace** entirely (referenced by bare name, no catalog/schema). Use it to materialize intermediate results for exploratory work or SQL pipelines without creating permanent objects. Backed by **Delta by default**, **any user can create one with no `CREATE TABLE` privilege**, it's **session-isolated** (invisible to everyone else), and Databricks **auto-drops and reclaims storage** when the session ends or after **seven days**, whichever comes first.

> **Applies to:** Databricks SQL · **Databricks Runtime 18.1 and above**. (New feature — pre-18.1 runtimes don't have it.)

## Key points

- **Session-scoped lifetime.** Exists only in the session that created it; **max 7 days** from session creation; gone at session end or 7 days, whichever is first. Applies to notebooks, SQL Editor, jobs, and JDBC/ODBC.
- **No catalog namespace.** Created and queried by **bare table name only** — no catalog/schema. Not a Unity Catalog object.
- **No privileges needed.** Any user can create one; **no `CREATE TABLE` on catalog/schema required** (contrast every other table type).
- **Session isolation.** Other users **cannot read, modify, or even detect** your temp tables — including a second user in the same notebook session.
- **Delta by default; do NOT specify `USING`.** Explicitly specifying a format **errors**. (So no Iceberg temp tables.)
- **Name precedence + shares a namespace with temp views.** A temp table shadows a permanent table of the same name within the session; you can't have a temp table and a temp **view** of the same name in one session.
- **DML yes, DDL/lifecycle features no.** `INSERT`/`UPDATE`/`MERGE INTO` work; **`DELETE FROM`, `ALTER TABLE`, clone, time travel, streaming, and DataFrame APIs do not.**
- **Storage is managed for you** and **auto-reclaimed** in the background after expiry (typically within a few days).

## Notes

### When to use (and when not)

Use a temp table to: store short-lived intermediate data during exploratory analysis or workflow development; reuse query results across multiple operations **in the same session**; get a table-like interface without polluting the catalog namespace.

If the data must **persist past the session** or be **shared with other users/jobs**, use a permanent UC table instead ([[managed-tables]]).

> 💡 **Clarification (not on page) — temp table vs temporary *view*.** Both are session-scoped and share one namespace, but a temp **table** *materializes* data (it's a real Delta dataset in managed storage you can `INSERT`/`UPDATE`/`MERGE` into), whereas a temp **view** is just a saved query definition (re-executed on read, no stored rows). The glossary already distinguishes these; this page is the table half. Also distinct from **global temporary views**, which are cross-session within a cluster and (per the learning-path delta note) **unsupported on serverless**.

### Create / replace

`CREATE [TEMPORARY|TEMP] TABLE` — empty with a schema, or `AS SELECT …` / `AS VALUES …` from query results. Replace with `[CREATE OR] REPLACE [TEMPORARY|TEMP] TABLE`.

```sql
CREATE TEMPORARY TABLE temp_customers (id INT, name STRING);

CREATE OR REPLACE TEMP TABLE temp_recent_orders AS
SELECT order_id, customer_id, order_date, amount
FROM prod.sales.orders
WHERE order_date >= current_date() - INTERVAL 30 DAYS;
```

> ⚠️ **Two `REPLACE` gotchas.** (1) **Don't add `USING`** — temp tables are Delta by default and specifying a format errors. (2) On `REPLACE`, the **`TEMPORARY`/`TEMP` keyword is mandatory** — a bare `REPLACE TABLE foo` replaces a *permanent* table named `foo`, not your temp one.

### Query + name resolution

Reference by bare name. Resolution order: **(1) temp tables in the current session, then (2) permanent tables in the current schema.** A temp table therefore **shadows** a same-named permanent table; to reach the permanent one, use the full three-level name (`prod.sales.customers`). See `[[name-resolution]]` semantics on the docs.

### Modify

`INSERT`, `UPDATE`, `MERGE INTO` are supported. **`DELETE FROM` is not** — use `MERGE INTO` with a filter, or recreate the table with filtered data.

### Drop + lifecycle

Auto-dropped at session end; explicit `DROP TEMP TABLE [IF EXISTS]` available. Hard ceiling of **7 days** from session creation regardless of activity.

### Storage & cleanup

Managed automatically; data does land in cloud storage. **Serverless** → default storage (uses your customer-managed key for managed services if configured). **Classic** → the workspace storage bucket set at workspace creation (encryption configurable there). After expiry — including disconnect or unexpected cluster shutdown — storage is reclaimed in the background, usually within a few days.

### Limitations (the list to remember)

`ALTER TABLE` ✗ · shallow/deep **clone** ✗ · **time travel** ✗ · **streaming** (e.g. `foreachBatch`) ✗ · **DataFrame APIs** ✗ (SQL only) · **multi-user** in a notebook session ✗ · **Dedicated (single-user) clusters** ✗ · **AWS GovCloud / GovCloud DoD** ✗. Path-overlap failures → "Resolve storage path conflicts".

## Quotes worth keeping

> "Temporary tables store data for the duration of a Databricks session." (intro)

> "Any user can create temporary tables. You don't need CREATE TABLE privileges on a catalog or schema in Unity Catalog." (Isolation and privileges)

## Open questions

- Page says data uses Delta and is stored in managed/default storage, but temp tables sit **outside** the UC namespace — unclear how (or whether) they relate to a catalog's **managed storage** location vs. pure workspace storage. The serverless-vs-classic split above suggests it's workspace-level, not catalog-level.

## Related sources

- [[tables-concepts]] — parent overview; lists temporary alongside managed/external/foreign as a table type.
- [[managed-tables]] — the persistent default; use instead when data must outlive the session or be shared.
- [[external-tables]] · [[foreign-tables]] — the other two non-default table types, both of which (unlike temp) are catalog-namespaced and need privileges.
