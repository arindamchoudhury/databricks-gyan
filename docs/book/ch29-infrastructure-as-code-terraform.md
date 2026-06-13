# Chapter 29 — Infrastructure as Code with Terraform

> **Level:** Expert · **Topic code:** E7
>
> **After this chapter you will be able to:**
> 
> - Choose the right workspace topology for your organisation (monolithic, environment-separated, domain-separated, hub-spoke)
> - Design a Unity Catalog namespace that scales — catalog-per-env, catalog-per-domain, or hybrid
> - Apply the correct isolation mechanism — workspace isolation, catalog isolation, workspace-catalog binding, row filters, column masking, or dynamic views
> - Separate deployment stages with per-stage admin delegation; decide what constitutes a "stage" boundary
> - Design multi-BU data governance using distributed or centralized publishing patterns
> - Provision a Databricks workspace on AWS entirely from Terraform using the `databricks_mws_*` resource family
> - Set up Unity Catalog — metastore, catalogs, schemas, and grants — programmatically
> - Organise Terraform code into layered modules with separate state files
> - Drive multi-environment deployments from config rather than copy-pasted HCL
> - Scale with Terragrunt stacks and units
> - Harden a deployment using the Security Reference Architecture (Private Link, CMK, no-public-IP, SAT)
> - Explain exactly which layer of your stack belongs to Terraform versus DABs — and why the boundary matters

---

## Why this matters in production

A team clicks its way through the Databricks UI to stand up workspace number one. The second workspace is mostly right. By workspace ten, nobody is sure whether cluster policies match, whether the Unity Catalog storage credential is pointing at the right S3 bucket, or whether the dev environment has the same group structure as prod. A security audit arrives and the question "what does this workspace actually contain?" has no good answer.

The failure mode is not laziness — it is the natural outcome of treating cloud infrastructure as a set of interactive forms rather than a set of declarations. Terraform fixes this by making the desired state of every Databricks resource explicit, reviewable, and reproducible. But Terraform is a tool with a scope: it owns the platform layer. Understanding where that scope ends — and where Declarative Automation Bundles (DABs, covered in Ch 20) begin — is the foundational architectural judgment this chapter is about.

---

## Workspace topology decisions

Before writing a line of Terraform, you need to decide how many workspaces you need and what each one owns. This decision drives everything else: how many VPCs you provision, how Unity Catalog is structured, and how teams are isolated from each other.

### The four patterns

```mermaid
graph TD
    subgraph MONO["1. Monolithic"]
        W1[one workspace\neverything in it]
    end

    subgraph ENV["2. Environment-separated (most common)"]
        W2[dev workspace]
        W3[staging workspace]
        W4[prod workspace]
    end

    subgraph DOMAIN["3. Domain-separated"]
        W5[platform workspace\nshared infra + UC admin]
        W6[marketing workspace]
        W7[finance workspace]
        W8[data-science workspace]
    end

    subgraph HUB["4. Hub-spoke"]
        W9[hub workspace\nUC metastore owner\nshared compute]
        W10[spoke: domain A]
        W11[spoke: domain B]
        W9 --> W10
        W9 --> W11
    end
```

| Pattern | Use when | Trade-off |
|---|---|---|
| **Monolithic** | Prototype, single team, ≤ 10 engineers | Simple to manage; no isolation at all |
| **Environment-separated** | Standard enterprise setup; dev/staging/prod data must not mix | Most common; each env has its own VPC and cost profile |
| **Domain-separated** | Large org with distinct business units each owning their data | Strong team autonomy; cross-domain queries need UC grants |
| **Hub-spoke** | Platform team owns infrastructure; domain teams own data; shared metastore | Cleanest governance; most complex to provision |

### How Unity Catalog changes the calculus

Before Unity Catalog, workspace = isolation boundary. Every workspace had its own Hive metastore with no cross-workspace sharing. You needed separate workspaces for dev/prod data because there was no other way to isolate them.

With Unity Catalog, the catalog is the isolation boundary. One workspace can hold both `dev_catalog` and `prod_catalog` with completely different grants. This collapses many multi-workspace designs into a single workspace — unless you need compute isolation (workspaces have separate cluster pools) or billing isolation (separate AWS accounts).

### Decision guide

```
Do you need compute isolation?    → separate workspaces
(prod jobs must not share resources with dev)

Do you need billing isolation?    → separate workspaces (ideally separate AWS accounts)

Do you need regulatory isolation? → separate workspaces (HIPAA/PCI scope boundaries)

Do you just need data isolation?  → Unity Catalog catalogs within one workspace
```

---

## Environment separation strategies

"Dev, staging, prod" is the goal. The question is what mechanism enforces the boundary. Three options exist, with very different isolation strength and operational cost.

### Option 1 — Workspace per environment (strongest)

```
dev workspace     → dev VPC, dev IAM roles, dev S3 buckets
staging workspace → staging VPC, staging IAM roles, staging S3 buckets
prod workspace    → prod VPC, prod IAM roles, prod S3 buckets
```

A dev engineer cannot access prod data by accident — they don't have credentials to the prod workspace. Prod cluster failures don't affect dev capacity.

**Cost:** Three VPCs, three NAT gateways (~$35/month each), three sets of MWS resources, three Unity Catalog metastore assignments. Higher Terraform surface area.

**When to use:** When "a dev job consuming all cluster capacity" or "a bug in dev schema migration deleting prod data" are risks you cannot accept.

### Option 2 — Catalog per environment (recommended default)

One workspace, multiple catalogs:

```
workspace: prod-workspace
Unity Catalog
├── dev_main      ← dev data, dev grants (data-engineers group only)
├── staging_main  ← staging data, staging grants
└── prod_main     ← prod data, prod grants (read-only for most users)
```

DABs targets each catalog by name:
```yaml
targets:
  dev:
    variables:
      catalog: dev_main
  prod:
    variables:
      catalog: prod_main
```

**Cost:** One VPC, one workspace. Prod and dev share the cluster pool — a runaway dev job can consume prod capacity.

**When to use:** Most teams. Provides strong data isolation at reasonable cost.

### Option 3 — Schema per environment (weakest)

One catalog, environment-prefixed schemas:

```
catalog: main
├── dev_bronze   dev_silver   dev_gold
└── prod_bronze  prod_silver  prod_gold
```

**Cost:** Lowest. Almost no infrastructure change between envs.

**Risk:** Schema-level grants are easy to misconfigure. One wrong `GRANT MODIFY ON SCHEMA prod_gold TO data-engineers` and dev engineers can write to prod.

**When to use:** Only for very small teams where one person owns both dev and prod — or for demos. Do not use in production for anything sensitive.

### Comparison

| | Workspace per env | Catalog per env | Schema per env |
|---|---|---|---|
| Data isolation | ✅ Complete | ✅ Strong | ⚠️ Weak |
| Compute isolation | ✅ Yes | ❌ Shared pool | ❌ Shared pool |
| Blast radius (misconfig) | Workspace-scoped | Catalog-scoped | Any table in workspace |
| Monthly infra cost delta | +~$200/env | ~$0/env | ~$0/env |
| Terraform complexity | High | Medium | Low |

---

## Unity Catalog topology

The Unity Catalog three-level namespace (`catalog.schema.table`) gives you two axes to design along: the catalog boundary and the schema boundary. Getting this wrong is expensive to fix later — moving tables between catalogs requires copying data.

### Catalog design patterns

**Pattern A — Catalog per environment**
```
dev_main.bronze.raw_events
prod_main.bronze.raw_events
```
Clean environment isolation. Easy to copy data from dev → prod. Natural fit with the catalog-per-environment deployment strategy.

**Pattern B — Catalog per domain**
```
marketing.bronze.campaign_events
finance.silver.revenue
platform.gold.company_metrics
```
Each business domain owns its catalog. Strong ownership: the marketing team controls grants on `marketing.*`. Cross-domain access requires explicit grants from the catalog owner. Unity Catalog lineage tracks cross-catalog data flows.

**Pattern C — Catalog per team**
```
team_analytics.experiments.*
team_ml.models.*
team_platform.shared.*
```
Fine-grained autonomy. Works well when teams have independent data contracts. Can sprawl — 20 teams = 20 catalogs.

**Pattern D — Hybrid (recommended for most enterprises)**
```
prod_marketing.bronze/silver/gold
prod_finance.bronze/silver/gold
prod_platform.bronze/silver/gold
dev_marketing.bronze/silver/gold   ← dev counterpart
```
Domain ownership + environment isolation in the catalog name. Clean grants: prod users read `prod_*`, dev users write `dev_*`. The `platform` catalog holds shared reference data that all other domains read.

### Schema as the medallion layer

Regardless of catalog pattern, schemas map to medallion layers:

