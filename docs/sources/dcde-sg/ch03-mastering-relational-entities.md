# Ch 3 — Mastering Relational Entities in Databricks

> **Source:** Derar Alhussein, *Databricks Certified Data Engineer Associate Study Guide* (O'Reilly, 1st Ed., Feb 2025) — Chapter 3, PDF pp. 169–230.
>
> **Companion notebooks:** `Chapter 3 - Mastering Relational Entities in Databricks/` — `3.1 - Databases and Tables.sql` (§4), `3.2A - Views.sql` (§9) and `3.2B - Views (Session 2).sql` (§9.4) map cell-for-cell to the hands-on sections below.
>
> **Added:** 2026-06-22
>
> **Tags:** databases, schemas, managed-tables, external-tables, ctas, constraints, clone, views, hive-metastore, unity-catalog, B4
>
> **Type:** book

> *Relational entities from the metastore down to storage: databases (= schemas), managed vs external tables and what DROP does to each, CTAS + table options, NOT NULL/CHECK constraints, deep vs shallow clone, and the three kinds of view (stored, temp, global temp).*

> 📌 **Notes adapted to the 2026 platform.** The book targets DBR 13.3 LTS and demos everything against the legacy `hive_metastore` catalog with `dbfs:` / `/mnt/demo` mount paths. Key shifts flagged with ⚠️ throughout: (1) **Unity Catalog is the default** in all new 2026 workspaces — a "database" is a **schema** in the 3-level namespace `catalog.schema.table`; (2) **DBFS root + mounts are deprecated** (off by default for accounts created after 2025-12-19) — the book's `dbfs:/mnt/demo` and `dbfs:/Shared/...` paths won't run on a UC-only workspace; use **UC Volumes / external locations**; (3) UC **external tables** require the `LOCATION` to sit under a **registered external location** (path + storage credential), not an arbitrary mount path; (4) **global temporary views are not supported on serverless compute** (the new default compute) and are treated as legacy; (5) UC adds **informational `PRIMARY KEY` / `FOREIGN KEY`** constraints on top of the book's enforced `NOT NULL` / `CHECK`. See [research-cache](../../research-cache/dcde-sg-ch03-facts/).

> 📎 **Overlaps:** builds directly on [Ch 2 — Managing Data with Delta Lake](ch02-managing-data-with-delta-lake/) (every table here is a Delta table). Data governance / Unity Catalog gets full treatment in Ch 8.

---

## 1. Understanding Relational Entities

Three entity types organize structured data in Databricks: **databases**, **tables**, **views**. The chapter's throughline is *how each entity maps to the metastore (metadata) versus storage (actual files)* — that mapping explains every behavior, especially what `DROP` deletes.

---

## 2. Databases in Databricks

A **database** in Databricks **is a schema** in a data catalog — the two words are interchangeable, and so are the DDL keywords:

```sql
CREATE DATABASE db_x;   -- identical to:
CREATE SCHEMA  db_x;
```

A schema is a logical container for tables, views, and functions.

**The metastore.** Every workspace ships with a local catalog called **`hive_metastore`** that all clusters can read/write. The Hive metastore is a metadata repository — it stores table/view/partition definitions, data formats, and storage locations. It stores *metadata only*, never the data itself.

> ⚠️ **`hive_metastore` is legacy — and on new workspaces it's gone entirely.** In 2026 the metastore concept is **Unity Catalog**, and the namespace is **three levels**: `catalog.schema.table`. A "database" maps to the **schema** level. Whether `hive_metastore` shows up as a top-level catalog depends on the **"Disable legacy features"** account setting: where HMS is *enabled*, it appears alongside the UC catalogs (UC runs next to it); where it's *disabled* — the **default for accounts created after 2025-12-19, with no opt-out** — `hive_metastore` does **not appear at all** and the Catalog Explorer shows only UC catalogs (e.g. `main`, `system`, the workspace catalog). The book's `USE CATALOG hive_metastore` line only works on a workspace where an admin has left HMS enabled; on a UC-only workspace it errors. See [Ch 2 §2.1](ch02-managing-data-with-delta-lake/) for the full HMS/DBFS deprecation note.

### 2.1 The default database

`hive_metastore` ships with a database named **`default`**. Tables created without naming a database land there. Their data goes to Hive's default warehouse directory, typically **`dbfs:/user/hive/warehouse`**.

### 2.2 Creating databases

`CREATE SCHEMA db_x` registers the schema in the metastore and creates a folder `db_x.db` under `/user/hive/warehouse`. The **`.db` extension** distinguishes database folders from table folders in the same directory.

### 2.3 Custom-location databases

Add `LOCATION` to put the schema's folder outside the default warehouse path:

```sql
CREATE SCHEMA custom
LOCATION 'dbfs:/Shared/schemas/custom.db';
```

The schema *definition* still lives in the metastore; only its data folder moves. Managed tables created inside it store their data under this custom path.

> ⚠️ **2026:** a UC schema's (or catalog's) **managed location** must itself be a **registered external location** (a governed cloud path backed by a storage credential). `dbfs:/Shared/...` is a DBFS path and won't work on a UC-only workspace.

