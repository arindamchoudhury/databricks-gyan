# Serverless compute for Lakeflow Jobs (workflows)

> **Source:** [docs.databricks.com/aws/en/jobs/run-serverless-jobs](https://docs.databricks.com/aws/en/jobs/run-serverless-jobs)
> **Added:** 2026-06-15
> **Source updated:** 2026-06-15
> **Tags:** serverless, jobs, lakeflow, workflows, compute, performance-modes, I6
> **Type:** documentation

Serverless compute lets Lakeflow Jobs run without any cluster provisioning — Databricks manages infrastructure, autoscaling, and Photon automatically ("focus on implementing your data processing and analysis pipelines"). **Unity Catalog** must be enabled and workloads must support **Standard access mode** (dedicated/single-user workloads still need classic clusters). Serverless is the **default compute** for supported task types: **notebook, Python script, dbt, Python wheel, JAR** (JAR = Public Preview).

## Creating / converting jobs

When you create a job using a supported task type, serverless compute is selected automatically.

[![Serverless pre-selected in job creation](assets/serverless-jobs/01-create-serverless-job.png)](assets/serverless-jobs/01-create-serverless-job.png)

To convert an existing job: **Job details** → under **Compute** click **Swap** → select serverless (or use the Compute dropdown in the task editor).

[![Swapping an existing task to serverless](assets/serverless-jobs/02-swap-to-serverless.png)](assets/serverless-jobs/02-swap-to-serverless.png)

Serverless jobs can also be scheduled directly from a notebook (see "Create and manage scheduled notebook jobs"), and dependencies are configured via serverless environment configuration.

## Performance modes

Both modes use the **same SKU** — the difference is startup behaviour and DBU consumption:

| Mode | Startup | DBU use | Best for |
|---|---|---|---|
| **Standard** | 4–6 min | Lower | Cost-sensitive, latency-tolerant jobs |
| **Performance Optimized** | Fast | Higher | Time-sensitive, SLA-bound workloads |

The setting affects only **serverless tasks** within the job.

> ⚠️ **Standard performance mode is not supported for one-time runs created via the `runs/submit` endpoint** — use Performance Optimized or the Jobs UI / DABs for those.

## Additional configuration

**High memory** *(Public Preview)* for notebook tasks via the **Environment** side panel. Only **specific Spark config parameters** can be set at session level inside a serverless job's notebook — not all `spark.conf.set(...)` calls are honoured.

## Auto-optimization

On by default — Databricks optimises compute per run and retries failed tasks. To disable (e.g. for non-idempotent workloads): **Retry Policy** dialog → uncheck **"Enable serverless auto-optimization"**.

## Monitoring and query details

The Jobs UI **timeline view** shows individual tasks with their query statements and runtimes.

[![Timeline view with tasks, query statements, runtimes](assets/serverless-jobs/03-timeline-view.png)](assets/serverless-jobs/03-timeline-view.png)

Click a statement → **query profile** (execution metrics + plan); task run details also link to **query history** filtered by task run ID. Monitor costs via the **billable usage system table** (includes user/workload attributes), and apply usage-policy tags for billing attribution *(Public Preview)*.

> 💡 For serverless jobs, the timeline + query profile replaces the Spark UI you'd get on classic clusters — same "what ran and how" question, different path (mirrors [[serverless-notebooks]]).

## Programmatic creation

Via the **Jobs REST API**, **Declarative Automation Bundles (DABs)** (the recommended IaC path), or the **Databricks SDK for Python**.

Related: [[serverless-pipelines]], [[serverless-notebooks]], [[serverless-limitations]], [[data-engineering-hub]], [[notebook-debugger]].
