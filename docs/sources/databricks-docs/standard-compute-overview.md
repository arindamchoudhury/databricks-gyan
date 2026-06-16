# Standard compute overview

> **Source:** [docs.databricks.com/aws/en/compute/standard-overview](https://docs.databricks.com/aws/en/compute/standard-overview)
> **Added:** 2026-06-16
> **Source updated:** 2025-10-07
> **Tags:** compute, classic-compute, access-modes, standard, lakeguard, multi-user, B1
> **Type:** documentation

## Summary

High-level overview of standard access mode compute. Standard compute is the multi-user shared compute mode — recommended for most workloads. Secured by Databricks Lakeguard. R is not supported; Scala requires DBR 13.3 LTS+ with Unity Catalog. A separate linked page covers the full requirements and limitations.

## Key points

- Standard compute = standard access mode; any permissioned user can attach and run concurrently.
- **Recommended for most workloads**: DE/ETL pipelines, collaborative data science, interactive exploration, cost optimization.
- **Use Dedicated instead** for: RDD APIs, distributed ML requiring privileged access, GPUs, or R.
- **R not supported** on standard compute.
- **Scala**: supported on DBR 13.3 LTS+ with Unity Catalog only.
- **Auto mode default**: resolves to Standard unless ML runtime or DBR < 14.3 is selected (then Dedicated).
- Security isolation provided by **Lakeguard** — separates user code from underlying Spark infrastructure.

## Notes

### What is standard compute

"Standard compute is compute configured with standard access mode. Standard compute resources can be used by any user given permission to do so."

Any number of users can attach and concurrently execute workloads on the same compute resource, enabling cost savings and simplified compute management. Contrast with Dedicated, which is single-user or group-assigned.

### Access mode selection

Configured in **Advanced** section of the compute creation UI. API field: `data_security_mode`.

Default is **Auto**:

- → Standard (unless ML runtime or DBR < 14.3 is selected)
- → Dedicated (if ML runtime or DBR < 14.3)

See [[classic-compute-configure]] for the full access mode configuration details and [[classic-compute-overview]] for permission levels.

### When to use standard vs dedicated

**Standard** — general-purpose shared compute:

- Data engineering and ETL pipelines
- Collaborative data science
- Interactive data exploration
- Cost optimization (multiple users share one resource)

**Dedicated** — when you need:

- RDD APIs
- Distributed ML frameworks requiring privileged machine access
- GPU workloads
- R language

### Language and runtime support

| Language | Support |
|---|---|
| Python | Full — all Databricks Runtime versions |
| SQL | Full — all Databricks Runtime versions |
| Scala | DBR 13.3 LTS+ with Unity Catalog only |
| R | **Not supported** |

### Lakeguard

Standard compute uses **Databricks Lakeguard** for user isolation and data governance. Lakeguard applies advanced code isolation techniques that separate each user's code from the underlying Spark infrastructure, enabling safe multi-user sharing.

## Open questions

- ❓ What are the full requirements and limitations of standard compute? (Separate page linked from source — not yet captured.)

## Related sources

- [[classic-compute-overview]] — permission levels (CAN ATTACH TO etc.) that control who can use standard compute.
- [[classic-compute-configure]] — how to set access mode to Standard in the UI and via API (`data_security_mode`).
- [[serverless-limitations]] — limitations when not using classic compute at all; useful contrast.