```
{catalog}.bronze   ← raw, immutable, append-only
{catalog}.silver   ← cleaned, validated, merged
{catalog}.gold     ← aggregated, business-ready
{catalog}.sandbox  ← ad-hoc experiments, no SLA (optional)
```

The `sandbox` schema pattern is underused: it gives engineers a designated space for exploration without polluting production schemas, with a weekly `DROP TABLE` scheduled job to clean up.

### Metastore topology

One Unity Catalog metastore per AWS region. Multiple workspaces in the same region share it:

```
us-east-1 metastore
├── prod workspace   → assigned to metastore
├── staging workspace → assigned to metastore
└── dev workspace    → assigned to metastore
```

All three workspaces see the same catalogs. Access control is enforced by grants — a prod-workspace user cannot see `dev_main` unless explicitly granted `USE_CATALOG`. This is the key advantage: shared governance plane, isolated access.

### Data publishing patterns (multi-BU)

In organisations with multiple business units sharing a metastore, two patterns govern how data flows between teams:

**Option 1 — Distributed publishing.** Each BU owns its catalogs (`bu1_prd`, `bu2_prd`) and publishes data directly. Other BUs access data via UC grants on specific schemas and tables. The central platform team provides workspace blueprints and creates environments for BUs, but each BU controls its own catalog's ACLs. Best when BU autonomy matters more than uniform quality standards.

**Option 2 — Centralized publishing.** BUs produce data to their own staging catalogs, then request the central team to publish to a central catalog (e.g., `bu1_published`). The central team enforces naming conventions, data quality checks, and sets the ACLs. All enterprise consumers go through the central catalog. Best for regulated industries or when a data stewardship team must sign off on all published data.

Naming convention in both patterns: `{bu}_{env}` catalogs (`central_prd`, `bu1_dev`, `bu1_stg`, `bu1_prd`) make ownership and stage obvious in every `SELECT` statement.

For **cross-region** multi-BU setups, **Databricks-to-Databricks OpenSharing** (the open protocol formerly called Delta Sharing, renamed June 2026) links metastores across AWS regions. Region 2 BUs see shared tables from region 1's metastore as read-only views in their own metastore — no data copy required. An alternative is Lakehouse Federation for heterogeneous sources. Both are separate topics from workspace provisioning but must be planned in the UC topology design.

---

## Unity Catalog isolation options

Unity Catalog provides four mechanisms to control what data a user sees. They operate at different granularities and suit different scenarios.

### 1. Catalog isolation (coarsest)

The user must be granted `USE_CATALOG` to see a catalog at all. Without it, the catalog does not appear in `SHOW CATALOGS`. This is the primary isolation mechanism for environment separation.

```sql
-- prod-workspace user cannot see dev_main unless granted:
GRANT USE_CATALOG ON CATALOG dev_main TO `data-engineers`;
```

Use for: environment boundaries, domain boundaries, any "this user group should not see this data at all" requirement.

### 2. Row filters

Filter rows a user sees based on their identity or group membership. The filter is a SQL function applied transparently at query time — the user does not know rows are being hidden.

```sql
-- Create a filter function
CREATE FUNCTION main.silver.customer_region_filter(region STRING)
  RETURN is_member('emea-team') = TRUE OR is_member('region-' || region) = TRUE;

-- Attach it to a table
ALTER TABLE main.silver.customers
  SET ROW FILTER main.silver.customer_region_filter ON (region);
```

Now members of `emea-team` see all rows; everyone else sees only rows for regions whose group they belong to — a user in the `region-US` group sees only `US` rows. Note there is no built-in `current_region()` function: mapping a user to their region is your own logic. Here it's a `region-<value>` group-naming convention, but a lookup table joined inside the function works equally well. The function evaluates per row and can be as complex as needed.

Use for: multi-tenant data in a shared table, regional data residency requirements, row-level RBAC without duplicating tables.

### 3. Column masking

Hide or transform sensitive column values based on user identity. Non-privileged users see a masked value (e.g., `****-****-****-1234`) while privileged users see the real value.

```sql
-- Create a masking function
CREATE FUNCTION main.silver.mask_pii(pii_value STRING)
  RETURN CASE
    WHEN is_member('pii-allowed') THEN pii_value
    ELSE regexp_replace(pii_value, '.', '*')
  END;

-- Attach to a column
ALTER TABLE main.silver.customers
  ALTER COLUMN email
  SET MASK main.silver.mask_pii;
```

Use for: PII masking (email, SSN, credit card), HIPAA/GDPR compliance, showing aggregate-only users obfuscated values while analysts with data-steward role see real values.

### 4. Dynamic views (pre-UC pattern, still valid)

Before row filters and column masks existed, teams used views to enforce access control. Still valid for complex logic that filter functions can't express:

```sql
CREATE VIEW main.silver.customers_safe AS
SELECT
  customer_id,
  region,
  CASE WHEN is_member('pii-allowed') THEN email ELSE 'REDACTED' END AS email,
  CASE WHEN is_member('pii-allowed') THEN phone ELSE 'REDACTED' END AS phone
FROM main.silver.customers_raw
WHERE is_member('emea-team') = TRUE OR region = 'GLOBAL';
```

Grant on the view, not the underlying table. Use when you need JOIN-based filtering (e.g., a user can only see rows referenced in an access-control table they own).

### 5. Workspace-catalog binding

By default every catalog in a metastore is visible to all workspaces assigned to that metastore (subject to grants). Setting `isolation_mode = "ISOLATED"` restricts a catalog to explicitly bound workspaces only — it stops appearing in `SHOW CATALOGS` from any *other* workspace. When you set ISOLATED via Terraform, the catalog is automatically bound to the workspace it was created from; every additional workspace must be bound explicitly with `databricks_workspace_binding`. This is stricter than catalog grants alone: even a metastore admin cannot discover the catalog from an unbound workspace.

```hcl
resource "databricks_catalog" "prod" {
  provider       = databricks.workspace
  name           = "prod_main"
  isolation_mode = "ISOLATED"   # only bound workspaces can see it (creating workspace auto-bound)
}

# Bind only to the prod workspace
resource "databricks_workspace_binding" "prod_to_prod_ws" {
  provider       = databricks.workspace
  securable_name = databricks_catalog.prod.name
  workspace_id   = var.prod_workspace_id
}

# Bind dev catalog only to the dev workspace
resource "databricks_workspace_binding" "dev_to_dev_ws" {
  provider       = databricks.workspace
  securable_name = databricks_catalog.dev.name
  workspace_id   = var.dev_workspace_id
}
```

The same `isolation_mode = "ISOLATED"` flag and `databricks_workspace_binding` resource apply to storage credentials and external locations. Manage all bindings from a single designated management workspace — typically the same workspace that owns the metastore.

This pattern pairs naturally with the workspace-per-env topology: the prod workspace can only see `prod_main`; dev engineers in the dev workspace cannot accidentally `SELECT *` from a prod table because `prod_main` is not bound to their workspace.

### Choosing the right mechanism

```
Need to hide entire catalogs from a group?  → Catalog-level grants
Need to hide rows based on user identity?   → Row filters (preferred) or Dynamic views
Need to mask column values?                 → Column masking
Complex multi-table access logic?           → Dynamic views
Audit trail of who saw what?               → All UC mechanisms log to audit logs
```

Row filters and column masks are preferable to dynamic views for new code: they attach to the table, not a separate object, and they survive `CLONE` and `SELECT *` without accidentally exposing data.

### Isolation option comparison

| Mechanism | Granularity | Performance | Complexity | Notes |
|---|---|---|---|---|
| Catalog grants | Catalog | None | Low | Primary boundary |
| Schema grants | Schema | None | Low | Good for team/medallion separation |
| Row filters | Row | Minor (filter pushed to scan) | Medium | UC native, preferred |
| Column masking | Column | None | Medium | UC native, preferred |
| Dynamic views | Rows + columns | JOIN overhead | High | Pre-UC pattern; still valid for complex logic |
| Workspace-catalog binding | Catalog (workspace visibility) | None | Low | Prevents catalog discovery from unbound workspaces; strongest isolation |

---

## Separation of deployment stages

A "stage" in a Databricks deployment is not just dev/prod — it is a boundary where code and data must be validated before promotion. The right number of stages depends on your risk tolerance and team size.

### The three-stage model (most common)

```mermaid
graph LR
    DEV["dev\n(catalog: dev_main)\nFast iteration\nNo SLA\nSynthetic data"]
    STAGING["staging\n(catalog: staging_main)\nIntegration testing\nProduction-like data\nCI/CD gated"]
    PROD["prod\n(catalog: prod_main)\nApproval required\nReal data\nMonitored"]

    DEV -->|PR + automated tests| STAGING
    STAGING -->|manual approval| PROD
```

What changes at each stage boundary:

