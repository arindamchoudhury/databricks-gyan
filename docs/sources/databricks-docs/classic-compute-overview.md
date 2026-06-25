# Classic compute overview

> **Source:** [docs.databricks.com/aws/en/compute/use-compute](https://docs.databricks.com/aws/en/compute/use-compute)
> **Added:** 2026-06-16
> **Source updated:** 2026-03-25
> **Tags:** compute, classic-compute, access-modes, permissions, clusters, B1
> **Type:** documentation

## Summary

Classic compute covers all-purpose, jobs, and Lakeflow Spark Declarative Pipelines compute resources that you create, configure, and manage yourself. Unlike serverless, these resources are deployed in your cloud provider account. This page is a high-level overview; the compute configuration reference is a separate page.

## Key points

- **Classic ≠ serverless**: classic compute runs in your cloud account; serverless runs in Databricks-managed infrastructure.
- Three classic compute types: **all-purpose**, **jobs**, **pipelines**.
- Four permission levels: CAN ATTACH TO → CAN RESTART → CAN MANAGE → NO PERMISSIONS (cumulative).
- Two access modes: **Standard** (multi-user, formerly "Shared") and **Dedicated** (single user or group, formerly "Single user").
- Workspace admins inherit CAN MANAGE on all compute in the workspace.
- Non-admin users without "Unrestricted cluster creation" entitlement can only use compute they are granted access to or create via assigned policies.

## Notes

### What is classic compute

"Classic compute refers to all-purpose, jobs, and Lakeflow Spark Declarative Pipelines compute resources that you create, configure, and manage for your workloads." Resources are deployed in your cloud provider account — distinct from serverless, which Databricks deploys and manages.

### Access permission levels

Four levels, cumulative (each includes all below it):

| Permission | What it grants |
|---|---|
| **CAN MANAGE** | Edit compute details, permissions, and size. Includes CAN RESTART. |
| **CAN RESTART** | Start, restart, and terminate compute. Includes CAN ATTACH TO. |
| **CAN ATTACH TO** | Attach notebooks; view compute metrics and Spark UI. |
| **NO PERMISSIONS** | No access. |

### Access modes

- **Standard** (formerly "Shared") — any user with CAN ATTACH TO can attach and run workloads concurrently. User workload isolation enforced; no access to lower-level resources.
- **Dedicated** (formerly "Single user") — assigned to a single user or group. Only the assigned user/group can attach.

> 💡 Access mode rename (2025): "Shared" → Standard, "Single user" → Dedicated. See [[ch01-getting-started-with-databricks]] §8 which covers this rename. Standard supports SQL + Python; Dedicated supports ML runtime, RDD, R, Scala.

### Creation permissions

- **Workspace admins** — can create any compute type; automatically inherit CAN MANAGE on all workspace compute.
- **Non-admin + "Unrestricted cluster creation" entitlement** — access all configuration settings when creating compute.
- **Other non-admin users** — can only use compute they are explicitly granted permissions to, or compute they create using **policies** they are assigned.

> 💡 Policies are the mechanism for letting non-admins create compute within guardrails (instance types, autoscaling limits, etc.) without full unrestricted access.

## Open questions

- ❓ How are compute policies configured and assigned?

## Related sources

- [[classic-compute-configure]] — full configuration reference for this compute type: instance types, autoscaling, EBS, Spark config, log delivery.
- [[serverless-notebooks]], [[serverless-jobs]], [[serverless-pipelines]] — the serverless alternative to classic compute; no cloud account deployment, no cluster config.
- [[serverless-limitations]] — limitations that apply when not using classic compute.
- [[ch01-getting-started-with-databricks]] — DCDE-SG Ch 1 §8 covers all-purpose vs job clusters and the access mode rename.
