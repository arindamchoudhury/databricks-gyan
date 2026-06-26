# Orchestrate Notebooks and Modularize Code

> **Source:** [docs.databricks.com/aws/en/notebooks/notebook-workflows](https://docs.databricks.com/aws/en/notebooks/notebook-workflows)
> **Added:** 2026-06-17
> **Source updated:** 2025-01-06
> **Tags:** notebooks, orchestration, workflows, dbutils, run, modularization, B1, I6
> **Type:** documentation

## Summary

Four patterns for orchestrating notebooks and modularizing code: Lakeflow Jobs (complex scheduling), `dbutils.notebook.run()` (dynamic/metadata-driven ETL), Workspace Files (code reuse), and `%run` (inline import fallback). Key distinction: `%run` runs inline and exposes all variables; `dbutils.notebook.run()` starts a separate job with string-only params and return values.

## Key points

- **Lakeflow Jobs** = recommended for orchestration with scheduling, triggers, task dependencies.
- **`dbutils.notebook.run()`** = escape hatch for dynamic/metadata-driven cases Jobs can't handle. Python and Scala only.
- **Workspace Files** = recommended for code modularization (not `%run`).
- **`%run`** = fallback when workspace files aren't accessible; merges callee scope into caller.
- `%run` must be **alone in its cell**; runs entire notebook inline.
- `dbutils.notebook.run()` arguments and return values are **strings only**; arguments must be **ASCII only**.
- `dbutils.notebook.run()` timeout of `0` = no timeout; Databricks outage >10 min fails the run regardless.
- Jobs from `dbutils.notebook` API must finish in **≤30 days**.
- Parallelism via Python/Scala `Threads` and `Futures`.

## Notes

### Four methods compared

| Method | Use case | Recommended for |
|---|---|---|
| Lakeflow Jobs | Scheduling, dependencies, triggers | Orchestration (primary choice) |
| `dbutils.notebook.run()` | Dynamic/metadata-driven ETL, programmatic control | When Jobs can't handle the use case |
| Workspace Files | Reusable functions, classes, modules | Code modularization (primary choice) |
| `%run` | Inline notebook import, when workspace files unavailable | Modularization fallback only |

### %run — inline execution

> "`%run` must be in a cell by itself, because it runs the entire notebook inline."

All functions and variables from the called notebook become available in the calling notebook's scope — no import needed.

**Path syntax**

```python
%run ./shared-code-notebook
%run ./dir/notebook
%run /Users/username@organization.com/directory/notebook
```

**Limitations**

- Cannot use `%run` to run a Python file and `import` its entities into a notebook (notebook paths only).
- Widget behavior: runs with default values unless values are explicitly passed.

### dbutils.notebook.run() — separate job

Starts a **new job** (not inline). Return value from callee via `dbutils.notebook.exit()`.

**Python**

```python
dbutils.notebook.run("notebook-name", 60, {"argument": "data", "argument2": "data2"})
```

**Scala**

```scala
dbutils.notebook.run("notebook-name", 60, Map("argument" -> "data", "argument2" -> "data2"))
```

> ⚠️ "Like all of the dbutils APIs, these methods are available only in Python and Scala." (Not R, not SQL.)

**Constraints**

- `arguments` accepts **only Latin/ASCII characters** — non-ASCII raises an error.
- Both arguments and return values must be **strings**.
- `timeout_seconds=0` = no timeout. If Databricks is down >10 minutes, the run fails regardless of timeout.
- Jobs created via this API must complete in **30 days or less**.

### Returning data from called notebooks

Use `dbutils.notebook.exit(value)` in the callee; value must be a string.

**Three strategies for structured data:**

**Strategy 1 — Global temp view** (return a view name; caller reads the view)

```python
# Callee
spark.range(5).toDF("value").createOrReplaceGlobalTempView("my_data")
dbutils.notebook.exit("my_data")

# Caller
returned_table = dbutils.notebook.run("LOCATION_OF_CALLEE_NOTEBOOK", 60)
global_temp_db = spark.conf.get("spark.sql.globalTempDatabase")
display(table(global_temp_db + "." + returned_table))
```

**Strategy 2 — DBFS** (write parquet; return the path)

```python
# Callee
dbutils.fs.rm("/tmp/results/my_data", recurse=True)
spark.range(5).toDF("value").write.format("parquet").save("dbfs:/tmp/results/my_data")
dbutils.notebook.exit("dbfs:/tmp/results/my_data")

# Caller
returned_table = dbutils.notebook.run("LOCATION_OF_CALLEE_NOTEBOOK", 60)
display(spark.read.format("parquet").load(returned_table))
```

**Strategy 3 — JSON string** (multiple values in one return)

```python
# Callee
import json
dbutils.notebook.exit(json.dumps({"status": "OK", "table": "my_data"}))

# Caller
import json
result = dbutils.notebook.run("LOCATION_OF_CALLEE_NOTEBOOK", 60)
print(json.loads(result))
```

### Error handling and retries

`dbutils.notebook.run()` raises an exception on failure — wrap in try/except:

```python
def run_with_retry(notebook, timeout, args={}, max_retries=3):
    num_retries = 0
    while True:
        try:
            return dbutils.notebook.run(notebook, timeout, args)
        except Exception as e:
            if num_retries > max_retries:
                raise e
            else:
                print("Retrying error", e)
                num_retries += 1

run_with_retry("LOCATION_OF_CALLEE_NOTEBOOK", 60, max_retries=5)
```

### Parallel execution

> "You can run multiple notebooks at the same time by using standard Scala and Python constructs such as Threads and Futures."

Full examples are in downloadable sample notebooks (not shown inline on the docs page). The pattern: dispatch multiple `dbutils.notebook.run()` calls via thread pool or `concurrent.futures`, then collect results.

## Quotes worth keeping

> "`%run` must be in a cell by itself, because it runs the entire notebook inline."

> "You cannot use `%run` to run a Python file and import the entities defined in that file into a notebook."

> "The arguments parameter accepts only Latin characters (ASCII character set). Using non-ASCII characters returns an error."

> "If Databricks is down for more than 10 minutes, the notebook run fails regardless of timeout_seconds."

> "Jobs created using the dbutils.notebook API must complete in 30 days or less."

## Open questions

- ❓ Does the 30-day job limit apply to the wall-clock run time of the called notebook, or to total pipeline time including retries?
- ❓ Can `dbutils.notebook.run()` target notebooks in other workspaces, or only the current workspace?
- ❓ When using global temp views to pass data between notebooks, are both notebooks required to be on the same cluster (shared SparkSession)?

## Related sources

- [[notebooks-overview]] — hub; "Orchestrate notebooks and modularize code" listed under Popular pages
- [[notebook-widgets]] — `%run /path $X="10"` passes widget values; constrained to classic compute only
- [[notebook-testing]] — workspace files (the recommended modularization pattern) are also where test files live
- [[lakeflow-jobs]] — DA-FREE M2-04; the recommended primary orchestration mechanism this page defers to


## Images

[![Shared code notebook](assets/notebook-workflows/01.png)](assets/notebook-workflows/01.png)
*Shared code notebook (941×264)*

[![Notebook import example](assets/notebook-workflows/02.png)](assets/notebook-workflows/02.png)
*Notebook import example (959×374)*