| Boundary | What gets validated |
|---|---|
| dev → staging | Unit tests pass, schema contracts match, pipeline runs without error |
| staging → prod | Integration tests pass, data quality checks pass, human approval |

### What "stage" means per layer

| Layer | Stage boundary enforcement |
|---|---|
| Terraform (workspace, VPC) | Different state files; prod requires separate approval gate in CI/CD |
| DABs (jobs, pipelines) | `--target dev/staging/prod` in the bundle; each target has its own catalog and cluster config |
| Unity Catalog (data) | `dev_main` → `staging_main` → `prod_main` catalogs; grants restrict who can write to prod |
| Unity Catalog (admin) | Each env can have a separate catalog admin — dev team has `CREATE_SCHEMA` on `dev_main`, no rights on `prod_main`; prod admin is a service principal used only by CI/CD |
| Cluster policies | Dev: on-demand small clusters allowed; prod: job clusters only, no interactive |

### Data in staging

The hardest staging problem: what data does staging run against? Three approaches:

1. **Anonymised copy of prod** — most realistic; requires a masking pipeline to copy and anonymise prod data into `staging_main`. Expensive to maintain.
2. **Synthetic data** — generated data matching prod schema and statistics. Easier to maintain; may miss edge cases in real data.
3. **Subset of prod (read-only)** — staging pipelines read from `prod_main` bronze (raw, immutable) but write to `staging_main`. Realistic inputs; dangerous if staging jobs mutate prod data.

Option 3 is the most common compromise: staging reads raw prod data (which is append-only and therefore safe to share) but writes to an isolated catalog.

---

## Config-driven scale

Once you have more than two environments or more than one domain, hardcoded HCL becomes unmanageable. Config-driven Terraform replaces repeated blocks with data structures and `for_each`.

### Environments from a map

Instead of copying `environments/dev/` and `environments/prod/` manually, drive both from a single variable:

```hcl
# modules/workspace/variables.tf
variable "environments" {
  type = map(object({
    prefix   = string
    vpc_cidr = string
    private_subnets = list(string)
  }))
  default = {
    dev = {
      prefix          = "dbx-dev"
      vpc_cidr        = "10.0.0.0/16"
      private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
    }
    prod = {
      prefix          = "dbx-prod"
      vpc_cidr        = "10.1.0.0/16"
      private_subnets = ["10.1.1.0/24", "10.1.2.0/24"]
    }
  }
}
```

This works well for networking and workspace provisioning. It does **not** work for resources that require separate state files — each environment's state must be isolated. The config-driven pattern shines at the module level; state separation still requires separate root modules (or Terragrunt units).

### Catalogs and grants from a map

```hcl
locals {
  catalogs = {
    dev_main = {
      schemas = ["bronze", "silver", "gold"]
      grants = {
        "data-engineers" = ["USE_CATALOG", "CREATE_SCHEMA", "CREATE_TABLE"]
        "data-analysts"  = ["USE_CATALOG"]
      }
    }
    prod_main = {
      schemas = ["bronze", "silver", "gold"]
      grants = {
        "data-engineers" = ["USE_CATALOG"]
        "data-analysts"  = ["USE_CATALOG"]
        "data-stewards"  = ["USE_CATALOG", "CREATE_SCHEMA", "CREATE_TABLE"]
      }
    }
  }
}

resource "databricks_catalog" "this" {
  for_each = local.catalogs
  provider = databricks.workspace
  name     = each.key
}

resource "databricks_schema" "this" {
  for_each = {
    for item in flatten([
      for cat, cfg in local.catalogs : [
        for schema in cfg.schemas : {
          key    = "${cat}.${schema}"
          cat    = cat
          schema = schema
        }
      ]
    ]) : item.key => item
  }
  provider     = databricks.workspace
  catalog_name = databricks_catalog.this[each.value.cat].id
  name         = each.value.schema
}
```

### When config-driven becomes too clever

Config-driven scale pays off when you genuinely repeat the same structure many times. It adds cognitive overhead — a new team member reading a `for_each` over a nested map needs to understand the data structure before they can understand what gets created. Draw the line at two levels of nesting. If your locals require three nested `for` expressions to flatten, split into explicit resources instead.

### Beyond HCL: YAML-driven config

For platform teams that provision many workspaces or catalogs on behalf of other teams, the next step is externalising the configuration into YAML files that non-Terraform engineers can edit:

```yaml
# config/workspaces.yaml
workspaces:
  - name: marketing-dev
    env: dev
    vpc_cidr: "10.10.0.0/16"
    catalog: marketing_dev
  - name: marketing-prod
    env: prod
    vpc_cidr: "10.11.0.0/16"
    catalog: marketing_prd
```

```hcl
# main.tf
locals {
  workspaces = yamldecode(file("${path.module}/config/workspaces.yaml")).workspaces
}

module "workspace" {
  for_each = { for ws in local.workspaces : ws.name => ws }
  source   = "../modules/aws-workspace"
  prefix   = each.value.name
  vpc_cidr = each.value.vpc_cidr
}
```

The advantage: a data engineer who wants a new workspace submits a PR editing `workspaces.yaml` rather than writing HCL. CI runs `terraform plan` on the change; a platform engineer reviews and merges. The underlying Terraform complexity is completely hidden. The disadvantage: you now have a custom DSL that teams must learn, and YAML validation errors become Terraform runtime errors. Use `yamldecode` + `can()` to validate required fields early.

### IAM from JSON

The same `jsondecode(file(...))` pattern applies to Databricks identity management. Keeping users, groups, and group membership in a checked-in JSON file makes access changes reviewable as code diffs — an auditor can see exactly who was added or removed and when.

```json
{
  "users": [
    { "user_name": "alice@example.com", "display_name": "Alice" },
    { "user_name": "bob@example.com",   "display_name": "Bob" }
  ],
  "groups": [
    { "name": "admins",         "members": ["alice@example.com"] },
    { "name": "data-engineers", "members": ["alice@example.com", "bob@example.com"] }
  ]
}
```

The corresponding Terraform creates account-level resources via `databricks.mws`:

```hcl
resource "databricks_user" "this" {
  for_each     = { for u in var.iam.users : u.user_name => u }
  provider     = databricks.mws
  user_name    = each.value.user_name
  display_name = each.value.display_name
}

resource "databricks_group" "this" {
  for_each     = { for g in var.iam.groups : g.name => g }
  provider     = databricks.mws
  display_name = each.key
}

resource "databricks_group_member" "this" {
  for_each = {
    for pair in flatten([
      for g in var.iam.groups : [
        for m in g.members : { group = g.name, user = m }
      ]
    ]) : "${pair.group}:${pair.user}" => pair
  }
  provider  = databricks.mws
  group_id  = databricks_group.this[each.value.group].id
  member_id = databricks_user.this[each.value.user].id
}
```

A `workspace_admin_group` variable then drives `databricks_mws_permission_assignment` so the group — not an individual user — holds workspace ADMIN:

```hcl
resource "databricks_mws_permission_assignment" "admin" {
  provider     = databricks.mws
  workspace_id = databricks_mws_workspaces.this.workspace_id
  principal_id = databricks_group.this[var.workspace_admin_group].id
  permissions  = ["ADMIN"]
}
```

**Prefer groups over users for workspace assignment.** Assigning a group means adding a new admin is a JSON edit and a `terraform apply` — no HCL change, no Terraform engineer required. Assigning an individual user means that person leaving the company triggers an emergency Terraform change instead of a routine access review. This distinction matters most when users are managed in an external IdP (Okta, Azure AD) synced via SCIM: group membership is already the IdP's language; Terraform just maps groups to workspace roles.

The `iam.json` file is committed to git — it contains no secrets, only email addresses and group names. The environment module passes it as:

```hcl
iam = jsondecode(file("${path.module}/iam.json"))
```

---

## The two-layer model

Every Databricks IaC deployment has two distinct layers with different owners, different change cadences, and different deployment tools.

```mermaid
graph TD
    subgraph PLATFORM["Platform Layer — Terraform"]
        A[Cloud Infra<br>VPC · Subnets · IAM · S3]
        B[Databricks Workspaces<br>databricks_mws_*]
        C[Unity Catalog<br>Metastore · Catalogs · Grants]
        D[Shared Platform Resources<br>Cluster Policies · SQL Warehouses<br>Groups · Service Principals]
    end

    subgraph APP["Application Layer — DABs"]
        E[Pipelines & Jobs]
        F[Notebooks & Libraries]
        G[Environment Configs<br>dev / staging / prod]
    end

    PLATFORM --> APP
```

**Platform layer (Terraform):** Changes infrequently. Managed by a platform or DevOps team. Requires cloud-provider credentials. Scope: anything that exists before a data engineer runs their first job — networking, workspace provisioning, UC topology, cluster policies, identity management.

