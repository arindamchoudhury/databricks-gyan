# Access Databricks data using external systems

> **Source:** [docs.databricks.com/aws/en/external-access/](https://docs.databricks.com/aws/en/external-access/)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-04
> **Tags:** unity-catalog, external-access, iceberg-rest-catalog, unity-rest-api, credential-vending, compatibility-mode, opensharing, external-tables, external-volumes, delta-clients, iceberg-clients, A7, I8, B4
> **Type:** documentation

## Summary
Overview of how UC-governed data is made available to **trusted external systems inside your org** (vs cross-org sharing, which is OpenSharing). Unity Catalog exposes data to outside clients through two open APIs — the **Unity REST API** (Delta clients) and the **Iceberg REST catalog** (Iceberg clients) — plus **credential vending** (external clients inherit UC privileges via temporary creds), **compatibility mode** (read-only access for clients that don't support the REST APIs, via a cloned copy), and direct **cloud URI** access for external tables/volumes. The page is the access-pattern map per UC object type.

## Key points

- Two scopes, don't confuse them: **external access** = trusted systems *inside* your org reading UC data; **OpenSharing** = sharing *outside* the org. This page is the former.
- **Unity REST API** → Delta clients; **Iceberg REST catalog** → Iceberg clients (Spark, Flink, Trino, Snowflake).
- **Credential vending** = external clients inherit UC privileges via temporary credentials (both Delta + Iceberg clients).
- **Compatibility mode** = read-only access for clients lacking REST-API support; they read a *cloned copy* of the data.
- Writing/creating UC **managed** tables from Delta clients is **Beta**.
- For **external tables** + **external volumes**: UC does **not** govern direct cloud-storage reads/writes — you must set cloud-account policies yourself; non-Delta formats have no transactional guarantees.

## Notes

### Access patterns by UC object

| UC object | Formats | Access patterns |
|---|---|---|
| **Managed tables** | Delta, Iceberg | Unity REST API, Iceberg REST catalog, OpenSharing, compatibility mode (read-only) |
| **Materialized views / streaming tables** | Delta, Iceberg | Read-only. External access for pipelines if client supports Delta 4.0 / Iceberg v3; compatibility mode for older clients. Unity REST API, Iceberg REST catalog, file access (via compatibility mode) |
| **External tables (Delta)** | Delta | Unity REST API, Iceberg REST catalog, OpenSharing, cloud URIs |
| **External tables (other)** | CSV, JSON, Avro, Parquet, ORC, text | Unity REST API, cloud URIs |
| **External volumes** | all data types | Cloud URIs |
| **Foreign tables*** | Delta, Iceberg | Unity REST API, Iceberg REST catalog (Preview), OpenSharing |
| **Foreign tables*** | CSV, JSON, Avro, Parquet, ORC, text | Unity REST API, cloud URIs |

\* Only foreign tables federated via **catalog federation** are supported. For fresh reads from external engines on foreign tables, periodically refresh metadata with Lakeflow jobs.

> **Compatibility mode** (managed tables, MVs, streaming tables): gives **read-only** access to clients that don't support the REST APIs, by exposing a **cloned copy** of the data.

### Credential vending

UC credential vending lets external clients **inherit privileges** on UC-governed data via temporary credentials. Both Iceberg and Delta clients support it. (This is the auth mechanism behind the REST-API access patterns above.)

### Access tables with Delta clients (Unity REST API)

Read/write/create UC managed + external Delta tables from supported Delta clients via the **Unity REST API**.

> **BETA:** creating and writing to UC **managed** tables from Delta clients is in Beta.

- **External tables:** UC does **not** govern reads/writes done directly against cloud object storage — configure cloud-account policies + credentials yourself.
- Don't modify the same Delta table in S3 from different workspaces/clients → corruption/loss risk. Use **Cloudflare R2** if you need writes from multiple clients.
- Confirm what reader/writer protocols + table features your client supports (see delta.io) — LC tables need writer v7 / reader v3 (see [[liquid-clustering]]).

### Access tables with Iceberg clients (Iceberg REST catalog)

UC gives Iceberg clients **read, write, and create** support for tables registered to UC. Supported clients: **Apache Spark, Apache Flink, Trino, Snowflake**.

### Share read-only across domains (OpenSharing)

OpenSharing grants read-only access to managed/external Delta tables across domains. Zero-copy-read systems: **SAP, Amperity, Oracle**. Also backs Databricks Marketplace and can grant read-only access to customers/partners. (Cross-org sharing detail belongs to the OpenSharing/Delta Sharing protocol — A7 in the learning path.)

### Non-Delta tabular data (external tables)

External tables support Parquet, ORC, CSV, JSON, etc. Data files live in a cloud URI location; other systems read them directly from object storage.

- UC does **not** govern direct cloud-storage access → set your own cloud policies.
- Non-Delta formats give **no transactional guarantees** → multi-system R/W risks consistency issues + corruption.
- UC may miss new partitions written externally → run `MSCK REPAIR TABLE table_name` regularly to register new files.

### Non-tabular data (external volumes)

Use external volumes for non-tabular files read/written by external systems. UC doesn't govern direct cloud-storage access (set cloud policies). Volumes provide APIs/SDKs for get/put. OpenSharing can share volumes to other Databricks accounts but **does not** integrate with external systems.

## Quotes worth keeping

> "Unity Catalog provides integrations to Delta Lake clients using the Unity REST API and Apache Iceberg clients using the Iceberg REST catalog." (What external access does Databricks support?)

> "Unity Catalog credential vending allows users to configure external clients to inherit privileges on data governed by Databricks." (Credential vending)

> "Unity Catalog does not govern reads and writes performed directly against cloud object storage from external systems, so you must configure additional policies and credentials in your cloud account…" (External tables — repeated for volumes)

## Open questions

- Compatibility-mode "cloned copy" — is that the same managed-table Compatibility Mode noted in [[managed-tables]], and how/when is the clone refreshed? Page doesn't say.
- Iceberg REST catalog on foreign tables is "Preview" — GA timeline not stated.

## Related sources

- [[managed-tables]] — names the same managed-only features (credential vending, Compatibility Mode); this page is the cross-engine access map for them.
- [[tables-concepts]] — the managed/external/foreign/volume object types whose access patterns this page tabulates.
- [[liquid-clustering]] — the writer-v7/reader-v3 protocol gate that decides whether an external Delta client can read a clustered table.
- [[predictive-optimization]] — excludes external tables + OpenSharing recipients, the same external surface this page governs.
