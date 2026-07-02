# Disable access to legacy features in new workspaces

> **Source:** [docs.databricks.com/aws/en/admin/account-settings/legacy-features](https://docs.databricks.com/aws/en/admin/account-settings/legacy-features)
> **Added:** 2026-07-02
> **Source updated:** 2026-04-22
> **Tags:** administration, unity-catalog, dbfs, hive-metastore, no-isolation-clusters, legacy, account-settings, B1
> **Type:** documentation

> 📌 **2026-09-30 account-wide rollout.** Databricks emailed account admins (2026-07-02) that starting **September 30, 2026**, *every* account — not just ones created after Dec 19, 2025 — gets this behavior by default for newly created workspaces. See the callout at the bottom for what's changing and what isn't.

> NOTE
>
> This setting is not available for accounts created after December 19, 2025. Accounts created after this date won't have access to legacy features by default.

This page describes how to use the **Disable legacy features** account setting so new workspaces in your account are provisioned without access to legacy features.

## What this setting disables

In all new workspaces in the account:

- DBFS root and mounts
- Hive Metastore
- No-isolation shared clusters
- Databricks Runtime versions prior to 13.3 LTS

Workspace admins can use workspace-level settings to disable legacy features in existing workspaces — or to re-enable them in new workspaces if needed. See "Manage legacy features at the workspace level" below.

## Before you begin

If your organization uses workspace deployment automation that depends on these legacy features, this setting could break your automation. Before disabling legacy features at the account level, adjust any scripts or internal processes for workspace creation that use DBFS root, DBFS mounts, or the Hive Metastore.

## Disable legacy features in your account

1. In the account console, click **Settings**.
2. Click the **Feature enablement** tab.
3. Set **Disable legacy features** to **Disabled**: legacy access features will not be available in new workspaces.

The setting can take up to five minutes to take effect.

## Manage legacy features at the workspace level

Databricks recommends disabling legacy features at the account level — it ensures new workspaces are created without the ability to use the legacy features by default.

If needed, a workspace admin can enable or disable these legacy features at the workspace level, even if the account-level setting is set to Disabled.

The following workspace-level settings manage legacy features in existing workspaces:

- Disable DBFS root and mounts
- Disable access to the Hive metastore used by your Databricks workspace
- Enforce user isolation cluster types on a workspace

> ⚠️ **No-isolation clusters are a special case.** No Isolation shared clusters do not respect the legacy Hive metastore disablement setting. To stop users creating/using them, enable **Enforce User Isolation** for the workspace separately.

## 2026-09-30 account-wide rollout (customer email, 2026-07-02)

Databricks account-team email announced this cutover expands to **all accounts** — including ones created before Dec 19, 2025 that still default to legacy access — for workspaces **created on or after September 30, 2026**. Existing workspaces and their workloads are unaffected; this only changes the default for new-workspace provisioning.

**What's changing** for new workspaces from that date: no DBFS root, no DBFS mounts, no Hive Metastore, no no-isolation clusters, no DBR versions before 13.3 LTS.

**What's NOT changing** — the `dbfs:` URI scheme itself keeps working for non-legacy paths:

- **Unity Catalog Volumes** — still reachable via `dbfs:/Volumes/...` and the POSIX-style `/Volumes/...` path.
- **System paths** — `dbfs:/databricks-datasets/` and other read-only Databricks-provided data stay accessible.
- **Internal workspace system data** — notebook revisions, job run details, command results, Spark logs (Databricks-generated, not user DBFS root data).

**Recommended actions:**

- Update CI/CD and workspace-creation automation that assumes DBFS root, DBFS mounts, or Hive Metastore are present.
- Set a metastore to **auto-assign** for every region you deploy workspaces in — otherwise a metastore must be attached manually after provisioning.
- Before migrating existing workflows into a post-cutover new workspace, confirm they don't depend on these legacy features or on DBR < 13.3 LTS.
- Existing workspaces aren't forced to change, but Databricks recommends migrating to Unity Catalog everywhere and proactively disabling DBFS root/mounts and Hive Metastore access using the workspace-level settings above.
- Test the new default early by turning on **Disable legacy features** (this page) in the account console before the September 30, 2026 deadline.

---
Related: [[high-level-architecture]] — "DBFS root/mounts are a deprecated pattern" is the summary line this note gives the full mechanics for; [[classic-compute-overview]] — no-isolation is one of the classic access-mode options this setting can retire.