**Application layer (DABs):** Changes on every sprint. Managed by data teams. Scope: pipelines, jobs, notebooks, experiment tracking — anything that lives *inside* a workspace and moves between dev/staging/prod. DABs uses `databricks.yml` + `resources/` YAML and deploys via `databricks bundle deploy --target prod`.

The canonical split (from Databricks engineering):

| Use **Terraform** for | Use **DABs** for |
|---|---|
| Workspace provisioning + cloud networking | Lakeflow pipelines and Lakeflow Jobs |
| Unity Catalog: metastore, catalogs, grants | Notebooks, Python libraries, MLflow experiments |
| Cluster policies | Per-project compute configs |
| Shared SQL Warehouses | Workflow schedules and alerts |
| Groups, users, service principals | CI/CD promotion (dev → staging → prod) |
| External locations, storage credentials | — |

> **2026 note:** DABs historically used Terraform internally to manage its state. Databricks is actively migrating this away (`databricks bundle migrate` removes the Terraform dependency). The conceptual split above becomes even cleaner as this migration progresses — but the boundary itself is unchanged.

---

## The Databricks Terraform provider

The `databricks/databricks` provider (>75M downloads, top 5% of all Terraform providers) covers almost every Databricks resource. It runs in two distinct modes, which must never be mixed in the same provider block:

> **Versions as of June 2026:** Databricks provider **1.117.0**, AWS provider **6.50.0** (6.0 GA April 2026 — see the [v6 upgrade guide](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/version-6-upgrade) if migrating from 5.x), Terraform **1.15.6**. The Databricks provider releases roughly weekly; use `~> 1.117` to allow patch and minor updates without crossing a breaking major. The AWS provider constraint `>= 5.76, <7.0` is intentional: it accepts both 5.x and 6.x so teams can migrate at their own pace.

| Mode | Endpoint | `host` value | Used for |
|---|---|---|---|
| **MWS / Account-level** | `accounts.cloud.databricks.com` | `"https://accounts.cloud.databricks.com"` | Workspace provisioning, UC metastore, account-level identity |
| **Workspace-level** | Workspace URL | `"https://<workspace>.cloud.databricks.com"` | Catalogs, grants, cluster policies, SQL warehouses |

The standard pattern uses provider **aliases** to keep both modes available in the same Terraform configuration:

```hcl
terraform {
  required_version = "~> 1.15"

  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.117"   # latest: 1.117.0 (2026-06-03)
    }
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.76, < 7.0"  # spans 5.x and 6.x; AWS provider 6.0 GA April 2026
    }
  }
}

# Account-level (MWS) provider — for workspace provisioning and UC metastore
provider "databricks" {
  alias      = "mws"
  host       = "https://accounts.cloud.databricks.com"
  account_id = var.databricks_account_id
  # Auth: set DATABRICKS_CLIENT_ID and DATABRICKS_CLIENT_SECRET env vars
  # for a service principal, or use profile = "..." for local development
}

# Workspace-level provider — for catalogs, grants, cluster policies, etc.
provider "databricks" {
  alias = "workspace"
  host  = databricks_mws_workspaces.this.workspace_url
}
```

Authentication in CI/CD uses a Databricks service principal (OAuth M2M). Set `DATABRICKS_CLIENT_ID` and `DATABRICKS_CLIENT_SECRET` as environment secrets; the provider picks them up automatically.

---

## Provisioning a workspace on AWS

AWS workspace creation is an **account-level operation**. Every resource in this section uses `provider = databricks.mws` and the MWS endpoint. These resources do not touch workspace internals — they configure the AWS infrastructure that backs the workspace.

### The four required components

```mermaid
flowchart LR
    A[IAM Cross-Account Role<br>aws_iam_role] --> D
    B[S3 Root Bucket<br>aws_s3_bucket] --> D
    C[VPC + Subnets<br>aws_vpc / aws_subnet] --> D
    D[databricks_mws_credentials<br>databricks_mws_storage_configurations<br>databricks_mws_networks<br>databricks_mws_workspaces]
    D --> E[Workspace URL]
```

### Step 1 — Cross-account IAM role

Databricks needs to assume an IAM role in your AWS account to create and manage resources (EC2 instances, security groups, etc.). The Terraform provider supplies data sources that compute the exact trust policy and permission policy for you:

```hcl
# Data source: computes the trust policy Databricks needs to assume this role
data "databricks_aws_assume_role_policy" "this" {
  provider    = databricks.mws
  external_id = var.databricks_account_id
}

# Data source: computes the permissions policy Databricks needs
data "databricks_aws_crossaccount_policy" "this" {
  provider = databricks.mws
}

resource "aws_iam_role" "cross_account" {
  name               = "${var.prefix}-databricks-cross-account"
  assume_role_policy = data.databricks_aws_assume_role_policy.this.json
}

resource "aws_iam_role_policy" "cross_account" {
  name   = "${var.prefix}-databricks-cross-account-policy"
  role   = aws_iam_role.cross_account.id
  policy = data.databricks_aws_crossaccount_policy.this.json
}

# IAM propagation delay: AWS confirms policy attachment before it is globally
# consistent. Without this delay, databricks_mws_credentials validation fails.
resource "time_sleep" "iam_propagation" {
  depends_on      = [aws_iam_role_policy.cross_account]
  create_duration = "20s"
}
```

> **Why `time_sleep`?** AWS confirms IAM policy attachment before the change has propagated globally. Databricks validates the cross-account role immediately when you create `databricks_mws_credentials`. Without a wait, this validation fails with a permissions error even though the policy exists. Twenty seconds is the recommended window from Databricks engineering.

### Step 2 — Root S3 bucket

```hcl
resource "aws_s3_bucket" "root" {
  bucket        = "${var.prefix}-databricks-root"
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "root" {
  bucket = aws_s3_bucket.root.id
  versioning_configuration { status = "Disabled" }
}

resource "aws_s3_bucket_public_access_block" "root" {
  bucket                  = aws_s3_bucket.root.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Bucket policy: allow Databricks to write to the root bucket
data "databricks_aws_bucket_policy" "root" {
  provider   = databricks.mws
  bucket     = aws_s3_bucket.root.bucket
}

resource "aws_s3_bucket_policy" "root" {
  bucket = aws_s3_bucket.root.id
  policy = data.databricks_aws_bucket_policy.root.json
}
```

### Step 3 — VPC and subnets

The "bring your own VPC" approach gives you control over routing, DNS, Private Link, and on-premises connectivity. The VPC needs at least two private subnets (Databricks places nodes across AZs) and a NAT gateway for outbound internet access.

```hcl
resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr        # e.g., "10.100.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = { Name = "${var.prefix}-databricks-vpc" }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.this.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = { Name = "${var.prefix}-private-${count.index}" }
}

resource "aws_security_group" "databricks" {
  vpc_id = aws_vpc.this.id
  name   = "${var.prefix}-databricks-sg"

  ingress {
    from_port = 0
    to_port   = 65535
    protocol  = "tcp"
    self      = true   # cluster nodes talk to each other
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

> **Plan your CIDR carefully.** On AWS, you can change VPC peering and routing rules later, but subnet sizes are fixed at creation. Databricks assigns **two IP addresses per node** — one for management traffic, one for the Spark container — so usable nodes ≈ (subnet IPs − 5 AWS-reserved) ÷ 2. A `/24` therefore supports only **~120 nodes** (not ~250); for large clusters use `/22` (~500) or larger. Workspace subnets must have a netmask between `/17` and `/26`. This is the single most common miscalculation in Databricks AWS deployments.

### Step 4 — MWS resources and workspace

```hcl
resource "databricks_mws_credentials" "this" {
  provider         = databricks.mws
  account_id       = var.databricks_account_id
  credentials_name = "${var.prefix}-credentials"
  role_arn         = aws_iam_role.cross_account.arn

  depends_on = [time_sleep.iam_propagation]
}

resource "databricks_mws_storage_configurations" "this" {
  provider                   = databricks.mws
  account_id                 = var.databricks_account_id
  storage_configuration_name = "${var.prefix}-storage"
  bucket_name                = aws_s3_bucket.root.bucket
}

resource "databricks_mws_networks" "this" {
  provider           = databricks.mws
  account_id         = var.databricks_account_id
  network_name       = "${var.prefix}-network"
  vpc_id             = aws_vpc.this.id
  subnet_ids         = aws_subnet.private[*].id
  security_group_ids = [aws_security_group.databricks.id]
}

resource "databricks_mws_workspaces" "this" {
  provider       = databricks.mws
  account_id     = var.databricks_account_id
  workspace_name = var.prefix
  aws_region     = var.region

  credentials_id           = databricks_mws_credentials.this.credentials_id
  storage_configuration_id = databricks_mws_storage_configurations.this.storage_configuration_id
  network_id               = databricks_mws_networks.this.network_id
}

