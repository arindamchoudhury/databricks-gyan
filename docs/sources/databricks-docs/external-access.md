# Access Databricks data using external systems

> **Source:** [docs.databricks.com/aws/en/external-access/](https://docs.databricks.com/aws/en/external-access/)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-04
> **Tags:** unity-catalog, external-access, iceberg-rest-catalog, unity-rest-api, credential-vending, compatibility-mode, opensharing, external-tables, external-volumes, delta-clients, iceberg-clients, A7, I8, B4
> **Type:** documentation

How UC-governed data is made available to **trusted external systems inside your org** — distinct from cross-org sharing (that's OpenSharing). Don't confuse the two scopes: **external access** = systems *inside* your org reading UC data (this page); **OpenSharing** = sharing *outside* the org.

> "Unity Catalog provides integrations to Delta Lake clients using the Unity REST API and Apache Iceberg clients using the Iceberg REST catalog."

UC exposes data via two open APIs — the **Unity REST API** (Delta clients) and the **Iceberg REST catalog** (Iceberg clients: Spark, Flink, Trino, Snowflake) — plus **credential vending** (external clients inherit UC privileges via temporary creds), **compatibility mode** (read-only via a cloned copy for clients lacking REST-API support), and direct **cloud URI** access for external tables/volumes.

## Access patterns by UC object

| UC object | Formats | Access patterns |
|---|---|---|
| **Managed tables** | Delta, Iceberg | Unity REST API, Iceberg REST catalog, OpenSharing, compatibility mode (read-only) |
| **MVs / streaming tables** | Delta, Iceberg | Read-only; external access if client supports Delta 4.0 / Iceberg v3, else compatibility mode |
| **External tables (Delta)** | Delta | Unity REST API, Iceberg REST catalog, OpenSharing, cloud URIs |
| **External tables (other)** | CSV, JSON, Avro, Parquet, ORC, text | Unity REST API, cloud URIs |
| **External volumes** | all data types | Cloud URIs |
| **Foreign tables\*** | Delta, Iceberg | Unity REST API, Iceberg REST catalog (Preview), OpenSharing |
| **Foreign tables\*** | CSV, JSON, Avro, Parquet, ORC, text | Unity REST API, cloud URIs |

\* Only foreign tables federated via **catalog federation**; for fresh reads from external engines, periodically refresh metadata with Lakeflow jobs.

> **Compatibility mode** gives **read-only** access to clients that don't support the REST APIs by exposing a **cloned copy** of the data.

## Credential vending

> "Unity Catalog credential vending allows users to configure external clients to inherit privileges on data governed by Databricks."

Both Iceberg and Delta clients support it — the auth mechanism behind the REST-API access patterns above.

## Delta clients (Unity REST API)

Read/write/create UC managed + external Delta tables from supported Delta clients.

> **BETA:** creating and writing to UC **managed** tables from Delta clients is in Beta.

For **external tables**, UC does **not** govern direct cloud-storage reads/writes — configure cloud-account policies + credentials yourself. Don't modify the same Delta table in S3 from different workspaces/clients (corruption risk; use **Cloudflare R2** for multi-client writes). Confirm reader/writer protocols (LC tables need writer v7 / reader v3 — see [[liquid-clustering]]).

## Iceberg clients (Iceberg REST catalog)

UC gives Iceberg clients **read, write, and create** for registered tables. Supported: **Apache Spark, Apache Flink, Trino, Snowflake**.

## Share read-only across domains (OpenSharing)

Grants read-only access to managed/external Delta tables across domains (zero-copy-read systems: SAP, Amperity, Oracle); also backs Databricks Marketplace. Cross-org detail belongs to the OpenSharing protocol (A7).

## Non-Delta tabular data & non-tabular data

> "Unity Catalog does not govern reads and writes performed directly against cloud object storage from external systems, so you must configure additional policies and credentials in your cloud account…"

**External tables** (Parquet/ORC/CSV/JSON/…): data files live at a cloud URI read directly; non-Delta formats give **no transactional guarantees** (multi-system R/W risks corruption), and UC may miss externally-written partitions — run `MSCK REPAIR TABLE` regularly. **External volumes**: non-tabular files via get/put APIs; OpenSharing can share volumes to other Databricks accounts but **not** to external systems.

Related: [[managed-tables]], [[tables-concepts]], [[foreign-tables]], [[liquid-clustering]], [[predictive-optimization]], [[data-governance-hub]].
