# Data governance with Databricks (Unity Catalog)

> **Source:** [docs.databricks.com/aws/en/data-governance](https://docs.databricks.com/aws/en/data-governance/)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-09
> **Tags:** data-governance, unity-catalog, access-control, abac, lineage, data-quality-monitoring, opensharing, clean-rooms, marketplace, audit, system-tables, I7, E2, A6, A7
> **Type:** documentation

The hub page for the whole **data governance** area. Governance is a framework of policies, processes, roles, and technical controls keeping data secure, trustworthy, and responsibly used across its lifecycle — with five named components: access control & security, data lineage & observability, data quality management, metadata management, and compliance enforcement. The page maps **Unity Catalog** onto **six governance pillars**, and UC governs **structured AND unstructured** data, multiple formats, and **AI assets (ML models)** — not just tables.

> "This page focuses on the governance of data using Unity Catalog. Related security topics, such as authentication, network configuration, data encryption, and privacy compliance, are covered in Security and compliance and Compliance overview."

## 1. Data access control

> "Unity Catalog gives your users potential access to all of your data, no matter where it is, from within Databricks, and that Unity Catalog controls their access and tracks their data usage."

A **hierarchical** privilege model from the account level **down to table rows and columns**, reaching data wherever it lives (UC managed storage, cloud storage, external DB systems). Tasks: **manage privileges** (securable objects), **ABAC** (policy-driven access by attribute/tag), **manage identities**, **fine-grained access control** (row filters + column masks → E2), **manage access to external storage/platforms**, and **manage access from external platforms** (inbound via Apache Iceberg or open-source UC APIs → [[external-access]], A7).

## 2. Data discoverability

**Catalog Explorer** + catalog browsers (in notebooks and the SQL editor); **AI-generated comments** (auto-documentation); **table insights** (most frequent users/queries); **data lineage**; **entity relationship diagrams (ERD)** for tables with foreign keys (the informational PK/FK from [[tables-concepts]]).

## 3. Data quality monitoring

A distinct UC feature: **anomaly detection** across all tables in a catalog/schema + **data profiling** of an individual table. Plus **certified and deprecated system tags** *(Private Preview)* to label catalogs/schemas/tables with quality or lifecycle status.

## 4. Data collaboration and sharing

UC shares data across all workspaces **in the same region**. For cross-region / cross-org / cross-platform: **OpenSharing** (the renamed Delta Sharing — share data + AI assets with anyone, Databricks or not), **Clean Rooms** (collaborate without sharing underlying data), and **Databricks Marketplace** (exchange data + AI products; also private exchanges).

## 5. Auditing

Audit logs capture who accessed which dataset and what they did; UC adds **system tables** — the easiest way to query account audit logs.

## 6. Legacy governance tools (UC replaces — avoid)

**Table access control** (legacy grant/revoke on Hive-metastore objects) and **IAM role credential passthrough** (auto-authenticate to S3 using the Databricks login identity).

Related: [[external-access]], [[tables-concepts]], [[managed-tables]], [[external-tables]], [[catalog-commits]].
