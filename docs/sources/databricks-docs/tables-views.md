# Tables and views in Databricks

> **Source:** [docs.databricks.com/aws/en/data-engineering/tables-views](https://docs.databricks.com/aws/en/data-engineering/tables-views)
> **Added:** 2026-06-26
> **Source updated:** 2026-01-23
> **Tags:** data-engineering, concepts, tables, views, materialized-views, streaming-tables, B4, I2, I3
> **Type:** documentation

A short Data engineering › Concepts page giving the high-level taxonomy of the four data objects you build pipelines around: **table**, **view**, **materialized view**, and **streaming table**. It's an index that points out to the deeper pages for each.

## Table

A structured dataset stored in a specific location. The **default table type in Databricks is a Unity Catalog managed table**. Tables can be queried and manipulated with SQL or the DataFrame APIs (`INSERT`, `UPDATE`, `DELETE`, `MERGE INTO`). → [[tables-concepts]]

## View

A **virtual table defined by a query that does not store data** — it can present data from one or more tables in a specific format or abstraction. Useful for simplifying complex queries, encapsulating business logic, and providing a consistent interface without duplicating storage.

## Materialized view

Like a view, defined by a query — but it **precomputes and stores the query's result**, so queries run faster than against a plain view at the cost of extra storage. Create/refresh a standalone MV in Databricks SQL, or define MVs (alongside streaming tables and views) in a Lakeflow Spark Declarative Pipeline. → [[materialized-views]]

## Streaming table

A type of **Unity Catalog managed table that includes the processing logic** that defines it, via **flows**. Create/refresh a standalone streaming table in Databricks SQL, or define streaming tables (alongside MVs and views) in a Lakeflow Spark Declarative Pipeline. → [[data-engineering-hub]] (SDP object model)

## Materialized view vs. streaming table

Both are common data-engineering objects: **materialized views use batch semantics; streaming tables use streaming semantics.** For the comparison and how to choose per workload, see [[batch-vs-streaming]].

Related: [[tables-concepts]], [[materialized-views]], [[batch-vs-streaming]], [[data-engineering-hub]], [[procedural-vs-declarative]].
