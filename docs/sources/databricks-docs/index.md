# Databricks Docs — official documentation notes

> **Source:** [docs.databricks.com](https://docs.databricks.com) (AWS docs)
> **Type:** documentation

Notes captured from individual Databricks official documentation pages. One file per page, source-faithful, with version notes where the docs reference specific runtimes/UI that may drift.

## Pages captured

Grouped by topic. Nav mirrors these groups.

### Platform & Architecture

| Page | Added | Tags |
|---|---|---|
| [High-level architecture](high-level-architecture/) | 2026-06-20 | architecture, control-plane, compute-plane, account, workspace, unity-catalog, serverless, classic, B1 |

### Administration

| Page | Added | Tags |
|---|---|---|
| [Disable access to legacy features in new workspaces](legacy-features/) | 2026-07-02 | administration, unity-catalog, dbfs, hive-metastore, no-isolation-clusters, legacy, account-settings, B1 |

### Compute

| Page | Added | Tags |
|---|---|---|
| [Serverless compute for notebooks](serverless-notebooks/) | 2026-06-15 | serverless, notebooks, query-insights, B1 |
| [Serverless compute for Lakeflow Jobs](serverless-jobs/) | 2026-06-15 | serverless, jobs, lakeflow, workflows, I6 |
| [Serverless compute for Lakeflow Pipelines](serverless-pipelines/) | 2026-06-16 | serverless, pipelines, lakeflow, ldp, dlt, I5 |
| [Serverless compute limitations](serverless-limitations/) | 2026-06-16 | serverless, limitations, streaming, caching, B1, I5, I6 |
| [Classic compute overview](classic-compute-overview/) | 2026-06-16 | compute, classic-compute, access-modes, permissions, B1 |
| [Classic compute configuration reference](classic-compute-configure/) | 2026-06-16 | compute, classic-compute, configuration, autoscaling, EBS, spark-config, B1 |
| [Standard compute overview](standard-compute-overview/) | 2026-06-16 | compute, classic-compute, access-modes, standard, lakeguard, B1 |
| [Dedicated compute overview](dedicated-compute-overview/) | 2026-06-16 | compute, classic-compute, access-modes, dedicated, RDD, GPU, R, B1 |
| [Compute pools (instance pools)](compute-pools/) | 2026-06-16 | compute, pools, autoscaling, cost, B1 |
| [SQL warehouse overview](sql-warehouse-overview/) | 2026-06-16 | compute, sql-warehouse, serverless, databricks-sql, BI, B1 |
| [SQL warehouse types](sql-warehouse-types/) | 2026-06-16 | compute, sql-warehouse, serverless, photon, predictive-io, IWM, B1 |
| [Photon](photon/) | 2026-06-16 | compute, photon, performance, vectorized, sql-warehouse, B1 |
| [Lakeguard](lakeguard/) | 2026-06-16 | compute, lakeguard, security, isolation, standard-compute, spark-connect, B1 |

### Notebooks

| Page | Added | Tags |
|---|---|---|
| [Debug notebooks (interactive debugger)](notebook-debugger/) | 2026-06-14 | notebooks, debugging, variable-explorer, B1 |
| [Notebooks Overview](notebooks-overview/) | 2026-06-17 | notebooks, python, sql, scala, R, EDA, ML, collaboration, B1 |
| [Dashboards in Notebooks](notebook-dashboards/) | 2026-06-17 | notebooks, dashboards, visualization, AI-BI, scheduling, sharing, B1 |
| [Unit Testing in Notebooks](notebook-testing/) | 2026-06-17 | notebooks, testing, pytest, testthat, scalatest, sql, CI-CD, B1 |
| [Databricks Widgets](notebook-widgets/) | 2026-06-17 | notebooks, widgets, parameters, sql, python, scala, R, dashboards, B1 |
| [Orchestrate Notebooks and Modularize Code](notebook-workflows/) | 2026-06-17 | notebooks, orchestration, workflows, dbutils, run, modularization, B1, I6 |
| [ipywidgets in Notebooks](notebook-ipywidgets/) | 2026-06-17 | notebooks, ipywidgets, python, interactive, visualization, B1 |
| [Share Code Between Notebooks (Workspace Files)](notebook-share-code/) | 2026-06-17 | notebooks, workspace-files, modularization, python, git, B1 |
| [Notebook Best Practices (Software Engineering)](notebook-best-practices/) | 2026-06-17 | notebooks, best-practices, git, testing, CI-CD, modularization, jobs, B1 |

### Performance & Spark UI

| Page | Added | Tags |
|---|---|---|
| [Spark UI Guide (diagnose cost and performance)](spark-ui-guide/) | 2026-06-17 | spark, spark-ui, performance, optimization, debugging, skew, spill, stages, tasks, B2, B16 |
| [Optimize Databricks, Spark and Delta Lake Workloads (guide)](optimize-data-workloads-guide/) | 2026-06-17 | spark, performance, optimization, delta-lake, shuffle, skew, spill, merge, vacuum, caching, photon, B2, B5, B12, B16, B17 |
| [Failing Jobs or Executors Removed](failing-spark-jobs/) | 2026-06-17 | spark, spark-ui, debugging, executors, memory, spot-instances, autoscaling, B2, B16 |
| [Look at Longest Stage](long-spark-stage/) | 2026-06-17 | spark, spark-ui, performance, debugging, stages, tasks, shuffle, B2, B16 |
| [Look for Skew or Spill](long-spark-stage-page/) | 2026-06-17 | spark, spark-ui, performance, debugging, skew, spill, memory, shuffle, B2, B16 |
| [Spark Memory Issues](spark-memory-issues/) | 2026-06-17 | spark, spark-ui, debugging, memory, OOM, executors, shuffle, broadcast, UDF, skew, streaming, B2, B16 |
| [Determine if Longest Stage is I/O Bound](long-spark-stage-io/) | 2026-06-17 | spark, spark-ui, performance, debugging, I/O, shuffle, delta-cache, photon, liquid-clustering, B2, B16 |
| [Look for Other Causes of Slow Stage Runtime](slow-spark-stage-low-io/) | 2026-06-17 | spark, spark-ui, performance, debugging, small-files, UDF, cartesian-join, explode, DAG, B2, B16 |
| [How to Determine if Spark is Rewriting Data](spark-rewriting-data/) | 2026-06-17 | spark, spark-ui, debugging, delta, merge, delete, update, rewriting, B2, B12, B16 |
| [One Spark Task](one-spark-task/) | 2026-06-17 | spark, spark-ui, debugging, tasks, parallelism, UDF, gzip, coalesce, repartition, B2, B16 |
| [Losing Spot Instances](losing-spot-instances/) | 2026-06-17 | spark, spark-ui, debugging, spot-instances, AWS, executors, B2, B16 |
| [SQL Hints: Join, Partition, and Skew](sql-join-hints/) | 2026-06-18 | spark, sql, join-hints, broadcast, shuffle, partitioning, performance, optimization, B2, B8 |
| [Adaptive Query Execution (AQE)](aqe/) | 2026-06-18 | spark, aqe, performance, optimization, broadcast, skew, shuffle, partitioning, B2, B8, B16 |

### Optimization & Performance (platform knobs)

| Page | Added | Tags |
|---|---|---|
| [Optimization recommendations (hub)](optimization-recommendations/) | 2026-06-24 | optimization, performance, databricks-runtime, hub, A1 |
| [Disk caching (Delta/DBIO cache)](disk-cache/) | 2026-06-24 | optimization, disk-cache, delta-cache, ssd, caching, spark-cache, A1 |
| [Dynamic file pruning](dynamic-file-pruning/) | 2026-06-24 | optimization, dynamic-file-pruning, dfp, join, photon, data-skipping, A1 |
| [Low shuffle merge](low-shuffle-merge/) | 2026-06-24 | optimization, merge, low-shuffle-merge, shuffle, delta, A1, I5 |
| [Cost-based optimizer (CBO)](cost-based-optimizer/) | 2026-06-24 | optimization, cbo, statistics, analyze-table, joins, explain, A1 |
| [Range join optimization](range-join/) | 2026-06-24 | optimization, range-join, join, bin-size, timestamp, interval, A1 |
| [Isolation levels and write conflicts](isolation-levels/) | 2026-06-24 | optimization, delta, isolation, write-serializable, concurrency, A1, B4 |

### Tables & SQL

| Page | Added | Tags |
|---|---|---|
| [Databricks tables concepts](tables-concepts/) | 2026-06-22 | tables, unity-catalog, managed, external, foreign, temporary, delta, iceberg, permissions, B4 |
| [Unity Catalog managed tables](managed-tables/) | 2026-06-23 | tables, unity-catalog, managed, delta, iceberg, predictive-optimization, catalog-commits, undrop, recovery-period, B4 |
| [Unity Catalog external tables](external-tables/) | 2026-06-24 | tables, unity-catalog, external, delta, external-location, storage-credential, drop-table, repair-table, B4 |
| [Partition discovery for external tables](external-partition-discovery/) | 2026-06-24 | tables, unity-catalog, external, partitioning, partition-metadata, msck-repair, hive-style, B4 |
| [Convert an external Delta table to managed](convert-external-managed/) | 2026-06-23 | tables, unity-catalog, managed, external, set-managed, migration, uniform, path-based-redirect, streaming, B4 |
| [Specify a managed storage location in Unity Catalog](managed-storage/) | 2026-06-23 | unity-catalog, managed-storage, storage-location, external-location, catalog, schema, metastore, volumes, B1, B4 |
| [Catalog commits](catalog-commits/) | 2026-06-24 | tables, unity-catalog, managed, delta, iceberg, catalog-commits, transactions, external-access, streaming, B4 |
| [Transactions](transactions/) | 2026-06-24 | tables, unity-catalog, transactions, acid, catalog-commits, isolation, concurrency, atomic, rollback, B4 |
| [Predictive optimization](predictive-optimization/) | 2026-06-24 | tables, unity-catalog, managed, delta, iceberg, predictive-optimization, optimize, vacuum, analyze, liquid-clustering, serverless, system-tables, B4, B5 |
| [Use liquid clustering for tables](liquid-clustering/) | 2026-06-24 | tables, delta, iceberg, liquid-clustering, cluster-by, optimize, zorder, partitioning, predictive-optimization, automatic-clustering, data-skipping, A2, I5 |
| [Access Databricks data using external systems](external-access/) | 2026-06-24 | unity-catalog, external-access, iceberg-rest-catalog, unity-rest-api, credential-vending, compatibility-mode, opensharing, external-tables, external-volumes, A7, I8, B4 |
| [Data governance with Databricks (UC hub)](data-governance-hub/) | 2026-06-24 | data-governance, unity-catalog, access-control, abac, lineage, data-quality-monitoring, opensharing, clean-rooms, marketplace, audit, system-tables, I7, E2, A6, A7 |
| [Automatic upgrades for managed tables](automatic-upgrades/) | 2026-06-24 | tables, unity-catalog, managed, automatic-upgrades, table-features, observation-window, verified-workloads, row-tracking, catalog-commits, checkpoint-v2, column-mapping, change-data-feed, B4, A2 |
| [Change data feed (CDF)](change-data-feed/) | 2026-06-24 | tables, delta, iceberg, change-data-feed, cdf, table_changes, readChangeFeed, row-tracking, structured-streaming, incremental-etl, cdc, gdpr, I5, I4, A4 |
| [Checkpoint V2](checkpoint-v2/) | 2026-06-24 | tables, delta, table-features, checkpoint-v2, concurrency, transaction-log, liquid-clustering, automatic-upgrades, v2Checkpoint, REORG, B4 |
| [Column mapping (rename & drop columns)](column-mapping/) | 2026-06-24 | tables, delta, column-mapping, rename-column, drop-column, schema-evolution, delta-protocol, streaming, schema-tracking-location, uniform, I5, A4 |
| [Row tracking](row-tracking/) | 2026-06-24 | tables, delta, iceberg, row-tracking, row-id, row-commit-version, row-lineage, delta-protocol, materialized-views, change-data-feed, I5 |
| [Merge (upsert into Delta)](merge/) | 2026-06-29 | delta, merge, upsert, scd, deduplication, when-matched, when-not-matched-by-source, incremental-sync, foreachBatch, I5, I4 |
| [Selective overwrite](selective-overwrite/) | 2026-06-29 | delta, overwrite, replace-where, replace-using, replace-on, dynamic-partition-overwrite, selective-overwrite, I5, I1 |
| [What is Lakeflow Connect?](lakeflow-connect-overview/) | 2026-06-29 | ingestion, lakeflow-connect, managed-connectors, standard-connectors, community-connectors, auto-loader, kafka, etl, incremental, A3, I1 |

| [File upload (Add data UI)](create-or-modify-table/) | 2026-06-29 | ingestion, file-upload, add-data-ui, delta, managed-table, csv, json, parquet, avro, unity-catalog, A3 |
| [Managed connectors in Lakeflow Connect](lakeflow-connect-managed/) | 2026-06-29 | ingestion, lakeflow-connect, managed-connectors, cdc, saas, database, kafka, streaming, query-based, file-connectors, serverless, A3 |

### Lakeflow Spark Declarative Pipelines — Concepts

| Page | Added | Tags |
|---|---|---|
| [Pipelines (SDP concepts)](ldp-concepts-pipelines/) | 2026-07-01 | lakeflow, declarative-pipelines, sdp, pipeline-graph, dag, pipeline-types, I3 |
| [Flows (SDP concepts)](ldp-concepts-flows/) | 2026-07-01 | lakeflow, declarative-pipelines, sdp, flows, append-flow, auto-cdc, update-flow, I3 |
| [Streaming tables (SDP concepts)](ldp-concepts-streaming-tables/) | 2026-07-02 | lakeflow, declarative-pipelines, sdp, streaming-tables, auto-loader, real-time-mode, watermarks, I3 |

### Lakeflow Spark Declarative Pipelines — Standalone pipelines

| Page | Added | Tags |
|---|---|---|
| [Schedule refreshes](ldp-dbsql-schedule-refreshes/) | 2026-07-10 | lakeflow, sdp, standalone-pipelines, trigger-on-update, schedule-cron, statement-timeout, performance-mode, I3, E8 |