---

## 3. Tables in Databricks — managed vs external

Two table types. The distinction is **who owns the data files**, which determines **what `DROP TABLE` deletes**.

| | **Managed table** | **External table** |
|---|---|---|
| Created with | `CREATE TABLE t (…)` (no `LOCATION`) | `CREATE TABLE t (…) LOCATION '<path>'` |
| Data location | inside the database directory (metastore-controlled) | a path *you* specify, outside the DB directory |
| Metadata owner | metastore | metastore |
| Data owner | metastore | you |
| `DROP TABLE` | deletes **metadata + data files** | deletes **metadata only**; data files persist |

**Managed table** — the default. The metastore owns metadata *and* data, managing the full lifecycle. Dropping it permanently deletes the underlying files. Convenient, but dangerous: a `DROP` is unrecoverable (modulo `UNDROP TABLE` within retention — a UC feature not in the book).

**External table** — the metastore owns metadata only; data files live at a `LOCATION` you control. Dropping it leaves the files intact. Use it when the data is shared with other tools or must outlive the table definition (e.g. data in an S3 bucket / ADLS container).

> 💡 **Exam framing:** "Dropping a managed table deletes its data files; dropping an external table does not." The presence/absence of `LOCATION` at create time is what makes a table external/managed.

> ⚠️ **2026 — what "external" means in UC.** On Unity Catalog an external table's `LOCATION` must fall under a **registered external location** (a cloud path + storage credential governing access), and you need `CREATE EXTERNAL TABLE` privilege on it. UC **managed** tables land in UC managed storage (`s3://…/__unity_storage/catalogs/<catalog_id>/tables/<table_id>`, addressed by GUID), not `dbfs:/user/hive/warehouse`. The book's arbitrary `dbfs:/mnt/demo/...` external paths are pre-UC mounts and won't resolve on a UC-only workspace — substitute a UC Volume or external-location path. The managed-vs-external *DROP semantics above are unchanged*.

