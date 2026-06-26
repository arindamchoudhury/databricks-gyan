# Serverless compute for notebooks

> **Source:** [docs.databricks.com/aws/en/compute/serverless/notebooks](https://docs.databricks.com/aws/en/compute/serverless/notebooks)
> **Added:** 2026-06-15
> **Source updated:** 2026-05-26
> **Tags:** serverless, notebooks, compute, query-insights, B1
> **Type:** documentation

Serverless compute for notebooks lets you run notebook code on Databricks-managed infrastructure with no cluster setup — attach, run, done. The one prerequisite is **Unity Catalog** enabled on the workspace (plus serverless interactive compute activated in the account); no special user permission is needed beyond workspace access. New notebooks **default to serverless** when code runs without a pre-selected compute resource.

## Attaching a notebook to serverless compute

Open the **compute dropdown** in the notebook toolbar → select the serverless option. On new notebooks, Databricks automatically selects serverless when code is executed with no resource pre-selected.

## Query insights

After running notebook cells, click **"See performance"** to review how efficiently Spark executed your SQL and Python queries.

[!["See performance" link after notebook cell execution](assets/serverless-notebooks/01-query-performance.png)](assets/serverless-notebooks/01-query-performance.png)
*The "See performance" link appears after a cell run; click "See query profile" for the full execution visualization.*

Individual Spark statements can be examined for metrics, **"See query profile"** opens the execution-plan visualization, and all serverless queries are logged in the workspace **Query History** page.

**Limitations:** profiles only appear **after** execution completes (live metrics update during, profile is post-run); statuses covered are RUNNING/CANCELED/FAILED/FINISHED; running queries **can't be canceled from query history** (cancel from the notebook/job); no verbose metrics; no query-profile downloads; **no Spark UI**; statement text shows only the **final executed line**.

> ⚠️ The absence of Spark UI is the sharpest difference from classic-cluster notebooks — query insights are the replacement tool for performance debugging on serverless.

## Serverless overspend protection

> "Serverless notebooks have a default execution timeout of 2.5 hours (9,000 seconds)."

Queries exceeding the timeout are canceled automatically to prevent runaway spend from long-idle or hung sessions.

- **Workspace admin override:** Settings → **Compute** → **Serverless interactive** → change the default (propagates in ~5 min).
- **Per-notebook override** (takes precedence): `spark.conf.set("spark.databricks.execution.timeout", <seconds>)`.

> 💡 Set a tighter per-notebook timeout on long-running ETL notebooks to catch hangs early rather than waiting 2.5 hours.

Related: [[notebook-debugger]], [[serverless-limitations]], [[ch01-getting-started-with-databricks]].
