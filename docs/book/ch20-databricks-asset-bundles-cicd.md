# Chapter 20: Declarative Automation Bundles (DABs) & CI/CD

> 🚧 **Stub.** This chapter is not yet written. It holds **parked material** relocated from Ch 1 so nothing is lost — fold it into the full chapter when topic **A5** is completed.

## Parked: the Databricks CLI (auth, profiles, targets)

DABs are CLI-driven — every `bundle validate / deploy / run` goes through the `databricks` CLI authenticating against a profile. This foundational material was moved here from Ch 1, which now only mentions the CLI in passing.

### The CLI binary

The current CLI is the Go-based binary from [github.com/databricks/cli](https://github.com/databricks/cli) — **not** the legacy `databricks-cli` pip package (deprecated Oct 2023). Mixing the two is a common setup error.

```bash
# Install
winget install Databricks.DatabricksCLI            # Windows
brew tap databricks/tap && brew install databricks   # macOS / Linux
```

### Authentication (OAuth U2M)

```bash
# OAuth user-to-machine — opens a browser to authorise
databricks auth login --host https://<workspace>.cloud.databricks.com
```

Workspace URL by cloud:

| Cloud | Workspace URL |
|-------|--------------|
| AWS (incl. Free Edition) | `https://<workspace>.cloud.databricks.com` |
| Azure | `https://<workspace>.azuredatabricks.net` |
| GCP | `https://<workspace>.gcp.databricks.com` |

Use `databricks configure --token` only if the workspace doesn't support OAuth (PAT-based fallback). For CI/CD, prefer a **service principal** with OAuth M2M rather than a user token — covered in the CI/CD section when written.

### Profiles — `~/.databrickscfg`

Each `auth login` saves a **named profile** to `~/.databrickscfg`. Commands without `-p` use the `DEFAULT` profile — if that profile is stale or points at a different workspace, authentication silently fails against the wrong target.

```bash
databricks auth profiles
# DEFAULT        https://dbc-....cloud.databricks.com   NO    ← stale
# my-workspace   https://dbc-....cloud.databricks.com   YES
```

- Pass `-p <profile>` on any command to target a specific profile explicitly.
- To make a workspace the default, re-run `databricks auth login` and accept `DEFAULT` as the profile name.

> 💡 DABs bind a profile per **target** (`dev`, `staging`, `prod`) in `databricks.yml`, so profile hygiene is the foundation for multi-environment deploys — the heart of this chapter.

## To write (full chapter)

- `databricks.yml` structure, `resources/` YAML (jobs, pipelines, dashboards)
- Targets, variables, and per-environment overrides
- `bundle validate` → `bundle deploy --target <t>` → `bundle run`
- Service-principal auth (OAuth M2M) for CI
- GitHub Actions / Azure DevOps pipeline example
