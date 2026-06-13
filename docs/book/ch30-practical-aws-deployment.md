# Ch 30 — Practical Databricks AWS Deployment with Terraform

A misconfigured IAM trust policy can silently accept the workspace request, return a workspace ID, and then fail hours later when the first cluster tries to start. The only way to catch this before it costs you is to run the Terraform code yourself — against a real AWS account — and watch each resource state transition. This chapter walks through deploying the codebase from [databricks-aws-terraform](../../databricks-aws-terraform) end to end.

---

## What you'll have after this chapter

- An S3 bucket holding all Terraform state (no DynamoDB)
- A VPC with two private subnets and one public subnet (NAT gateway optional — off by default for serverless)
- A Databricks workspace registered in your account console
- An account-level `admins` group containing your user, assigned workspace ADMIN
- A Unity Catalog metastore with a `main` catalog containing bronze, silver, and gold schemas
- A `dev` secret scope (empty by default; add secrets to `secrets.json` to populate it)

---

## Free Edition vs paid account

> **If you have a Databricks Free Edition account**, you already have one workspace provisioned by Databricks — you cannot create additional workspaces via `databricks_mws_*`. **Skip Steps 1–3** (bootstrap, networking, workspace). Go straight to [Step 4 — Unity Catalog](#step-4--unity-catalog-layer), which works against any existing workspace including Free Edition. You will still need a service principal (see below) and Terraform installed, but no AWS account is required for the UC layer alone.
>
> Steps 1–3 require a **paid Databricks account on AWS** (Trial or Enterprise) where you have permission to provision new workspaces. The standard way to get one is through the **AWS Marketplace**: search for "Databricks" at `https://us-east-1.console.aws.amazon.com/marketplace/search?text=databricks`, subscribe, and your DBU charges will flow through your AWS bill.
>
> **AWS Marketplace subscription — avoid the auto-created workspace.** After accepting the offer, AWS shows a "Set up your account" button. **Do not click it.** That wizard always creates a default workspace (named `workspace`, storage: *Default*, credentials: *Serverless only*) before you can intervene. Instead, after the subscription confirms, navigate directly to `accounts.cloud.databricks.com` — the Marketplace billing link is already attached. Provision your workspace via Terraform in Step 2.
>
> If you already clicked "Set up your account" and now have an unwanted `workspace` in your account console, delete it: **account console → Workspaces → click the workspace → Delete workspace**. Because it uses Databricks-managed (*Default*) storage, there is nothing in your AWS account to clean up. Your Terraform-managed workspace is unaffected.
>
> **Cost note for learners:** provisioning the workspace, VPC, S3 bucket, and Unity Catalog metastore via Terraform incurs only standard AWS infrastructure costs — no DBU charges. DBUs only accrue when a cluster or SQL warehouse is running. The main ongoing cost is the **NAT gateway (~$0.045/hour, ~$32/month)**, which sits in your VPC to give classic cluster nodes outbound access to the Databricks control plane. If you plan to use **serverless compute only** (serverless SQL Warehouses, serverless jobs), compute runs in Databricks-managed infrastructure and never touches your VPC — the NAT gateway is idle overhead. In that case, set `enable_nat_gateway = false` in `modules/networking/main.tf` to remove it, or simply destroy the full stack after each learning session (`terraform destroy` in reverse layer order takes ~5 minutes).

---

## Prerequisites

Before running a single `terraform init`:

| Requirement | Free Edition | Paid account |
|---|---|---|
| Terraform 1.15+ | ✅ needed | ✅ needed |
| Databricks account | ✅ accounts.cloud.databricks.com | ✅ accounts.cloud.databricks.com |
| Service principal with Account Admin | ✅ needed | ✅ needed |
| AWS CLI + IAM permissions | ❌ skip Steps 1–3 | ✅ needed |

**Creating the service principal** (works on both Free and paid):

1. In the Databricks account console go to **Settings → Identity and access → Service Principals → Add service principal**
2. Give it a name, e.g. `terraform-deployer`
3. On the workspace entitlements screen, set the following and click **Add service principal**:

| Entitlement | Setting | Why |
|---|---|---|
| Consumer access | On | Default; allows read access to shared data |
| Databricks SQL access | On | Needed to manage SQL warehouses via Terraform |
| Workspace access | On | Required to authenticate into the workspace at all |
| **Admin access** | **On** | Required to manage catalogs, schemas, grants, and workspace-level config |

<ol start="4">
<li><strong>Paid account only</strong> — in the <strong>account console</strong> (<code>accounts.cloud.databricks.com</code>, a separate URL from the workspace) → <strong>User management → Service principals</strong> → click <code>terraform-deployer</code> → <strong>Roles</strong> → assign <strong>Account Admin</strong>. Required for <code>databricks_mws_*</code> (Steps 1–3). <em>Free Edition users skip this — workspace Admin access already set above is sufficient for Step 4.</em></li>
<li>In the workspace SP page (<strong>Workspace settings → Identity and access → Service principals → terraform-deployer</strong>) → <strong>Secrets</strong> tab → <strong>Generate secret</strong> — save the <strong>Application Id</strong> as <code>client_id</code> and the generated value as <code>client_secret</code></li>
</ol>

---

## Repository layout

```
databricks-aws-terraform/
├── bootstrap/           S3 state bucket — run once
├── modules/
│   ├── networking/      VPC, subnets, NAT, security group
│   ├── workspace/       IAM cross-account role, root S3, MWS workspace
│   └── unity-catalog/   Metastore, UC IAM, catalog, schemas, grants
└── environments/
    ├── dev/
    │   ├── 01-networking/
    │   ├── 02-workspace/
    │   └── 03-unity-catalog/
    └── prod/            (same structure, prod CIDRs)
```

Each `environments/*/0N-*/` directory is a thin root module that calls the corresponding reusable module and stores its state independently. The numbered prefixes enforce deploy order at a glance.

```mermaid
graph LR
    bootstrap["bootstrap<br/>(S3 bucket)"]
    net["01-networking<br/>(VPC)"]
    ws["02-workspace<br/>(MWS)"]
    uc["03-unity-catalog<br/>(UC)"]

    bootstrap -->|state bucket name| net
    net -->|vpc_id, subnet_ids, sg_ids| ws
    ws -->|workspace_url, workspace_id| uc
```

---

## Step 1 — Bootstrap the state bucket

The bootstrap layer is the only one without a remote backend — it uses local state. Run it once; the bucket it creates holds all other state files.

```powershell
cd C:\opt\learn\databricks\databricks-aws-terraform\bootstrap

cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars: set region and prefix (bucket name is auto-generated)

terraform init
terraform validate
terraform plan
terraform apply
```

Expected output on success:

```
Apply complete! Resources: 5 added, 0 changed, 0 destroyed.

Outputs:
state_bucket_name = "myorg-databricks-tf-state-a1b2c3d4"
state_bucket_region = "eu-central-1"
```

The bucket name is `<prefix>-databricks-tf-state-<random8hex>` — globally unique without any manual naming.

**What gets created:** one S3 bucket with versioning, AES256 encryption, and public access blocked. `force_destroy = false` protects the bucket from accidental deletion.

**Why no DynamoDB?** Terraform 1.10 introduced S3 native locking via `use_lockfile = true`. The backend writes a `.tflock` object to S3 before any write operation. No DynamoDB table, no provisioned capacity, no cost at rest.

Verify the bucket in the AWS console under S3 — it should show the bucket name and zero objects.

---

## Step 2 — Networking layer

```powershell
# Get the generated bucket name from bootstrap output
terraform -chdir=C:\opt\learn\databricks\databricks-aws-terraform\bootstrap output -raw state_bucket_name

cd environments/dev/01-networking

cp backend.tfvars.example backend.tfvars
# Edit: bucket = "<value from above>", region = "eu-central-1"

cp terraform.tfvars.example terraform.tfvars
# Edit if needed: change AZs for your region

terraform init -backend-config="backend.tfvars"   # quotes required on PowerShell (dot in filename)
terraform validate
terraform plan
terraform apply
```

**What gets created:**

| Resource | Value |
|---|---|
| VPC | 10.0.0.0/16 |
| Private subnets | 10.0.1.0/24, 10.0.2.0/24 (us-east-1a, us-east-1b) |
| Public subnet | 10.0.0.0/24 (for NAT egress if enabled) |
| NAT gateway | None by default (`enable_nat_gateway = false`); set `true` only for classic clusters |
| Security group | self-referential ingress + all egress |

The default security group is configured for Databricks: cluster nodes communicate with each other on all ports (self-referential rule), and all outbound traffic is allowed so nodes can reach the Databricks control plane.

Verify with:

```powershell
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=dbx-dev-vpc" --query "Vpcs[].VpcId"
```

---

## Step 3 — Workspace layer

This layer creates the most sensitive resources: the cross-account IAM role that Databricks uses to manage EC2 instances in your VPC.

```powershell
cd environments/dev/02-workspace

cp backend.tfvars.example backend.tfvars
# Edit: bucket and region

cp terraform.tfvars.example terraform.tfvars
# Edit: databricks_account_id, databricks_client_id, state_bucket, workspace_name = "dev"
```

**Before applying, edit `iam.json`** to set your Databricks account email:

```json
{
  "users": [
    { "user_name": "your.email@example.com", "display_name": "Your Name" }
  ],
  "groups": [
    { "name": "admins", "members": ["your.email@example.com"] }
  ]
}
```

```powershell
terraform init -backend-config="backend.tfvars"   # quotes required on PowerShell (dot in filename)
terraform validate
terraform plan
terraform apply
```

**Resource creation sequence:**

1. `aws_iam_role.cross_account` — the role Databricks assumes
2. `aws_iam_role_policy.cross_account` — the policy granting EC2/networking permissions
3. **`time_sleep` 20 seconds** — waits for IAM to propagate globally. Without this, `databricks_mws_credentials` validates the role immediately and fails with "unable to assume role" even though the role exists.
4. `aws_s3_bucket.root_storage` — DBFS root (workspace home directory, cluster logs, init scripts)
5. `databricks_mws_credentials` — registers the IAM role with Databricks account
6. `databricks_mws_storage_configurations` — registers the S3 bucket with Databricks account
7. `databricks_mws_networks` — registers the VPC + subnets + security group with Databricks account
8. `databricks_mws_workspaces` — combines the above three into a workspace (takes 2–5 minutes to provision)
9. `databricks_user.this` — creates account-level users from `iam.json`
10. `databricks_group.this` — creates account-level groups from `iam.json`
11. `databricks_group_member.this` — adds users to their groups
12. `databricks_mws_permission_assignment.admin` — assigns the `admins` group as workspace ADMIN

Expected apply time: 4–8 minutes (the workspace provisioning waits for Databricks to complete the VPC peering and cluster setup).

```powershell
terraform output workspace_url   # e.g. https://dbc-76ed85a0-8687.cloud.databricks.com
terraform output workspace_id    # e.g. 1234567890123456
```

Open the workspace URL in your browser. It should show the Databricks UI. If you see a "You do not have permission" error, the permission assignment hasn't propagated yet — wait 30 seconds and refresh. Verify the workspace also appears in the **Accounts console → Workspaces** list.

> **Finding workspace ID and URL in the UI:** in the account console (`accounts.cloud.databricks.com`) click the workspace row — the workspace ID is the number in the browser URL bar: `https://accounts.cloud.databricks.com/workspaces/<workspace_id>`. The workspace URL is shown on the configuration page as the **Per-workspace URL**.

---

## Step 4 — Unity Catalog layer

> **Free Edition users start here.** Set `workspace_url` and `workspace_id` from your existing workspace: in the Databricks UI go to the top-right user menu → **User Settings** — or copy the URL from your browser (e.g. `https://1234567890.cloud.databricks.com`). The workspace ID is the number in the URL. You do not need to fill in `state_bucket` — use a local backend instead (remove the `backend.tf` file and run `terraform init` without `-backend-config`).

```powershell
cd environments/dev/03-unity-catalog

cp backend.tfvars.example backend.tfvars
cp terraform.tfvars.example terraform.tfvars
# Edit: paste workspace_url and workspace_id from step 3 outputs
# Also set: admin_user = "your.email@example.com"
```

**Optionally populate `secrets.json`** before applying (the file is gitignored — never commit actual values):

```json
{
  "scopes": [
    {
      "name": "dev",
      "secrets": [
        { "key": "my-api-key", "value": "actual-value-here" }
      ]
    }
  ]
}
```

If you leave `secrets.json` empty (`"secrets": []`) or absent, the scope is created with no secrets — you can add them later with another `terraform apply`.

```powershell
terraform init -backend-config="backend.tfvars"   # quotes required on PowerShell (dot in filename)
terraform validate
terraform plan
terraform apply
```

**Resource creation sequence:**

1. `aws_s3_bucket.catalog` — a dedicated S3 bucket for catalog-level storage (versioning disabled, AES256, public access blocked)
2. `databricks_storage_credential.this` — created **first**, with a hardcoded role ARN string; Databricks generates the real `external_id` here
3. `data.databricks_aws_unity_catalog_assume_role_policy.this` — reads `external_id` from the storage credential; generates the correct IAM trust policy JSON (includes both Databricks' IAM principal and the self-assume statement)
4. `aws_iam_role.catalog_storage` — created with the trust policy from the data source; no two-pass patching needed
5. `data.databricks_aws_unity_catalog_policy.this` — generates the S3 access IAM policy JSON using the provider's built-in data source (keeps permissions in sync as Databricks evolves its requirements)
6. `aws_iam_policy.catalog_storage` + `aws_iam_role_policy_attachment.catalog_storage` — managed policy attached to the role (preferred over inline `aws_iam_role_policy`)
7. **`time_sleep` 30 seconds** — waits for both the trust policy update and the S3 policy attachment to propagate through AWS IAM before Databricks validates
8. `databricks_external_location.catalog` — registers `s3://<bucket>` with the storage credential; Databricks verifies the IAM role can actually assume itself at this point
9. `data.databricks_metastores.all` + local — looks up the auto-provisioned metastore by the region-derived name pattern (`metastore_aws_<region_underscored>`)
10. `databricks_metastore_assignment.this` — assigns the existing metastore to the workspace (no metastore creation — accounts after Nov 2023 already have one per region)
11. `databricks_default_namespace_setting.this` — sets workspace default catalog to `main`
12. `databricks_catalog.this` — with `storage_root` pointing to the external location (trailing `/` required; provider normalizes to this form)
13. `databricks_schema.bronze/silver/gold`
14. **`time_sleep` 15 seconds** — Databricks' permissions API takes a moment to register newly-created schemas; grants immediately after schema creation fail
15. `databricks_grants.catalog/bronze/silver/gold`
16. `databricks_secret_scope.this` — creates secret scopes defined in `secrets.json`
17. `databricks_secret.this` — creates secrets within each scope

**Why catalog-level storage, not metastore-level?** Databricks auto-provisions one metastore per region using Databricks-managed S3 (in Databricks' own AWS account). You cannot reference that storage root from your own Terraform — `databricks_catalog.storage_root` would point to a bucket you don't own. The fix is to create your own S3 bucket and wire it to the catalog via a storage credential and external location.

**The credential-before-role pattern:** `databricks_storage_credential` is created with a hard-coded ARN string (not a Terraform resource reference to `aws_iam_role`). This breaks the circular dependency: storage credential needs the role ARN; the IAM role's trust policy needs the `external_id` from the storage credential. By decoupling the ARN string from the resource reference, Terraform can create the credential first, then create the role with the correct trust policy in one `apply` pass.

Verify in the workspace:

```sql
SHOW CATALOGS;                    -- should include "main"
SHOW SCHEMAS IN main;             -- should show bronze, silver, gold
SHOW GRANTS ON CATALOG main;      -- should show your admin_user
SHOW GRANTS ON SCHEMA main.bronze;
```

---

## Common errors

| Error | Cause | Fix |
|---|---|---|
| Duplicate workspace named `workspace` appears in account console | Clicked "Set up your account" in the AWS Marketplace subscription wizard, which auto-creates a default workspace | Delete it from the account console (no AWS cleanup needed — it uses Databricks-managed storage). Next time, navigate directly to `accounts.cloud.databricks.com` after the subscription confirms instead of using that button |
| `unable to assume role` during `databricks_mws_credentials` | IAM propagation not complete | `time_sleep` 20s in the workspace module handles this; increase to 30s if still failing |
| `BucketAlreadyOwnedByYou` | S3 bucket name not globally unique | Change the prefix in tfvars; bootstrap uses `random_id` to avoid this automatically |
| `account has reached the limit for metastores in region` | Accounts created after Nov 2023 get one auto-provisioned metastore per region; `databricks_metastore` tries to create a second | This codebase does not create a metastore — it uses a data source to look up the existing one. If you see this, an old version of the module is still in state; run `terraform state rm module.unity_catalog.databricks_metastore.this` |
| `EntityAlreadyExists: Role with name X already exists` | Two `aws_iam_role` resources with the same name — the old two-pass IAM patch pattern | Fixed in this codebase by the `databricks_aws_unity_catalog_assume_role_policy` data source; no second role resource |
| `non self-assuming` on `databricks_external_location` | IAM trust policy was just updated; Databricks validated before AWS propagated the change | `time_sleep` 30s after `aws_iam_role_policy_attachment` handles this |
| `Provider produced inconsistent final plan` for `storage_root` | Databricks provider appends a trailing `/` to `storage_root`; plan was computed without it | Fixed in code: `storage_root = "${databricks_external_location.catalog.url}/"` |
| `securable_full_name "main.bronze" is not a valid name` or `invalid schema name: 'bronze'` | Schema grants run immediately after schema creation; Databricks' permissions API hasn't registered the schema yet | `time_sleep` 15s after schema creation in the module handles this |
| `default_catalog_name` deprecation warning | `databricks_metastore_assignment.default_catalog_name` is deprecated (still works, but no longer recommended) | Fixed: use `databricks_default_namespace_setting` resource instead |
| `Unable to view page` / "not assigned to workspace" on first login | User not in the `admins` group or permission assignment not yet propagated | Check `iam.json` has your email in the `admins` group; re-run `terraform apply` in `02-workspace`; wait 30s and refresh |
| `User with username X already exists` on `databricks_user` | User was created manually in the account console before Terraform ran | Import: `terraform import 'module.workspace.databricks_user.this["x@example.com"]' <user_id>` then re-apply |
| Secret value visible in `terraform plan` output | `sensitive = true` missing on the `secrets` variable | Declared correctly in this codebase; if you copied the variable elsewhere, add `sensitive = true` |
| Backend init fails with `NoSuchBucket` | Bootstrap not applied yet | Run `terraform apply` in `bootstrap/` first |
| `workspace_url` or `workspace_id` empty in UC tfvars | Forgot to fill in from step 3 outputs | `terraform -chdir=../02-workspace output workspace_url` |
| Windows Defender blocks provider binary | Antivirus scanning new `.exe` | Add `.terraform/providers/` to Defender exclusions; `terraform validate` retries automatically |

---

## Destroy (reverse order)

Always destroy in reverse layer order. Destroying workspace first while the metastore still references it leaves orphaned state.

```powershell
# From 03-unity-catalog/
terraform destroy

# From 02-workspace/
terraform destroy

# From 01-networking/
terraform destroy

# Only destroy bootstrap if you want to delete the state bucket too
# (terraform destroy in bootstrap/ will fail by default since force_destroy = false)
```

To delete the state bucket itself, change `force_destroy = false` to `true` in `bootstrap/main.tf`, run `terraform apply`, then `terraform destroy`.

---

## What comes next

This deployment gives you a working, standard workspace. To harden it toward production:

- **Private Link** — add VPC endpoints for the Databricks REST API and SCC relay so traffic never leaves the AWS backbone. See Ch 29 §Security Reference Architecture.
- **Customer-Managed Keys** — add two KMS keys (workspace storage + managed services) as shown in the SRA `cmk.tf`.
- **Terragrunt** — eliminate the DRY violation between dev and prod by extracting common configuration into a root `terragrunt.hcl`. See Ch 29 §Terragrunt.
- **CI/CD** — add a GitHub Actions workflow that runs `terraform plan` on PRs and `terraform apply` on merge to main. See Ch 29 §CI/CD.

---

## Summary

- The state bucket is bootstrapped once; all other layers use S3 native locking (`use_lockfile = true`)
- Three layers deploy in strict order: networking → workspace → unity-catalog
- Each layer reads upstream outputs via `terraform_remote_state` (networking) or explicit variable (workspace URL for UC)
- Users and groups are defined in `iam.json` (committed); the `admins` group is assigned workspace ADMIN via `databricks_mws_permission_assignment` — membership changes require only a JSON edit, not HCL
- Accounts created after Nov 2023 get one auto-provisioned metastore per region; the UC module looks it up via `data "databricks_metastores"` rather than creating one
- Catalog-level storage (your own S3 bucket + storage credential + external location) is required because you cannot set `storage_root` to the auto-provisioned metastore's Databricks-managed bucket
- The `databricks_aws_unity_catalog_assume_role_policy` data source breaks the storage-credential ↔ IAM-role circular dependency: create the credential first (hardcoded ARN string, no Terraform resource dependency), then let the data source read the real `external_id` and generate the correct trust policy for the IAM role in the same `apply` pass
- Three `time_sleep` resources absorb propagation delays: 20s after workspace cross-account IAM, 30s after catalog IAM role + policy attachment, 15s after schema creation before applying grants
- `databricks_default_namespace_setting` sets the workspace default catalog (replaces the deprecated `default_catalog_name` on `databricks_metastore_assignment`)
- Secret scopes and secrets are defined in `secrets.json` (gitignored); the file is optional — if absent or empty, the layer applies cleanly with no secrets created
- Dev and prod share the same modules; only tfvars, `iam.json`, and `secrets.json` differ
