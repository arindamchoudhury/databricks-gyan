# SQL warehouse types

> **Source:** [docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-types](https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-types)
> **Added:** 2026-06-16
> **Source updated:** 2026-02-12
> **Tags:** compute, sql-warehouse, serverless, photon, predictive-io, IWM, databricks-sql, B1
> **Type:** documentation

Three SQL warehouse types — **Serverless > Pro > Classic** — differentiated by which performance features they support and where compute runs. Serverless is recommended for most workloads and is the only type with Intelligent Workload Management; Pro and Classic run compute in the customer's AWS account and take ~4 minutes to start vs **2–6 seconds** for serverless. No SQL warehouse type supports credential passthrough — Unity Catalog is the required governance layer.

| Feature | Serverless | Pro | Classic |
|---|---|---|---|
| **Photon Engine** | ✓ | ✓ | ✓ |
| **Predictive IO** | ✓ | ✓ | — |
| **Intelligent Workload Management** | ✓ | — | — |

- **Photon** — "the built-in vectorized query engine… makes your existing SQL and DataFrame API calls faster and reduces your total cost per workload." On all types.
- **Predictive IO** — "a suite of features for speeding up selective scan operations in SQL queries." Serverless + Pro.
- **Intelligent Workload Management (IWM)** — "AI-powered prediction and dynamic management" that gives workloads the right resources quickly; handles variable query demand, queuing, and rapid autoscaling. Serverless only.

## Serverless SQL warehouses

Support **all** Databricks SQL performance features; compute runs in Databricks-managed infrastructure; startup **2–6 seconds**. "Choose a serverless SQL warehouse for the best startup performance, the most efficient IO, smarter handling of query demand that varies greatly over time, and rapid autoscaling when query queuing occurs." Best for ETL, BI, exploratory analysis, and variable query demand.

## Pro SQL warehouses

Support Photon and Predictive IO but **not** IWM; compute runs in the **customer's AWS account**; startup **~4 minutes**. Use Pro when serverless isn't available in the workspace region, or when you have **custom-defined networking** to connect to databases in your cloud/on-prem network (federation or hybrid architecture).

## Classic SQL warehouses

Support Photon but **not** Predictive IO or IWM; compute runs in the **customer's AWS account**; startup **~4 minutes**. The entry-level choice — "run interactive queries for data exploration with entry-level performance."

## Defaults by surface

| Surface | Default when serverless available | Default when serverless unavailable |
|---|---|---|
| UI | Serverless | Pro |
| API | Classic | Classic |

> 💡 API defaulting to **Classic** is a common gotcha — explicitly set the warehouse type when creating via API if you want serverless or pro.

## Credential passthrough

"SQL warehouses do not support credential passthrough. Databricks recommends using Unity Catalog for data governance." Applies to all three types.

Related: [[sql-warehouse-overview]], [[photon]], [[classic-compute-overview]], [[serverless-limitations]].
