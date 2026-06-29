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

## DIP-Dummies — *The Data Intelligence Platform For Dummies* (Kaplan & Kara, Wiley 2nd Databricks Special Ed., © 2026)

| Title | Type | Added | Tags |
|---|---|---|---|
| [Book Overview & reading log](dip-dummies/index.md) | book | 2026-06-20 | data-intelligence, overview |
| [Ch 1: Understanding Data Intelligence](dip-dummies/ch01-understanding-data-intelligence.md) | book | 2026-06-20 | data-intelligence, genai, concepts |
| [Ch 2: Lakehouse as Foundation for Data and AI](dip-dummies/ch02-lakehouse-foundation.md) | book | 2026-06-20 | lakehouse, genai-vs-classical-ai, B1 |
| [Ch 3: Getting Started with the Platform](dip-dummies/ch03-databricks-platform.md) | book | 2026-06-20 | platform-components, unity-catalog, lakeflow, lakebase, dbsql, B1 |
| [Ch 4: Building AI Applications](dip-dummies/ch04-building-ai-applications.md) | book | 2026-06-20 | agent-bricks, mlops, mcp, ai-bi, databricks-apps |
| [Ch 5: Ten Reasons You Need a DIP](dip-dummies/ch05-ten-reasons.md) | book | 2026-06-20 | summary, benefits |

## Lakehouse-Dummies — *The Data Lakehouse For Dummies* (Kaplan & Kara, Wiley 2nd Databricks Special Ed., © 2026)

| Title | Type | Added | Tags |
|---|---|---|---|
| [Book Overview & reading log](lakehouse-dummies/index.md) | book | 2026-06-20 | lakehouse, overview |
| [Ch 1: Making the Case for Data Lakehouses](lakehouse-dummies/01-making-the-case.md) | book | 2026-06-20 | data-warehouse, data-lake, silos, ACID, B1 |
| [Ch 2: Explaining Data Lakehouses](lakehouse-dummies/02-explaining-lakehouses.md) | book | 2026-06-20 | lakehouse, maturity-curve, serverless, B1 |
| [Ch 3: Understanding the Underlying Technology](lakehouse-dummies/03-underlying-technology.md) | book | 2026-06-20 | delta-lake, unity-catalog, lakebase, mlops, B1, B5 |
| [Ch 4: Bringing Data Intelligence to the Lakehouse](lakehouse-dummies/04-data-intelligence.md) | book | 2026-06-20 | data-intelligence, genie, agent-bricks, rag |
| [Ch 5: Ten Reasons You Need a Data Lakehouse](lakehouse-dummies/05-ten-reasons.md) | book | 2026-06-20 | summary, benefits |

## Databricks Blog — concept & engineering posts (databricks.com/blog)

| Title | Type | Added | Tags |
|---|---|---|---|
| [What Is a Data Lakehouse?](databricks-blog/what-is-a-lakehouse.md) | blog | 2026-06-20 | lakehouse, architecture, data-lake, data-warehouse, foundations, B1 |

## SunnyData — practitioner blog (Hubert Dudek)

| Title | Type | Added | Tags |
|---|---|---|---|
| [Source overview](sunnydata/index.md) | blog | 2026-06-26 | sunnydata, practitioner, hubert-dudek |
| [Unity Catalog commits — write mechanics, staged commits, ABAC](sunnydata/catalog-commits.md) | blog | 2026-06-26 | unity-catalog, catalog-commits, staged-commits, dynamodb, abac, external-access, B4 |
| [Multi-statement transactions (MSTs) — atomic SQL across Delta tables](sunnydata/multi-statement-transactions.md) | blog | 2026-06-26 | unity-catalog, transactions, multi-statement, begin-atomic, catalog-commits, delta, iceberg, lakebase, B4 |

## Databricks Papers — research papers & whitepapers

| Title | Type | Added | Tags |
|---|---|---|---|
| [Lakehouse: A New Generation of Open Platforms…](databricks-papers/lakehouse-cidr-2021.md) | paper | 2026-06-21 | lakehouse, architecture, delta-lake, metadata-layer, tpc-ds, foundations, B1 |

