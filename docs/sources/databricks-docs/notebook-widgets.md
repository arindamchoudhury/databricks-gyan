# Databricks Widgets

> **Source:** [docs.databricks.com/aws/en/notebooks/widgets](https://docs.databricks.com/aws/en/notebooks/widgets)
> **Added:** 2026-06-17
> **Source updated:** 2026-06-17
> **Tags:** notebooks, widgets, parameters, sql, python, scala, R, dashboards, B1
> **Type:** documentation

## Summary

Widgets add interactive input parameters to notebooks and dashboards. Four types exist (text, dropdown, combobox, multiselect). They're created via UI or the `dbutils.widgets` API (Python/Scala/R) or `CREATE WIDGET` DDL (SQL). Values are always strings. SQL parameter markers (`:param`) — introduced in DBR 15.2 — protect against injection and are the recommended way to use widget values in SQL cells.

## Key points

- **Four types:** text, dropdown, combobox, multiselect.
- **Widgets only accept string values** — no integers, booleans, or other types.
- SQL API (`CREATE WIDGET`, `REMOVE WIDGET`, `:param`) is equivalent to `dbutils.widgets` but different syntax.
- SQL parameter markers require **DBR 15.2+**; DDL string clause markers (`LOCATION :path`) require **DBR 18.0+**.
- Three on-change behaviors: Run Notebook, Run Accessed Commands (default), Do Nothing. **"Run Accessed Commands" does not rerun SQL cells.**
- `%run` can pass widget values as `$X="10"` — but **not on SQL warehouses**.
- Dashboards show all widgets at top; an **Update** button triggers notebook re-run with new values.

## Notes

### Widget types

| Type | Behavior |
|---|---|
| text | Free-text input box |
| dropdown | Pick one value from a fixed list |
| combobox | Pick from list OR type a custom value |
| multiselect | Pick one or more values from a list |

### Creating widgets

**Python**

```python
dbutils.widgets.dropdown("state", "CA", ["CA", "IL", "MI", "NY", "OR", "VA"])
```

**Scala**

```scala
dbutils.widgets.dropdown("state", "CA", Seq("CA", "IL", "MI", "NY", "OR", "VA"))
```

**R**

```r
dbutils.widgets.dropdown("state", "CA", list("CA", "IL", "MI", "NY", "OR", "VA"))
```

**SQL**

```sql
CREATE WIDGET DROPDOWN state DEFAULT "CA" CHOICES SELECT * FROM
(VALUES ("CA"), ("IL"), ("MI"), ("NY"), ("OR"), ("VA"))
```

> "The widget API in SQL is slightly different but equivalent to the other languages."

**Via UI:** Edit > Add parameter. Configure: Parameter Name, Widget Label (display name), Type, Default value, Possible choices.

### Accessing widget values

**Python / Scala / R**

```python
dbutils.widgets.get("state")    # single widget
dbutils.widgets.getAll()        # dict of all widget values
```

**SQL (parameter markers)**

```sql
SELECT :state
```

> "Parameter markers protect your code from SQL injection attacks by clearly separating provided values from the SQL statements."

**SQL IDENTIFIER() — dynamic table/schema names**

```sql
SHOW TABLES IN IDENTIFIER(:database)

SELECT * FROM IDENTIFIER(:database || '.' || :table)
WHERE col == :filter_value
LIMIT 100
```

**SQL DDL string clauses (DBR 18.0+)**

```sql
CREATE EXTERNAL TABLE my_table USING DELTA LOCATION :path
```

For DBR 14.3–17.3 LTS: use `EXECUTE IMMEDIATE` to construct statements dynamically instead.

**Version requirements**

| Feature | Minimum DBR |
|---|---|
| SQL parameter markers (`:param` in queries) | 15.2 |
| `:param` in DDL string clauses (`LOCATION`, etc.) | 18.0 |

### Removing widgets

**Python / Scala / R**

```python
dbutils.widgets.remove("state")
dbutils.widgets.removeAll()
```

**SQL**

```sql
REMOVE WIDGET state
```

### On-change execution behavior

Configured per widget. Three options:

**Run Notebook** — reruns the entire notebook on every value change.

**Run Accessed Commands** *(default)* — reruns only cells that call `dbutils.widgets.get()` for that widget.

> ⚠️ "SQL cells are not rerun in this configuration."

**Do Nothing** — no automatic re-execution; user must manually rerun cells.

### Widgets in dashboards

> "When you create a dashboard from a notebook with input widgets, all the widgets display at the top. In presentation mode, every time you update the value of a widget, you can click the **Update** button to re-run the notebook and update your dashboard with new values."

See [[notebook-dashboards]] for the broader dashboard context.

### Passing widget values via %run

Default behavior when calling `%run` on a notebook that has widgets:

> "If you run a notebook that contains widgets, the specified notebook is run with the widget's default values."

Override values with named arguments (cluster-attached notebooks only):

```python
%run /path/to/notebook $X="10" $Y="1"
```

> ⚠️ **Not available for SQL warehouses.** Parameter passing via `%run` is a classic-compute-only feature.

## Quotes worth keeping

> "Widgets only accept string values."

> "SQL cells are not rerun in this [Run Accessed Commands] configuration."

> "Parameter markers protect your code from SQL injection attacks by clearly separating provided values from the SQL statements."

## Open questions

- ❓ Can `dbutils.widgets.getAll()` be called from SQL cells, or only Python/Scala/R?
- ❓ For multiselect widgets, does `dbutils.widgets.get()` return a comma-separated string or a list?
- ❓ Does "Run Accessed Commands" track `dbutils.widgets.getAll()` calls and rerun cells that use that?

## Related sources

- [[notebooks-overview]] — hub; widgets listed under "Popular pages"
- [[notebook-dashboards]] — dashboards display widgets at top; Update button re-runs notebook
- [[notebook-testing]] — pattern of passing parameters to notebooks complements `%run $X="10"` widget passing
- [[workspace-walkthrough]] — DA-FREE M1; introduces the notebook UI where widgets appear
