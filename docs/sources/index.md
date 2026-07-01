# Sources

Course notebooks and external sources captured as structured notes.

## DA-FREE — *Get Started with Data Engineering* (Databricks Academy)

| Title | Type | Added | Tags |
|---|---|---|---|
| [M1: Databricks Workspace Walkthrough](da-free/workspace-walkthrough/) | notebook | 2026-06-11 | workspace, UI, compute, unity-catalog, B1 |
| [M2-01: Creating and Working with a Delta Table](da-free/creating-delta-table/) | notebook | 2026-06-11 | delta, CTAS, DML, time-travel, B5 |
| [M2-02: Ingesting Data into Delta Lake](da-free/ingesting-data/) | notebook | 2026-06-11 | ingestion, COPY-INTO, auto-loader, B6 |
| [M2-03: Transforming Data Using the Medallion Architecture](da-free/medallion-architecture/) | notebook | 2026-06-11 | medallion, bronze, silver, gold, B7 |
| [M2-04: Creating a Simple Databricks Job](da-free/lakeflow-jobs/) | notebook | 2026-06-11 | jobs, lakeflow, orchestration, I6 |

## DCDE-SG — *Databricks Certified Data Engineer Associate Study Guide* (Alhussein, O'Reilly 2025)

| Title | Type | Added | Tags |
|---|---|---|---|
| [Book Overview & reading log](dcde-sg/index/) | book | 2026-06-14 | dcdea, exam-prep |
| [Ch 1: Getting Started with Databricks](dcde-sg/ch01-getting-started-with-databricks/) | book | 2026-06-14 | platform, architecture, clusters, notebooks, B1 |
| [Ch 2: Managing Data with Delta Lake](dcde-sg/ch02-managing-data-with-delta-lake/) | book | 2026-06-19 | delta, transaction-log, acid, time-travel, optimize, vacuum, B5 |

## DIP-Dummies — *The Data Intelligence Platform For Dummies* (Kaplan & Kara, Wiley 2nd Databricks Special Ed., © 2026)

| Title | Type | Added | Tags |
|---|---|---|---|
| [Book Overview & reading log](dip-dummies/index/) | book | 2026-06-20 | data-intelligence, overview |
| [Ch 1: Understanding Data Intelligence](dip-dummies/ch01-understanding-data-intelligence/) | book | 2026-06-20 | data-intelligence, genai, concepts |
| [Ch 2: Lakehouse as Foundation for Data and AI](dip-dummies/ch02-lakehouse-foundation/) | book | 2026-06-20 | lakehouse, genai-vs-classical-ai, B1 |
| [Ch 3: Getting Started with the Platform](dip-dummies/ch03-databricks-platform/) | book | 2026-06-20 | platform-components, unity-catalog, lakeflow, lakebase, dbsql, B1 |
| [Ch 4: Building AI Applications](dip-dummies/ch04-building-ai-applications/) | book | 2026-06-20 | agent-bricks, mlops, mcp, ai-bi, databricks-apps |
| [Ch 5: Ten Reasons You Need a DIP](dip-dummies/ch05-ten-reasons/) | book | 2026-06-20 | summary, benefits |

## Lakehouse-Dummies — *The Data Lakehouse For Dummies* (Kaplan & Kara, Wiley 2nd Databricks Special Ed., © 2026)

| Title | Type | Added | Tags |
|---|---|---|---|
| [Book Overview & reading log](lakehouse-dummies/index/) | book | 2026-06-20 | lakehouse, overview |
| [Ch 1: Making the Case for Data Lakehouses](lakehouse-dummies/01-making-the-case/) | book | 2026-06-20 | data-warehouse, data-lake, silos, ACID, B1 |
| [Ch 2: Explaining Data Lakehouses](lakehouse-dummies/02-explaining-lakehouses/) | book | 2026-06-20 | lakehouse, maturity-curve, serverless, B1 |
| [Ch 3: Understanding the Underlying Technology](lakehouse-dummies/03-underlying-technology/) | book | 2026-06-20 | delta-lake, unity-catalog, lakebase, mlops, B1, B5 |
| [Ch 4: Bringing Data Intelligence to the Lakehouse](lakehouse-dummies/04-data-intelligence/) | book | 2026-06-20 | data-intelligence, genie, agent-bricks, rag |
| [Ch 5: Ten Reasons You Need a Data Lakehouse](lakehouse-dummies/05-ten-reasons/) | book | 2026-06-20 | summary, benefits |