output "workspace_url" {
  value = databricks_mws_workspaces.this.workspace_url
}
```

The workspace URL from the output feeds the workspace-level provider alias. Workspace provisioning typically takes 5–7 minutes.

---

## Unity Catalog setup with Terraform

UC setup requires both provider modes. Account-level resources (`databricks_metastore`, `databricks_metastore_assignment`) use `provider = databricks.mws`; workspace-level UC objects (`databricks_catalog`, `databricks_grants`) use `provider = databricks.workspace`.

### Why no `storage_root` on the metastore

The `databricks_metastore` resource accepts an optional `storage_root` attribute that sets a default S3 location for all managed tables. **Do not set it.**

When `storage_root` is absent, every catalog must explicitly declare its own managed storage location. This forces you to think about storage isolation at the catalog level — the right unit of isolation — instead of letting tables accumulate in a shared bucket that becomes impossible to govern later.

```hcl
# Accounts created after November 2023 receive one metastore per region
# automatically — you cannot create a second one. Look it up instead.
data "databricks_metastores" "all" {
  provider = databricks.mws
}

locals {
  # Auto-provisioned name pattern: metastore_aws_<region_underscored>
  # e.g. eu-central-1 → metastore_aws_eu_central_1
  metastore_name = "metastore_aws_${replace(var.region, "-", "_")}"
  metastore_id   = data.databricks_metastores.all.ids[local.metastore_name]
}

resource "databricks_metastore_assignment" "this" {
  provider     = databricks.mws
  metastore_id = local.metastore_id
  workspace_id = databricks_mws_workspaces.this.workspace_id
}
```

> **Auto-provisioned metastores.** Databricks accounts created after November 2023 receive one metastore per AWS region automatically. The `resource "databricks_metastore"` block will fail with `METASTORE_LIMIT_EXCEEDED` on these accounts — use `data "databricks_metastores"` to look up the existing one instead. Older accounts can still create metastores. The auto-provisioned naming convention is `metastore_aws_<region_underscored>`; if your metastore was renamed, pass the name explicitly.

Once the metastore is assigned, set the workspace default catalog so SQL code without a catalog qualifier resolves to your UC catalog instead of `hive_metastore`. Use `databricks_default_namespace_setting` (workspace-level):

```hcl
resource "databricks_default_namespace_setting" "this" {
  provider = databricks.workspace
  namespace {
    value = var.default_catalog_name   # e.g. "engineering" or "dev_main"
  }
  depends_on = [databricks_metastore_assignment.this]
}
```

This is especially important during migrations: existing notebooks that write `SELECT * FROM bronze.events` continue to work without modification.

### External location for catalog storage

Before creating a catalog with managed storage, you need a storage credential (the IAM role Databricks uses to access S3) and an external location (the S3 path itself).

There is a genuine circular dependency to navigate: the IAM role's trust policy requires an `external_id` that Databricks generates when the storage credential is created — but the storage credential needs the IAM role ARN. Break the cycle with the **credential-before-role** pattern: create the storage credential first with a hardcoded ARN string (no Terraform resource reference), then read the `external_id` from the created credential to generate the correct trust policy for the IAM role.

```hcl
# Step 1 — storage credential first, hardcoded ARN string breaks the cycle
# (no Terraform dependency on aws_iam_role, so Terraform creates this first)
resource "databricks_storage_credential" "this" {
  provider = databricks.workspace
  name     = "${var.prefix}-storage-cred"

  aws_iam_role {
    role_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.prefix}-uc-storage"
  }

  depends_on = [databricks_metastore_assignment.this]
}

# Step 2 — data source reads the real external_id from the created credential
data "databricks_aws_unity_catalog_assume_role_policy" "this" {
  provider       = databricks.workspace
  aws_account_id = data.aws_caller_identity.current.account_id
  role_name      = "${var.prefix}-uc-storage"
  external_id    = databricks_storage_credential.this.aws_iam_role[0].external_id
}

# Step 3 — IAM role created with correct trust policy (including self-assume)
resource "aws_iam_role" "uc_storage" {
  name               = "${var.prefix}-uc-storage"
  assume_role_policy = data.databricks_aws_unity_catalog_assume_role_policy.this.json
}

# Managed policy (not inline) — provider keeps S3 permissions current
data "databricks_aws_unity_catalog_policy" "this" {
  provider       = databricks.workspace
  aws_account_id = data.aws_caller_identity.current.account_id
  bucket_name    = aws_s3_bucket.catalog.id
  role_name      = "${var.prefix}-uc-storage"
}

resource "aws_iam_policy" "uc_storage" {
  name   = "${var.prefix}-uc-storage-policy"
  policy = data.databricks_aws_unity_catalog_policy.this.json
}

resource "aws_iam_role_policy_attachment" "uc_storage" {
  role       = aws_iam_role.uc_storage.name
  policy_arn = aws_iam_policy.uc_storage.arn
}

# IAM eventual consistency — wait before Databricks validates the external location
resource "time_sleep" "wait_for_iam" {
  depends_on      = [aws_iam_role_policy_attachment.uc_storage]
  create_duration = "30s"
}

resource "databricks_external_location" "catalog_storage" {
  provider        = databricks.workspace
  name            = "${var.prefix}-catalog-location"
  url             = "s3://${aws_s3_bucket.catalog.bucket}/"
  credential_name = databricks_storage_credential.this.name
  depends_on      = [time_sleep.wait_for_iam]
}
```

> **Why `data "databricks_aws_unity_catalog_policy"`?** The `databricks_aws_unity_catalog_policy` data source generates the S3 IAM policy with the exact permissions Databricks currently requires. Databricks updates these permissions over time (new features need new S3 actions). Using the data source means your IAM policy stays in sync with provider upgrades at no extra cost. Never hardcode the S3 actions — the generated list is longer and more precise than anything you'd write manually.

### Catalogs, schemas, and grants

```hcl
resource "databricks_catalog" "engineering" {
  provider     = databricks.workspace
  name         = "engineering"
  storage_root = "s3://${aws_s3_bucket.catalog.bucket}/engineering/"

  depends_on = [databricks_external_location.catalog_storage]
}

resource "databricks_schema" "bronze" {
  provider     = databricks.workspace
  catalog_name = databricks_catalog.engineering.id
  name         = "bronze"
}

resource "databricks_schema" "silver" {
  provider     = databricks.workspace
  catalog_name = databricks_catalog.engineering.id
  name         = "silver"
}
```

### `databricks_grants` versus `databricks_grant`

This distinction causes subtle bugs in large deployments:

| Resource | Behaviour | When to use |
|---|---|---|
| `databricks_grants` | **Authoritative** — replaces *all* existing grants on the object | Managing all permissions for an object in one place |
| `databricks_grant` | **Authoritative per principal** — updates one principal's grants, leaves others untouched | When different teams manage different principals' access |

Never use both for the same object. If `databricks_grants` runs after `databricks_grant`, it erases the per-principal grant.

```hcl
# Authoritative: all grants on engineering catalog defined here
resource "databricks_grants" "engineering" {
  provider = databricks.workspace
  catalog  = databricks_catalog.engineering.name

  grant {
    principal  = "data-engineers"
    privileges = ["USE_CATALOG", "CREATE_SCHEMA"]
  }
  grant {
    principal  = "data-scientists"
    privileges = ["USE_CATALOG"]
  }
}
```

### Secrets management

Databricks secrets store sensitive values (API keys, passwords, connection strings) at workspace level. Secret scopes namespace the secrets; a notebook reads them with `dbutils.secrets.get("scope", "key")` — the value is never logged or displayed.

The same JSON-from-file pattern used for IAM drives secret creation. Because secret values are sensitive, the JSON file is gitignored — only a `secrets.json.example` with placeholder values is committed:

```json
{
  "scopes": [
    {
      "name": "dev",
      "secrets": [
        { "key": "my-api-key",  "value": "replace-me" },
        { "key": "db-password", "value": "replace-me" }
      ]
    }
  ]
}
```

```hcl
resource "databricks_secret_scope" "this" {
  for_each = { for s in var.secrets.scopes : s.name => s }
  provider = databricks.workspace
  name     = each.key
}

