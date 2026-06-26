# Temporary tables

> **Source:** [docs.databricks.com/aws/en/tables/temporary-tables](https://docs.databricks.com/aws/en/tables/temporary-tables)
> **Added:** 2026-06-25
> **Source updated:** 2026-06-23
> **Tags:** tables, table-types, temporary, session-scoped, delta, sql, dbr-18.1, no-privileges
> **Type:** documentation

A **temporary table** is the fourth table type alongside [[managed-tables]], [[external-tables]], and [[foreign-tables]] — but a different beast: it stores data **only for the duration of a Databricks session** and lives **outside the catalog namespace** entirely (referenced by bare name, no catalog/schema). Use it to materialize intermediate results for exploratory work or SQL pipelines without creating permanent objects. It's backed by **Delta by default**, **any user can create one with no `CREATE TABLE` privilege**, it's **session-isolated** (invisible to everyone else), and Databricks **auto-drops and reclaims storage** at session end or after **seven days**, whichever comes first. It applies to **Databricks SQL** and **Databricks Runtime 18.1+** (a new feature — pre-18.1 runtimes don't have it).

## When to use (and when not)

Use a temp table to: store short-lived intermediate data during exploratory analysis or workflow development; reuse query results across multiple operations **in the same session**; get a table-like interface without polluting the catalog namespace. If the data must **persist past the session** or be **shared with other users/jobs**, use a permanent UC table instead ([[managed-tables]]).

> 💡 **Temp table vs temporary *view*** (clarification, not on page). Both are session-scoped and share one namespace, but a temp **table** *materializes* data (a real Delta dataset in managed storage you can `INSERT`/`UPDATE`/`MERGE` into), whereas a temp **view** is just a saved query definition (re-executed on read, no stored rows). This page is the table half. Also distinct from **global temporary views**, which are cross-session within a cluster and (per the learning-path delta note) **unsupported on serverless**.

## Create / replace

`CREATE [TEMPORARY|TEMP] TABLE` — empty with a schema, or `AS SELECT …` / `AS VALUES …` from query results. Replace with `[CREATE OR] REPLACE [TEMPORARY|TEMP] TABLE`.

```sql
CREATE TEMPORARY TABLE temp_customers (id INT, name STRING);

CREATE OR REPLACE TEMP TABLE temp_recent_orders AS
SELECT order_id, customer_id, order_date, amount
FROM prod.sales.orders
WHERE order_date >= current_date() - INTERVAL 30 DAYS;
```

> ⚠️ **Two `REPLACE` gotchas.** (1) **Don't add `USING`** — temp tables are Delta by default and specifying a format errors. (2) On `REPLACE`, the **`TEMPORARY`/`TEMP` keyword is mandatory** — a bare `REPLACE TABLE foo` replaces a *permanent* table named `foo`, not your temp one.

## Query and name resolution

Reference by bare name. Resolution order: **(1) temp tables in the current session, then (2) permanent tables in the current schema.** A temp table therefore **shadows** a same-named permanent table; to reach the permanent one, use the full three-level name (`prod.sales.customers`).

## Modify

`INSERT`, `UPDATE`, and `MERGE INTO` are supported. **`DELETE FROM` is not** — use `MERGE INTO` with a filter, or recreate the table with filtered data.

## Drop and lifecycle

Auto-dropped at session end; explicit `DROP TEMP TABLE [IF EXISTS]` available. Hard ceiling of **7 days** from session creation regardless of activity. Applies to notebooks, SQL Editor, jobs, and JDBC/ODBC.

> "Any user can create temporary tables. You don't need CREATE TABLE privileges on a catalog or schema in Unity Catalog." Other users **cannot read, modify, or even detect** your temp tables — including a second user in the same notebook session.

## Storage and cleanup

Managed automatically; data does land in cloud storage. **Serverless** → default storage (uses your customer-managed key for managed services if configured). **Classic** → the workspace storage bucket set at workspace creation. After expiry — including disconnect or unexpected cluster shutdown — storage is reclaimed in the background, usually within a few days.

## Limitations

`ALTER TABLE` ✗ · shallow/deep **clone** ✗ · **time travel** ✗ · **streaming** (e.g. `foreachBatch`) ✗ · **DataFrame APIs** ✗ (SQL only) · **multi-user** in a notebook session ✗ · **Dedicated (single-user) clusters** ✗ · **AWS GovCloud / GovCloud DoD** ✗. Path-overlap failures → "Resolve storage path conflicts".

Related: [[tables-concepts]], [[managed-tables]], [[external-tables]], [[foreign-tables]].
