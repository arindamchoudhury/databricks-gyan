# Unity Catalog commits — write mechanics, staged commits, ABAC

> **Source:** [SunnyData / Hubert Dudek — "Unity Catalog commits: make your managed delta layer safer and more performant"](https://www.sunnydata.ai/blog/unity-catalog-catalog-commits-databricks)
> **Published:** 2026-06-03
> **Added:** 2026-06-26
> **Tags:** unity-catalog, catalog-commits, catalogManaged, staged-commits, dynamodb, abac, external-access, transactions, delta, B4
> **Type:** practitioner blog

## Summary

A practitioner deep-dive on **catalog commits** (the `delta.feature.catalogManaged` table feature). It assumes the docs-level "what it is" — commit coordination moves from the filesystem to Unity Catalog, the data stays in open Delta on cloud storage, only the *coordination* moves — and instead explains the **write mechanics** the docs leave implicit: the staged-commits 4-step sequence, the on-storage `_delta_log/_staged_commits/` folder, how to inspect catalog commits via REST, why this replaces the old AWS DynamoDB log store, and how it extends governance (ABAC) to external reads. Companion to the docs note [[catalog-commits]] — read that first for requirements/preview-gates; read this for *how the write actually happens*.

## Key points

- **One-line thesis:** with catalog commits, supported readers/writers **resolve table state through Unity Catalog** instead of directly against the filesystem. Data stays in open Delta format on cloud storage; only commit coordination moves to UC as the central authority.
- **What it buys you (compounding value):** concurrency control (UC picks the winning commit when writers compete), governance (clients resolve state through UC), foundation for faster reads (some commit metadata served from UC), new capabilities (multi-statement / multi-table transactions), and UC as the single source of truth for latest table state.
- **Enable:** `TBLPROPERTIES ('delta.feature.catalogManaged' = 'supported')` on a UC **managed** Delta table.
- **The value compounds** with multi-table transactions, concurrent writers from multiple engines/teams, and external clients reading/writing UC-managed tables under fine-grained access rules. For a single Databricks writer the difference looks small.

## Notes

### The staged-commits write sequence (the core mechanic)

A catalog-commit-enabled write is a **four-step** sequence:

1. **Stage** — the writer stages the commit in `_delta_log/_staged_commits/`.
2. **Propose** — the writer proposes the commit to Unity Catalog.
3. **Validate & resolve** — UC validates the proposal and returns the **winning** commit (this is where concurrent writers are arbitrated).
4. **Publish** — the approved commit is published to `_delta_log`.

This sequence is what gives catalog commits strict **concurrency control**, **security control**, and **schema control** — note the schema is now primarily managed by **UC, not Delta**.

> The `_delta_log/_staged_commits/` folder is visible on storage. It's part of commit coordination and is especially useful when **multiple clients (including external engines)** write to the same Delta table. Staged commits are the same machinery behind multi-statement, multi-table transactions ([[transactions]]).

### Inspecting catalog commits (REST)

- Endpoint: `GET /api/2.1/unity-catalog/delta/preview/commits` — returns the catalog-ratified commit info for a **catalog-commit-enabled** table.
- For a **standard managed table** (no `catalogManaged` feature), the endpoint returns **nothing** — a quick way to confirm the feature is actually on.
- ⚠️ The post flags this as a **preview** endpoint that "**will soon change**" — treat the exact path as unstable.

### Why this exists — UC replaces the DynamoDB log store

- Historically on **AWS**, guaranteeing Delta **ACID on S3** with multiple writers required an external log store — **DynamoDB** — to coordinate commits (the classic `delta.enableMultiClusterWrites` / S3 commit-coordination setup).
- Catalog commits move that coordination **into Unity Catalog**: UC now acts as the database/cache that holds the authoritative commit log. The DynamoDB dependency goes away.
- Mental model: **UC behaves like a database in front of the table** — serving table state to engines directly instead of every engine fetching individual JSON files from `_delta_log`.

### Read performance (observed)

- In the query plan for the same table, the **amount of data read is slightly lower and usually faster** with catalog commits — the effect is biggest on **unoptimized tables with many commits** (lots of small Delta-log JSONs to process).
- Reason: table information is stored in UC's database and can be **served to engines directly**, rather than reconstructing state by reading many small `_delta_log` JSONs from storage.
- Framing: catalog commits "lay the **foundation** for stronger performance" — it's an enabler, not a one-shot speed switch.

### External access & ABAC (the governance extension)

- When multiple engines write to UC-managed tables, they need a **shared coordination point**. Instead of each engine writing to storage independently, an external engine should **first coordinate with the catalog** and check whether it's allowed to commit — making UC the **control point for external writes** and avoiding ungoverned writes, silent metadata drift, and inconsistent table state.
- The same model improves **external reads**: catalog commits let external engines integrate with UC policies, enabling fine-grained **row- and column-level ABAC** enforcement when UC-managed tables are read from external engines.
- Demo in the post: open-source Unity Catalog running locally, reading from a Databricks Unity Catalog.

## Quotes worth keeping

> "With catalog commits, supported readers and writers resolve table state through Unity Catalog. The data still lives in open Delta format on cloud storage, but commit coordination moves from filesystem-only coordination to Unity Catalog."

> "Prior to catalog commits, when using Databricks on AWS, DynamoDB was used to guarantee Delta ACID on S3 buckets. Now that functionality has been moved to Unity Catalog."

> "Unity Catalog becomes the central place where table state, commit approval, and external access meet."

## Related sources

- [[catalog-commits]] — the **docs note** (requirements, DBR versions, preview gates, limitations, enable/disable/check SQL). This SunnyData note is the *mechanics* companion to it.
- [[transactions]] — multi-statement, multi-table transactions; staged commits are the substrate that makes them atomic across tables.
- [[managed-tables]] — catalog commits is a managed-table-only feature.
- [[external-access]] — external-engine reads/writes that catalog commits govern (and where ABAC enforcement applies).

## References

- [Unity Catalog commits — SunnyData / Hubert Dudek](https://www.sunnydata.ai/blog/unity-catalog-catalog-commits-databricks) — this post
- Related SunnyData post referenced inline: "The Lakehouse Finally Has Real Transactions" (multi-statement transactions)
- Learning path: **B4 — Spark SQL & Relational Entities** (reference #9, catalog commits)
