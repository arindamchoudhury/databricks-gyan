# Sources

Course notebooks and external sources captured as structured notes.

## DA-FREE — *Get Started with Data Engineering* (Databricks Academy)

| Title | Type | Added | Tags |
|---|---|---|---|
| [M1: Databricks Workspace Walkthrough](da-free/workspace-walkthrough.md) | notebook | 2026-06-11 | workspace, UI, compute, unity-catalog, B1 |
| [M2-01: Creating and Working with a Delta Table](da-free/creating-delta-table.md) | notebook | 2026-06-11 | delta, CTAS, DML, time-travel, B5 |
| [M2-02: Ingesting Data into Delta Lake](da-free/ingesting-data.md) | notebook | 2026-06-11 | ingestion, COPY-INTO, auto-loader, B6 |
| [M2-03: Transforming Data Using the Medallion Architecture](da-free/medallion-architecture.md) | notebook | 2026-06-11 | medallion, bronze, silver, gold, B7 |
| [M2-04: Creating a Simple Databricks Job](da-free/lakeflow-jobs.md) | notebook | 2026-06-11 | jobs, lakeflow, orchestration, I6 |

## DCDE-SG — *Databricks Certified Data Engineer Associate Study Guide* (Alhussein, O'Reilly 2025)

| Title | Type | Added | Tags |
|---|---|---|---|
| [Book Overview & reading log](dcde-sg/index.md) | book | 2026-06-14 | dcdea, exam-prep |
| [Ch 1: Getting Started with Databricks](dcde-sg/ch01-getting-started-with-databricks.md) | book | 2026-06-14 | platform, architecture, clusters, notebooks, B1 |
| [Ch 2: Managing Data with Delta Lake](dcde-sg/ch02-managing-data-with-delta-lake.md) | book | 2026-06-19 | delta, transaction-log, acid, time-travel, optimize, vacuum, B5 |

## Databricks Docs — official documentation (docs.databricks.com)