> ⚠️ **2026 — the table-type model is wider than the book's two.** Per [Databricks tables concepts](https://docs.databricks.com/aws/en/tables/tables-concepts), Databricks now defines **three primary table types** plus session-scoped tables, across **two** open storage formats:
>
> | Table type | Managing catalog | Notes |
> |---|---|---|
> | **Managed** | Unity Catalog (owns metadata **+** data) | The **default**, and what Databricks **recommends for every new table** — auto perf optimization, lower storage/compute cost, readable by external engines (e.g. Trino). DROP deletes data. |
> | **External** | none (UC owns metadata, files only) | Manual perf/cost optimization. DROP keeps data. Use when files are shared with other tools. |
> | **Foreign** | an external system via Lakehouse Federation | **Read-only** on Databricks (e.g. a federated Postgres/Snowflake table). Not in the book. |
> | **Temporary** | none (session-scoped managed table) | Auto-dropped at session end; no catalog/schema privilege needed. A *table*, distinct from a temp **view** (§9.2). |
>
> - **Storage formats:** **Delta Lake is the default** for managed + external (book is right that everything's Delta by default). **Apache Iceberg** is now also supported (managed + foreign) for Iceberg-ecosystem interop — the book predates this.
> - **Note the recommendation flips the book's framing.** The book pitches external tables as the "flexible/control" choice; in UC, **managed is the recommended default** (governance + auto-optimization), external is for when files must live outside UC's lifecycle.
> - **UC permissions for these ops** (book omits, since HMS had none): `CREATE TABLE` on the schema to create; `SELECT` to query; `SELECT`+`MODIFY` to write; **`MANAGE`** to `DROP` or `REPLACE`. Plus `USE CATALOG` + `USE SCHEMA` on the parents.

---

## 4. Putting it into practice — notebook `3.1 - Databases and Tables`

Three scenarios, each repeating the managed-vs-external contrast: the **default** schema, a **new** schema, and a **custom-location** schema. Open the Catalog Explorer (left sidebar **Catalog** tab) to watch objects appear/disappear, or use the catalog icon in the notebook editor.

### 4.1 Working in the default schema

```sql
USE CATALOG hive_metastore;

-- Managed table: no LOCATION → data under the DB directory
CREATE TABLE managed_default
  (country STRING, code STRING, dial_code STRING);
INSERT INTO managed_default VALUES ('France', 'Fr', '+33');

DESCRIBE EXTENDED managed_default;
```

`DESCRIBE EXTENDED` returns advanced metadata; three fields matter:

- **Type** → `MANAGED`
- **Location** → `dbfs:/user/hive/warehouse/managed_default`
- **Provider** → `delta` (it's a Delta table)

```sql
-- External table: LOCATION present → data lives outside the DB directory
CREATE TABLE external_default
  (country STRING, code STRING, dial_code STRING)
LOCATION 'dbfs:/mnt/demo/external_default';
INSERT INTO external_default VALUES ('France', 'Fr', '+33');

DESCRIBE EXTENDED external_default;   -- Type → EXTERNAL, Location → dbfs:/mnt/demo/...
```

**Dropping — the payoff.**

```sql
DROP TABLE managed_default;
SELECT * FROM managed_default;
-- [TABLE_OR_VIEW_NOT_FOUND]  (metadata gone)
```
```python
%fs ls 'dbfs:/user/hive/warehouse/managed_default'
# FileNotFoundException — data files deleted too
```

```sql
DROP TABLE external_default;
SELECT * FROM external_default;     -- TABLE_OR_VIEW_NOT_FOUND (metadata gone)
```
```python
%fs ls 'dbfs:/mnt/demo/external_default'   # files STILL THERE
```

The dropped external table's data is still queryable directly by path, proving the files survive:

```sql
SELECT * FROM DELTA.`dbfs:/mnt/demo/external_default`;   -- works after DROP
```

Clean up the orphaned files manually:

```python
%python
dbutils.fs.rm('dbfs:/mnt/demo/external_default', True)   # recurse = True
```

> ⚠️ `%fs`, `dbutils.fs.rm`, and `DELTA.\`dbfs:/mnt/...\`` all assume DBFS mounts. On a UC-only workspace these paths don't exist; use a UC Volume path (`/Volumes/<catalog>/<schema>/<volume>/...`) and note that UC managed-table files aren't browsable with `%fs ls` at all.

### 4.2 Working in a new schema

```sql
CREATE SCHEMA new_default;
DESCRIBE DATABASE EXTENDED new_default;   -- Location → .../warehouse/new_default.db

USE DATABASE new_default;                 -- set current schema

CREATE TABLE managed_new_default
  (country STRING, code STRING, dial_code STRING);
INSERT INTO managed_new_default VALUES ('France', 'Fr', '+33');

CREATE TABLE external_new_default
  (country STRING, code STRING, dial_code STRING)
LOCATION 'dbfs:/mnt/demo/external_new_default';
INSERT INTO external_new_default VALUES ('France', 'Fr', '+33');
```

Same result as §4.1, just inside `new_default.db`: the managed table sits under the schema folder; the external table sits at its `LOCATION`. After `DROP TABLE`, the managed table's files vanish (`FileNotFoundException` under `new_default.db/`), the external table's files persist at `/mnt/demo/`.

### 4.3 Working in a custom-location schema

```sql
CREATE SCHEMA custom
LOCATION 'dbfs:/Shared/schemas/custom.db';
DESCRIBE DATABASE EXTENDED custom;        -- Location → dbfs:/Shared/schemas/custom.db

USE DATABASE custom;
CREATE TABLE managed_custom  (…);         -- data → dbfs:/Shared/schemas/custom.db/managed_custom
CREATE TABLE external_custom (…) LOCATION 'dbfs:/mnt/demo/external_custom';
```

The lesson generalizes: a **managed** table always lands inside its schema's directory — *wherever that directory is* (default warehouse or custom location) — and `DROP` deletes its files. An **external** table always lands at its own `LOCATION` and survives `DROP`. The schema's location only moves where managed tables go; it never changes the managed-vs-external behavior.

> 💡 **Three takeaways the demos hammer home:**
> 1. `LOCATION` on `CREATE TABLE` → external. No `LOCATION` → managed.
> 2. `DROP` a managed table = data gone. `DROP` an external table = metadata gone, data stays.
> 3. A managed table's physical home follows its *schema's* location; an external table ignores it.

---

## 5. Setting up Delta tables — CTAS

`CREATE TABLE AS SELECT` creates **and** populates a table from a query in one statement:

```sql
CREATE TABLE table_2
AS SELECT * FROM table_1;
```

- **Schema is inferred** from the query result — no manual column declaration.
- Can transform during creation (rename, project, filter):

```sql
CREATE TABLE table_2
AS SELECT col_1, col_3 AS new_col_3 FROM table_1;
```

Options can be layered onto the `CREATE TABLE` clause:

```sql
CREATE TABLE new_users
  COMMENT "Contains PII"
  PARTITIONED BY (city, birth_date)
  LOCATION '/some/path'
  AS SELECT id, name, email, birth_date, city FROM users;
```

- **`COMMENT`** — descriptive note aiding discovery (here flags PII).
- **`PARTITIONED BY`** — splits data into subfolders by column value. Helps *large* tables via efficient retrieval, but for small/medium tables the **small-files problem** (many tiny files → poor compaction + data skipping) usually outweighs the benefit. Apply partitioning selectively.
- **`LOCATION`** — makes the table external (as in §3).

> ⚠️ **2026:** prefer **liquid clustering** over `PARTITIONED BY` for new tables (see [Ch 2 §7](ch02-managing-data-with-delta-lake/)). Partitioning is discouraged for tables < 1 TB.

### 5.1 `CREATE TABLE` vs CTAS

| | Regular `CREATE TABLE` | CTAS |
|---|---|---|
| Schema declaration | **Manual** — declare every column + type | **Inferred** from the SELECT |
| Populating data | Creates an **empty** table; needs `INSERT INTO` | Creates **and** loads in one step |

---

## 6. Table constraints

After creating a Delta table you can add constraints to protect integrity. The book lists **two** types:

- **`NOT NULL`** constraints
- **`CHECK`** constraints

```sql
ALTER TABLE table_name ADD CONSTRAINT <name> <definition>;
```

**Rule:** existing data must already satisfy a constraint before you add it, or the `ALTER` fails. Once enforced, any new write that violates it fails.

A `CHECK` constraint is like a `WHERE` clause — a condition incoming rows must satisfy:

```sql
ALTER TABLE my_table
ADD CONSTRAINT valid_date CHECK (date >= '2024-01-01' AND date <= '2024-12-31');
```

`valid_date` is the constraint name; any insert/update with a date outside 2024 is rejected.

> ⚠️ **2026 — UC adds informational keys.** Beyond the book's two *enforced* constraints, Unity Catalog supports **informational `PRIMARY KEY` and `FOREIGN KEY`** constraints. These are **not enforced** (Databricks won't reject violating rows) — they exist for **query optimization** and for ER-diagram / lineage tooling, and surface in `INFORMATION_SCHEMA.TABLE_CONSTRAINTS`. `CHECK` remains the only constraint validated against both existing and new data.

---

## 7. Cloning Delta Lake tables

Two ways to copy a table for backup or experimentation.

**Deep clone** — copies **data + metadata**. Standalone copy; slow for large tables (all files copied). Can run incrementally — re-run with `CREATE OR REPLACE` to sync new changes from source:

```sql
CREATE TABLE table_clone DEEP CLONE source_table;
CREATE OR REPLACE TABLE table_clone DEEP CLONE source_table;   -- incremental re-sync
```

**Shallow clone** — copies **only the transaction log** (metadata + file references). No data movement → fast. Ideal for testing changes against a table without touching its data — perfect for dev environments:

```sql
CREATE TABLE table_clone SHALLOW CLONE source_table;
```

**Either way:** modifications to the clone are tracked **separately** from the source, so experiments never corrupt the original.

> ⚠️ **2026 — UC clone rules.** Shallow clone for UC managed tables needs **DBR 13.3+**. You can only clone **managed→managed** and **external→external**, and you **cannot nest** shallow clones. Caution with shallow clones of *managed* tables: a `VACUUM` on the source can delete files the clone still references (the clone points at the source's files). External-table shallow clones are safer here.

---

## 8. Exploring Views

A **view** is a virtual table with no physical data — a **saved SQL query** that re-executes against its source tables *every time it's queried*. A view over a join, for example, re-runs the join on each read.

Three types: **stored views**, **temporary views**, **global temporary views**.

---

## 9. View types in practice — notebook `3.2A - Views`

Seed table for all examples:

```sql
USE CATALOG hive_metastore;

CREATE TABLE IF NOT EXISTS cars
  (id INT, model STRING, brand STRING, year INT);

INSERT INTO cars VALUES
  (1, 'Cybertruck', 'Tesla', 2024),
  (2, 'Model S', 'Tesla', 2023),
  (3, 'Model Y', 'Tesla', 2022),
  (4, 'Model X 75D', 'Tesla', 2017),
  (5, 'G-Class G63', 'Mercedes-Benz', 2024),
  (6, 'E-Class E200', 'Mercedes-Benz', 2023),
  (7, 'C-Class C300', 'Mercedes-Benz', 2016),
  (8, 'Everest', 'Ford', 2023),
  (9, 'Puma', 'Ford', 2021),
  (10, 'Focus', 'Ford', 2019);

SHOW TABLES;   -- lists tables AND views in the current database
```

### 9.1 Stored views

Persisted in the metastore like a table definition; accessible across sessions and clusters. Created with `CREATE VIEW … AS <query>`:

```sql
CREATE VIEW view_tesla_cars
AS SELECT * FROM cars WHERE brand = 'Tesla';

SHOW TABLES;                       -- isTemporary = false
SELECT * FROM view_tesla_cars;     -- re-runs the WHERE against cars each time
```

### 9.2 Temporary views

Bound to the **Spark session**; auto-dropped when the session ends. Add `TEMP` (or `TEMPORARY`):

```sql
CREATE TEMP VIEW temp_view_cars_brands
AS SELECT DISTINCT brand FROM cars;

SELECT * FROM temp_view_cars_brands;
SHOW TABLES;   -- isTemporary = true; database column is empty (not tied to any DB)
```

**A new Spark session starts when you:**

- open a new notebook,
- detach + reattach a notebook to a cluster,
- restart the Python interpreter (e.g. after a `pip install`),
- restart the cluster.

### 9.3 Global temporary views

Tied to the **cluster**, not a single session — any notebook on the same running cluster can read it. Stored in a special database named **`global_temp`**, which you must qualify on read. Add `GLOBAL TEMP`:

```sql
CREATE GLOBAL TEMP VIEW global_temp_view_recent_cars
AS SELECT * FROM cars WHERE year >= 2022 ORDER BY year DESC;

SELECT * FROM global_temp.global_temp_view_recent_cars;   -- must qualify with global_temp.

SHOW TABLES;                  -- does NOT list it (only shows the default DB)
SHOW TABLES IN global_temp;   -- lists the global temp view
```

> ⚠️ **2026 — global temp views are unsupported on serverless.** Serverless compute (the new default) runs on **Spark Connect**, which **does not support global temporary views**. Databricks now treats them as a **legacy** feature and recommends **session temp views** or **tables** for cross-session/notebook sharing. They still work on classic clusters where the book's demo runs.

### 9.4 Session lifetime demo — notebook `3.2B - Views (Session 2)`

Opening a second notebook = a **new Spark session** on the **same cluster**:

```sql
USE CATALOG hive_metastore;

SHOW TABLES;
-- cars (table)            ✅ persisted in metastore
-- view_tesla_cars (view)  ✅ stored view, persisted in metastore
-- temp_view_cars_brands   ❌ GONE — temp view died with session 1

SHOW TABLES IN global_temp;
SELECT * FROM global_temp.global_temp_view_recent_cars;   -- ✅ still alive (same cluster)
```

This proves the lifecycle differences: stored view survives across sessions; temp view does not; global temp view survives across sessions on the *same cluster*.

### 9.5 Comparison of view types

| | **Stored view** | **Temp view** | **Global temp view** |
|---|---|---|---|
| Syntax | `CREATE VIEW` | `CREATE TEMP VIEW` | `CREATE GLOBAL TEMP VIEW` |
| Persisted in metastore | ✅ | ❌ | ❌ |
| Accessibility | across sessions + clusters | current session only | across sessions, **same cluster** |
| Stored in DB | the target database | none | `global_temp` |
| Dropped when | `DROP VIEW` only | session ends | cluster restarts/terminates |

### 9.6 Dropping views

```sql
DROP VIEW view_tesla_cars;                              -- stored view
DROP VIEW temp_view_cars_brands;                        -- temp view (manual early drop)
DROP VIEW global_temp.global_temp_view_recent_cars;     -- global temp (qualify it)
DROP TABLE cars;                                        -- cleanup
```

Temp and global temp views drop automatically (session end / cluster restart) but can be dropped early with `DROP VIEW`.

---

## 10. Summary

| Command / concept | What it does |
|---|---|
| `CREATE SCHEMA` / `CREATE DATABASE` | Create a schema (interchangeable keywords) |
| `CREATE SCHEMA … LOCATION` | Custom-location schema |
| `CREATE TABLE t (…)` | **Managed** table (DROP deletes data) |
| `CREATE TABLE t (…) LOCATION '<p>'` | **External** table (DROP keeps data) |
| `CREATE TABLE … AS SELECT` (CTAS) | Create + populate; schema inferred |
| `ALTER TABLE … ADD CONSTRAINT … CHECK/NOT NULL` | Enforced constraints (UC adds informational PK/FK) |
| `DEEP CLONE` | Copy data + metadata (standalone, slow) |
| `SHALLOW CLONE` | Copy log only (fast, references source data) |
| `CREATE VIEW` | Stored view (persisted, cross-session) |
| `CREATE TEMP VIEW` | Session-scoped view |
| `CREATE GLOBAL TEMP VIEW` | Cluster-scoped view in `global_temp` (legacy; unsupported on serverless) |
| SHOW TABLES \[IN db\] | List tables + views (default DB unless `IN` given) |
| `DESCRIBE EXTENDED` / `DESCRIBE DATABASE EXTENDED` | Inspect type, location, provider |

---

## Sample Exam Questions (from book)

**Q1 — Conceptual:** Dropping a Delta table removes its catalog entry *and* deletes the underlying data files. Why?
→ **D.** The table was registered as a **managed table**; by default managed tables delete both metadata and data files when dropped.
*(Not deep/shallow clone, not external — external would keep the files; not a stored view.)*

**Q2 — Code:** Create an external Delta table at `dbfs:/ecommerce/customers`. Which statement is correct?
→ **3.** `CREATE TABLE customers (id INT, name STRING, email STRING) LOCATION 'dbfs:/ecommerce/customers';`
*(External tables are made with the `LOCATION` keyword — not `EXTERNAL`, `PATH =`, `AS EXTERNAL`, or `LOCATION AS OF`.)*

---

## References

- Managed vs external tables (UC): <https://docs.databricks.com/aws/en/tables/external>
- ADD CONSTRAINT (NOT NULL / CHECK / PK / FK): <https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-syntax-ddl-alter-table-add-constraint>
- CREATE TABLE CLONE: <https://docs.databricks.com/aws/en/sql/language-manual/delta-clone>
- Shallow clone for Unity Catalog tables: <https://docs.databricks.com/aws/en/delta/clone-unity-catalog>
- Views (stored / temp / global temp): <https://docs.databricks.com/aws/en/views/>
- Serverless compute limitations (global temp views unsupported): <https://docs.databricks.com/aws/en/compute/serverless/limitations>
