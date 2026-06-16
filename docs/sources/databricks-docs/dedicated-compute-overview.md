# Dedicated compute overview

> **Source:** [docs.databricks.com/aws/en/compute/dedicated-overview](https://docs.databricks.com/aws/en/compute/dedicated-overview)
> **Added:** 2026-06-16
> **Source updated:** 2026-06-11
> **Tags:** compute, classic-compute, access-modes, dedicated, single-user, RDD, GPU, R, B1
> **Type:** documentation

## Summary

High-level overview of dedicated access mode compute. Dedicated compute is single-user or single-group compute — needed specifically when a workload requires RDD APIs, GPUs, R, or privileged machine access. For everything else, standard compute is cheaper and simpler. Group assignment is Public Preview. A separate linked page covers full requirements and limitations.

## Key points

- Dedicated compute = only the assigned user or group can use it (no multi-user sharing).
- **Four reasons to choose dedicated over standard**: RDD APIs, GPU instances, R language, privileged machine access.
- **Group assignment** (single group, Public Preview): shared access within one group — not full multi-user like standard.
- **Fine-grain access control** requires DBR 15.4 LTS+ *and* serverless compute enablement.
- Auto mode defaults to Dedicated when ML runtime or DBR < 14.3 is selected.
- For all other workloads, use standard — better cost efficiency, simpler management.

## Notes

### What is dedicated compute

"Dedicated compute is compute configured with dedicated access mode. This means the compute resource can only be used by the single user or group assigned to it."

Contrast with [[standard-compute-overview]] — standard allows any permissioned user to attach concurrently; dedicated locks the resource to one principal.

### Access mode selection

Configured in **Advanced** section during compute creation. API field: `data_security_mode`.

Default is **Auto**: resolves to Standard unless ML runtime or DBR < 14.3 is selected, in which case Dedicated is used. See [[classic-compute-configure]] for configuration details.

### When to use dedicated compute

Use dedicated *only* when you need one of:

| Reason | Detail |
|---|---|
| **RDD APIs** | Direct access to Spark's Resilient Distributed Dataset API layer |
| **GPU instances** | GPU-accelerated compute for deep learning, distributed ML |
| **R language** | R is not supported on standard compute at all |
| **Privileged machine access** | Lower-level system resource access not available on standard |

All other workloads → use standard compute for cost efficiency and simplified management.

### User and group assignment

Two assignment types:

- **Single user** — exclusive access for one user only.
- **Single group** *(Public Preview)* — shared access within one group. Only one group can be assigned; not equivalent to standard's open multi-user model.

### Fine-grain access control

Fine-grain access control on dedicated compute requires:

1. Databricks Runtime **15.4 LTS or above**
2. **Serverless compute enablement** in the workspace

## Open questions

- ❓ What are the full requirements and limitations of dedicated compute? (Separate page linked from source — not yet captured.)
- ❓ What specific capabilities does group access for dedicated compute unlock vs standard compute? (Separate group-access page not yet captured.)

## Related sources

- [[standard-compute-overview]] — the counterpart access mode; multi-user shared compute. Use standard unless you specifically need RDD/GPU/R/privileged access.
- [[classic-compute-configure]] — how to set `data_security_mode` to Dedicated in the UI and API.
- [[classic-compute-overview]] — permission levels that control who can attach to dedicated compute.
- [[serverless-limitations]] — serverless compute also lacks RDD and R; dedicated classic compute is the alternative.