| Title | Type | Added | Tags |
|---|---|---|---|
| [Debug Notebooks (Interactive Debugger)](databricks-docs/notebook-debugger.md) | documentation | 2026-06-14 | notebooks, debugging, variable-explorer, B1 |
| [Serverless Compute for Notebooks](databricks-docs/serverless-notebooks.md) | documentation | 2026-06-15 | serverless, notebooks, query-insights, B1 |
| [Serverless Compute for Lakeflow Jobs](databricks-docs/serverless-jobs.md) | documentation | 2026-06-15 | serverless, jobs, lakeflow, workflows, I6 |
| [Serverless Compute for Lakeflow Pipelines](databricks-docs/serverless-pipelines.md) | documentation | 2026-06-16 | serverless, pipelines, lakeflow, ldp, I5 |
| [Serverless compute limitations](databricks-docs/serverless-limitations.md) | documentation | 2026-06-16 | serverless, limitations, streaming, caching, B1, I5, I6 |
| [Classic compute overview](databricks-docs/classic-compute-overview.md) | documentation | 2026-06-16 | compute, classic-compute, access-modes, permissions, B1 |
| [Classic compute configuration reference](databricks-docs/classic-compute-configure.md) | documentation | 2026-06-16 | compute, classic-compute, configuration, autoscaling, EBS, spark-config, B1 |
| [Standard compute overview](databricks-docs/standard-compute-overview.md) | documentation | 2026-06-16 | compute, classic-compute, access-modes, standard, lakeguard, B1 |
| [Dedicated compute overview](databricks-docs/dedicated-compute-overview.md) | documentation | 2026-06-16 | compute, classic-compute, access-modes, dedicated, RDD, GPU, R, B1 |
| [Compute pools (instance pools)](databricks-docs/compute-pools.md) | documentation | 2026-06-16 | compute, pools, autoscaling, cost, B1 |
| [SQL warehouse overview](databricks-docs/sql-warehouse-overview.md) | documentation | 2026-06-16 | compute, sql-warehouse, serverless, databricks-sql, BI, B1 |
| [SQL warehouse types](databricks-docs/sql-warehouse-types.md) | documentation | 2026-06-16 | compute, sql-warehouse, serverless, photon, predictive-io, IWM, B1 |
| [Photon](databricks-docs/photon.md) | documentation | 2026-06-16 | compute, photon, performance, vectorized, sql-warehouse, B1 |
| [Lakeguard](databricks-docs/lakeguard.md) | documentation | 2026-06-16 | compute, lakeguard, security, isolation, standard-compute, spark-connect, B1 |
| [Notebooks Overview](databricks-docs/notebooks-overview.md) | documentation | 2026-06-17 | notebooks, python, sql, scala, R, EDA, ML, collaboration, B1 |
| [Dashboards in Notebooks](databricks-docs/notebook-dashboards.md) | documentation | 2026-06-17 | notebooks, dashboards, visualization, AI-BI, scheduling, sharing, B1 |
| [Unit Testing in Notebooks](databricks-docs/notebook-testing.md) | documentation | 2026-06-17 | notebooks, testing, pytest, testthat, scalatest, sql, CI-CD, B1 |
| [Databricks Widgets](databricks-docs/notebook-widgets.md) | documentation | 2026-06-17 | notebooks, widgets, parameters, sql, python, scala, R, dashboards, B1 |
| [Orchestrate Notebooks and Modularize Code](databricks-docs/notebook-workflows.md) | documentation | 2026-06-17 | notebooks, orchestration, workflows, dbutils, run, modularization, B1, I6 |
| [ipywidgets in Notebooks](databricks-docs/notebook-ipywidgets.md) | documentation | 2026-06-17 | notebooks, ipywidgets, python, interactive, visualization, B1 |
| [Share Code Between Notebooks (Workspace Files)](databricks-docs/notebook-share-code.md) | documentation | 2026-06-17 | notebooks, workspace-files, modularization, python, git, B1 |
| [Notebook Best Practices (Software Engineering)](databricks-docs/notebook-best-practices.md) | documentation | 2026-06-17 | notebooks, best-practices, git, testing, CI-CD, modularization, jobs, B1 |
| [Spark UI Guide (diagnose cost and performance)](databricks-docs/spark-ui-guide.md) | documentation | 2026-06-17 | spark, spark-ui, performance, optimization, debugging, skew, spill, stages, tasks, B2, B16 |
| [Optimize Databricks, Spark and Delta Lake Workloads](databricks-docs/optimize-data-workloads-guide.md) | documentation | 2026-06-17 | spark, performance, optimization, delta-lake, shuffle, skew, spill, merge, vacuum, caching, photon, B2, B5, B12, B16, B17 |
| [Failing Jobs or Executors Removed](databricks-docs/failing-spark-jobs.md) | documentation | 2026-06-17 | spark, spark-ui, debugging, executors, memory, spot-instances, autoscaling, B2, B16 |
| [Look at Longest Stage](databricks-docs/long-spark-stage.md) | documentation | 2026-06-17 | spark, spark-ui, performance, debugging, stages, tasks, shuffle, B2, B16 |
| [Look for Skew or Spill](databricks-docs/long-spark-stage-page.md) | documentation | 2026-06-17 | spark, spark-ui, performance, debugging, skew, spill, memory, shuffle, B2, B16 |
| [Spark Memory Issues](databricks-docs/spark-memory-issues.md) | documentation | 2026-06-17 | spark, spark-ui, debugging, memory, OOM, executors, shuffle, broadcast, UDF, skew, streaming, B2, B16 |
| [Determine if Longest Stage is I/O Bound](databricks-docs/long-spark-stage-io.md) | documentation | 2026-06-17 | spark, spark-ui, performance, debugging, I/O, shuffle, delta-cache, photon, liquid-clustering, B2, B16 |
| [Look for Other Causes of Slow Stage Runtime](databricks-docs/slow-spark-stage-low-io.md) | documentation | 2026-06-17 | spark, spark-ui, performance, debugging, small-files, UDF, cartesian-join, explode, DAG, B2, B16 |
| [How to Determine if Spark is Rewriting Data](databricks-docs/spark-rewriting-data.md) | documentation | 2026-06-17 | spark, spark-ui, debugging, delta, merge, delete, update, rewriting, B2, B12, B16 |
| [One Spark Task](databricks-docs/one-spark-task.md) | documentation | 2026-06-17 | spark, spark-ui, debugging, tasks, parallelism, UDF, gzip, coalesce, repartition, B2, B16 |
| [Losing Spot Instances](databricks-docs/losing-spot-instances.md) | documentation | 2026-06-17 | spark, spark-ui, debugging, spot-instances, AWS, executors, B2, B16 |
| [SQL Hints: Join, Partition, and Skew](databricks-docs/sql-join-hints.md) | documentation | 2026-06-18 | spark, sql, join-hints, broadcast, shuffle, partitioning, performance, optimization, B2, B8 |
| [Adaptive Query Execution (AQE)](databricks-docs/aqe.md) | documentation | 2026-06-18 | spark, aqe, performance, optimization, broadcast, skew, shuffle, partitioning, B2, B8, B16 |