resource "databricks_secret" "this" {
  for_each = {
    for pair in flatten([
      for s in var.secrets.scopes : [
        for sec in s.secrets : { scope = s.name, key = sec.key, value = sec.value }
      ]
    ]) : "${pair.scope}:${pair.key}" => pair
  }
  provider     = databricks.workspace
  scope        = databricks_secret_scope.this[each.value.scope].name
  key          = each.value.key
  string_value = each.value.value
}
```

The environment module reads the file with a `fileexists()` guard so the layer applies cleanly even when no secrets are defined yet:

```hcl
secrets = fileexists("${path.module}/secrets.json") ? jsondecode(file("${path.module}/secrets.json")) : { scopes = [] }
```

The variable is declared `sensitive = true` so Terraform never prints secret values in plan or apply output.

**Secret scope ACLs.** By default only the creator of a scope (the service principal running Terraform) has `MANAGE` permission. Grant read access to user groups with `databricks_secret_acl`:

```hcl
resource "databricks_secret_acl" "read" {
  for_each   = { for s in var.secrets.scopes : s.name => s }
  provider   = databricks.workspace
  scope      = databricks_secret_scope.this[each.key].name
  principal  = "data-engineers"
  permission = "READ"
}
```

Use in a notebook — the value is `[REDACTED]` if printed but usable in API calls:

```python
api_key = dbutils.secrets.get(scope="dev", key="my-api-key")
```

---

## Code organisation: modules and state separation

### The core rule: separate state per lifecycle

The most important structural decision in Databricks Terraform is **how many state files you have and what each one owns**. Changes at different layers have different risk profiles and different change frequency:

| State file | Contains | Changes how often |
|---|---|---|
| `global/` | Git servers, Terraform backend infra | Rarely |
| `account/` | UC metastore, account-level groups, service principals | Occasionally |
| `workspace/<env>/` | Workspace, VPC, IAM, storage config | Per environment, infrequently |
| `catalog/<env>/` | Catalogs, schemas, grants, external locations | Per sprint |
| `platform/<env>/` | Cluster policies, SQL warehouses, shared compute | Per quarter |

Keeping workspace provisioning and catalog management in separate state files means a `terraform plan` on a catalog change doesn't evaluate 40 VPC resources. It also means a broken catalog apply cannot accidentally destroy workspace networking.

### Module layout

```
infra/
├── modules/                  # reusable building blocks
│   ├── aws-workspace/        # VPC + IAM + MWS resources → workspace URL
│   ├── unity-catalog/        # metastore + storage credential + external location
│   ├── catalog/              # single catalog + schemas + grants
│   └── cluster-policy/       # reusable cluster policy template
├── global/                   # state: backend infra, Git config
│   └── main.tf
├── account/                  # state: metastore, account groups
│   └── main.tf
├── environments/
│   ├── dev/
│   │   ├── workspace/        # state: workspace + networking
│   │   ├── catalog/          # state: dev catalogs + grants
│   │   └── platform/         # state: cluster policies, SQL warehouses
│   └── prod/
│       ├── workspace/
│       ├── catalog/
│       └── platform/
```

**Flat module design is strongly recommended:** root modules call child modules directly; child modules should not call other modules. A two-level call stack (root → child) is easy to follow. Three or more levels (root → wrapper → child → sub-child) makes `terraform graph` unreadable and `module.X.module.Y.module.Z.resource_name` addresses appear in error messages. If you feel the urge to have a module call another module, the two modules probably belong in the same module.

Root modules (`environments/dev/workspace/main.tf` etc.) are thin: they call child modules and pass environment-specific variables. All logic lives in the modules.

### Passing outputs between state files

A workspace-level Terraform config needs the workspace URL from the workspace-provisioning state. Use `terraform_remote_state` data sources:

```hcl
# In environments/dev/catalog/main.tf
data "terraform_remote_state" "workspace" {
  backend = "s3"
  config = {
    bucket = var.tf_state_bucket
    key    = "environments/dev/workspace/terraform.tfstate"
    region = var.region
  }
}

provider "databricks" {
  host = data.terraform_remote_state.workspace.outputs.workspace_url
}
```

---

## Scaling with Terragrunt

Once you have more than two environments or more than one business unit, raw Terraform requires you to copy-paste backend configurations, provider blocks, and variable definitions across every root module. Terragrunt eliminates this duplication.

### Stacks and units

Terragrunt 1.x organises deployments into **units** (a single Terraform root module with a `terragrunt.hcl`) and **stacks** (a set of units with a `terragrunt.stack.hcl`). Each unit has an independently managed state file, but Terragrunt handles dependency ordering between units automatically.

```
live/
├── root.hcl                     # global variables, remote state backend, provider generation
├── environments/
│   ├── dev/
│   │   ├── environment.hcl      # env = "dev", region = "us-east-1"
│   │   ├── workspace/
│   │   │   └── terragrunt.hcl   # unit: references ../../../modules/aws-workspace
│   │   ├── catalog/
│   │   │   └── terragrunt.hcl   # unit: depends on workspace output
│   │   └── platform/
│   │       └── terragrunt.hcl
│   └── prod/
│       ├── environment.hcl      # env = "prod", region = "us-east-1"
│       ├── workspace/
│       │   └── terragrunt.hcl
│       └── catalog/
│           └── terragrunt.hcl
```

### `root.hcl` — define once, inherit everywhere

```hcl
# live/root.hcl
locals {
  environment = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  env_name    = local.environment.locals.env
  region      = local.environment.locals.region
  prefix      = "myco-${local.env_name}"
}

# Auto-generate provider configuration in every unit
generate "provider" {
  path      = "providers.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<-EOF
    provider "aws" {
      region = "${local.region}"
    }
    provider "databricks" {
      alias      = "mws"
      host       = "https://accounts.cloud.databricks.com"
      account_id = var.databricks_account_id
    }
  EOF
}

# Auto-create S3 backend with per-unit state isolation
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket         = "myco-terraform-state-${local.region}"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = local.region
    encrypt        = true
    dynamodb_table = "myco-terraform-locks"
  }
}
```

### `terragrunt.hcl` for a unit

```hcl
# live/environments/dev/catalog/terragrunt.hcl

include "root" {
  path   = find_in_parent_folders("root.hcl")
  expose = true
}

terraform {
  source = "../../../../modules/catalog"
}

# Declare dependency on the workspace unit — Terragrunt orders apply correctly
dependency "workspace" {
  config_path = "../workspace"
  mock_outputs = {
    workspace_url = "https://mock.cloud.databricks.com"
  }
  mock_outputs_allowed_terraform_commands = ["plan", "validate"]
}

inputs = {
  workspace_url = dependency.workspace.outputs.workspace_url
  env_name      = include.root.locals.env_name
  prefix        = include.root.locals.prefix
}
```

### Deploying a full environment

```bash
# Deploy all units in dev, respecting dependency order
cd live/environments/dev
terragrunt run --all apply

# Deploy only the catalog unit
cd live/environments/dev/catalog
terragrunt apply

# Control parallelism when hitting Databricks API rate limits
terragrunt run --all --parallelism 2 -- apply
```

### Terragrunt caveats for Databricks

| Caveat | What happens | Fix |
|---|---|---|
| Workspace-level provider needs workspace URL | Data sources that read workspace resources fail during `plan` when the workspace unit hasn't been applied yet | Add `mock_outputs` in `dependency` blocks |
| Rate limiting on `run --all` | Parallel unit execution hits Databricks API limits | `--parallelism 2` |
| Auth for multiple workspaces | Each workspace unit needs its own provider with the workspace URL | Use `dependency` output as `host` in the workspace provider |
| Provider generation for workspace provider | `root.hcl` can only generate MWS provider; workspace provider needs the URL | Generate it per-unit using a `generate` block that reads the workspace dependency output |

### Terragrunt hooks

Hooks let you run shell commands before or after Terraform commands — useful for pre-flight validation, notification, and CI/CD integration:

```hcl
# In a terragrunt.hcl unit
terraform {
  before_hook "validate_tfvars" {
    commands = ["apply"]
    execute  = ["./scripts/validate-workspace-vars.sh"]
  }

  after_hook "notify_slack" {
    commands = ["apply"]
    execute  = ["./scripts/notify.sh", "workspace deployed"]
  }

  error_hook "on_apply_fail" {
    commands  = ["apply"]
    execute   = ["./scripts/alert.sh", "apply failed"]
    on_errors = [".*"]
  }
}
```

Hooks have access to `TG_CTX_TF_PATH` (path to the `tofu`/`terraform` binary), `TG_CTX_COMMAND` (plan/apply/destroy), and `TG_CTX_HOOK_NAME`. (The config directory is available as `TG_CTX_TERRAGRUNT_DIR`, but that — along with `TG_CTX_HOOK_TYPE` and `TG_CTX_SOURCE` — is gated behind the `hook-context-env` experiment.) Execution order follows definition order; multiple hooks of the same type are supported. Hooks fire per-unit, not per-stack — if you need stack-level notifications, call `terragrunt run --all apply` from a CI step that wraps the result.

---

## Terraform CI/CD pipeline

A Terraform CI/CD pipeline has four stages. All four run on every change to infrastructure code:

```mermaid
flowchart LR
    A[Base & Compliance<br>fmt · validate · plan<br>terraform-compliance] --> B[Unit Tests<br>Terraform built-in tests<br>or Terratest — plan only]
    B --> C[Integration Tests<br>Terratest with apply<br>in sandbox environment]
    C --> D[Apply<br>to target environment<br>on merge to main]
