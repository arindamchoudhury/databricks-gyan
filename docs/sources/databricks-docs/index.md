# Databricks Docs — official documentation notes

> **Source:** [docs.databricks.com](https://docs.databricks.com) (AWS docs)
> **Type:** documentation

Notes captured from individual Databricks official documentation pages. One file per page, source-faithful, with version notes where the docs reference specific runtimes/UI that may drift.

## Pages captured

Grouped by topic. Nav mirrors these groups.

### Platform & Architecture

| Page | Added | Tags |
|---|---|---|
| [High-level architecture](high-level-architecture.md) | 2026-06-20 | architecture, control-plane, compute-plane, account, workspace, unity-catalog, serverless, classic, B1 |

### Compute

| Page | Added | Tags |
|---|---|---|
| [Serverless compute for notebooks](serverless-notebooks.md) | 2026-06-15 | serverless, notebooks, query-insights, B1 |
| [Serverless compute for Lakeflow Jobs](serverless-jobs.md) | 2026-06-15 | serverless, jobs, lakeflow, workflows, I6 |
| [Serverless compute for Lakeflow Pipelines](serverless-pipelines.md) | 2026-06-16 | serverless, pipelines, lakeflow, ldp, dlt, I5 |
| [Serverless compute limitations](serverless-limitations.md) | 2026-06-16 | serverless, limitations, streaming, caching, B1, I5, I6 |
| [Classic compute overview](classic-compute-overview.md) | 2026-06-16 | compute, classic-compute, access-modes, permissions, B1 |
| [Classic compute configuration reference](classic-compute-configure.md) | 2026-06-16 | compute, classic-compute, configuration, autoscaling, EBS, spark-config, B1 |
| [Standard compute overview](standard-compute-overview.md) | 2026-06-16 | compute, classic-compute, access-modes, standard, lakeguard, B1 |
| [Dedicated compute overview](dedicated-compute-overview.md) | 2026-06-16 | compute, classic-compute, access-modes, dedicated, RDD, GPU, R, B1 |
| [Compute pools (instance pools)](compute-pools.md) | 2026-06-16 | compute, pools, autoscaling, cost, B1 |
| [SQL warehouse overview](sql-warehouse-overview.md) | 2026-06-16 | compute, sql-warehouse, serverless, databricks-sql, BI, B1 |
| [SQL warehouse types](sql-warehouse-types.md) | 2026-06-16 | compute, sql-warehouse, serverless, photon, predictive-io, IWM, B1 |
| [Photon](photon.md) | 2026-06-16 | compute, photon, performance, vectorized, sql-warehouse, B1 |
| [Lakeguard](lakeguard.md) | 2026-06-16 | compute, lakeguard, security, isolation, standard-compute, spark-connect, B1 |

### Notebooks

| Page | Added | Tags |
|---|---|---|
| [Debug notebooks (interactive debugger)](notebook-debugger.md) | 2026-06-14 | notebooks, debugging, variable-explorer, B1 |
| [Notebooks Overview](notebooks-overview.md) | 2026-06-17 | notebooks, python, sql, scala, R, EDA, ML, collaboration, B1 |
| [Dashboards in Notebooks](notebook-dashboards.md) | 2026-06-17 | notebooks, dashboards, visualization, AI-BI, scheduling, sharing, B1 |
| [Unit Testing in Notebooks](notebook-testing.md) | 2026-06-17 | notebooks, testing, pytest, testthat, scalatest, sql, CI-CD, B1 |
| [Databricks Widgets](notebook-widgets.md) | 2026-06-17 | notebooks, widgets, parameters, sql, python, scala, R, dashboards, B1 |
| [Orchestrate Notebooks and Modularize Code](notebook-workflows.md) | 2026-06-17 | notebooks, orchestration, workflows, dbutils, run, modularization, B1, I6 |
| [ipywidgets in Notebooks](notebook-ipywidgets.md) | 2026-06-17 | notebooks, ipywidgets, python, interactive, visualization, B1 |
| [Share Code Between Notebooks (Workspace Files)](notebook-share-code.md) | 2026-06-17 | notebooks, workspace-files, modularization, python, git, B1 |
| [Notebook Best Practices (Software Engineering)](notebook-best-practices.md) | 2026-06-17 | notebooks, best-practices, git, testing, CI-CD, modularization, jobs, B1 |

### Performance & Spark UI

| Page | Added | Tags |
|---|---|---|
| [Spark UI Guide (diagnose cost and performance)](spark-ui-guide.md) | 2026-06-17 | spark, spark-ui, performance, optimization, debugging, skew, spill, stages, tasks, B2, B16 |
| [Optimize Databricks, Spark and Delta Lake Workloads (guide)](optimize-data-workloads-guide.md) | 2026-06-17 | spark, performance, optimization, delta-lake, shuffle, skew, spill, merge, vacuum, caching, photon, B2, B5, B12, B16, B17 |
| [Failing Jobs or Executors Removed](failing-spark-jobs.md) | 2026-06-17 | spark, spark-ui, debugging, executors, memory, spot-instances, autoscaling, B2, B16 |
| [Look at Longest Stage](long-spark-stage.md) | 2026-06-17 | spark, spark-ui, performance, debugging, stages, tasks, shuffle, B2, B16 |
| [Look for Skew or Spill](long-spark-stage-page.md) | 2026-06-17 | spark, spark-ui, performance, debugging, skew, spill, memory, shuffle, B2, B16 |
| [Spark Memory Issues](spark-memory-issues.md) | 2026-06-17 | spark, spark-ui, debugging, memory, OOM, executors, shuffle, broadcast, UDF, skew, streaming, B2, B16 |
| [Determine if Longest Stage is I/O Bound](long-spark-stage-io.md) | 2026-06-17 | spark, spark-ui, performance, debugging, I/O, shuffle, delta-cache, photon, liquid-clustering, B2, B16 |
| [Look for Other Causes of Slow Stage Runtime](slow-spark-stage-low-io.md) | 2026-06-17 | spark, spark-ui, performance, debugging, small-files, UDF, cartesian-join, explode, DAG, B2, B16 |
| [How to Determine if Spark is Rewriting Data](spark-rewriting-data.md) | 2026-06-17 | spark, spark-ui, debugging, delta, merge, delete, update, rewriting, B2, B12, B16 |
| [One Spark Task](one-spark-task.md) | 2026-06-17 | spark, spark-ui, debugging, tasks, parallelism, UDF, gzip, coalesce, repartition, B2, B16 |
| [Losing Spot Instances](losing-spot-instances.md) | 2026-06-17 | spark, spark-ui, debugging, spot-instances, AWS, executors, B2, B16 |
| [SQL Hints: Join, Partition, and Skew](sql-join-hints.md) | 2026-06-18 | spark, sql, join-hints, broadcast, shuffle, partitioning, performance, optimization, B2, B8 |
| [Adaptive Query Execution (AQE)](aqe.md) | 2026-06-18 | spark, aqe, performance, optimization, broadcast, skew, shuffle, partitioning, B2, B8, B16 |

### Optimization & Performance (platform knobs)

| Page | Added | Tags |
|---|---|---|
| [Optimization recommendations (hub)](optimization-recommendations.md) | 2026-06-24 | optimization, performance, databricks-runtime, hub, A1 |
| [Disk caching (Delta/DBIO cache)](disk-cache.md) | 2026-06-24 | optimization, disk-cache, delta-cache, ssd, caching, spark-cache, A1 |
| [Dynamic file pruning](dynamic-file-pruning.md) | 2026-06-24 | optimization, dynamic-file-pruning, dfp, join, photon, data-skipping, A1 |
| [Low shuffle merge](low-shuffle-merge.md) | 2026-06-24 | optimization, merge, low-shuffle-merge, shuffle, delta, A1, I5 |
| [Cost-based optimizer (CBO)](cost-based-optimizer.md) | 2026-06-24 | optimization, cbo, statistics, analyze-table, joins, explain, A1 |
| [Range join optimization](range-join.md) | 2026-06-24 | optimization, range-join, join, bin-size, timestamp, interval, A1 |
| [Isolation levels and write conflicts](isolation-levels.md) | 2026-06-24 | optimization, delta, isolation, write-serializable, concurrency, A1, B4 |

### Tables & SQL

| Page | Added | Tags |
|---|---|---|
| [Databricks tables concepts](tables-concepts.md) | 2026-06-22 | tables, unity-catalog, managed, external, foreign, temporary, delta, iceberg, permissions, B4 |
| [Unity Catalog managed tables](managed-tables.md) | 2026-06-23 | tables, unity-catalog, managed, delta, iceberg, predictive-optimization, catalog-commits, undrop, recovery-period, B4 |
| [Convert an external Delta table to managed](convert-external-managed.md) | 2026-06-23 | tables, unity-catalog, managed, external, set-managed, migration, uniform, path-based-redirect, streaming, B4 |
| [Specify a managed storage location in Unity Catalog](managed-storage.md) | 2026-06-23 | unity-catalog, managed-storage, storage-location, external-location, catalog, schema, metastore, volumes, B1, B4 |
| [Catalog commits](catalog-commits.md) | 2026-06-24 | tables, unity-catalog, managed, delta, iceberg, catalog-commits, transactions, external-access, streaming, B4 |
| [Transactions](transactions.md) | 2026-06-24 | tables, unity-catalog, transactions, acid, catalog-commits, isolation, concurrency, atomic, rollback, B4 |
| [Predictive optimization](predictive-optimization.md) | 2026-06-24 | tables, unity-catalog, managed, delta, iceberg, predictive-optimization, optimize, vacuum, analyze, liquid-clustering, serverless, system-tables, B4, B5 |
| [Use liquid clustering for tables](liquid-clustering.md) | 2026-06-24 | tables, delta, iceberg, liquid-clustering, cluster-by, optimize, zorder, partitioning, predictive-optimization, automatic-clustering, data-skipping, A2, I5 |
| [Access Databricks data using external systems](external-access.md) | 2026-06-24 | unity-catalog, external-access, iceberg-rest-catalog, unity-rest-api, credential-vending, compatibility-mode, opensharing, external-tables, external-volumes, A7, I8, B4 |

To add another: *"take notes on &lt;docs.databricks.com URL&gt;."*