## Databricks Blog — concept & engineering posts (databricks.com/blog)

| Title | Type | Added | Tags |
|---|---|---|---|
| [What Is a Data Lakehouse?](databricks-blog/what-is-a-lakehouse/) | blog | 2026-06-20 | lakehouse, architecture, data-lake, data-warehouse, foundations, B1 |
| [From Monolith to Lakebase to LTAP](databricks-blog/lakebase-ltap-rethinking-database-storage/) | blog | 2026-07-01 | lakebase, ltap, postgres, safekeeper, pageserver, oltp, olap, htap, E8 |

## SunnyData — practitioner blog (Hubert Dudek)

| Title | Type | Added | Tags |
|---|---|---|---|
| [Source overview](sunnydata/index/) | blog | 2026-06-26 | sunnydata, practitioner, hubert-dudek |
| [Unity Catalog commits — write mechanics, staged commits, ABAC](sunnydata/catalog-commits/) | blog | 2026-06-26 | unity-catalog, catalog-commits, staged-commits, dynamodb, abac, external-access, B4 |
| [Multi-statement transactions (MSTs) — atomic SQL across Delta tables](sunnydata/multi-statement-transactions/) | blog | 2026-06-26 | unity-catalog, transactions, multi-statement, begin-atomic, catalog-commits, delta, iceberg, lakebase, B4 |

## Databricks Papers — research papers & whitepapers

| Title | Type | Added | Tags |
|---|---|---|---|
| [Lakehouse: A New Generation of Open Platforms…](databricks-papers/lakehouse-cidr-2021/) | paper | 2026-06-21 | lakehouse, architecture, delta-lake, metadata-layer, tpc-ds, foundations, B1 |

## Databricks Docs — official documentation (docs.databricks.com)

