# SQL warehouse types

> **Source:** [docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-types](https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-types)
> **Added:** 2026-06-16
> **Source updated:** 2026-02-12
> **Tags:** compute, sql-warehouse, serverless, photon, predictive-io, IWM, databricks-sql, B1
> **Type:** documentation

## Summary

Three SQL warehouse types exist — Serverless, Pro, and Classic — differentiated by which performance features they support and where compute runs. Serverless is recommended for most workloads and is the only type with Intelligent Workload Management. Pro and Classic run compute in the customer's AWS account and take ~4 minutes to start vs 2–6 seconds for serverless. No SQL warehouse type supports credential passthrough; Unity Catalog is the required data governance layer.

## Key points

- **Three types**: Serverless > Pro > Classic (in descending capability order).
- **Photon**: all three types.
- **Predictive IO**: serverless + pro only.
- **IWM (Intelligent Workload Management)**: serverless only.
- **Startup**: serverless 2–6 s; pro/classic ~4 min.
- **Compute location**: serverless = Databricks-managed; pro/classic = customer's AWS account.
- **No credential passthrough** on any warehouse type — use Unity Catalog.
- **UI default**: serverless (where available); falls back to pro if serverless not in region.
- **API default**: classic.
- **Use pro** only when serverless is unavailable in the region or custom networking is needed (federation/hybrid).
- **Use classic** only for basic entry-level interactive exploration.

## Notes

### Performance capabilities by type

| Feature | Serverless | Pro | Classic |
|---|---|---|---|
| **Photon Engine** | ✓ | ✓ | ✓ |
| **Predictive IO** | ✓ | ✓ | — |
| **Intelligent Workload Management** | ✓ | — | — |

### Feature definitions

**Photon Engine**: "The built-in vectorized query engine on Databricks. It makes your existing SQL and DataFrame API calls faster and reduces your total cost per workload." Present on all warehouse types.

**Predictive IO**: "A suite of features for speeding up selective scan operations in SQL queries. Predictive IO can provide a wide range of speedups." Serverless and pro only.

**Intelligent Workload Management (IWM)**: "A set of features that enhances Databricks SQL Serverless's ability to process large numbers of queries quickly and cost-effectively. Using AI-powered prediction and dynamic management techniques, IWM works to verify that workloads have the right amount of resources quickly." Serverless only. Handles variable query demand, queuing, and rapid autoscaling.

### Serverless SQL warehouses

"Using the Databricks serverless architecture, a serverless SQL warehouse supports all of the performance features of Databricks SQL."

Compute runs in Databricks-managed infrastructure (not the customer's account). Startup: **2–6 seconds**.

"Choose a serverless SQL warehouse for the best startup performance, the most efficient IO, smarter handling of query demand that varies greatly over time, and rapid autoscaling when query queuing occurs."

**Best for**: ETL, business intelligence, exploratory analysis, workloads with variable query demand.

### Pro SQL warehouses

"A pro SQL warehouse supports Photon and Predictive IO, but does not support Intelligent Workload Management."

Compute runs in **customer's AWS account**. Startup: **~4 minutes**.

**Use pro when**:

- Serverless SQL warehouses are not available in the workspace region.
- Custom networking required: "You have custom-defined networking and want to connect to databases in your network in the cloud or on-premises for federation or a hybrid-type architecture."

### Classic SQL warehouses

"A classic SQL warehouse supports Photon but does not support Predictive IO or Intelligent Workload Management."

Compute runs in **customer's AWS account**. Startup: **~4 minutes**.

"Use a classic SQL warehouse to run interactive queries for data exploration with entry-level performance and Databricks SQL features."

Entry-level choice — only Photon, slowest startup, no IWM or Predictive IO.

### Defaults by surface

| Surface | Default when serverless available | Default when serverless unavailable |
|---|---|---|
| UI | Serverless | Pro |
| API | Classic | Classic |

> 💡 API defaulting to Classic is a common gotcha — explicitly set the warehouse type when creating via API if you want serverless or pro.

### Credential passthrough

"SQL warehouses do not support credential passthrough. Databricks recommends using Unity Catalog for data governance."

Applies to all three types. Unity Catalog is the governance layer for SQL warehouse data access.

## Open questions

- ❓ What are the exact pricing differences between serverless, pro, and classic (DBU rates)?
- ❓ What specific operations does Predictive IO accelerate beyond "selective scan operations"?

## Related sources

- [[sql-warehouse-overview]] — landing page; what SQL warehouses are, Starter Warehouse, auto-start.
- [[serverless-notebooks]], [[serverless-jobs]], [[serverless-pipelines]] — serverless for classic compute; separate from serverless SQL warehouses.
- [[classic-compute-overview]] — all-purpose/job compute; entirely separate compute type from SQL warehouses.
