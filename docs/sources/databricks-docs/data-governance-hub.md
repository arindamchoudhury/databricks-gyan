# Data governance with Databricks (Unity Catalog)

> **Source:** [docs.databricks.com/aws/en/data-governance](https://docs.databricks.com/aws/en/data-governance/)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-09
> **Tags:** data-governance, unity-catalog, access-control, abac, lineage, data-quality-monitoring, opensharing, clean-rooms, marketplace, audit, system-tables, I7, E2, A6, A7
> **Type:** documentation

## Summary

The hub page for the whole **data governance** area. Defines governance as a framework of policies, processes, roles, and technical controls keeping data secure, trustworthy, and responsibly used across its lifecycle. Then maps **Unity Catalog** onto six governance pillars: **access control, discoverability, data quality monitoring, collaboration/sharing, auditing**, plus a **legacy tools** section UC replaces. This page is the index that ties together I7 (UC governance), E2 (privacy/compliance), A6 (monitoring/quality), and A7 (sharing/interop) in the learning path.

> Scope boundary: this page is governance **of data via Unity Catalog**. Adjacent security topics — authentication, network config, encryption, privacy compliance — live under "Security and compliance" and "Compliance overview", not here.

## Key points

- **Five named components of governance**: access control & security · data lineage & observability · data quality management · metadata management · compliance enforcement.
- **UC as the complete solution** delivers six capabilities: data unification, access control, discoverability, quality, collaboration/sharing, auditing.
- UC governs **structured AND unstructured** data, multiple formats, **AI assets (ML models)** too — not just tables. Open-source, multi-platform, deeply integrated into Databricks.
- Access control is **hierarchical** — account level down to **table rows and columns** — and reaches data **wherever it lives** (UC managed storage, cloud storage, external DB systems).
- **Data quality monitoring** is a distinct UC feature: anomaly detection across a catalog/schema + profiling of an individual table.
- Sharing tier = **OpenSharing + Clean Rooms + Marketplace** (cross-org, cross-platform).
- Auditing = **audit logs surfaced via system tables** (system tables = easiest way to query account audit logs).
- **Legacy (avoid):** Hive-metastore Table access control + IAM role credential passthrough — UC replaces both.

## Notes

### Six governance pillars under Unity Catalog

**1. Data access control**

Hierarchical privilege model: grant users / groups / service principals access from **account level down to table rows and columns**. Controls assets in UC dedicated storage **or** other platforms (cloud storage, DB systems) — the point is UC gives potential access to all data wherever it sits, while controlling and tracking usage. Tasks linked from the hub:

- **Manage privileges** — securable objects UC manages + how to control access (→ [[external-access]], [[tables-concepts]] privilege matrix).
- **Manage attribute-based access control (ABAC)** — policy-driven access by attribute/tag, not just per-object grants.
- **Manage identities** — identities in the UC context (users, groups, service principals).
- **Fine-grained access control** — **row filters and column masks** (→ E2, [[learning-path]] line 531).
- **Manage access to external storage and data platforms** — cloud storage, external data platforms, external non-data services.
- **Manage access from external platforms** — inbound access via **Apache Iceberg or open-source Unity Catalog APIs** (→ [[external-access]], A7).

**2. Data discoverability**

- **Catalog Explorer** — browse/search data + AI assets by name and metadata (comments, tags).
- **Catalog browsers** — discovery built into notebook + new SQL editors.
- **AI-generated comments** — auto-documentation of assets to aid discovery.
- **Table insights** — Catalog Explorer UI showing most frequent users + queries of any table.
- **Data lineage** — capture + visualize data flow across the org (feature/model lineage covered separately under "Feature governance and lineage").
- **Entity relationship diagrams (ERD)** — relationships for tables with foreign keys defined (ties to the informational PK/FK from [[tables-concepts]]).

**3. Data quality monitoring**

Quality tooling is integrated into Delta Lake, Spark, and Databricks broadly. UC adds:

- **Data quality monitoring** — **anomaly detection** across all tables in a catalog/schema + **data profiling** of statistical properties/quality of an individual table.
- **Certified and deprecated system tags (Private Preview)** — label catalogs/schemas/tables with quality or lifecycle status to enforce governance, aid discovery, raise trust in analytics/AI.

**4. Data collaboration and sharing**

UC lets users collaborate on the same data across all account workspaces **in the same region**. For cross-region / cross-org / cross-platform:

- **OpenSharing** — secure sharing of data + AI assets with users outside the org, Databricks or not (the renamed Delta Sharing).
- **Clean Rooms** — Databricks-managed environment where multiple participants (Databricks + non-Databricks) collaborate **without sharing underlying data** with each other.
- **Databricks Marketplace** — open forum for exchanging data + AI products; also supports a private data exchange.

**5. Auditing**

Audit logs capture fine-grained detail on **who accessed which dataset and what they did**. UC adds **system tables** — the easiest way to access/query account audit logs. See Audit log reference + System tables reference.

**6. Legacy governance tools (UC replaces — avoid)**

- **Table access control** — legacy model to programmatically grant/revoke on Hive-metastore objects.
- **IAM role credential passthrough** — legacy: users auto-authenticate to S3 from clusters using their Databricks login identity.

## Quotes worth keeping

> "Unity Catalog gives your users potential access to all of your data, no matter where it is, from within Databricks, and that Unity Catalog controls their access and tracks their data usage." (Data access control)

> "This page focuses on the governance of data using Unity Catalog. Related security topics, such as authentication, network configuration, data encryption, and privacy compliance, are covered in Security and compliance and Compliance overview." (intro — scope boundary)

## Open questions

- "Certified and deprecated system tags" are Private Preview — GA timing unknown.
- Hub mentions ABAC as a managed task; depth (policy syntax, evaluation order vs grants) not on this page.

## Related sources

- [[external-access]] — the "manage access from external platforms" task (Iceberg/UC REST APIs, credential vending) detailed.
- [[tables-concepts]] — securable objects + the per-operation privilege matrix this hub's access-control pillar points at.
- [[managed-tables]] / [[external-tables]] — the governed objects; external tables are where UC governance reaches into your own cloud storage.
- [[catalog-commits]] — the substrate enabling enforceable constraints + safe external-engine writes referenced under access from external platforms.
