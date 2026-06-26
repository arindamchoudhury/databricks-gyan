# Classic compute overview

> **Source:** [docs.databricks.com/aws/en/compute/use-compute](https://docs.databricks.com/aws/en/compute/use-compute)
> **Added:** 2026-06-16
> **Source updated:** 2026-03-25
> **Tags:** compute, classic-compute, access-modes, permissions, clusters, B1
> **Type:** documentation

> "Classic compute refers to all-purpose, jobs, and Lakeflow Spark Declarative Pipelines compute resources that you create, configure, and manage for your workloads."

Unlike serverless, classic compute is deployed in **your cloud provider account** — you create, configure, and manage it. The three classic compute types are **all-purpose**, **jobs**, and **pipelines**. This page is the high-level overview; the configuration reference is [[classic-compute-configure]].

## Access permission levels

Four levels, cumulative (each includes all below it):

| Permission | What it grants |
|---|---|
| **CAN MANAGE** | Edit compute details, permissions, and size. Includes CAN RESTART. |
| **CAN RESTART** | Start, restart, and terminate compute. Includes CAN ATTACH TO. |
| **CAN ATTACH TO** | Attach notebooks; view compute metrics and Spark UI. |
| **NO PERMISSIONS** | No access. |

## Access modes

- **Standard** (formerly "Shared") — any user with CAN ATTACH TO can attach and run workloads concurrently, with user-workload isolation and no access to lower-level resources. Supports SQL + Python.
- **Dedicated** (formerly "Single user") — assigned to a single user or group; only they can attach. Supports ML runtime, RDD, R, Scala.

> 💡 Access-mode rename (2025): "Shared" → Standard, "Single user" → Dedicated (see [[ch01-getting-started-with-databricks]] §8).

## Creation permissions

- **Workspace admins** — can create any compute type and automatically inherit CAN MANAGE on all workspace compute.
- **Non-admin + "Unrestricted cluster creation" entitlement** — access all configuration settings when creating compute.
- **Other non-admin users** — can only use compute they're explicitly granted, or compute they create using **policies** they're assigned (the mechanism for letting non-admins create compute within guardrails — instance types, autoscaling limits — without full unrestricted access).

Related: [[classic-compute-configure]], [[serverless-notebooks]], [[serverless-jobs]], [[serverless-pipelines]], [[serverless-limitations]], [[ch01-getting-started-with-databricks]].
