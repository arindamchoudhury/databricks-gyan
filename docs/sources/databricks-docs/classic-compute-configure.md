# Classic compute configuration reference

> **Source (AWS):** [docs.databricks.com/aws/en/compute/configure](https://docs.databricks.com/aws/en/compute/configure)
> **Source (GCP):** [docs.databricks.com/gcp/en/compute/configure](https://docs.databricks.com/gcp/en/compute/configure)
> **Added:** 2026-06-16
> **Source updated:** 2026-06-11
> **Tags:** compute, classic-compute, configuration, autoscaling, EBS, spark-config, instance-types, gcp, B1
> **Type:** documentation

## Summary

Full configuration reference for classic compute (all-purpose and job clusters) covering both AWS and GCP. Covers every setting in the compute creation UI: runtime version, instance types, autoscaling behaviour, advanced instance options (GPU, Graviton/Fleet on AWS; local SSDs on GCP), tags, access modes, storage, logging, and Spark configuration. Cloud-specific sections are labelled. The overview page ([[classic-compute-overview]]) covers what classic compute is and permission levels; this page covers how to configure it.

## Key points

- **Compute policy** gates what users can configure — only admins or users with "Unrestricted cluster creation" can configure everything freely.
- **Autoscaling** behaves differently on Premium (optimised) vs Standard (exponential) plans; don't mix with `spark.dynamicAllocation.enabled`.
- **Autoscaling is not available for `spark-submit` jobs** and has limitations with Structured Streaming scale-down.
- **Driver node**: always on-demand even when workers use spot; defaults to same type as worker; consider upsizing if you `collect()` large datasets.
- **Graviton** instance types offer best price/performance but have notable limitations (no DCS, no Databricks SQL, no GovCloud, no Python UDFs below DBR 15.2, no mixed Graviton/non-Graviton). *AWS only.*
- **Fleet** instance types auto-pick the best spot instance at launch; no GPU support. *AWS only.*
- **AWS Capacity Blocks** reserve compute capacity for a specific time+AZ; no equivalent on GCP.
- **Autoscaling local storage**: auto-attaches EBS GP3 volumes (AWS) or resizes Zonal SSD PD (GCP) up to 5 TB/instance; never detached mid-run.
- **Google service account** (GCP) replaces instance profiles (AWS) as the mechanism for accessing cloud storage without static keys.
- **HA zone** (GCP): `HA` availability zone option spreads instances across zones in a region; may increase inter-zone egress costs.
- **Log delivery** to a Volume requires Standard mode or Dedicated-to-user (not Dedicated-to-group).
- **Local disk encryption** available (Public Preview) via Clusters API only; has performance overhead.
- **Spark secrets in config**: use `{{secrets/<scope>/<name>}}` syntax instead of plaintext passwords.

## Notes

### Compute policy

Policies constrain which configuration options appear when a user creates compute. Users without "Unrestricted cluster creation" entitlement can *only* create compute via assigned policies. The **Personal Compute** policy (single-machine resources) is available to all users by default.

### Runtime version

**Recommendations by use case**

- All-purpose compute → most current runtime
- Job compute (production) → LTS version
- Data science / ML → Databricks Runtime ML version

All runtimes include Apache Spark.

### Photon acceleration

Enabled by default on DBR 9.1 LTS and above. Toggle on the creation form.

### Worker and driver node types

A compute resource has one **driver node** and zero or more **worker nodes**. Driver defaults to the same type as workers; can be set independently.

> ⚠️ AWS: "Do not use a pool with spot instances as your driver type. Select an on-demand driver type to prevent your driver from being reclaimed."
> ⚠️ GCP: "Do not use a pool with preemptible VM instances as your driver type."

The driver maintains notebook state, the SparkContext, and the Spark master. Upsize the driver if you plan to `collect()` large results into the notebook. Detach unused notebooks from the driver to avoid state bloat.

To run a Spark job, you need at least one worker. Workers run Spark executors and ancillary services.

#### Flexible node types

Fall back to alternative compatible instance types when the primary is unavailable. Improves launch reliability by reducing capacity failures.

#### Worker IP addresses

Each worker gets two private IPs: one for Databricks internal traffic, one for the Spark container (intra-cluster). This isolates traffic between multiple compute resources.

#### GPU instance types

For deep learning and computationally demanding tasks. *AWS:* Amazon EC2 P2 instances deprecated.

#### AWS Graviton instance types

Arm64-based processors with the best price-to-performance ratio on EC2 per Databricks.

**Minimum runtime versions**

- Non-Photon: DBR 9.1 LTS+
- Photon: DBR 10.2+
- ML: DBR 15.4 LTS ML+

**Limitations**

- Python UDFs: not supported below DBR 15.2
- No Databricks Container Services
- No Databricks SQL
- No Databricks on AWS GovCloud
- No access to workspace files / Git folders from web terminals
- Cannot mix Graviton and non-Graviton instance types in the same cluster (different runtimes required)

Precision: basic floating-point operations unchanged; single triangle functions differ from Intel by at most 1.11e-16. Third-party tool/library support may be affected.

If an instance type isn't available in the workspace region → compute creation fails. Always verify regional availability.

#### AWS Fleet instance types

Variable instance types that resolve to the best available instance of the same size class (e.g., `m-fleet.xlarge` → whichever `.xlarge` general-purpose instance has best spot capacity and price). Uses AWS Spot Placement Score API. Memory and core count are guaranteed to match the fleet type chosen.

**Limitations**

- Spot bid percentage settings via API/JSON have no effect on fleet workers
- No GPU support
- Not available on some older workspaces

#### GCP instance types with local SSDs

Some GCP instance types include locally attached SSDs for shuffle files and cache data. Local SSDs are encrypted with default Google Cloud server-side encryption and use automatic disk caching.

- Supported on first- and second-generation types: n1, n2, n2d (and others — check GCP pricing estimator for current list)
- Instance types with `-lssd` suffix have a fixed, built-in SSD count; others allow you to choose the count under **Advanced > Instances > Local SSD**
- The **Default** option uses the standard SSD configuration for the instance type

> 💡 Unlike AWS where shuffle storage is added via EBS, GCP shuffle/cache storage comes from local SSDs provisioned with the instance type.

**GCP default worker node storage** (provisioned automatically):

| Storage | Size/Count | Purpose |
|---|---|---|
| Boot disk | 30 GB | Host OS + Databricks services |
| Container root volume | 150 GB | Spark worker, services, logs |
| Local SSDs | 375 GB each | Shuffle files and cache data |
| Remote SSD | 80 GB (or 0 GB if local SSD present), autoscales | Overflow / autoscaling storage |

### Single-node compute

Intended for small datasets and non-distributed workloads (single-node ML libraries).

**Properties**

- Runs Spark locally; driver acts as both master and worker
- Spawns one executor thread per logical core, minus 1 for the driver
- All logs (`stderr`, `stdout`, `log4j`) go to the driver log
- **Cannot be converted to multi-node**

**Limitations vs multi-node**

- No GPU scheduling on single-node
- Large-scale data processing will exhaust resources
- Cannot scale to 0 workers (that's a multi-node constraint; single-node is always 0 workers)
- Parquet files with UDT columns fail with "The Spark driver has stopped unexpectedly and is restarting." Workaround: disable the native Parquet reader via Spark config property

### Autoscaling

Dynamically reallocates workers based on job characteristics.

**When the cloud terminates instances below the minimum**, Databricks continuously retries to re-provision to maintain the minimum.

**Scope restrictions**

- Not available for `spark-submit` jobs
- Limited ability to scale *down* for Structured Streaming workloads — use Lakeflow Spark Declarative Pipelines with enhanced autoscaling instead

> ⚠️ Never enable `spark.dynamicAllocation.enabled` alongside Databricks autoscaling. Conflicting decisions → executor churn, `NODES_LOST` errors, stuck tasks.

**Resize example** (reconfiguring to 5–10 autoscale):

| Initial workers | Workers after |
|---|---|
| 6 | 6 |
| 12 | 10 (capped at max) |
| 3 | 5 (raised to min) |

#### Optimised autoscaling (Premium plan)

- Scales up from min to max in at most 2 scaling events
- Can scale down even on non-idle compute by inspecting shuffle file state
- Scale-down window: **40 s** for job compute, **150 s** for all-purpose compute
- Tunable via `spark.databricks.aggressiveWindowDownS` (max 600 s = 10 min; the `S` suffix = seconds)

#### Standard autoscaling (Standard plan)

- Starts by adding 8 nodes, then scales up exponentially
- Scales down when 90% of nodes are not busy for 10 minutes and compute has been idle for at least 30 seconds
- Scales down exponentially, starting with 1 node

#### Autoscaling with pools

- Pool's idle instance count must be ≥ min compute size, or pool benefit is lost (startup time equals non-pool startup)
- Max compute size must be ≤ pool max capacity, or compute creation fails

### Advanced performance settings

**Spot instances (AWS)**: first instance (driver) is always on-demand; subsequent workers use spot.

**Preemptible instances (GCP)**: much cheaper than on-demand instances but "Google Cloud might stop (preempt) these instances if it requires access to those resources for other tasks." Availability varies with GCE capacity. Enable via the UI checkbox or instance pool config; when unavailable, system defaults to on-demand unless configured otherwise.

**Automatic termination**: terminates after a configurable inactivity period (minutes since last command).

### Tags

Key-value pairs applied to cloud resources (VMs, disk volumes) and usage logs. Useful for cost monitoring by group.

> ⚠️ For pool-launched compute, custom tags appear only in DBU usage reports — they do **not** propagate to cloud resources.

### Access modes

See [[classic-compute-overview]] for the Standard vs Dedicated summary. Additional detail from this page:

- Default is **Auto**: uses Standard unless ML runtime or DBR < 14.3 is selected, in which case it switches to Dedicated.
- "Databricks recommends that you use standard access mode unless your required functionality is not supported."
- Init scripts and libraries supported by all access modes on DBR 13.3 LTS+; requirements and support levels vary.

### Cloud identity for storage access

The mechanism for accessing cloud storage without static keys differs by cloud:

**AWS — Instance profiles**: Databricks recommends **Unity Catalog external locations** over instance profiles for S3 access. If you do use an instance profile:

> ⚠️ "Once a compute resource launches with an instance profile, anyone who has attach permissions to this compute resource can access the underlying resources controlled by this role." Use Compute permissions to restrict access.

**GCP — Google service account**: Associate a Google service account with compute via **Advanced > Google service account** (enter the service account email). The service account must be in the same project as the Databricks setup account. Used to authenticate with GCS and BigQuery data sources.

### Availability zones

Default is **Auto**: Databricks picks the AZ based on available IPs in workspace subnets; retries other AZs on insufficient capacity errors. Auto-AZ only applies at startup — nodes stay in the chosen AZ until restart.

Set a specific AZ when using reserved instances in a particular AZ (AWS) or to target a zone where you have resources.

**GCP — High availability (HA) zone**: Select `HA` as the availability zone to spread instances across multiple zones in the region, reducing single-zone failure risk. Trade-off: may increase cost due to inter-zone egress charges.

### AWS Capacity Blocks *(AWS only)*

Reserve compute capacity for a specific time and AZ. No GCP equivalent. Setup:

1. Purchase the Capacity Block in the AWS portal
2. Tag the compute resource: `X-Databricks-AwsCapacityBlockId` = your Capacity Block ID
3. Disable spot instances
4. Select the AZ assigned by AWS (must match workspace subnet)

> Capacity Blocks must be *active* before launching compute resources using them.

### Autoscaling local storage

Databricks monitors free disk space on workers and automatically expands storage when a worker runs low. Same 5 TB limit on both clouds; behaviour differs by platform:

**AWS**: auto-attaches new **EBS GP3** volumes.

- Volumes are **never detached mid-run** — only when the instance is returned to AWS
- Default AWS account cap: 50 TiB; request an increase if needed
- Use with autoscaling compute or auto-termination to keep EBS costs in check

**GCP**: auto-**resizes** the existing **Zonal SSD PD** (persistent disk) attached to the worker before it runs out of space.

Both: limit is **5 TB total disk per instance** (including local storage).

### AWS EBS volumes (fixed)

When autoscaling local storage is *disabled* on AWS, you can configure fixed EBS volumes. Default volumes provisioned per worker:

| Volume | Size | Purpose |
|---|---|---|
| Encrypted EBS root | 30 GB | Host OS + Databricks services |
| Encrypted EBS container root | 150 GB | Spark worker, services, logs |
| Encrypted EBS worker log *(HIPAA only)* | 75 GB | Databricks logs |

**EBS shuffle volumes** (General Purpose SSD): add extra volumes for instance types without local disk, or to increase Spark shuffle storage. Databricks encrypts these for both on-demand and spot instances.

**SSD type**: gp2 or gp3; Databricks recommends gp3. Default gp3 configuration matches gp2 maximum performance for equivalent volume size.

### Local disk encryption (Public Preview)

Encrypts shuffle data and ephemeral data on locally attached instance disks. Key is generated per node, lives in memory during use, stored encrypted on disk, and destroyed with the node.

> ⚠️ "Your workloads may run more slowly because of the performance impact of reading and writing encrypted data to and from local volumes."

Enabled only via the Clusters API: set `enable_local_disk_encryption: true`.

### Spark configuration

Set Spark properties in **Advanced > Spark tab**, one `key value` pair per line. Alternatively use `spark_conf` in the create/update Cluster API. Admins can enforce Spark configurations via compute policies.

**Secrets in Spark config** — never put passwords in plaintext:

```
spark.<property-name> {{secrets/<scope-name>/<secret-name>}}
```

Example: `spark.password {{secrets/acme-app/password}}`

### Compute log delivery

Driver, worker, and event logs delivered every 5 minutes, archived hourly. Delivery continues until the compute resource is terminated.

**Destination options**

- **Volumes** (recommended) — Unity Catalog volume path; most secure. Requires Standard mode *or* Dedicated mode assigned to a user (not a group). Compute owner or assigned user needs `READ VOLUME` + `WRITE VOLUME`.
- **S3** *(AWS only)* — requires instance profile with `PutObject` and `PutObjectAcl` permissions.
- **DBFS** (legacy) — only available if DBFS root/mounts are not disabled.

> 💡 GCP: S3 is not available. GCP log delivery supports Volumes and DBFS only.

Logs land in a subfolder named after the cluster ID: e.g., `/Volumes/catalog/schema/volume/06308418893214/`.

### Environment variables

Set custom environment variables accessible from init scripts via **Advanced > Spark tab > Environment variables**, or via `spark_env_vars` in the Cluster API. Databricks-predefined environment variables cannot be overridden.

## Open questions

- ❓ What specific Spark config property disables the native Parquet reader for the UDT single-node workaround?
- ❓ What are the support-level differences for init scripts across Standard vs Dedicated access modes on DBR 13.3 LTS+?

## Related sources

- [[classic-compute-overview]] — permission levels, access mode summary, creation entitlements; this page is the companion config reference.
- [[serverless-limitations]] — covers what is not available on serverless (no Spark config, no custom instance types, no EBS, no init scripts).
- [[serverless-notebooks]], [[serverless-jobs]], [[serverless-pipelines]] — the serverless alternative path; no cluster config needed.
