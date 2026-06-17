# Compute pools (instance pools)

> **Source:** [docs.databricks.com/aws/en/compute/pool-index](https://docs.databricks.com/aws/en/compute/pool-index)
> **Added:** 2026-06-16
> **Source updated:** 2024-10-29
> **Tags:** compute, classic-compute, pools, autoscaling, cost, B1
> **Type:** documentation

## Summary

Instance pools are sets of idle, pre-warmed VMs that reduce cluster start and autoscaling times. Databricks does not charge DBUs for idle pool instances, but the cloud provider does. Creation requires an entitlement (admins by default); non-admins need CLI/API. Three permission levels govern who can attach to or manage a pool. Deleting a pool is irreversible and breaks terminated clusters that reference it.

## Key points

- **Idle billing**: no DBU charges; cloud provider VM billing still applies.
- **Creation entitlement**: "Allow pool creation" — admins by default; non-admins must use CLI/API (no UI button).
- **Attachment**: choose pool from Driver Type or Worker Type dropdown; API fields `driver_instance_pool_id` / `instance_pool_id`.
- **Three permission levels**: NO PERMISSIONS, CAN ATTACH TO, CAN MANAGE.
- **Never use spot pool as driver** — driver is always on-demand; spot pool for driver risks reclamation.
- **Autoscaling constraints**: pool idle count must ≥ min compute size, and max compute size must ≤ pool max capacity (see [[classic-compute-configure]]).
- **Tags on pool-launched compute** only appear in DBU usage reports — not propagated to cloud resources.
- **Deletion is irreversible**: running clusters lose scale-up ability; terminated clusters fail to restart.

## Notes

### What pools are

"Databricks pools are a set of idle, ready-to-use instances. When cluster nodes are created using the idle instances, cluster start and auto-scaling times are reduced."

Pre-warmed VMs sit in the pool until a cluster needs them. At that point startup time is cut to the time needed to install the Databricks runtime on the idle VM rather than provisioning a fresh instance from scratch.

### Billing

"Databricks does not charge DBUs while instances are idle in the pool. Instance provider billing does apply."

Idle pool VMs accrue cloud compute costs (EC2, GCE, Azure VM) regardless of whether any cluster is using them. The Databricks DBU charge only starts when an instance leaves the pool and joins a running cluster.

### Creating a pool

**Entitlement required**: "Allow pool creation". By default only workspace admins have it.

"Non-admin users with the Allow pool creation entitlement can only create pools using the CLI or API. The **Create Pool** button in the UI is available only to workspace admins."

UI path: **Compute** → **Pools** tab → **Create Pool** → configure → **Create**.

### Attaching a cluster to a pool

**UI**: select the pool from the **Driver Type** or **Worker Type** dropdown when configuring the cluster.

**API**: set `driver_instance_pool_id` for the driver node and `instance_pool_id` for the worker nodes in the cluster create/edit payload.

> ⚠️ Never attach a spot-instance pool as the driver type — the driver node must always be on-demand. See [[classic-compute-configure]] §driver node.

**Autoscaling with pools** (from [[classic-compute-configure]]):

- Pool's idle instance count must be ≥ the compute's minimum workers, or startup time reverts to non-pool speed (pool benefit is lost).
- Max compute size must be ≤ pool's max capacity, or compute creation fails.

### Pool permissions

Three levels:

| Permission | What it grants |
|---|---|
| **CAN MANAGE** | Configure pool settings and permissions |
| **CAN ATTACH TO** | Attach clusters to the pool |
| **NO PERMISSIONS** | No access |

To configure permissions on a pool you must have CAN MANAGE on it. Permissions manageable via workspace UI, Permissions API, or Terraform provider.

### Deleting a pool

Deletion terminates all idle instances in the pool and removes its configuration. **Cannot be undone.**

Effects on attached clusters:

- **Running clusters**: continue to run but cannot allocate pool instances during resize or autoscale up.
- **Terminated clusters**: will fail to start (no pool to draw from).

## Open questions

- ❓ What configuration options are available when creating a pool (min idle instances, max capacity, idle instance auto-termination, instance type, preloaded runtime)? Detailed pool config not on this page — likely in a separate reference or API docs.

## Related sources

- [[classic-compute-configure]] — autoscaling-with-pools constraints (idle count vs min workers, max size vs pool capacity); driver-type spot warning; tag propagation caveat.
- [[classic-compute-overview]] — permission model for compute; pools have their own parallel permission system.