| Title | Type | Added | Tags |
|---|---|---|---|
| [High-level Architecture](databricks-docs/high-level-architecture/) | documentation | 2026-06-20 | architecture, control-plane, compute-plane, account, workspace, unity-catalog, serverless, classic, B1 |
| [Debug Notebooks (Interactive Debugger)](databricks-docs/notebook-debugger/) | documentation | 2026-06-14 | notebooks, debugging, variable-explorer, B1 |
| [Serverless Compute for Notebooks](databricks-docs/serverless-notebooks/) | documentation | 2026-06-15 | serverless, notebooks, query-insights, B1 |
| [Serverless Compute for Lakeflow Jobs](databricks-docs/serverless-jobs/) | documentation | 2026-06-15 | serverless, jobs, lakeflow, workflows, I6 |
| [Serverless Compute for Lakeflow Pipelines](databricks-docs/serverless-pipelines/) | documentation | 2026-06-16 | serverless, pipelines, lakeflow, ldp, I5 |
| [Serverless compute limitations](databricks-docs/serverless-limitations/) | documentation | 2026-06-16 | serverless, limitations, streaming, caching, B1, I5, I6 |
| [Classic compute overview](databricks-docs/classic-compute-overview/) | documentation | 2026-06-16 | compute, classic-compute, access-modes, permissions, B1 |
| [Classic compute configuration reference](databricks-docs/classic-compute-configure/) | documentation | 2026-06-16 | compute, classic-compute, configuration, autoscaling, EBS, spark-config, B1 |
| [Standard compute overview](databricks-docs/standard-compute-overview/) | documentation | 2026-06-16 | compute, classic-compute, access-modes, standard, lakeguard, B1 |
| [Dedicated compute overview](databricks-docs/dedicated-compute-overview/) | documentation | 2026-06-16 | compute, classic-compute, access-modes, dedicated, RDD, GPU, R, B1 |
| [Compute pools (instance pools)](databricks-docs/compute-pools/) | documentation | 2026-06-16 | compute, pools, autoscaling, cost, B1 |
| [SQL warehouse overview](databricks-docs/sql-warehouse-overview/) | documentation | 2026-06-16 | compute, sql-warehouse, serverless, databricks-sql, BI, B1 |
| [SQL warehouse types](databricks-docs/sql-warehouse-types/) | documentation | 2026-06-16 | compute, sql-warehouse, serverless, photon, predictive-io, IWM, B1 |
| [Photon](databricks-docs/photon/) | documentation | 2026-06-16 | compute, photon, performance, vectorized, sql-warehouse, B1 |
| [Lakeguard](databricks-docs/lakeguard/) | documentation | 2026-06-16 | compute, lakeguard, security, isolation, standard-compute, spark-connect, B1 |
| [Notebooks Overview](databricks-docs/notebooks-overview/) | documentation | 2026-06-17 | notebooks, python, sql, scala, R, EDA, ML, collaboration, B1 |
| [Dashboards in Notebooks](databricks-docs/notebook-dashboards/) | documentation | 2026-06-17 | notebooks, dashboards, visualization, AI-BI, scheduling, sharing, B1 |
| [Unit Testing in Notebooks](databricks-docs/notebook-testing/) | documentation | 2026-06-17 | notebooks, testing, pytest, testthat, scalatest, sql, CI-CD, B1 |
| [Databricks Widgets](databricks-docs/notebook-widgets/) | documentation | 2026-06-17 | notebooks, widgets, parameters, sql, python, scala, R, dashboards, B1 |
| [Orchestrate Notebooks and Modularize Code](databricks-docs/notebook-workflows/) | documentation | 2026-06-17 | notebooks, orchestration, workflows, dbutils, run, modularization, B1, I6 |
| [ipywidgets in Notebooks](databricks-docs/notebook-ipywidgets/) | documentation | 2026-06-17 | notebooks, ipywidgets, python, interactive, visualization, B1 |
| [Share Code Between Notebooks (Workspace Files)](databricks-docs/notebook-share-code/) | documentation | 2026-06-17 | notebooks, workspace-files, modularization, python, git, B1 |
| [Notebook Best Practices (Software Engineering)](databricks-docs/notebook-best-practices/) | documentation | 2026-06-17 | notebooks, best-practices, git, testing, CI-CD, modularization, jobs, B1 |
| [Spark UI Guide (diagnose cost and performance)](databricks-docs/spark-ui-guide/) | documentation | 2026-06-17 | spark, spark-ui, performance, optimization, debugging, skew, spill, stages, tasks, B2, B16 |
| [Optimize Databricks, Spark and Delta Lake Workloads](databricks-docs/optimize-data-workloads-guide/) | documentation | 2026-06-17 | spark, performance, optimization, delta-lake, shuffle, skew, spill, merge, vacuum, caching, photon, B2, B5, B12, B16, B17 |
| [Failing Jobs or Executors Removed](databricks-docs/failing-spark-jobs/) | documentation | 2026-06-17 | spark, spark-ui, debugging, executors, memory, spot-instances, autoscaling, B2, B16 |
| [Look at Longest Stage](databricks-docs/long-spark-stage/) | documentation | 2026-06-17 | spark, spark-ui, performance, debugging, stages, tasks, shuffle, B2, B16 |
| [Look for Skew or Spill](databricks-docs/long-spark-stage-page/) | documentation | 2026-06-17 | spark, spark-ui, performance, debugging, skew, spill, memory, shuffle, B2, B16 |
| [Spark Memory Issues](databricks-docs/spark-memory-issues/) | documentation | 2026-06-17 | spark, spark-ui, debugging, memory, OOM, executors, shuffle, broadcast, UDF, skew, streaming, B2, B16 |
| [Determine if Longest Stage is I/O Bound](databricks-docs/long-spark-stage-io/) | documentation | 2026-06-17 | spark, spark-ui, performance, debugging, I/O, shuffle, delta-cache, photon, liquid-clustering, B2, B16 |
| [Look for Other Causes of Slow Stage Runtime](databricks-docs/slow-spark-stage-low-io/) | documentation | 2026-06-17 | spark, spark-ui, performance, debugging, small-files, UDF, cartesian-join, explode, DAG, B2, B16 |
| [How to Determine if Spark is Rewriting Data](databricks-docs/spark-rewriting-data/) | documentation | 2026-06-17 | spark, spark-ui, debugging, delta, merge, delete, update, rewriting, B2, B12, B16 |
| [One Spark Task](databricks-docs/one-spark-task/) | documentation | 2026-06-17 | spark, spark-ui, debugging, tasks, parallelism, UDF, gzip, coalesce, repartition, B2, B16 |
| [Losing Spot Instances](databricks-docs/losing-spot-instances/) | documentation | 2026-06-17 | spark, spark-ui, debugging, spot-instances, AWS, executors, B2, B16 |
| [SQL Hints: Join, Partition, and Skew](databricks-docs/sql-join-hints/) | documentation | 2026-06-18 | spark, sql, join-hints, broadcast, shuffle, partitioning, performance, optimization, B2, B8 |
| [Adaptive Query Execution (AQE)](databricks-docs/aqe/) | documentation | 2026-06-18 | spark, aqe, performance, optimization, broadcast, skew, shuffle, partitioning, B2, B8, B16 |
| [Databricks tables concepts](databricks-docs/tables-concepts/) | documentation | 2026-06-22 | tables, unity-catalog, managed, external, foreign, temporary, delta, iceberg, permissions, B4 |
| [Unity Catalog managed tables](databricks-docs/managed-tables/) | documentation | 2026-06-23 | tables, unity-catalog, managed, delta, iceberg, predictive-optimization, catalog-commits, undrop, recovery-period, B4 |
| [Unity Catalog external tables](databricks-docs/external-tables/) | documentation | 2026-06-24 | tables, unity-catalog, external, delta, external-location, storage-credential, drop-table, repair-table, B4 |
| [Partition discovery for external tables](databricks-docs/external-partition-discovery/) | documentation | 2026-06-24 | tables, unity-catalog, external, partitioning, partition-metadata, msck-repair, hive-style, B4 |
| [Convert an external Delta table to managed](databricks-docs/convert-external-managed/) | documentation | 2026-06-23 | tables, unity-catalog, managed, external, set-managed, migration, uniform, path-based-redirect, streaming, B4 |
| [Specify a managed storage location in Unity Catalog](databricks-docs/managed-storage/) | documentation | 2026-06-23 | unity-catalog, managed-storage, storage-location, external-location, catalog, schema, metastore, volumes, B1, B4 |
| [Catalog commits](databricks-docs/catalog-commits/) | documentation | 2026-06-24 | tables, unity-catalog, managed, delta, iceberg, catalog-commits, transactions, external-access, streaming, B4 |
| [Transactions](databricks-docs/transactions/) | documentation | 2026-06-24 | tables, unity-catalog, transactions, acid, catalog-commits, isolation, concurrency, atomic, rollback, B4 |
| [Predictive optimization](databricks-docs/predictive-optimization/) | documentation | 2026-06-24 | tables, unity-catalog, managed, delta, iceberg, predictive-optimization, optimize, vacuum, analyze, serverless, system-tables, B4, B5 |
| [Use liquid clustering for tables](databricks-docs/liquid-clustering/) | documentation | 2026-06-24 | tables, delta, iceberg, liquid-clustering, cluster-by, optimize, zorder, partitioning, automatic-clustering, A2, I5 |
| [Access Databricks data using external systems](databricks-docs/external-access/) | documentation | 2026-06-24 | unity-catalog, external-access, iceberg-rest-catalog, unity-rest-api, credential-vending, compatibility-mode, opensharing, A7, I8, B4 |
| [Data governance with Databricks (UC hub)](databricks-docs/data-governance-hub/) | documentation | 2026-06-24 | data-governance, unity-catalog, access-control, abac, lineage, data-quality-monitoring, opensharing, clean-rooms, marketplace, audit, system-tables, I7, E2, A6, A7 |
| [Automatic upgrades for managed tables](databricks-docs/automatic-upgrades/) | documentation | 2026-06-24 | tables, unity-catalog, managed, automatic-upgrades, table-features, observation-window, verified-workloads, B4, A2 |
| [Change data feed (CDF)](databricks-docs/change-data-feed/) | documentation | 2026-06-24 | tables, delta, iceberg, change-data-feed, cdf, table_changes, structured-streaming, cdc, gdpr, I5, I4, A4 |
| [Checkpoint V2](databricks-docs/checkpoint-v2/) | documentation | 2026-06-24 | tables, delta, table-features, checkpoint-v2, concurrency, transaction-log, liquid-clustering, automatic-upgrades, B4 |
| [Column mapping (rename & drop columns)](databricks-docs/column-mapping/) | documentation | 2026-06-24 | tables, delta, column-mapping, rename-column, drop-column, schema-evolution, delta-protocol, streaming, I5, A4 |
| [Row tracking](databricks-docs/row-tracking/) | documentation | 2026-06-24 | tables, delta, iceberg, row-tracking, row-id, row-commit-version, materialized-views, change-data-feed, I5 |
| [Optimization recommendations (hub)](databricks-docs/optimization-recommendations/) | documentation | 2026-06-24 | optimization, performance, databricks-runtime, hub, A1 |
| [Disk caching (Delta/DBIO cache)](databricks-docs/disk-cache/) | documentation | 2026-06-24 | optimization, disk-cache, delta-cache, ssd, caching, A1 |
| [Dynamic file pruning](databricks-docs/dynamic-file-pruning/) | documentation | 2026-06-24 | optimization, dynamic-file-pruning, dfp, join, photon, A1 |
| [Low shuffle merge](databricks-docs/low-shuffle-merge/) | documentation | 2026-06-24 | optimization, merge, low-shuffle-merge, shuffle, delta, A1, I5 |
| [Cost-based optimizer (CBO)](databricks-docs/cost-based-optimizer/) | documentation | 2026-06-24 | optimization, cbo, statistics, analyze-table, joins, A1 |
| [Range join optimization](databricks-docs/range-join/) | documentation | 2026-06-24 | optimization, range-join, join, bin-size, interval, A1 |
| [Isolation levels and write conflicts](databricks-docs/isolation-levels/) | documentation | 2026-06-24 | optimization, delta, isolation, write-serializable, concurrency, A1, B4 |
| [Work with foreign tables](databricks-docs/foreign-tables/) | documentation | 2026-06-25 | tables, unity-catalog, foreign, federation, lakehouse-federation, query-federation, catalog-federation, hive-metastore, read-only, B4, A7 |
| [Convert a foreign table to a managed Unity Catalog table](databricks-docs/convert-foreign-managed/) | documentation | 2026-06-25 | tables, unity-catalog, foreign, managed, set-managed, federation, hms, glue, public-preview, B4 |
| [Convert a foreign table to an external Unity Catalog table](databricks-docs/convert-foreign-external/) | documentation | 2026-06-25 | tables, unity-catalog, foreign, external, set-external, federation, hms, glue, public-preview, B4 |
| [Temporary tables](databricks-docs/temporary-tables/) | documentation | 2026-06-25 | tables, table-types, temporary, session-scoped, delta, sql, dbr-18.1, no-privileges |
| [Data engineering with Databricks (Lakeflow hub)](databricks-docs/data-engineering-hub/) | documentation | 2026-06-25 | data-engineering, lakeflow, lakeflow-connect, declarative-pipelines, lakeflow-designer, lakeflow-jobs, databricks-runtime, flows, streaming-tables, materialized-views, sinks, B6, I1, I2, I3, I6, A3, A6 |
| [Procedural vs. declarative data processing](databricks-docs/procedural-vs-declarative/) | documentation | 2026-06-25 | data-engineering, concepts, procedural, declarative, lakeflow-jobs, declarative-pipelines, spark, I3, I6 |
| [Materialized views (and the serverless compute model)](databricks-docs/materialized-views/) | documentation | 2026-06-25 | materialized-view, lakeflow, declarative-pipelines, serverless, dbsql, incremental-refresh, row-tracking, federation, I3, I8, A7 |
| [Batch vs. streaming data processing](databricks-docs/batch-vs-streaming/) | documentation | 2026-06-26 | data-engineering, concepts, batch, streaming, structured-streaming, incremental, medallion, lakeflow, materialized-views, streaming-tables, I1, I2, B7 |
| [Tables and views in Databricks](databricks-docs/tables-views/) | documentation | 2026-06-26 | data-engineering, concepts, tables, views, materialized-views, streaming-tables, B4, I2, I3 |
| [Schema evolution in Databricks](databricks-docs/schema-evolution/) | documentation | 2026-06-27 | data-engineering, concepts, schema-evolution, mergeSchema, auto-loader, structured-streaming, streaming-tables, materialized-views, delta, views, type-widening, column-mapping, from_json, from_avro, I1, I2, I5 |
| [Select columns to ingest (Lakeflow Connect)](databricks-docs/lakeflow-connect-column-selection/) | documentation | 2026-06-30 | lakeflow-connect, managed-connectors, ingestion, column-selection, table-configuration, A3 |
| [Fully refresh target tables (Lakeflow Connect)](databricks-docs/lakeflow-connect-full-refresh/) | documentation | 2026-06-30 | lakeflow-connect, managed-connectors, full-refresh, cdc, ingestion, A3 |
| [Monitor ingestion gateway progress with event logs](databricks-docs/lakeflow-connect-gateway-event-logs/) | documentation | 2026-06-30 | lakeflow-connect, managed-connectors, gateway, event-log, monitoring, cdc, snapshot, A3, A6 |
| [Enable history tracking / SCD Type 2 (Lakeflow Connect)](databricks-docs/lakeflow-connect-scd/) | documentation | 2026-06-30 | lakeflow-connect, managed-connectors, scd, scd-type-2, history-tracking, sequence-by, A3 |
| [Monitor managed ingestion pipeline cost](databricks-docs/lakeflow-connect-monitor-costs/) | documentation | 2026-06-30 | lakeflow-connect, managed-connectors, cost-monitoring, system-tables, billing, dbu, A3, A6 |
| [Create multi-destination pipelines](databricks-docs/lakeflow-connect-multi-destination/) | documentation | 2026-06-30 | lakeflow-connect, managed-connectors, multi-destination, fan-out, destination-table, A3 |
| [Name a destination table](databricks-docs/lakeflow-connect-table-rename/) | documentation | 2026-06-30 | lakeflow-connect, managed-connectors, destination-table, table-rename, A3 |
| [Common pipeline maintenance tasks](databricks-docs/lakeflow-connect-pipeline-maintenance/) | documentation | 2026-06-30 | lakeflow-connect, managed-connectors, pipeline-maintenance, operations, staging-files, A3 |
| [Apply tags to managed ingestion pipelines](databricks-docs/lakeflow-connect-pipeline-tags/) | documentation | 2026-06-30 | lakeflow-connect, managed-connectors, pipeline-tags, cost-attribution, A3 |
| [Select rows to ingest (row filtering)](databricks-docs/lakeflow-connect-row-filtering/) | documentation | 2026-06-30 | lakeflow-connect, managed-connectors, row-filtering, ingestion, A3 |
| [Configure the Run as identity](databricks-docs/lakeflow-connect-run-as/) | documentation | 2026-06-30 | lakeflow-connect, managed-connectors, run-as, service-principal, identity, A3 |
| [Managed connector FAQs](databricks-docs/lakeflow-connect-faq/) | documentation | 2026-06-30 | lakeflow-connect, managed-connectors, faq, schema-evolution, pricing, A3 |
| [Managed database connectors (CDC)](databricks-docs/lakeflow-connect-cdc-overview/) | documentation | 2026-06-30 | lakeflow-connect, database-connectors, cdc, ingestion-gateway, staging-storage, A3 |
| [Query-based connectors](databricks-docs/lakeflow-connect-query-based-overview/) | documentation | 2026-06-30 | lakeflow-connect, query-based-connectors, cursor-column, lakehouse-federation, scd, A3 |
| [foreachBatch — write to arbitrary data sinks](databricks-docs/structured-streaming-foreach/) | documentation | 2026-06-30 | structured-streaming, foreach-batch, idempotency, dead-letter-queue, I2, I5 |
| [Delta Lake table streaming reads and writes](databricks-docs/structured-streaming-delta-lake/) | documentation | 2026-06-30 | structured-streaming, delta-lake, skipChangeCommits, withEventTimeOrder, I2, I5 |
| [Subscribe to Google Pub/Sub](databricks-docs/streaming-pub-sub/) | documentation | 2026-06-30 | structured-streaming, pub-sub, google-cloud, I2 |
| [Connect to Lakebase (streaming sink)](databricks-docs/streaming-lakebase/) | documentation | 2026-06-30 | structured-streaming, lakebase, postgresql, streaming-sink, E8, I2 |
| [Lakeflow Spark Declarative Pipelines (hub)](databricks-docs/ldp-overview/) | documentation | 2026-07-01 | lakeflow, declarative-pipelines, sdp, hub, dlt-to-ldp-rename, apache-spark-declarative-pipelines, I3 |
