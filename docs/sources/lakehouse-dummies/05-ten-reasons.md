# Ch 5 — Ten Reasons Why You Need a Data Lakehouse

> **Source:** Kaplan & Kara, *The Data Lakehouse For Dummies* (Wiley, 2nd Databricks Special Ed., © 2026) — Chapter 5, PDF pp. 27–29.
> **Added:** 2026-06-20
> **Tags:** summary, benefits
> **Type:** book

> *The standard "For Dummies" closing list — a one-screen recap of the whole booklet's argument.*

> 📎 **Overlaps:** mirrors [[ch05-ten-reasons]] (DIP §5), reframed lakehouse-first instead of platform-first.

---

The booklet lists ten benefits (the "ten" is approximate — the list runs ten bullets):

1. **Eliminates data silos** — all data (structured, semistructured, streaming, unstructured) centralized and unified.
2. **Unifies DW + BI + OLTP + ML + AI** — one foundation for all workloads: lake flexibility/cost + warehouse analytics.
3. **Unified and open governance** — access management, auditing, monitoring, lineage across formats/sources/clouds; easy discovery, access, sharing.
4. **Increases team efficiency & collaboration** — more personas working together, faster, more scalable, cheaper.
5. **Reduces cost & data redundancy** — no redundant copies; fewer multi-vendor license fees.
6. **Simplifies data engineering** — ingest/transform batch + streaming without managing infrastructure; AI-powered Data Intelligence Platform understands your data and pipelines.
7. **Scales** — to trillions of records via decoupled storage/compute, high performance, low latency.
8. **Open source** — at every layer to prevent lock-in: Delta Lake + Iceberg (reliability), Apache Spark (processing), MLflow (ML lifecycle), ~~Delta Sharing~~ **OpenSharing** (live data sharing). ⚠️ Booklet says "Delta Sharing"; per project convention now **OpenSharing** (Linux Foundation, June 2026).
9. **AI applications** — connect apps to business data using the org's own terminology/semantics; AI agents that reason across the data estate.
10. **Foundation for data intelligence** — semantic understanding drives intelligent search, code assistance, autoscaling, Databricks AI/BI visualizations, and natural-language self-service for non-technical users.

---

## References

- Source: PDF pp. 27–29.
- Related: [[01-making-the-case]], [[ch05-ten-reasons]] (DIP).