## Databricks Docs — official documentation (docs.databricks.com)

| Title | Type | Added | Tags |
|---|---|---|---|
| [High-level Architecture](databricks-docs/high-level-architecture.md) | documentation | 2026-06-20 | architecture, control-plane, compute-plane, account, workspace, unity-catalog, serverless, classic, B1 |
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
| [Databricks tables concepts](databricks-docs/tables-concepts.md) | documentation | 2026-06-22 | tables, unity-catalog, managed, external, foreign, temporary, delta, iceberg, permissions, B4 |
| [Unity Catalog managed tables](databricks-docs/managed-tables.md) | documentation | 2026-06-23 | tables, unity-catalog, managed, delta, iceberg, predictive-optimization, catalog-commits, undrop, recovery-period, B4 |
| [Unity Catalog external tables](databricks-docs/external-tables.md) | documentation | 2026-06-24 | tables, unity-catalog, external, delta, external-location, storage-credential, drop-table, repair-table, B4 |
| [Partition discovery for external tables](databricks-docs/external-partition-discovery.md) | documentation | 2026-06-24 | tables, unity-catalog, external, partitioning, partition-metadata, msck-repair, hive-style, B4 |
| [Convert an external Delta table to managed](databricks-docs/convert-external-managed.md) | documentation | 2026-06-23 | tables, unity-catalog, managed, external, set-managed, migration, uniform, path-based-redirect, streaming, B4 |
| [Specify a managed storage location in Unity Catalog](databricks-docs/managed-storage.md) | documentation | 2026-06-23 | unity-catalog, managed-storage, storage-location, external-location, catalog, schema, metastore, volumes, B1, B4 |
| [Catalog commits](databricks-docs/catalog-commits.md) | documentation | 2026-06-24 | tables, unity-catalog, managed, delta, iceberg, catalog-commits, transactions, external-access, streaming, B4 |
| [Transactions](databricks-docs/transactions.md) | documentation | 2026-06-24 | tables, unity-catalog, transactions, acid, catalog-commits, isolation, concurrency, atomic, rollback, B4 |
| [Predictive optimization](databricks-docs/predictive-optimization.md) | documentation | 2026-06-24 | tables, unity-catalog, managed, delta, iceberg, predictive-optimization, optimize, vacuum, analyze, serverless, system-tables, B4, B5 |
| [Use liquid clustering for tables](databricks-docs/liquid-clustering.md) | documentation | 2026-06-24 | tables, delta, iceberg, liquid-clustering, cluster-by, optimize, zorder, partitioning, automatic-clustering, A2, I5 |
| [Access Databricks data using external systems](databricks-docs/external-access.md) | documentation | 2026-06-24 | unity-catalog, external-access, iceberg-rest-catalog, unity-rest-api, credential-vending, compatibility-mode, opensharing, A7, I8, B4 |
| [Data governance with Databricks (UC hub)](databricks-docs/data-governance-hub.md) | documentation | 2026-06-24 | data-governance, unity-catalog, access-control, abac, lineage, data-quality-monitoring, opensharing, clean-rooms, marketplace, audit, system-tables, I7, E2, A6, A7 |
| [Automatic upgrades for managed tables](databricks-docs/automatic-upgrades.md) | documentation | 2026-06-24 | tables, unity-catalog, managed, automatic-upgrades, table-features, observation-window, verified-workloads, B4, A2 |
| [Change data feed (CDF)](databricks-docs/change-data-feed.md) | documentation | 2026-06-24 | tables, delta, iceberg, change-data-feed, cdf, table_changes, structured-streaming, cdc, gdpr, I5, I4, A4 |
| [Checkpoint V2](databricks-docs/checkpoint-v2.md) | documentation | 2026-06-24 | tables, delta, table-features, checkpoint-v2, concurrency, transaction-log, liquid-clustering, automatic-upgrades, B4 |
| [Column mapping (rename & drop columns)](databricks-docs/column-mapping.md) | documentation | 2026-06-24 | tables, delta, column-mapping, rename-column, drop-column, schema-evolution, delta-protocol, streaming, I5, A4 |
| [Row tracking](databricks-docs/row-tracking.md) | documentation | 2026-06-24 | tables, delta, iceberg, row-tracking, row-id, row-commit-version, materialized-views, change-data-feed, I5 |
| [Optimization recommendations (hub)](databricks-docs/optimization-recommendations.md) | documentation | 2026-06-24 | optimization, performance, databricks-runtime, hub, A1 |
| [Disk caching (Delta/DBIO cache)](databricks-docs/disk-cache.md) | documentation | 2026-06-24 | optimization, disk-cache, delta-cache, ssd, caching, A1 |
| [Dynamic file pruning](databricks-docs/dynamic-file-pruning.md) | documentation | 2026-06-24 | optimization, dynamic-file-pruning, dfp, join, photon, A1 |
| [Low shuffle merge](databricks-docs/low-shuffle-merge.md) | documentation | 2026-06-24 | optimization, merge, low-shuffle-merge, shuffle, delta, A1, I5 |
| [Cost-based optimizer (CBO)](databricks-docs/cost-based-optimizer.md) | documentation | 2026-06-24 | optimization, cbo, statistics, analyze-table, joins, A1 |
| [Range join optimization](databricks-docs/range-join.md) | documentation | 2026-06-24 | optimization, range-join, join, bin-size, interval, A1 |
| [Isolation levels and write conflicts](databricks-docs/isolation-levels.md) | documentation | 2026-06-24 | optimization, delta, isolation, write-serializable, concurrency, A1, B4 |
| [Work with foreign tables](databricks-docs/foreign-tables.md) | documentation | 2026-06-25 | tables, unity-catalog, foreign, federation, lakehouse-federation, query-federation, catalog-federation, hive-metastore, read-only, B4, A7 |
| [Convert a foreign table to a managed Unity Catalog table](databricks-docs/convert-foreign-managed.md) | documentation | 2026-06-25 | tables, unity-catalog, foreign, managed, set-managed, federation, hms, glue, public-preview, B4 |
| [Convert a foreign table to an external Unity Catalog table](databricks-docs/convert-foreign-external.md) | documentation | 2026-06-25 | tables, unity-catalog, foreign, external, set-external, federation, hms, glue, public-preview, B4 |
| [Temporary tables](databricks-docs/temporary-tables.md) | documentation | 2026-06-25 | tables, table-types, temporary, session-scoped, delta, sql, dbr-18.1, no-privileges |
| [Data engineering with Databricks (Lakeflow hub)](databricks-docs/data-engineering-hub.md) | documentation | 2026-06-25 | data-engineering, lakeflow, lakeflow-connect, declarative-pipelines, lakeflow-designer, lakeflow-jobs, databricks-runtime, flows, streaming-tables, materialized-views, sinks, B6, I1, I2, I3, I6, A3, A6 |
| [Procedural vs. declarative data processing](databricks-docs/procedural-vs-declarative.md) | documentation | 2026-06-25 | data-engineering, concepts, procedural, declarative, lakeflow-jobs, declarative-pipelines, spark, I3, I6 |
| [Materialized views (and the serverless compute model)](databricks-docs/materialized-views.md) | documentation | 2026-06-25 | materialized-view, lakeflow, declarative-pipelines, serverless, dbsql, incremental-refresh, row-tracking, federation, I3, I8, A7 |
| [Batch vs. streaming data processing](databricks-docs/batch-vs-streaming.md) | documentation | 2026-06-26 | data-engineering, concepts, batch, streaming, structured-streaming, incremental, medallion, lakeflow, materialized-views, streaming-tables, I1, I2, B7 |
| [Tables and views in Databricks](databricks-docs/tables-views.md) | documentation | 2026-06-26 | data-engineering, concepts, tables, views, materialized-views, streaming-tables, B4, I2, I3 |
| [Schema evolution in Databricks](databricks-docs/schema-evolution.md) | documentation | 2026-06-27 | data-engineering, concepts, schema-evolution, mergeSchema, auto-loader, structured-streaming, streaming-tables, materialized-views, delta, views, type-widening, column-mapping, from_json, from_avro, I1, I2, I5 |