```

### GitHub Actions skeleton

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  pull_request:
    paths: ["infra/**"]
  push:
    branches: [main]
    paths: ["infra/**"]

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "~1.15"   # latest stable: 1.15.6 (June 2026)

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_TERRAFORM_ROLE_ARN }}
          aws-region: us-east-1

      - name: Terraform fmt check
        run: terraform fmt -check -recursive infra/

      - name: Terraform validate
        run: |
          cd infra/environments/dev/workspace
          terraform init -backend=false
          terraform validate

      - name: Terraform plan
        env:
          DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
          DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
          TF_VAR_databricks_account_id: ${{ secrets.DATABRICKS_ACCOUNT_ID }}
        run: |
          cd infra/environments/dev/workspace
          terraform init
          terraform plan -out=plan.tfplan

  apply:
    needs: plan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: dev           # requires manual approval gate in GitHub
    steps:
      - uses: actions/checkout@v4
      # ... same setup steps ...
      - name: Terraform apply
        run: terraform apply plan.tfplan
```

### S3 backend with DynamoDB locking

```hcl
# Applied once manually (bootstrap); then all other state files use this backend
terraform {
  backend "s3" {
    bucket         = "myco-terraform-state-us-east-1"
    key            = "environments/dev/workspace/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "myco-terraform-locks"  # prevents concurrent applies
  }
}
```

---

## Production-hardened deployments: the Security Reference Architecture

The workspace provisioning code in this chapter gets you a working Databricks environment. It does not get you one that passes an enterprise security review. The **Security Reference Architecture (SRA)** — `terraform-databricks-sra` — is Databricks' official opinionated template for a hardened production deployment, modelled after their most security-conscious customers.

The SRA is not a module you call — it is a complete deployable Terraform configuration that you clone, fill in your variables, and run. Its value is as a learning artefact: reading it shows you every security control Databricks recommends, expressed as concrete Terraform resources.

### What the SRA adds beyond basic provisioning

```mermaid
flowchart TD
    subgraph BASIC["Basic workspace (this chapter so far)"]
        A[VPC + subnets]
        B[IAM cross-account role]
        C[S3 root bucket]
        D[databricks_mws_workspaces]
    end

    subgraph HARDENED["SRA additions"]
        E[Private Link\nVPC Interface endpoints:\nREST API + SCC relay]
        F[VPC endpoint policies\nS3 · STS · Kinesis\nrestrictive allow-lists]
        G[Two CMK keys\nworkspace storage\nmanaged services]
        H[Network Connectivity\nConfiguration + Network Policy]
        I[Restrictive root\nbucket policy]
        J[Legacy settings disabled\nDBFS · legacy access]
        K[Audit log delivery\nto S3]
        L[Compliance Security Profile\nHIPAA · PCI · HITRUST opt-in]
        M[Security Analysis Tool\nautomated posture scanning]
    end

    BASIC --> HARDENED
```

### Private Link

The basic deployment routes control-plane traffic (notebook commands, cluster API calls) over the public internet. Private Link routes it through AWS VPC Interface Endpoints, keeping traffic entirely within the AWS network:

| Endpoint | What it protects |
|---|---|
| `general_access` (REST API) | HTTPS traffic from cluster nodes to Databricks control plane |
| `scc_tunnel_dataplane_relay_access` (SCC relay) | Secure Cluster Connectivity tunnel — the channel Databricks uses to reach cluster nodes without public IPs |
| S3 Gateway endpoint | S3 data traffic stays on AWS backbone, not internet |
| STS Interface endpoint | IAM token requests stay on AWS backbone |
| Kinesis Interface endpoint | Audit log streaming stays on AWS backbone |

Each endpoint has a **restrictive policy** allowing only the specific AWS accounts and actions needed — not the default "allow all" that AWS creates by default.

### Customer-Managed Keys (CMK)

The SRA creates two separate KMS keys:

```hcl
# Key 1: workspace storage — encrypts DBFS root and EBS volumes on cluster nodes
resource "aws_kms_key" "workspace_storage" { ... }

# Key 2: managed services — encrypts control-plane data (notebooks, secrets,
# query results stored by Databricks in their infrastructure)
resource "aws_kms_key" "managed_services" { ... }
```

Two separate keys enforce separation of concerns: rotating or revoking the managed-services key doesn't affect data-plane storage, and vice versa. The workspace storage key's policy explicitly allows Databricks to use it `kms:ViaService` for `ec2.*.amazonaws.com`, which is required for EBS volume encryption on cluster nodes.

### Disabled legacy settings

```hcl
resource "databricks_disable_legacy_access_setting" "access" {
  disable_legacy_access { value = true }
}

resource "databricks_disable_legacy_dbfs_setting" "dbfs" {
  disable_legacy_dbfs { value = true }
}
```

These two resources enforce two important baseline controls: `disable_legacy_access` prevents older credential-passing patterns that bypass Unity Catalog governance; `disable_legacy_dbfs` blocks mounting external storage via `dbutils.fs.mount` and direct DBFS access patterns that predate Unity Catalog Volumes. Both are `false` by default in new workspaces — the SRA turns them on as day-one configuration.

### Network Connectivity Configuration (NCC)

The NCC is an account-level object that tells Databricks which network egress rules apply to serverless compute in this workspace. Without it, serverless clusters (SQL Warehouses, serverless jobs) use Databricks-managed networking. With it, you control which destinations serverless compute can reach:

```hcl
module "network_connectivity_configuration" {
  source = "./modules/databricks_account/network_connectivity_configuration"
  providers = { databricks = databricks.mws }
  region          = var.region
  resource_prefix = var.resource_prefix
}
```

### Security Analysis Tool (SAT)

The SAT is the most operationally valuable SRA component. It deploys as a Databricks workflow (a scheduled job) that runs automated checks against your workspace configuration and scores your security posture across categories: network security, identity and access, data protection, and governance.

The output is a Databricks SQL dashboard. Each finding links to the relevant Databricks documentation and the Terraform resource that would fix it. Running SAT after initial deployment tells you exactly where your configuration diverges from Databricks' security recommendations — without needing a human security review.

```hcl
module "security_analysis_tool" {
  count  = var.enable_security_analysis_tool ? 1 : 0
  source = "./modules/security_analysis_tool"

  providers             = { databricks = databricks.created_workspace }
  databricks_account_id = var.databricks_account_id
  workspace_id          = module.databricks_mws_workspace.workspace_id
  run_on_serverless     = true
  sql_warehouse_enable_serverless = true

  depends_on = [module.unity_catalog_catalog_creation]
}
```

### Using the SRA

The SRA is a point-in-time reference, not a versioned library. Clone it, read `aws/tf/variables.tf` to understand what you need to provide, and run it in a sandbox account first. The key variables are: `databricks_account_id`, `aws_account_id`, `region`, `resource_prefix`, `admin_user`, and `deployment_name`.

For a new production deployment, the recommended workflow is:
1. Use the SRA as your starting template rather than building from scratch
2. Strip the components you don't need (SAT can be disabled with `enable_security_analysis_tool = false`)
3. Wrap it in Terragrunt for multi-environment management
4. Run SAT on every environment quarterly to catch configuration drift

> **SRA is not formally supported by Databricks.** It is provided for exploration and as a reference implementation. Don't file support tickets — use the [GitHub Issues](https://github.com/databricks/terraform-databricks-sra/issues) page.

---

## Pitfalls reference

| Pitfall | Symptom | Root cause | Fix |
|---|---|---|---|
| Wrong provider alias | `Error: cannot create workspace with workspace-level provider` | Using `databricks.workspace` for `databricks_mws_*` resources | All `databricks_mws_*` resources must use `provider = databricks.mws` |
| IAM propagation delay | `ValidationException: CrossAccountRole does not exist` on `databricks_mws_credentials` | AWS confirms IAM policy attachment before global consistency | Add `time_sleep` of 20s after `aws_iam_role_policy`, before `databricks_mws_credentials` |
| `storage_root` on metastore | All managed tables land in a shared root bucket | Default metastore storage path is a catch-all | Create `databricks_metastore` without `storage_root`; require explicit `storage_root` on each catalog |
| Mixed `databricks_grants` and `databricks_grant` | Grants disappear or get overwritten on plan | `databricks_grants` is authoritative and erases per-principal grants | Use one or the other for a given securable, never both |
| Account-level and workspace-level resources in same state | Slow plans; risk of destroying workspace networking on catalog change | Tightly coupled lifecycle | Separate state files by layer |
| Subnet too small | `Error: no free IPs in subnet` when cluster nodes can't get IPs | CIDR planned for tens of nodes, not hundreds | Plan CIDR at /22 or larger for production workspaces |
| Missing `depends_on` to metastore assignment | `Error: catalog cannot be created without metastore assignment` | Terraform parallelises workspace-level UC object creation before metastore is assigned | Add `depends_on = [databricks_metastore_assignment.this]` to `databricks_catalog` and `databricks_storage_credential` |
| Terragrunt plan failure before workspace exists | `Error reading workspace attributes` in catalog plan | Data sources run during plan; workspace doesn't exist yet | Set `mock_outputs` in all `dependency` blocks with realistic placeholder values |
| Hardcoded account ID in trust policy | IAM role accepts any principal in the Databricks account | Custom trust policy instead of `data.databricks_aws_assume_role_policy` | Always use the provider's data sources for trust and permissions policies |
| Auto-provisioned metastore | `METASTORE_LIMIT_EXCEEDED` on `databricks_metastore` creation | Accounts after Nov 2023 receive one metastore per region automatically | Use `data "databricks_metastores"` to look up the existing metastore by name |
| UC storage credential circular dependency | `EntityAlreadyExists` on IAM role, or trust policy has wrong `external_id` | IAM trust policy needs `external_id` from credential, but credential needs role ARN | Credential-before-role: create `databricks_storage_credential` with hardcoded ARN string; read `external_id` via `databricks_aws_unity_catalog_assume_role_policy` data source; then create the IAM role |
| Assigning users directly to workspace | Adding a new admin requires an HCL change; removing a leaver requires emergency Terraform | Individual user assigned via `databricks_mws_permission_assignment` instead of a group | Assign the group to the workspace; manage membership in `iam.json` |
| Secret scope MANAGE permission locked to SP | Human engineers cannot update or delete secrets after Terraform creates the scope | Service principal that created the scope is the sole MANAGE holder by default | Add `databricks_secret_acl` with `MANAGE` for the `admins` group immediately after scope creation |
| UC IAM eventual consistency | `non self-assuming` error on `databricks_external_location` | AWS confirms IAM policy attachment seconds before global propagation; Databricks validates immediately | Add `time_sleep` of 30s after `aws_iam_role_policy_attachment`, before `databricks_external_location` |
| Schema grant propagation delay | `securable_full_name is not a valid name` or `invalid schema name` on `databricks_grants` | Databricks permissions API needs ~15s to register newly created schemas | Add `time_sleep` of 15s after schema creation; add `depends_on` to all schema-level grant resources |
| `storage_root` trailing slash | `Provider produced inconsistent final plan` on `databricks_catalog` | Provider normalizes `storage_root` to append `/` at apply time, but plan computed without it | Always append `/` to `storage_root`: `"s3://bucket/path/"` |

---

## Summary

- **Choose workspace topology before writing Terraform:** monolithic for prototypes; environment-separated for most teams; domain-separated when business units need autonomy; hub-spoke for large enterprises with a platform team.
- **Unity Catalog changes the isolation equation:** before UC, workspace = isolation boundary. With UC, catalog = isolation boundary. Separate workspaces are only necessary for compute isolation, billing isolation, or regulatory scope boundaries.
- **Three environment separation strategies:** workspace-per-env (strongest, most expensive), catalog-per-env (recommended default), schema-per-env (weakest — only for small teams).
- **Hybrid catalog topology scales best:** `{env}_{domain}` catalog names (e.g., `prod_marketing`, `dev_marketing`) give both domain ownership and environment isolation in one consistent naming scheme.
- **Match the isolation mechanism to the requirement:** catalog grants for coarse isolation; `isolation_mode = "ISOLATED"` + `databricks_workspace_binding` for preventing catalog discovery across workspaces; row filters for row-level RBAC; column masking for PII; dynamic views for complex multi-table logic.
- **Multi-BU governance follows two patterns:** distributed publishing (each BU governs its own catalogs) or centralized publishing (central team quality-gates all published data). Cross-region data sharing uses Databricks-to-Databricks OpenSharing (formerly Delta Sharing) between metastores.
- **A deployment stage is a validation + approval boundary:** dev → staging (automated tests) → prod (human approval). Staging data should read raw prod inputs but write to an isolated catalog.
- **Config-driven Terraform replaces copy-pasted HCL:** drive catalog and grant structure from `locals` maps with `for_each`; stop at two nesting levels before explicit resources become clearer. For platform-team self-service, externalise the config into YAML files read with `yamldecode()`.
- **IAM from JSON:** keep users, groups, and group membership in a committed `iam.json`; assign the workspace admin group via `databricks_mws_permission_assignment` rather than an individual user — membership changes stay out of HCL.
- **Secrets from JSON (gitignored):** drive `databricks_secret_scope` and `databricks_secret` from a `secrets.json` that is gitignored; mark the variable `sensitive = true`; use `fileexists()` so the layer applies cleanly with no file present. Add `databricks_secret_acl` to give the `admins` group `MANAGE` access so engineers can update secrets without re-running Terraform as the SP.
- **Flat module design:** root modules call child modules directly; child modules do not call other modules. More than two levels of module nesting creates unreadable `terraform graph` output and cryptic error addresses.
- **The platform/application split is the foundational decision:** Terraform owns workspaces, networking, Unity Catalog topology, and shared platform resources. DABs owns pipelines, jobs, and notebooks. Never merge these layers.
- **AWS workspace provisioning is account-level:** all `databricks_mws_*` resources use `provider = databricks.mws`. The four required components are the IAM cross-account role, the S3 root bucket, the VPC/subnets, and the MWS resource chain.
- **Add `time_sleep` after IAM policy attachment** to absorb AWS propagation delay before `databricks_mws_credentials` validates the role.
- **Omit `storage_root` from `databricks_metastore`:** force every catalog to declare its own storage location, keeping governance clean at the catalog boundary.
- **`databricks_grants` is authoritative** — it replaces all grants on an object. `databricks_grant` is per-principal. Never mix them on the same securable.
- **Separate state files by lifecycle:** account, workspace, catalog, and platform layer each get their own state. A catalog change should not re-evaluate VPC resources.
- **Terragrunt eliminates DRY violations:** `root.hcl` defines remote state backend and provider generation once; each unit's `terragrunt.hcl` specifies only its module source, inputs, and dependencies. Use hooks (`before_hook`, `after_hook`, `error_hook`) for CI/CD notifications and validation scripts.
- **CI/CD pipeline stages:** `fmt → validate → plan` on PR; `apply` on merge to main, gated by environment approval.

---

## What comes next

This chapter closes the Expert tier. Ch 27 (End-to-End Lakehouse Architecture) brought all the pipeline and data patterns together; Ch 29 brings the infrastructure underneath them under version control. The full picture is now: Terraform provisions the platform, DABs deploys the pipelines, the Databricks SDK (Ch 28) automates runtime operations, and Lakeflow Jobs orchestrates the execution. These four tools — Terraform, DABs, the SDK, and Jobs — are the complete operator toolkit for a production Databricks lakehouse.

---

## References

- [Databricks Terraform provider on AWS](https://docs.databricks.com/aws/en/dev-tools/terraform/)
- [Provisioning AWS Databricks workspace — Terraform Registry guide](https://registry.terraform.io/providers/databricks/databricks/latest/docs/guides/aws-workspace)
- [Unity Catalog setup on AWS — Terraform Registry guide](https://registry.terraform.io/providers/databricks/databricks/latest/docs/guides/unity-catalog)
- [databricks_mws_workspaces resource reference](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/mws_workspaces)
- [databricks_metastore resource reference](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/metastore)
- [terraform-databricks-examples — CI/CD pipeline templates](https://github.com/databricks/terraform-databricks-examples/tree/main/cicd-pipelines)
- [terraform-databricks-lakehouse-blueprints — production modules](https://github.com/databricks/terraform-databricks-lakehouse-blueprints)
- [terraform-databricks-sra — Security Reference Architecture](https://github.com/databricks/terraform-databricks-sra) · local: `C:\opt\learn\databricks\repos\terraform-databricks-sra`
- [terraform-provider-databricks — provider source code](https://github.com/databricks/terraform-provider-databricks) · local: `C:\opt\learn\databricks\repos\terraform-provider-databricks`
- [Terragrunt documentation — stacks and units](https://terragrunt.gruntwork.io/docs/)
- [Deploying Databricks at scale with Terragrunt (Medium)](https://medium.com/@dominik.schuessele/deploying-databricks-workspaces-at-scale-in-enterprises-using-terragrunt-52c561b667ec)
- [Terraform vs Databricks Asset Bundles — Alex Ott (Medium)](https://medium.com/@alexott_en/terraform-vs-databricks-asset-bundles-6256aa70e387)
