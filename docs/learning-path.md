# Learning Path: Databricks Data Engineering

> **Last updated:** 2026-06-30 (Phase 5: added [structured-streaming-foreach](sources/databricks-docs/structured-streaming-foreach/) as **I2 reference #11** + cross-ref in I5 — at-least-once/`txnAppId`/`txnVersion`; not for continuous mode; stateful must consume full batch; empty DF handling; DLQ pattern; error propagation rule. Was name-dropped in I5 merge note. I2 still ⬜.) · **2026-06-30** (Phase 5: added [lakeflow-connect-query-based-overview](sources/databricks-docs/lakeflow-connect-query-based-overview/) as **A3 reference #20** (PP) — cursor-column ingestion, no gateway/staging, scheduled; two approaches (foreign-connection vs foreign-catalog); APPEND_ONLY SCD mode unique to query-based; deletion_condition; higher source load than CDC. Was name-dropped. A3 still ⬜.) · **2026-06-30** (Phase 5: added [lakeflow-connect-cdc-overview](sources/databricks-docs/lakeflow-connect-cdc-overview/) as **A3 reference #19** — DB connector 5-component arch detail: gateway continuous (log truncation risk), staging 30-day auto-purge, idle billing, snapshot sizing, SQL Server also supports full-snapshot, cross-cloud. Was name-dropped. A3 still ⬜.) · **2026-06-30** (Phase 5: added [lakeflow-connect-faq](sources/databricks-docs/lakeflow-connect-faq/) as **A3 reference #18** — 15 Q&As: schema evolution rules, multi-dest→API-only, concurrent skips, pipeline-delete drops tables, ALTER allowed (not schedule), pricing model, gateway requires classic compute, CDF auto-on. True gap. A3 still ⬜.) · **2026-06-30** (Phase 5: added [lakeflow-connect-run-as](sources/databricks-docs/lakeflow-connect-run-as/) as **A3 reference #17** — Run as identity: default = owner (user); set to service principal for resilience. UI-only. Was name-dropped in common-patterns. A3 still ⬜.) · **2026-06-30** (Phase 5: added [lakeflow-connect-row-filtering](sources/databricks-docs/lakeflow-connect-row-filtering/) as **A3 reference #16** (Beta) — `table_configuration.row_filter`; GA/SFDC/ServiceNow/query-based only (no CDC/gateway connectors); key gotchas: GA numeric unquoted, ServiceNow OR not supported + reference filters post-fetch, filter change doesn't delete prior ingested rows. **Gap** — absent from A3 before. A3 still ⬜.) · **2026-06-30** (Phase 5: added [lakeflow-connect-pipeline-tags](sources/databricks-docs/lakeflow-connect-pipeline-tags/) as **A3 reference #15** (PP) — `tags` object in pipeline spec (API/CLI only); distinct from serverless usage policies; propagates to system tables + billing → enables cost-attribution queries. Was name-dropped. A3 still ⬜.) · **2026-06-30** (Phase 5: added [lakeflow-connect-pipeline-maintenance](sources/databricks-docs/lakeflow-connect-pipeline-maintenance/) as **A3 reference #14** — 8 ops tasks; gotcha: schedule uses Jobs API not Pipelines API; staging cleanup: auto after Jan 6 2025, 25-day delete / 30-day physical removal, data-gap risk; gateway restart forces < 6h table discovery. Was name-dropped in common-patterns. A3 still ⬜.) · **2026-06-30** (Phase 5: added [lakeflow-connect-table-rename](sources/databricks-docs/lakeflow-connect-table-rename/) as **A3 reference #12** — `destination_table` param overrides default source-table name per object; required for same-schema duplicates; UI "Destination table" field; DABs/Notebook/CLI examples for GA/Salesforce/Workday. Renumbered monitor-costs → #13, gateway-event-logs → #14. Was name-dropped in multi-destination. A3 still ⬜.) · **2026-06-30** (Phase 5: added [lakeflow-connect-multi-destination](sources/databricks-docs/lakeflow-connect-multi-destination/) as **A3 reference #11** — fan-out to multiple destination catalogs/schemas; top-level catalog/schema = event log not default destination; `destination_table` for duplicate-name avoidance. Was name-dropped in common-patterns. A3 still ⬜.) · **2026-06-30** (Phase 5: added [lakeflow-connect-monitor-costs](sources/databricks-docs/lakeflow-connect-monitor-costs/) as **A3+A6 reference #11** — `system.billing.usage` cost monitoring: billing params, maintenance vs processing split, 8 SQL query patterns. Was name-dropped in common-patterns. A3+A6 still ⬜.) · **2026-06-30** (Phase 5: added [lakeflow-connect-scd](sources/databricks-docs/lakeflow-connect-scd/) as **A3 reference #10** — `scd_type: SCD_TYPE_2` history tracking: `__START_AT`/`__END_AT`, `sequence_by` for DB connectors, GA table restrictions, full-refresh wipes history, contrast with SDP `APPLY CHANGES INTO`. Was name-dropped in common-patterns. A3 still ⬜.) · **2026-06-30** (Phase 5: added [lakeflow-connect-gateway-event-logs](sources/databricks-docs/lakeflow-connect-gateway-event-logs/) as **A3+A6 reference #10** — `event_log()` gateway monitoring: `flow_progress` deltas + CDC latency vs `operation_progress` snapshot % + ETA; discovery vs batch latency diagnosis; SQL query library. Absent before. A3+A6 still ⬜.) · **2026-06-30** (Phase 5: added [lakeflow-connect-column-selection](sources/databricks-docs/lakeflow-connect-column-selection/) as **A3 reference #8** — `include_columns`/`exclude_columns` in `table_configuration`, with DABs/Notebook/CLI examples for GA/Salesforce/Workday. Added [lakeflow-connect-full-refresh](sources/databricks-docs/lakeflow-connect-full-refresh/) as **A3 reference #9** — three trigger interfaces, CDC-optimized atomic full refresh, full refresh window scheduling (`full_refresh_window`), auto full refresh policy (`auto_full_refresh_policy`) with pipeline- vs table-level override. Both were name-dropped only. A3 still ⬜.) · **2026-06-29** (Phase 5: added the [lakeflow-connect-managed](sources/databricks-docs/lakeflow-connect-managed/) docs note as **A3 reference #5** (replacing bare DB-DOCS link) — six connector types: database/CDC (MySQL/PostgreSQL/SQL Server, requires gateway + staging), query-based (schedule queries, no gateway), SaaS (Salesforce/HubSpot/Jira/Workday), file-source (Drive/SharePoint), streaming (RabbitMQ), community. Architecture: Connection + SDP pipeline + streaming tables; CDC adds gateway + staging. Incremental: full first run then change tracking/cursor. Networking: SaaS API / Private Link / VPC peering / Direct Connect/ExpressRoute. DABs for CI/CD. Retries with backoff + cursor position storage on failure. Coverage was name-dropped (bare DB-DOCS link). Wired into nav under Data engineering › Lakeflow Connect. A3 still ⬜.) · **2026-06-29** (Phase 5: added the [create-or-modify-table](sources/databricks-docs/create-or-modify-table/) docs note as **A3 reference #7** — the file-upload Add data UI: 10 files/2 GB limit, CSV/TSV/JSON/Avro/Parquet/text only, no compressed files, SQL warehouse/serverless/dedicated compute, create-or-overwrite managed Delta table in UC or Hive metastore, per-format options (CSV delimiter/header/type-detection/multiline/merge-schema; JSON type-detection/multiline/comments/single-quotes/timestamp), multi-file = row append only, column mapping used for special chars. Coverage was name-dropped via lakeflow-connect-overview. Wired into nav under Data engineering › Lakeflow Connect; registered in sources index. A3 still ⬜.) · **2026-06-29** (Phase 5: added the [lakeflow-connect-overview](sources/databricks-docs/lakeflow-connect-overview/) docs note as **A3 reference #6** — the Lakeflow Connect hub: two service models, ETL stack layer model (start most managed; fully-managed connectors → SDP), four connector types (managed / community / standard / file upload), DIY/partner options, and ingestion alternatives (Lakehouse Federation + OpenSharing for zero-copy). Coverage was name-dropped only. Wired into nav under Data engineering › Lakeflow Connect; registered in sources index. No version/rename corrections. A3 still ⬜.) · **2026-06-29** (Phase 5: added the [selective-overwrite](sources/databricks-docs/selective-overwrite/) docs note as **I5 reference #9** — four Delta selective-overwrite options as lighter MERGE alternatives: `REPLACE USING` (recommended; column-equality overwrite, all compute, no config — SQL DBR 16.3+, Python/Scala DBR 18.2+), `REPLACE WHERE` (predicate-based; validates all rows satisfy predicate; empty source may delete — SQL DBR 12.2 LTS+, Python/Scala DBR 9.1 LTS+), `REPLACE ON` (boolean expression, NULL-safe `<=>` matching — SQL DBR 17.1+, Python/Scala DBR 18.2+), `partitionOverwriteMode=dynamic` (legacy, classic-only for SQL). Coverage was absent — prior `overwriteSchema` matches are a distinct schema-evolution concept. Wired into nav under Data engineering › Concepts; registered in sources index. No version/rename corrections. I5 still ⬜.) · **2026-06-29** (Phase 5: added the [merge](sources/databricks-docs/merge/) docs note as **I5 reference #8** — full `MERGE INTO` mechanics: basic upsert, `WHEN NOT MATCHED BY SOURCE` (DBR 12.2 LTS+) for updating/deleting unmatched target rows (add a condition or it rewrites the whole table; no source columns can be referenced), clause evaluation order and semantics, the deduplication pattern (insert-only merge + date-bounded window + `foreachBatch` for streaming dedup), pointer to `AUTO CDC` for SCD, and the incremental sync pattern (same date filter on source + target to propagate deletes atomically). Also documents the DBR 16.0+ vs ≤15.4 LTS difference in duplicate-match detection. Wired into nav under Data engineering › Concepts; registered in sources index. No version/rename corrections. I5 still ⬜.) · **2026-06-29 (Phase 5: added the [what-is-cdc](sources/databricks-docs/what-is-cdc/) concept note as **I4 reference #6** — CDC vs snapshots, SCD Type 1 (current state) vs Type 2 (`__START_AT`/`__END_AT` history), `AUTO CDC` (native change feeds; monotonically-increasing sequencing column required; initial hydration via once flows) vs `AUTO CDC FROM SNAPSHOT` (Python only; diffs consecutive snapshots into a synthetic change feed; misses interim intra-period changes; ascending version order required). Added the [aggregation](sources/databricks-docs/aggregation/) concept note as **I2 reference #10** — four aggregation types: batch (full recompute, cost scales with data), stateful (streaming; **watermarks required** or state builds up infinitely → OOM), incremental (materialized views — recommended for frequently-queried pre-computed aggregates), approximate (`approx_count_distinct`/`approx_percentile`/`approx_top_k`/`TABLESAMPLE`). Wired both into nav under Data engineering › Concepts; registered in sources index. No version/rename corrections. I2 + I4 still ⬜.) · **2026-06-22 (Phase 5: reconciled B4 against this session's new material — DCDE-SG Ch 3 reading notes + the captured [tables-concepts](sources/databricks-docs/tables-concepts/) docs note. Reframed "What it is" from Hive-metastore-centric to UC three-level namespace; added a 2026-deltas callout (UC-only workspaces have no HMS/DBFS, three table types incl. foreign + Iceberg, managed-recommended default, global temp views unsupported on serverless); added tables-concepts as a B4 reference. Reviewed full B4 topic vs actual Ch 3 scope — expanded "What it is" + Milestone to cover CTAS, constraints, deep/shallow clone, and the three view types (were missing); extended the deltas callout with UC informational PK/FK and shallow-clone caveats. B4 still ⬜ — reading note ≠ topic completion.) · **2026-06-23** (Phase 5: added the [managed-tables](sources/databricks-docs/managed-tables/) docs note as B4 reference #6; added `UNDROP TABLE` + configurable recovery period to the B4 milestone. B4 still ⬜.) · **2026-06-23** (Phase 5: added the [convert-external-managed](sources/databricks-docs/convert-external-managed/) docs note as B4 reference #7; added `SET MANAGED`/`UNSET MANAGED` external→managed conversion + 14-day rollback to the B4 milestone. B4 still ⬜.) · **2026-06-23** (Phase 5: added the [managed-storage](sources/databricks-docs/managed-storage/) docs note as B4 reference #8 — managed storage location hierarchy. B4 still ⬜.) · **2026-06-24** (Phase 5: added the [catalog-commits](sources/databricks-docs/catalog-commits/) docs note as B4 reference #9 — catalog commits feature (`delta.feature.catalogManaged`). No version/rename corrections needed. B4 still ⬜.) · **2026-06-24** (Phase 5: added the [transactions](sources/databricks-docs/transactions/) docs note as B4 reference #10 — multi-statement ACID transactions, the capability catalog commits unlocks. No version/rename corrections needed. B4 still ⬜.) · **2026-06-24** (Phase 5: added the [predictive-optimization](sources/databricks-docs/predictive-optimization/) docs note as A2 reference #5 — deep dive behind the existing PO callout (3 ops, ZORDER skip, inheritance model + ALTER syntax, VACUUM retention trap, serverless billing, system table, exclusions). PO facts already current in A2/I5 — no version corrections. A2 still ⬜.) · **2026-06-24** (Phase 5: added the [liquid-clustering](sources/databricks-docs/liquid-clustering/) docs note as A2 reference #5 (PO note bumped to #6). **Version fix:** corrected "DBR 14+" → LC is GA for Delta on **DBR 15.4 LTS+** (Iceberg PP 16.4 LTS+, v3 features 18.0+) in both A2 "Why" and the I5 Z-order callout; updated A2 DB-DOCS link to the moved `/tables/clustering` URL. A2 still ⬜.) · **2026-06-24** (Phase 5 — **gap fill:** external access was uncovered (only a passing "credential vending" token in B4). Renamed A7 "Lakehouse Federation & OpenSharing" → "Lakehouse Federation, External Access & OpenSharing"; reframed it as three interop directions (Federation inbound / external-engine reads / OpenSharing cross-org); added Unity REST API + Iceberg REST catalog + credential vending + compatibility mode to "What it is"; added the [external-access](sources/databricks-docs/external-access/) docs note as ref #5 + the DB-DOCS external-access link; extended the interactive + milestone. A7 still ⬜.) · **2026-06-24** (Phase 5 — **gap fill:** the [Optimization recommendations](https://docs.databricks.com/aws/en/optimizations) hub listed 6 perf features the path never named. Added a new "Platform optimization knobs" subsection under A1 with full lessons (what / when-to-use / how-to-learn / milestone) for **disk caching, dynamic file pruning, low shuffle merge, cost-based optimizer, range join optimization, and Delta isolation levels**, plus a deprecated-bloom-filter skip note. Expanded A1 "What it is"/"Why". Facts verified against the six DB-DOCS subpages. A1 still ⬜.) · **2026-06-24** (captured 7 research notes for the A1 knobs — [optimization-recommendations](sources/databricks-docs/optimization-recommendations/) hub + disk-cache, dynamic-file-pruning, low-shuffle-merge, cost-based-optimizer (3 EXPLAIN screenshots), range-join, isolation-levels — and credited each in its A1 lesson reference; added 6 glossary terms. A1 still ⬜.) · **2026-06-24** (Phase 5: added the [external-tables](sources/databricks-docs/external-tables/) docs note as B4 reference #11 — the external table *type* (metadata-only governance, `LOCATION` you pick, DROP leaves data, 7 formats, `MSCK REPAIR … SYNC METADATA`); fills the external-type gap (path had managed #6 + convert-from-external #7 but no dedicated external-table ref). No version/rename corrections. B4 still ⬜.) · **2026-06-24** (Phase 5 — **gap fill:** the [data-governance hub](sources/databricks-docs/data-governance-hub/) maps UC onto six governance pillars the path under-named. Reframed I7 "What it is" around all six (added the **discoverability suite** — Catalog Explorer/AI comments/table insights/ERD — **ABAC** as first-class access control, and **auditing via system tables**), added the hub note as I7 ref #5, and extended the I7 milestone (name six pillars, ABAC-vs-grants, ERD, audit logs). Added **UC data quality monitoring** (anomaly detection + profiling) to A6 "What it is" — was genuinely absent. A7 (OpenSharing/Clean Rooms/Marketplace) + A4 (PII/masking/audit) already covered — no change. No version/rename corrections. I7 + A6 still ⬜.) · **2026-06-24** (Phase 5: added the [automatic-upgrades](sources/databricks-docs/automatic-upgrades/) docs note as B4 reference #12 — automatic enablement of GA managed-table features via observation window + verified workloads. New PP feature; no version/rename corrections. B4 still ⬜.) · **2026-06-24** (Phase 5: added the [change-data-feed](sources/databricks-docs/change-data-feed/) docs note as I5 ref #4 + A4 ref #4. **New distinction:** automatic CDF (PP, read-time, DBR 18+, Delta+Iceberg v3, cheaper writes) vs legacy CDF (`delta.enableChangeDataFeed`); added an automatic-CDF callout to I5 and an A4 caveat that automatic CDF is unsupported on tables with row filters/column masks (→ those must use legacy CDF for delete propagation). No version/rename corrections to existing claims. I5 + A4 still ⬜.) · **2026-06-24** (Phase 5: added the [column-mapping](sources/databricks-docs/column-mapping/) docs note as I5 ref #5 — the rename/drop-column schema-evolution feature (modes, protocol bump, path/CDF/streaming breakage, remove-rewrite vs DROP FEATURE). Was only name-dropped in two feature lists before; now explained. No version/rename corrections. I5 still ⬜.) · **2026-06-24** (Phase 5: added the [row-tracking](sources/databricks-docs/row-tracking/) docs note as I5 ref #6 — the row-id/row-commit-version lineage substrate behind automatic CDF + row-level concurrency (DBR 14.1+, Iceberg v3 built-in, one-way protocol bump, slow backfill, half-disable gotcha). Was only name-dropped before. No version/rename corrections. I5 still ⬜.) · **2026-06-24** (Phase 5: added the [checkpoint-v2](sources/databricks-docs/checkpoint-v2/) docs note as B4 reference #13 — the concurrency/log-checkpoint table feature (`delta.checkpointPolicy='v2'`, DBR 13.3 LTS+, auto-on for liquid clustering + automatic upgrades, `DROP FEATURE v2Checkpoint`). Was only name-dropped in #12's feature list; now explained standalone. No version/rename corrections. B4 still ⬜.) · **2026-06-24** (Phase 5 — **source-note reconcile sweep:** folded ~20 previously-unwired captured docs notes into the path (current material only; skipped foundational/superseded sources). **B1:** added access-mode rename callout (Shared→Standard, Single-user→Dedicated) + Lakeguard, and refs for high-level-architecture, classic/standard/dedicated compute, serverless-limitations. **I8:** added SQL warehouse-types callout (Serverless/Pro/Classic, Predictive IO, IWM, API-defaults-to-Classic gotcha) + 2 refs. **I2:** serverless two-trigger restriction callout + serverless-limitations ref. **I3:** serverless-pipelines ref (exclusive features). **I6:** serverless-jobs ref. **E1:** photon + compute-pools refs. **A1:** grouped Spark-UI/tuning captured notes (AQE, join hints, troubleshooting set). No topic status flips — all references, not completions.) · **2026-06-24** (Phase 5: added the [external-partition-discovery](sources/databricks-docs/external-partition-discovery/) docs note as B4 reference #14 — partition discovery for external tables: default recursive listing vs opt-in partition metadata logging (`partitionMetadataEnabled`, DBR 13.3 LTS+), `MSCK REPAIR`/`ALTER TABLE … ADD PARTITION` sync, non-Delta only. Was only name-dropped via the `MSCK REPAIR` line in #11; now explained. No version/rename corrections. B4 still ⬜.) · **2026-06-25** (Phase 5 — **gap fill:** the third table *type*, **foreign tables**, was only name-dropped in B4's callout + A7. Added the [foreign-tables](sources/databricks-docs/foreign-tables/) docs note as **B4 reference #15** and **A7 reference #6** (Interactive bumped to #7): foreign/federated tables in a UC foreign catalog, query- vs catalog-federation registration, read-only except internal federated HMS, no UC transactional guarantees, migration-stopgap framing. Wired into nav under Tables › Table types › Foreign tables. No version/rename corrections. B4 + A7 still ⬜.) · **2026-06-25** (Phase 5: added the [materialized-views](sources/databricks-docs/materialized-views/) docs note as **I3 reference #7** + a serverless callout and milestone clause. **Clarification:** a standalone MV's create/refresh always runs on an auto-created **serverless** Lakeflow pipeline (billed serverless DBUs even from a dedicated warehouse; submit from a Pro/Serverless SQL warehouse or serverless notebook; classic can't run the refresh) — vs an MV inside a regular pipeline, which follows that pipeline's serverless-or-classic compute. Wired into nav under Data engineering. No version/rename corrections. I3 still ⬜.) · **2026-06-25** (Phase 5: added the [convert-foreign-managed](sources/databricks-docs/convert-foreign-managed/) docs note as **B4 reference #16** — `SET MANAGED MOVE`/`COPY` foreign→managed conversion (PP, DBR 17.3+, HMS/Glue only); note includes the page's **embedded YouTube walkthrough** (foreign→managed at 5:30). Made the foreign-tables note's `convert-foreign-managed` mentions wikilinks. Wired into nav under Tables › Table types › Foreign tables. No version/rename corrections. B4 still ⬜. Also extended the B4 milestone with foreign→managed `SET MANAGED MOVE`/`COPY` conversion + `UNSET MANAGED` rollback.) · **2026-06-25** (Phase 5: added the [convert-foreign-external](sources/databricks-docs/convert-foreign-external/) docs note as **B4 reference #17** — `SET EXTERNAL` foreign→external conversion (PP, DBR 17.3+, HMS/Glue; data stays in place, broader formats, `DROP`-to-rollback, Catalog-Explorer verification, Glue SerDe fix). Extended the B4 milestone with foreign→external. Wired into nav under Tables › Table types › Foreign tables. No version/rename corrections. B4 still ⬜.) · **2026-06-25** (Phase 5 — **gap fill:** the **fourth table type**, **temporary tables**, was only name-dropped in B4's deltas callout. Added the [temporary-tables](sources/databricks-docs/temporary-tables/) docs note as **B4 reference #18** — session-scoped, Delta-by-default, outside the catalog namespace, no `CREATE TABLE` privilege, session-isolated, auto-drop at 7 days, `CREATE {OR REPLACE} TEMP TABLE` (no `USING`), DML yes / no `DELETE`·`ALTER`·clone·time-travel·streaming·DataFrame·Dedicated-clusters; applies to **Databricks SQL + DBR 18.1+**. Added a **new-distinction callout** (temp *table* vs temp *view*) and extended the B4 milestone. Wired into nav under Tables › Table types › Temporary tables. No version/rename corrections. B4 still ⬜.) · **2026-06-25** (Phase 5: added the [data-engineering-hub](sources/databricks-docs/data-engineering-hub/) docs note as **I3 reference #8** — the Lakeflow umbrella hub (Connect/SDP/Designer/Jobs + Databricks Runtime). **Gap fill:** extended I3 "What it is" with the SDP **object model** (flows + sinks were under-named; streaming tables + MVs already present). Wired into nav under Data engineering. No version/rename corrections. I3 still ⬜.) · **2026-06-25** (Phase 5: added the [procedural-vs-declarative](sources/databricks-docs/procedural-vs-declarative/) concept note as **I3 reference #9** + a paradigm clause in I3 "Why you need it" (declarative SDP vs procedural Spark/Jobs). Wired into nav under Data engineering. No version/rename corrections. I3 still ⬜.) · **2026-06-26** (DAIS-2026 reconcile vs the SunnyData/databrickster announcement roundup. Confirmed the big items were already absorbed — Lakebase/LTAP (E8), Lakehouse//RT + Reyden (E9), ZeroOps (A6 callout), OpenSharing rename (A7). Filled three genuinely-missing in-scope gaps as awareness-only callouts: **Genie Ontology** (knowledge graph / semantic context layer on UC Metrics, OntoRank, Preview) added to **I7**; **ZeroBus Ingest** (push-based, Kafka-free serverless ingestion into UC Delta; GA, Lakeflow Connect) added to **I1** + its milestone; **on-prem/hybrid OpenSharing via the Databricks Storage Ecosystem** (zero-copy Serverless/Genie/LLM on on-prem data; Everpure/MinIO/Qumulo partners) added to **A7**. Facts verified against Databricks blog/newsroom. Out-of-scope app-dev/marketing announcements (CustomerLake/CDP, Databricks Apps + App Builder, Reverse ETL, Omnigent) deliberately **not** added — outside the DE cert track. No topic status flips — all awareness callouts. I1/I7/A7 still ⬜.) · **2026-06-26** (follow-up — reversed the prior "not added" call at user request and folded in the remaining four. **Reverse ETL** added to **A7** as the fourth outbound-to-operational interop direction (real DE; extended the A7 milestone), with **CustomerLake/CDP** as its driving use case in the same callout. **Databricks Apps + App Builder** added to **E9** as the app layer atop LTAP-writes + Lakehouse//RT-reads (awareness-only). **Omnigent** added as a one-line awareness tag on the I7 Genie Ontology callout. Reverse ETL is the only one treated as in-scope DE content; the other three are explicitly flagged awareness-only. Facts verified against Databricks blog/newsroom. No topic status flips. A7/E9/I7 still ⬜.) · **2026-06-26** (gap fill from the SunnyData "Databricks Custom Container Runtimes" post: **custom container runtimes (Databricks Container Services / DCS)** were uncovered — the path had DABs/CI-CD/Terraform but nothing on shipping the *runtime* as a Docker image. Added a "runtime as code" callout to **E3** (DevOps) + DB-DOCS refs (dedicated + standard variants) and extended the E3 milestone. **Doc-verified correction to the blog:** DCS is no longer Dedicated-only — there's now a separate **Standard-compute** DCS variant that expects a *different* base image (wrong-variant image fails to launch); kept `enableDcs` toggle + credentials-in-secrets. Awareness-level for the certs (DCDEP "Debugging & Deploying" 10%). No topic status flips. E3 still ⬜.) · **2026-06-26** (new source created: **`sources/sunnydata/`** (SunnyData / Hubert Dudek practitioner blog) with its index + the first note, [sunnydata-catalog-commits](sources/sunnydata/catalog-commits/), capturing the catalog-commits **write mechanics** the docs note leaves implicit — staged-commits 4-step sequence + `_delta_log/_staged_commits/`, the `/api/2.1/unity-catalog/delta/preview/commits` REST inspection endpoint, the DynamoDB→UC log-store framing, observed read-size win, and ABAC enforcement on external reads. Cross-linked from the [catalog-commits](sources/databricks-docs/catalog-commits/) docs note and wired into **B4 reference #9**; registered in the sources index. Catalog commits was already covered as a topic — this only deepens the mechanics. No topic status flips. B4 still ⬜.) · **2026-06-26** (added a second SunnyData note, [sunnydata-multi-statement-transactions](sources/sunnydata/multi-statement-transactions/) — "The Lakehouse Finally Has Real Transactions" (Hubert Dudek + Benjamin Mathew), 3 figures embedded inline: the `BEGIN ATOMIC` SQL surface, the `.mst.json` staged-commit file, the success-vs-rollback Delta-log walkthrough, and the SQL-only / not-OLTP(→Lakebase) / not-OSS-Spark boundaries. Wired into **B4 reference #10**, cross-linked from the transactions docs note and the [sunnydata catalog-commits note](sources/sunnydata/catalog-commits/), registered in the sources index + zensical nav. Also generalized `embed_images.py` to download-only (skip the gallery append) when a note already references its images inline. MSTs already covered as a topic (B4 #10) — this deepens the mechanics. No topic status flips. B4 still ⬜.) · **2026-06-26** (folded the [batch-vs-streaming](sources/databricks-docs/batch-vs-streaming/) docs note into the path — it had been created + wired into nav/sources but not referenced by any topic. Added as **I2 reference #8** with a Medallion-layer callout (streaming at Bronze / batch+incremental-refresh MVs at Silver/Gold; "streaming" is broader than Kafka), and as **B7 reference #5** + extended the B7 milestone (which layers default to streaming vs batch and why). Concept-only; no new product facts. No topic status flips. I2 + B7 still ⬜. (procedural-vs-declarative was already wired as I3 #9.)) · **2026-06-27** (Phase 5 — **gap fill:** schema evolution was only name-dropped (I5 "What it is" + the I1 `mergeSchema` milestone) with no dedicated coverage. Added the [schema-evolution](sources/databricks-docs/schema-evolution/) concept note as **I5 reference #7** + **I2 reference #9**, with a new **per-component** callout under I5: schema evolution is **not a global switch** — each pipeline stage (connector → format parser → engine → data set) evolves independently and *all* must agree, or the stream fails. Captured the five change-type taxonomy and which Delta lever covers each (additive → `mergeSchema`; rename/drop → column mapping; broadening → type widening; arbitrary type change → `overwriteSchema` + full rewrite), the streaming "schema locked at planning → fail-then-restart" rule (I2), and the view `SCHEMA EVOLUTION` vs `SCHEMA TYPE EVOLUTION` distinction. Wired into nav under Data engineering › Concepts; registered in the sources index. No version/rename corrections. I2 + I5 still ⬜.)
> **Prior:** 2026-06-21 (research pass: synced B5/B6/B7 completion; verified certs/runtime/catalog against official sources; added DBR 19 Beta, Lakeflow Designer GA, DCDEA section rename, Predictive Optimization to A2/I5, Genie ZeroOps to A6. Confirmed DA-DE and DA-ADE module structures unchanged — DA-ADE Data Privacy module still present. Replaced retired DA-MGUC course (I7) with "Get Started with Data Governance on Databricks"; confirmed DA-DIUC and DA-SQL links live.)
> **Current stable version:** Databricks Runtime 18 (released 2026-06-10) · Apache Spark 4.1.0
> **LTS version:** DBR 17.3 LTS (released 2025-10-22) · Apache Spark 4.0.0
> **In Beta:** DBR 19 (released 2026-06-15) · Apache Spark 4.2.0 — not yet GA; learn against DBR 18.
>
> **How to read this page.** Topics are the primary unit. Each topic has a "How to learn it"
> section that recommends a multi-modal path — video first, then exercises, then depth reading.
> Resources (books, courses, docs) serve the topics; they are not the organizing structure.
>
> **Naming note:** Delta Live Tables (DLT) is now officially called **Lakeflow Spark Declarative Pipelines**.
> Databricks Workflows is now **Lakeflow Jobs**. Both old and new names appear in resources.

---

## Resources at a glance

| Abbrev | Name | Type | URL |
|---|---|---|---|
| **DCDE-SG** | Databricks Certified Data Engineer Associate Study Guide (Alhussein, O'Reilly 2025) | Book | https://www.oreilly.com/library/view/databricks-certified-data/9781098166823/ |
| **UDEDW** | Ultimate Data Engineering with Databricks (Malhotra, 2024) | Book | https://www.amazon.com/dp/8196994788 |
| **BBDE** | Big Book of Data Engineering, 4th Edition (Databricks, free) | Ebook | https://www.databricks.com/resources/ebook/big-book-of-data-engineering |
| **DA-FREE** | Get Started with Databricks for Data Engineering (Databricks Academy, 2 hrs, free) | Official Course | https://www.databricks.com/training/catalog/get-started-with-databricks-for-data-engineering-1511 |
| **DA-DE** | Data Engineering with Databricks (Databricks Academy, 16 hrs) — M1: Lakeflow Connect · M2: Lakeflow Jobs · M3: Spark Declarative Pipelines · M4: DevOps Essentials | Official Course | https://www.databricks.com/training/catalog/data-engineering-with-databricks-911 |
| **DA-ADE** | Advanced Data Engineering with Databricks (Databricks Academy, 16 hrs) — M1: Advanced Pipelines · M2: Data Privacy · M3: Performance Optimization · M4: Automated DABs Deployment | Official Course | https://www.databricks.com/training/catalog/advanced-data-engineering-with-databricks-971 |
| **DA-DG** | Get Started with Data Governance on Databricks (Databricks Academy, 3 hrs, free) — replaces "Data Management and Governance with Unity Catalog", retired 2025-12-12 | Official Course | https://www.databricks.com/training/catalog/get-started-with-data-governance-on-databricks-4678 |
| **DA-DIUC** | Data Interoperability with Unity Catalog (Databricks Academy) | Official Course | https://www.databricks.com/training/catalog/data-interoperability-with-unity-catalog-4557 |
| **DA-SQL** | SQL Analytics on Databricks (Databricks Academy) | Official Course | https://www.databricks.com/training/catalog/sql-analytics-on-databricks-3928 |
| **DB-DOCS** | Databricks official documentation | Docs | https://docs.databricks.com/aws/en/ |
| **DB-DELTA** | Delta Lake documentation | Docs | https://docs.delta.io/latest/ |
| **REPO-DLT** | delta-live-tables-notebooks — official Databricks DLT/Lakeflow example pipelines (CDC, streaming, Kimball, ML) | GitHub repo | https://github.com/databricks/delta-live-tables-notebooks |
| **REPO-NBP** | notebook-best-practices — before/after modularization example (COVID EDA); shared module `covid_analysis/transforms.py`; 4 pytest unit tests in `tests/transforms_test.py`; `notebooks/run_unit_tests.py` runs pytest via `pytest.main()` inside a Databricks notebook; GitHub Actions CI using `databricks/run-notebook` action | GitHub repo | https://github.com/databricks/notebook-best-practices |
| **REPO-TF** | terraform-databricks-lakehouse-blueprints — production lakehouse infra (Unity Catalog, Private Link, multi-cloud) | GitHub repo | https://github.com/databricks/terraform-databricks-lakehouse-blueprints |
| **REPO-TF-EX** | terraform-databricks-examples — official Databricks Terraform code examples including CI/CD pipeline templates | GitHub repo | https://github.com/databricks/terraform-databricks-examples |
| **SPEC-TF** | Specialist Session: "Managing Databricks at scale using Terraform" (Vuong Nguyen & Alex Ott, Databricks 2025) — AWS workspace provisioning, Unity Catalog setup, Terragrunt, Terraform vs DABs, CI/CD for Terraform | Local PDF | `C:\opt\learn\databricks\specialist sessions\Databricks Specialist Sessions_ Managing Databricks at scale using Terraform.pdf` |
| **REPO-SRA** | terraform-databricks-sra — Security Reference Architecture: production-hardened Databricks workspace templates for AWS/Azure/GCP (Private Link, CMK, no-public-IP, audit log delivery, Compliance Security Profile, Security Analysis Tool) | Local repo / GitHub | `C:\opt\learn\databricks\repos\terraform-databricks-sra` · https://github.com/databricks/terraform-databricks-sra |
| **REPO-TF-PROVIDER** | terraform-provider-databricks — Terraform provider source code (Go); useful for understanding undocumented resource behaviour, debugging unexpected plan/apply errors, or checking what fields a resource actually accepts | Local repo / GitHub | `C:\opt\learn\databricks\repos\terraform-provider-databricks` · https://github.com/databricks/terraform-provider-databricks |

---

## Certifications

| Cert | Provider | Level | Topics tested (weights) | Fee | When to attempt |
|---|---|---|---|---|---|
| **Databricks Certified Data Engineer Associate (DCDEA)** | Databricks | Intermediate | Databricks Intelligence Platform 10%, Development & Ingestion 30%, Data Processing & Transformations 31%, Productionizing Pipelines 18%, Data Governance & Quality 11% | $200 | After Intermediate level |
| **Databricks Certified Data Engineer Professional (DCDEP)** | Databricks | Advanced | Python/SQL Code 22%, Cost & Performance Optimization 13%, Monitoring & Alerting 10%, Data Security & Compliance 10%, Debugging & Deploying 10%, Data Transformation/Quality 10%, Data Ingestion 7%, Data Governance 7%, Data Modelling 6%, Data Sharing & Federation 5% | $200 | After Advanced level |

Both exams: online proctored, multiple choice, valid 2 years, no formal prerequisites.

---

## Beginner

**Goal:** Understand the Databricks Lakehouse platform, write PySpark and Spark SQL transformations, read/write Delta tables, and build simple batch pipelines following the Medallion pattern.
**Estimated time:** ~30 hrs

---

### ✅ B1 — Databricks Platform & Workspace

**What it is:** The Databricks control/data plane architecture, workspace UI, cluster types, and notebook environment.

**Why you need it:** Everything else runs on top of this platform; without a mental model of how it works you can't reason about cost, connectivity, or failures.

**How to learn it:**

1. **Free course — DA-FREE** (~2 hrs) — Official Databricks workspace tour covering platform architecture, cluster types, Delta Lake intro, and Lakeflow overview. Self-paced, no cost; complete all demos.
2. **Hands-on — Sign up for Databricks Free Edition** (~1 hr) — Attach **Serverless** compute (Free Edition is serverless-only — no cluster creation), run a `spark.range(10).display()` notebook, browse a Unity Catalog Volume in the Data Explorer, and inspect a query in the query profile. Sign up at [docs.databricks.com/aws/en/getting-started/free-edition](https://docs.databricks.com/aws/en/getting-started/free-edition).
3. **Book chapter — DCDE-SG Ch 1** (~2 hrs) — Read "Introducing the Databricks Platform", "Understanding High-Level Architecture", "Creating Clusters", and "Working with Notebooks". Skip the chapter on Deployment of Databricks Resources (not needed yet).
4. **Reference — DB-DOCS** — Bookmark the [Clusters](https://docs.databricks.com/aws/en/compute/) and [Notebooks](https://docs.databricks.com/aws/en/notebooks/) docs pages for cluster config reference.
5. **Reference — [High-level architecture](sources/databricks-docs/high-level-architecture/)** (captured notes) — the current platform model: **control plane** (Databricks account) vs **compute plane** (serverless = Databricks account / classic = your cloud account), the **account → workspace → Unity Catalog metastore** hierarchy, and **workspace storage** (file-system + system data, distinct from your UC data; never delete it on classic). DBFS root/mounts are a deprecated pattern.
6. **Reference — Compute access modes & isolation** (captured notes) — [classic compute overview](sources/databricks-docs/classic-compute-overview/) (all-purpose/jobs/pipelines, the four cumulative permission levels), [standard](sources/databricks-docs/standard-compute-overview/) vs [dedicated](sources/databricks-docs/dedicated-compute-overview/) access modes, and [Lakeguard](sources/databricks-docs/lakeguard/) (the container + Spark Connect isolation that secures multi-user Standard/serverless/SQL-warehouse compute).
7. **Reference — [Serverless compute limitations](sources/databricks-docs/serverless-limitations/)** (captured notes) — what serverless can't do: no RDD/R/Scala-in-notebooks, no Spark UI/logs (use query profile), no `df.cache()` family, streaming restricted to `AvailableNow`/`Once`, UC required, 7-day max runtime. The constraints you trade away for zero cluster management.

> 📌 **Compute access-mode rename (2025) — current terms.** Classic-cluster access modes were renamed: **"Shared" → Standard** (multi-user, the recommended default; isolated by **Lakeguard**) and **"Single user" → Dedicated** (one user/group; the only mode with RDD/R/GPU/privileged access). The API field is `data_security_mode`; **Auto** resolves to Standard unless an ML runtime or DBR < 14.3 is selected. Old material still says Shared/Single-user.

**Milestone:** You can attach serverless compute in Free Edition and run a notebook, explain the difference between all-purpose and job clusters (paid-workspace concepts), distinguish **Standard vs Dedicated access modes** and when each is required, describe what the control plane and compute plane are, and explain what Lakeguard isolates on shared compute.

---

### ✅ B2 — Apache Spark Architecture on Databricks

**What it is:** The Spark driver/executor model, DAG execution, stages, and tasks — how Spark actually runs your code.

**Why you need it:** Performance problems, OOM errors, and slow jobs all trace back to this model; you can't tune what you don't understand.

**How to learn it:**

1. **Book chapter — DCDE-SG Ch 1, "Apache Spark on Databricks" section** (~30 min) — Since you know Spark, focus on the Databricks-specific layer: AQE enabled by default, serverless compute vs classic clusters, and where Photon fits. A quick skim rather than a deep read.
2. **Interactive — Spark UI in Free Edition** (~1 hr) — Run a join between two DataFrames and inspect the DAG, stages, and tasks in the Spark UI. Look at shuffle read/write sizes.
3. **Reference — DB-DOCS: [Spark UI](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide.html)** — Bookmark for when you tune jobs later.

**Milestone:** You can explain what happens between `df.count()` and a result appearing — job → stages → tasks → executors — and find the corresponding DAG in the Spark UI.

---

### ⬜ B3 — PySpark DataFrame API Fundamentals

**What it is:** The core PySpark API: reading data, selecting/filtering/transforming columns, aggregations, joins, and writing output.

**Why you need it:** Every data pipeline starts here; this is the language you write ETL in.

**How to learn it:**

1. **Interactive — Free Edition** (~1 hr) — Since you know PySpark, this is an orientation run: read a JSON file, apply transforms with `F.col()` / `F.when()`, join two DataFrames, write the result as a Delta table. Confirm the Databricks notebook environment works as expected before moving on.
2. **Book chapter — DCDE-SG Ch 4, "Transforming Data with Apache Spark"** (~2 hrs) — Focus on Databricks-specific additions: higher-order functions (`filter`, `transform`), SQL UDFs, and nested JSON flattening. These may differ from vanilla PySpark you've used elsewhere.
3. **Reference — [PySpark API docs](https://spark.apache.org/docs/latest/api/python/)** — `pyspark.sql.functions` module; bookmark and consult while coding.

> ⚠️ **DBR 18 Python UDF change:** Arrow is now the default interchange format for Python UDFs (was opt-in). TIMESTAMP inputs to UDFs no longer carry timezone metadata. If your UDFs rely on timezone-aware timestamps, test on DBR 18 before upgrading.

**Milestone:** You can read a JSON file into a DataFrame, flatten nested fields, join it with a second dataset, aggregate by a key, and write the result as a partitioned Delta table — all in PySpark.

---

### ⬜ B4 — Spark SQL & Relational Entities

**What it is:** SQL relational entities on Databricks within the Unity Catalog three-level namespace (`catalog.schema.table`): schemas (databases) and their storage location; the managed / external / foreign table types and what `DROP` does to each; `CREATE TABLE … AS SELECT` (CTAS); table constraints (`NOT NULL`, `CHECK`, plus UC's informational `PRIMARY KEY`/`FOREIGN KEY`); deep vs shallow `CLONE`; and the three view kinds — stored, temporary, and global temporary — distinguished by session scope.

**Why you need it:** Most data engineers use SQL for 80% of transformations; relational entities are how you make data shareable across notebooks and jobs.

**How to learn it:**

1. **Free course — DA-FREE, "Data Transformation Overview" section** (~30 min) — Covers creating databases, tables, and views in the Databricks context, including the managed vs external table distinction.
2. **Interactive — Free Edition SQL notebook** (~2 hrs) — Create a database, build a managed table from a CSV with CTAS, create a temp view and a persisted view, then query across all three.
3. **Book chapter — DCDE-SG Ch 3, "Mastering Relational Entities in Databricks"** (~1.5 hrs) — CTAS, table constraints, cloning Delta tables, view types comparison. Read the "CTAS Statements" and "Exploring Views" sections carefully.
4. **Reference — DB-DOCS: [SQL language reference](https://docs.databricks.com/aws/en/sql/language-manual/)** — Bookmark for DDL syntax lookup.
5. **Reference — [Databricks tables concepts](sources/databricks-docs/tables-concepts/)** (captured notes) — the current UC table model the book predates: three table types (managed/external/foreign) + temporary, two formats (Delta/Iceberg), managed-recommended default, and the per-operation permission matrix. Read alongside DCDE-SG Ch 3 to correct its `hive_metastore` framing.
6. **Reference — [Unity Catalog managed tables](sources/databricks-docs/managed-tables/)** (captured notes) — deep-dive on the default table type: create/drop SQL + privileges, `USING iceberg` (else Delta), deep/shallow clone rules, `UNDROP TABLE` + the configurable recovery period (0 or 7–30 days), and the managed-only feature set (predictive optimization, catalog commits, multi-statement transactions, full-text search, credential vending, Compatibility Mode).
7. **Reference — [Convert an external Delta table to managed](sources/databricks-docs/convert-external-managed/)** (captured notes) — the in-place external→managed migration: `ALTER TABLE … SET MANAGED` (vs CTAS/DEEP CLONE), `TRUNCATE UNIFORM HISTORY` for UniForm tables, two-phase copy + downtime estimates, 14-day rollback via `UNSET MANAGED`, path-based redirect (DBR 18.1+), and streaming restart behavior.
8. **Reference — [Specify a managed storage location in UC](sources/databricks-docs/managed-storage/)** (captured notes) — *where* managed-table/volume files land: the metastore → catalog → schema hierarchy (lower overrides higher, catalog-level recommended), `MANAGED LOCATION` at create vs `ALTER … SET MANAGED LOCATION` (DBR 18.1+, new objects only), Storage Root vs Storage Location, and the `CREATE MANAGED STORAGE` privilege.
9. **Reference — [Catalog commits](sources/databricks-docs/catalog-commits/)** (captured notes) — the managed-only Delta feature that moves commit coordination from the file system to Unity Catalog (`delta.feature.catalogManaged`, off by default): the enabling substrate behind multi-table transactions, plus faster planning (UC serves metadata, skips cloud storage), enforceable constraints, and safe external-engine writes (Beta). Reqs: UC managed tables, DBR 16.4+ to use / 18.0+ to toggle. Streaming/MV/single-user-cluster limitations. For the **write mechanics** the docs leave implicit — the staged-commits 4-step sequence (stage in `_delta_log/_staged_commits/` → propose → UC returns the winning commit → publish to `_delta_log`), the REST inspection endpoint, the **DynamoDB→UC** framing (UC replaces the old AWS S3 log store), and **ABAC on external reads** — see the practitioner note [sunnydata-catalog-commits](sources/sunnydata/catalog-commits/).
10. **Reference — [Transactions](sources/databricks-docs/transactions/)** (captured notes) — multi-statement, multi-table ACID transactions (the capability catalog commits unlocks): non-interactive `BEGIN ATOMIC…END` (row-level concurrency, recommended) vs interactive `BEGIN TRANSACTION;…COMMIT;` (table-level), snapshot-at-first-access isolation, optimistic concurrency + conflict scenarios, one-Delta-log-entry-per-transaction, and the limit list (DML-only, no DDL/streaming/time-travel/RLS, ≤100 tables, 48 h max). Beyond B4 exam scope but the modern primitive behind warehousing workloads. For the **SQL surface + on-storage mechanics** — the `BEGIN ATOMIC` example, the `.mst.json` staged-commit file, the success-vs-rollback walkthrough in the Delta log, and the SQL-only / not-OLTP(→Lakebase) / not-OSS-Spark boundaries — see the practitioner note [sunnydata-multi-statement-transactions](sources/sunnydata/multi-statement-transactions/).
11. **Reference — [Unity Catalog external tables](sources/databricks-docs/external-tables/)** (captured notes) — the external table *type* itself (complement to managed #6 and the convert-from-external #7): UC governs metadata only, data files sit at a `LOCATION` you pick in a registered external location; `DROP` removes metadata but **leaves the data files**; 7 file formats (DELTA/CSV/JSON/AVRO/PARQUET/ORC/TEXT); the two recommended use cases (UC-incompatible formats; direct non-Databricks client access where **UC privileges aren't enforced**); create perms (`CREATE EXTERNAL TABLE` + USE CATALOG/SCHEMA + CREATE TABLE), the multi-metastore S3 write hazard, and `MSCK REPAIR TABLE … SYNC METADATA` for out-of-band metadata edits.
12. **Reference — [Automatic upgrades for managed tables](sources/databricks-docs/automatic-upgrades/)** (captured notes) — how UC managed tables get GA recommended **table features turned on automatically** (no `ALTER TABLE`): the observation window (50 days PP / 100 days GA), **verified workloads** (cluster DBR ≥ feature min version) and the rule that one unverified/external access poisons the feature for the whole schema, the new/existing schema×table behavior matrix, the six features + min DBRs (auto CDF, auto liquid clustering, catalog commits, checkpoint V2, column mapping, row tracking), detecting it via a hash-username `SET TBLPROPERTIES` in history, and reverting (`RESTORE` / `ALTER TABLE … DROP FEATURE`). Excludes external tables, MVs, streaming tables, and OpenSharing-shared tables.
13. **Reference — [Checkpoint V2](sources/databricks-docs/checkpoint-v2/)** (captured notes) — the Delta table feature behind "checkpoint V2" in #12's list, now explained standalone: V2 log-checkpoint format that lets Delta **support more concurrent writers and cut write conflicts** on large/hot tables (DBR 13.3 LTS+). Enable per table (`delta.checkpointPolicy='v2'`), auto-on for liquid-clustering tables (DBR 14.1+) and via automatic upgrades; downgrade with `ALTER TABLE … DROP FEATURE v2Checkpoint`; manual checkpoint via `REORG TABLE`.
14. **Reference — [Partition discovery for external tables](sources/databricks-docs/external-partition-discovery/)** (captured notes) — the partition-discovery mechanics behind #11's `MSCK REPAIR` mention, now explained standalone: UC's **default** strategy recursively lists directories under `LOCATION` (slow at scale); **partition metadata logging** (`partitionMetadataEnabled='true'`, opt-in DBR 13.3 LTS+) switches to Hive-metastore-style behavior — UC reads only **registered** partition metadata and stops auto-scanning, so out-of-band/path-based writes need a manual repair. Non-Delta only (Parquet/ORC/CSV/Avro/JSON). Sync with `MSCK REPAIR TABLE … SYNC|ADD|DROP PARTITIONS` (Hive-style layouts) or `ALTER TABLE … ADD PARTITION … LOCATION` (non-Hive); list with `SHOW PARTITIONS`; session toggle `spark.databricks.nonDelta.partitionLog.enabled`. Databricks recommends liquid clustering over partitioning generally.
15. **Reference — [Work with foreign tables](sources/databricks-docs/foreign-tables/)** (captured notes) — the **third table type** itself (complement to managed #6 and external #11), previously only name-dropped: a foreign/federated table registered in a UC **foreign catalog** whose data *and* metadata stay in an external system, UC adding query governance only. Two registration paths — **query federation** (JDBC to PostgreSQL/MySQL) vs **catalog federation** (Hive Metastore/AWS Glue/Snowflake Horizon). **Read-only** except an *internal* federated Hive metastore; **no UC transactional guarantees** even when backed by Delta/Iceberg, and most optimizations need a UC managed table. Positioned as a migration stopgap (→ `convert-foreign-managed`, or replicate via materialized views). Cross-refs A7. Note the federated-HMS back-compat behavior and the "Updated by = last metadata-refresh `session_user`" quirk.
16. **Reference — [Convert a foreign table to managed](sources/databricks-docs/convert-foreign-managed/)** (captured notes, **embedded video walkthrough**) — the `SET MANAGED {MOVE | COPY}` migration off a foreign table into a UC managed table (Public Preview, DBR 17.3+, HMS/Glue federation only): preserves history/name/perms/views, sets predictive optimization to `INHERIT`; `MOVE` (in-place, kills external/path access, `UNSET MANAGED` rollback, 7-day data delete) vs `COPY` (duplicates data, source untouched); prereqs (Delta + external HMS table type), cross-region cost + streaming-restart caveats, and bulk-convert via discoverx.
17. **Reference — [Convert a foreign table to external](sources/databricks-docs/convert-foreign-external/)** (captured notes) — the lighter `ALTER TABLE … SET EXTERNAL {DRY RUN}` conversion (PP, DBR 17.3+, HMS/Glue only): UC governs metadata, **data files stay put** (no MOVE/COPY); broader formats (Delta/Parquet/ORC/Avro/JSON/CSV/TEXT vs Delta-only for managed); rollback = just `DROP` (re-federates as foreign); verify in **Catalog Explorer** (not `DESCRIBE EXTENDED`, which lies here); Glue Parquet-SerDe metadata fix + no-concurrent-writes caveat.
18. **Reference — [Temporary tables](sources/databricks-docs/temporary-tables/)** (captured notes) — the **fourth table type**, previously only name-dropped in the deltas callout: a session-scoped, **Delta-by-default** table that lives **outside the catalog namespace** (bare-name reference, no catalog/schema). **Any user can create one with no `CREATE TABLE` privilege**; session-isolated (others can't read/modify/detect it); auto-dropped at session end or after **7 days**; storage managed + auto-reclaimed (serverless → default storage; classic → workspace bucket). `CREATE {OR REPLACE} TEMP TABLE` (don't add `USING`; `REPLACE` needs the `TEMP` keyword or it hits a permanent table); `INSERT`/`UPDATE`/`MERGE` yes, but **no `DELETE FROM`, `ALTER`, clone, time travel, streaming, or DataFrame APIs**, and **not on Dedicated (single-user) clusters**. **Applies to Databricks SQL + Databricks Runtime 18.1+.**

**Milestone:** You can: explain managed vs external vs foreign tables and what `DROP TABLE` does to data in each; create and populate a table with CTAS; add a `CHECK` / `NOT NULL` constraint and explain why UC `PRIMARY KEY`/`FOREIGN KEY` are informational-only; explain deep vs shallow `CLONE` and when each is safe; recover a dropped managed table with `UNDROP TABLE` and explain the configurable recovery period; convert an external table to managed with `ALTER TABLE … SET MANAGED` and roll it back within 14 days; convert a foreign table (HMS/Glue-federated, Delta) to managed with `SET MANAGED MOVE` vs `COPY` and explain how to roll back (`UNSET MANAGED`, before any `DROP`); convert a foreign table to **external** with `SET EXTERNAL` (data stays in place; rollback = `DROP` → re-federate) and explain when you'd pick it over `SET MANAGED`; distinguish stored, temporary, and global-temporary views by their session scope; and distinguish a temporary **view** (a saved query, re-run on read) from a temporary **table** (a materialized, session-scoped Delta dataset; Databricks SQL + DBR 18.1+) — including that a temp table needs no `CREATE TABLE` privilege, is session-isolated, auto-drops at 7 days, and shares a namespace with temp views.

> 📌 **2026 deltas vs the DCDE-SG Ch 3 book** (from the [Ch 3 reading notes](sources/dcde-sg/ch03-mastering-relational-entities/)): (1) The book's `hive_metastore` + `dbfs:/mnt` demos **don't run on a UC-only workspace** — new accounts (after 2025-12-19) ship with Hive metastore and DBFS disabled with no opt-out, so `hive_metastore` doesn't even appear as a catalog. Use a UC catalog/schema + UC Volumes instead. (2) Databricks now defines **three table types — managed, external, *foreign*** (foreign = read-only Lakehouse Federation, see I8) — plus session-scoped temporary tables, across **two formats: Delta (default) + Apache Iceberg**. The book only covers managed/external/Delta. (3) **Managed is the recommended default** for new tables (auto-optimization, lower cost), inverting the book's "external = flexibility" framing. (4) **Global temporary views are unsupported on serverless** (the default compute) — attach a classic cluster for that one demo, or skip it. (5) Beyond the book's enforced `NOT NULL`/`CHECK`, UC adds **informational `PRIMARY KEY`/`FOREIGN KEY`** constraints — *not* enforced (no row rejection); they serve query optimization + lineage/ER tooling and surface in `INFORMATION_SCHEMA`. (6) **Shallow clone caveats** the book omits: UC shallow clone needs DBR 13.3+, only managed→managed / external→external, no nesting — and a shallow clone of a *managed* table can break when the source's `VACUUM` deletes files the clone still references.

> 📌 **New distinction — temporary *table* vs temporary *view* (Databricks SQL + DBR 18.1+)** (from the [temporary-tables note](sources/databricks-docs/temporary-tables/)): the "session-scoped temporary tables" mentioned above are a **first-class, materialized table type**, not a kind of view. A temp **view** is a saved query re-executed on read (no stored rows); a temp **table** materializes data as a session-scoped Delta dataset. The temp table needs **no `CREATE TABLE` privilege**, lives **outside the catalog namespace** (bare name), is **session-isolated**, and **auto-drops at session end or 7 days**. The two **share one namespace** (can't have both of the same name in a session). Supports `INSERT`/`UPDATE`/`MERGE` but **not** `DELETE FROM`, `ALTER`, clone, time travel, streaming, DataFrame APIs, or Dedicated clusters. Don't confuse with **global temporary views** (cross-session within a cluster, unsupported on serverless — see delta #4).

---

### ✅ B5 — Delta Lake Fundamentals

**What it is:** Delta Lake's ACID transaction model, the transaction log (_delta_log), and basic table operations: CREATE, INSERT, UPDATE, DELETE, MERGE.

**Why you need it:** Delta Lake is the default storage format for all Databricks tables; every pipeline you write reads or writes Delta.

**How to learn it:**

1. **Free course — DA-FREE, "Delta Lake Overview" and "Demo: Creating and Working with a Delta Table"** (~30 min) — Official Databricks walkthrough of Delta table internals, the transaction log, and basic table operations.
2. **Interactive — Free Edition** (~2 hrs) — Create a Delta table, INSERT rows, UPDATE a subset, view `DESCRIBE HISTORY`, run `SELECT * VERSION AS OF 0`.
3. **Book chapter — DCDE-SG Ch 2, "Managing Data with Delta Lake"** (~2 hrs) — Transaction log mechanics, time travel, OPTIMIZE, VACUUM. Read all sections; this is the densest beginner chapter.
4. **Reference — DB-DELTA docs** — [Delta Lake quickstart](https://docs.delta.io/latest/quick-start.html) and [table operations](https://docs.delta.io/latest/delta-update.html).

**Milestone:** You can explain what the `_delta_log` contains, run a time-travel query using both `VERSION AS OF` and `TIMESTAMP AS OF`, and describe why VACUUM is needed and what it does.

---

### ✅ B6 — Data Ingestion Basics

**What it is:** The three core batch ingestion patterns — CTAS (Create Table As Select from file), COPY INTO, and reading raw file formats (Parquet, JSON, CSV, Avro).

**Why you need it:** Every pipeline starts with ingestion; knowing which method to use and why prevents full-table rewrites.

**How to learn it:**

1. **Official course — DA-DE Module 1, "Cloud Storage Ingestion with LakeFlow Connect Standard Connectors"** (~2 hrs) — Hands-on lab covering CTAS, COPY INTO, and cloudFiles.
2. **Book chapter — DCDE-SG Ch 5, "Processing Incremental Data" — COPY INTO section** (~1 hr) — Covers idempotency guarantees and when to prefer COPY INTO vs CTAS.
3. **Interactive — Free Edition** (~1.5 hrs) — Upload a CSV to DBFS, ingest it three ways: plain `spark.read.csv()`, CTAS, and COPY INTO. Verify row counts match and check COPY INTO's idempotency by running it twice.
4. **Reference — DB-DOCS: [COPY INTO](https://docs.databricks.com/aws/en/ingestion/copy-into/)** — Syntax and supported formats reference.

**Milestone:** You can ingest a JSON file using COPY INTO, explain why running it twice doesn't duplicate rows, and describe when you'd choose CTAS over COPY INTO.

---

### ✅ B7 — Medallion Architecture

**What it is:** The multi-hop data design pattern — Bronze (raw ingest), Silver (validated/cleaned), Gold (aggregated/business-ready) — and the principles behind it.

**Why you need it:** This is the foundational design pattern for Databricks pipelines; all production work is structured around it.

**How to learn it:**

1. **Free course — DA-FREE, "Data Transformation Overview" and "Demo: Transforming Data Using the Medallion Architecture"** (~30 min) — Official Databricks walkthrough of Bronze/Silver/Gold layers with a live demo.
2. **Book chapter — BBDE Chapter: "Applying Software Development and DevOps Best Practices to Delta Live Tables Pipelines"** (~1 hr) — Shows how the Medallion pattern maps to production Lakeflow pipeline code.
3. **Hands-on — Free Edition** (~2 hrs) — Build a 3-table pipeline: raw JSON → Bronze Delta table → Silver with deduplication and type casting → Gold with aggregation. No orchestration yet — just run each notebook manually.
4. **Reference — DB-DOCS: [Medallion architecture](https://docs.databricks.com/aws/en/lakehouse/medallion.html)**
5. **Reference — [Batch vs. streaming data processing](sources/databricks-docs/batch-vs-streaming/)** (captured notes) — the page's Medallion-layer recommendation: **streaming at Bronze** (stateless append), **batch with materialized-view incremental refresh at Silver/Gold** (stateful transforms/aggregations — batch is simpler and always accurate). Maps the batch-vs-streaming choice onto the three layers you build here; the streaming mechanics live in **I2**.

**Milestone:** You can build a 3-layer Medallion pipeline in notebooks, explain why Bronze preserves raw data unchanged, describe the difference between Silver validation logic and Gold aggregation logic, and say which layers default to streaming vs batch and why.

---

### ✅ Beginner Checkpoint

You are ready to advance when you can:
- Write a PySpark pipeline that reads from a file, applies joins and aggregations, and writes a Delta table
- Explain the Delta transaction log and run a time-travel query
- Build a 3-hop Medallion pipeline across Bronze/Silver/Gold tables
- Describe the Databricks control/data plane architecture and cluster types

**Certification target:** These topics are prerequisite context for the DCDEA — not yet sufficient. Continue through Intermediate before attempting the exam.

---

## Intermediate

**Goal:** Build production-grade incremental pipelines with Auto Loader and Lakeflow Spark Declarative Pipelines, implement CDC, orchestrate multi-task jobs, and govern data with Unity Catalog.
**Estimated time:** ~45 hrs

---

### ⬜ I1 — Auto Loader & Incremental Ingestion

**What it is:** The `cloudFiles` Auto Loader source: continuously discovers and ingests new files from cloud storage with exactly-once guarantees and automatic schema inference.

**Why you need it:** COPY INTO is idempotent but batch; Auto Loader is streaming-based and handles high-volume, continuously arriving files at scale.

**How to learn it:**

1. **Official course — DA-DE Module 1, "Ingestion Alternatives" and Auto Loader lab** (~1.5 hrs) — The hands-on lab is essential; run it.
2. **Book chapter — DCDE-SG Ch 5, "Incremental Data Ingestion — Auto Loader section"** (~1 hr) — Covers schema inference, schema evolution, checkpoint locations, and the difference between directory listing mode and file notification mode.
3. **Interactive — Free Edition** (~2 hrs) — Build an Auto Loader stream from a DBFS landing zone: write 10 JSON files, start the stream, write 10 more, verify they appear in the target Delta table. Check the checkpoint directory.
4. **Reference — DB-DOCS: [Auto Loader](https://docs.databricks.com/aws/en/ingestion/auto-loader/)** — Schema evolution and configuration options reference.

> ⚠️ **DBR 17.3+ breaking change:** `input_file_name()` is removed. Use `df.select("_metadata.file_name")` instead. Any Auto Loader pipeline using `input_file_name()` will fail on DBR 17.3+.

> 🆕 **ZeroBus Ingest (GA, part of Lakeflow Connect):** know it as the **push-based** ingestion alternative to the pull-based file/source patterns on this topic. Where Auto Loader and COPY INTO *pull* files that have landed in cloud storage, ZeroBus is a serverless, fully-managed **push API** that writes records (events, telemetry, app/clickstream data, on-prem feeds) **directly into Unity Catalog Delta tables — no Kafka or intermediate message bus**. Sub-5-second latency, thousands of concurrent clients, up to ~100 MB/s per connection (>10 GB/s aggregate to a single table). Reach for it when producers can emit straight to the API and you want to drop the streaming-bus hop; stick with Auto Loader when data arrives as files. (Awareness-only for the DCDEA — the cert tests Auto Loader/COPY INTO — but it's the modern "events without Kafka" path and how Databricks now ingests on-prem event streams.) See the [GA announcement](https://www.databricks.com/blog/announcing-general-availability-zerobus-ingest).

**Milestone:** You can write an Auto Loader stream that ingests new JSON files incrementally, handles schema evolution with `mergeSchema`, and explain what the checkpoint directory contains and why it matters — and explain when you'd reach for **push-based ZeroBus Ingest** instead of pull-based Auto Loader/COPY INTO.

---

### ⬜ I2 — Structured Streaming with Spark

**What it is:** Spark Structured Streaming: the streaming query model, triggers (once, continuous, available-now), output modes (append, complete, update), watermarks, and stateful aggregations.

**Why you need it:** Lakeflow Spark Declarative Pipelines and Auto Loader both build on Structured Streaming; understanding it lets you reason about latency, state, and late-data handling.

**How to learn it:**

1. **Official course — DA-DE Module 3, streaming tables sections** (~1.5 hrs) — Covers the micro-batch model, triggers, checkpointing, and how Structured Streaming maps to Lakeflow Declarative Pipelines syntax.
2. **Book chapter — DCDE-SG Ch 5, "Streaming Data with Apache Spark" and "Spark Structured Streaming"** (~1.5 hrs) — Output modes, query configurations, streaming guarantees. Read carefully.
3. **Official course — DA-DE Module 3, Streaming Tables section** (~1 hr) — Shows how streaming concepts map to Lakeflow Declarative Pipelines syntax.
4. **Local repo — REPO-DLT** — Read the `kafka-fraud-detection` or `twitter-sentiment-analysis` example to see a complete streaming Lakeflow pipeline (Kafka source → Bronze streaming table → Silver transformations). Read the notebook code for patterns; don't worry about running it.
5. **Interactive — Free Edition** (~2 hrs) — Build a streaming word count with a 10-second trigger, using a Delta table as source and another as sink. Run with Trigger.AvailableNow, then with Trigger.Once. Compare behavior.
6. **Reference — DB-DOCS: [Structured Streaming](https://docs.databricks.com/aws/en/structured-streaming/)** — Trigger types and watermark reference.
7. **Reference — [Serverless compute limitations](sources/databricks-docs/serverless-limitations/)** (captured notes) — the serverless streaming constraints that shape this topic in practice (see callout).
8. **Reference — [Batch vs. streaming data processing](sources/databricks-docs/batch-vs-streaming/)** (captured notes) — the *concept* under this topic: the distinguishing question is whether the engine **tracks what it has already processed** (batch reprocesses all available source data and overwrites; streaming processes only new data and appends). Covers the late-/out-of-order-data complications that make **stateful** streaming (joins, aggregations, dedup) hard, the pros/cons + the Lakeflow product for each semantic, and the per-Medallion-layer recommendation (see callout).
9. **Reference — [Schema evolution in Databricks](sources/databricks-docs/schema-evolution/)** (captured notes) — the streaming-specific rule that bites here: a Structured Streaming query's **schema is locked at planning time** and reused by every micro-batch, so a mid-run source-schema change makes the query **fail by design** — you recover by **restarting** so Spark re-plans. The data set the stream writes to must *also* support evolution (streaming tables merge-evolve and auto-restart; materialized views full-recompute; Delta sinks need `mergeSchema`/column mapping/`overwriteSchema`). Detailed mechanism inventory lives in **I5 #7**.
10. **Reference — [Aggregate data on Databricks](sources/databricks-docs/aggregation/)** (captured notes) — the four aggregation types that frame stateful streaming:
11. **Reference — [foreachBatch — write to arbitrary data sinks](sources/databricks-docs/structured-streaming-foreach/)** (captured notes) — `streamingDF.writeStream.foreachBatch(fn)` applies batch functions to each micro-batch; required for MERGE in streaming (see I5 #8). **At-least-once** by default; use `batchId` → `txnAppId`/`txnVersion` for exactly-once on Delta. Does **not** work with continuous mode (use `foreach()` instead). Stateful operators: must consume entire batch or query fails next batch. Empty DataFrame: Delta OPTIMIZE writes empty batches → must handle `isEmpty()`. DBR 14.0 (Standard mode): `print()` → driver logs; `dbutils.widgets` unavailable; objects must be serializable. Multiple sinks: prefer multiple SS writers (foreachBatch serializes writes → latency). Error handling: propagate to orchestrator (Jobs/Airflow); Delta writes use `txnAppId`/`txnVersion` — no local retry. Exception table: transient → catch+retry/DLQ; idempotent duplicates → suppress; logic/schema/critical → propagate. DLQ pattern: split valid/invalid per micro-batch → separate Delta tables, both with `txnVersion`/`txnAppId`. Was name-dropped in I5 merge note. I2 still ⬜. **batch** (full recompute each run; cost and latency scale with data size), **stateful** (streaming; tracks observed records over time; **watermarks are required** — omitting them causes state to accumulate infinitely, leading to slowdowns and OOM); **incremental** (materialized views auto-track source changes and update aggregates on refresh — the recommended alternative to repeated batch queries or stateful streaming for pre-computed aggregates); **approximate** (`approx_count_distinct`, `approx_percentile`, `approx_top_k`, `TABLESAMPLE` — trade precision for speed on very large datasets).

> 💡 **Batch vs. streaming by Medallion layer (current platform guidance).** The default isn't "stream everything": Databricks recommends **streaming at Bronze** (ingestion is stateless append — you get streaming's efficiency without stateful complexity), and **batch with materialized-view incremental refresh at Silver/Gold** (transformation/aggregation is stateful — batch is simpler and always accurate; reach for streaming there only when latency/efficiency outweighs accuracy). On Databricks "streaming" is broader than Kafka — the unified Spark/Structured Streaming engine can read cloud object storage and Delta as streams, run triggered or continuous. This is the *why* behind choosing Auto Loader/streaming tables at Bronze (**I1**) and reasoning about triggers/watermarks/state here (**I2**).

> ⚠️ **Serverless only supports two triggers (current).** On serverless compute, only `Trigger.AvailableNow()` (recommended) and `Trigger.Once()` (deprecated but supported) work — `Trigger.ProcessingTime(...)` and `Trigger.Continuous(...)` raise `INFINITE_STREAMING_TRIGGER_NOT_SUPPORTED`. Spark's default is `ProcessingTime("0 seconds")`, so you **must** override it on serverless. (Note: this restriction applies to serverless *notebooks/jobs*, **not** to Lakeflow pipeline modes — see I3.) For genuinely continuous work use a continuous Lakeflow pipeline or `AvailableNow` on a scheduled job.

**Milestone:** You can write a streaming aggregation with a watermark, explain the difference between `Trigger.AvailableNow` and `Trigger.Once`, describe why append mode is preferred over complete mode for large tables, and state which triggers are available on serverless compute.

---

### ⬜ I3 — Lakeflow Spark Declarative Pipelines

**What it is:** Databricks' declarative ETL framework (formerly Delta Live Tables): define tables as SQL SELECT or Python function results; the engine manages execution order, incremental updates, data quality, and retries. Its object model: **flows** (the processing unit, same DataFrame API as Spark/Structured Streaming) write into **streaming tables**, **materialized views**, or **sinks** (external targets — Kafka, Event Hubs, UC external tables, or custom Python), all wrapped and run as a managed **pipeline**.

**Why you need it:** It's the standard way to build production pipelines on Databricks — handles incremental logic, observability, and data quality enforcement that you'd otherwise write manually. It's the **declarative** paradigm: you say *what* to produce and the engine plans execution — the opposite of the **procedural** Spark + Lakeflow Jobs model (I6), where you script the steps yourself. Reach for procedural only when the logic is too bespoke to express declaratively or you must hand-tune.

**How to learn it:**

1. **Official course — DA-DE Module 3, "Build Data Pipelines with Lakeflow Spark Declarative Pipelines"** (~4 hrs) — The most authoritative hands-on intro; complete all labs including the multi-hop pipeline lab.
2. **Book chapter — DCDE-SG Ch 6, "Exploring Delta Live Tables" through "Extending DLT Pipelines"** (~2 hrs) — Pipeline definitions, expectations syntax, live tables vs materialized views vs streaming tables, the LIVE schema.
3. **Reference — DB-DOCS: [Lakeflow Spark Declarative Pipelines](https://docs.databricks.com/aws/en/dlt/)** (~1 hr) — Walk through the pipeline syntax reference: streaming tables vs materialized views, CONSTRAINT syntax, pipeline configuration options. More current than any published book on this topic.
4. **Local repo — REPO-DLT** — Browse `wikipedia` and `divvy-bikesharing` examples first (clean, well-commented multi-hop pipelines). Then study `cdc-from-dms` and `apply-changes-from-snapshot` once you reach I4.
5. **Reference — DB-DOCS: [Lakeflow Spark Declarative Pipelines](https://docs.databricks.com/aws/en/dlt/)** — Pipeline configuration and Python/SQL syntax reference.
6. **Reference — [Serverless compute for Lakeflow pipelines](sources/databricks-docs/serverless-pipelines/)** (captured notes) — serverless is the recommended compute for **new** pipelines (UC required; enabling it wipes any classic cluster config): triggered/continuous/**real-time** modes all supported (and exempt from the serverless `AvailableNow`/`Once` trigger limit), the Standard vs Performance-Optimized DBU trade-off, and three serverless-exclusive features — **incremental refresh** (full-refresh fallback), **stream pipelining** (concurrent microbatches, on by default), and **vertical autoscaling**.
7. **Reference — [Materialized views (standalone + serverless)](sources/databricks-docs/materialized-views/)** (captured notes) — the MV compute model: a standalone MV (`CREATE MATERIALIZED VIEW` in Databricks SQL) is a UC managed table whose **create + every refresh always run on an auto-created serverless pipeline** (type `MV/ST`), billed as serverless Lakeflow SDP DBUs and independent of the warehouse that launched it. You submit from a **Pro/Serverless SQL warehouse** or a **serverless notebook**; the warehouse only coordinates. Plus triggers (ad-hoc / `TRIGGER ON UPDATE` / `SCHEDULE CRON`), sync vs `ASYNC` refresh, incremental-vs-full (needs Delta + row tracking + CDF), and the federation→replicate-foreign-table pattern.
8. **Reference — [Data engineering with Databricks (Lakeflow hub)](sources/databricks-docs/data-engineering-hub/)** (captured notes) — the orienting map of the whole DE surface: **Lakeflow** = Connect (ingest) + SDP (transform) + Designer + Jobs (orchestrate), on the Databricks Runtime. Names the SDP **object model** in full (flows / streaming tables / materialized views / sinks) — the **flows** and **sinks** pieces this topic otherwise under-names — and cross-maps every Lakeflow component to its learning-path topic (A3/I1/B6, I3, I6/A6, I2/E2).
9. **Reference — [Procedural vs. declarative data processing](sources/databricks-docs/procedural-vs-declarative/)** (captured notes) — the concept *under* this topic: **procedural** (say *how* — Apache Spark + Lakeflow Jobs, step-by-step, manual tuning) vs **declarative** (say *what* — SDP, system-planned/optimized). Includes the when-to-choose decision table; the justification for reaching for SDP vs hand-written Spark/Jobs (I6).

> 📌 DCDE-SG (Feb 2025) uses the term "Delta Live Tables" throughout. The framework is now **Lakeflow Spark Declarative Pipelines** but the SQL/Python API is identical. Treat the names as synonyms when reading the book.

> 🆕 **Lakeflow Designer** (GA June 2026) — a no-code, drag-and-drop + natural-language ETL builder. Every visual flow it produces compiles to a **Lakeflow Spark Declarative Pipeline** and runs under Unity Catalog governance. It's a UI on top of the engine you learn here, not a separate framework. After you can hand-write a declarative pipeline, build the same Medallion flow in Designer once and read the generated code to see how the visual operators map to streaming tables / materialized views.

> ⚡ **Materialized views are serverless under the hood.** A *standalone* MV (the Databricks SQL `CREATE MATERIALIZED VIEW` path Databricks recommends for replicating a foreign table into UC) always processes its create and refreshes on an **auto-created serverless pipeline** — you can't run that refresh on a classic cluster, and you're billed serverless Lakeflow SDP DBUs even if you launched it from a **dedicated** warehouse. You *submit* from a **Pro or Serverless** SQL warehouse (Classic isn't supported for federation) or a **serverless notebook**; the warehouse only coordinates. Prerequisite: serverless Lakeflow pipelines must be enabled in your workspace/region. (An MV authored *inside a regular pipeline* instead follows that pipeline's compute, which can be serverless **or** classic — so "MV = serverless" is specifically the standalone/DBSQL story.)

**Milestone:** You can build a 3-layer Medallion Lakeflow pipeline in SQL with at least two `CONSTRAINT` expectations, explain the difference between a Materialized View and a Streaming Table, explain that a standalone MV's create/refresh always runs on an auto-created **serverless** pipeline (submitted from a Pro/Serverless SQL warehouse or serverless notebook; classic compute can't run the refresh and serverless DBUs are billed even from a dedicated warehouse), and describe what happens when an expectation fails with `ON VIOLATION DROP ROW`.

---

### ⬜ I4 — Change Data Capture with APPLY CHANGES

**What it is:** The `APPLY CHANGES INTO` API for consuming CDC events (INSERT, UPDATE, DELETE) and materializing SCD Type 1 (upsert) or SCD Type 2 (full history) target tables.

**Why you need it:** Real production systems constantly change source data; CDC is the pattern for keeping lakehouse tables in sync without full reloads.

**How to learn it:**

1. **Official course — DA-DE Module 3, "Capturing Data Changes" lab** (~2 hrs) — Hands-on with `APPLY CHANGES INTO`; complete the lab.
2. **Book chapter — DCDE-SG Ch 6, "Capturing Data Changes" through "Processing Change Data Capture"** (~1.5 hrs) — CDC feed mechanics, source types (append-only vs complete), SCD Type 1 vs 2.
3. **Interactive — Free Edition** (~2 hrs) — Build a CDC pipeline: simulate a source that appends change events (op=I/U/D), run `APPLY CHANGES INTO` for SCD Type 1, then modify for SCD Type 2 history. Verify the history table has correct `__START_AT`/`__END_AT` columns.
4. **Local repo — REPO-DLT** — Study the `cdc-from-dms` folder (AWS DMS → Lakeflow CDC pipeline) and the `apply-changes-from-snapshot` folder (snapshot-based CDC without a CDC stream). Both are well-structured real examples.
5. **Reference — DB-DOCS: [APPLY CHANGES INTO](https://docs.databricks.com/aws/en/dlt/cdc.html)** — Sequence columns, KEYS, IGNORE NULL UPDATES options.
6. **Reference — [Change data capture and snapshots](sources/databricks-docs/what-is-cdc/)** (captured notes) — the CDC *concept* page behind `APPLY CHANGES INTO`: CDC feed vs snapshot ingestion, SCD Type 1 (overwrite — current state only) vs SCD Type 2 (versioned rows with `__START_AT`/`__END_AT`, active record has `__END_AT = NULL`), the `AUTO CDC` API (native change feeds from CDC-enabled DBs or Delta CDF; sequencing column must be monotonically increasing; `NULL` values not supported; initial hydration via *once flows* before switching to triggered/continuous), and `AUTO CDC FROM SNAPSHOT` (Python-only; diffs consecutive snapshots to generate a synthetic change feed; applies same SCD logic as `AUTO CDC`; **caveat**: misses interim changes within a snapshot period; out-of-order snapshots are ignored).

**Milestone:** You can write an `APPLY CHANGES INTO` statement for both SCD Type 1 and Type 2, explain what the `SEQUENCE BY` column is and why it's required, describe what `AUTO CDC` does in Lakeflow pipelines, and explain when to use `AUTO CDC FROM SNAPSHOT` instead and its snapshot-period caveat.

---

### ⬜ I5 — Delta Lake Advanced Operations

**What it is:** MERGE INTO for upserts, time travel, OPTIMIZE, VACUUM, Z-order (legacy), Liquid Clustering (current), Change Data Feed, and schema evolution.

**Why you need it:** Production Delta tables need ongoing maintenance; MERGE drives most ETL logic; understanding table optimization prevents query slowdowns.

**How to learn it:**

1. **Book chapter — DCDE-SG Ch 2, "Updating Tables & Exploring History" through "Optimizing Tables"** (~2 hrs) — MERGE INTO, time travel, VACUUM retention, Z-order (note: now superseded by Liquid Clustering).
2. **Interactive — Free Edition** (~2 hrs) — Run MERGE INTO for upsert logic on a 1M-row table; then run OPTIMIZE ZORDER; then enable Change Data Feed (`delta.enableChangeDataFeed`) and query `table_changes`.
3. **Reference — DB-DOCS: [Delta Lake table operations](https://docs.databricks.com/aws/en/delta/)** — MERGE syntax, Change Data Feed, schema evolution options.
4. **Reference — [Change data feed (CDF)](sources/databricks-docs/change-data-feed/)** (captured notes) — the CDF feature deep-dive: the two implementations (**Automatic CDF**, PP, read-time via row tracking, Delta + Iceberg v3, DBR 18+ — cheaper writes; vs **Legacy CDF**, write-time, Delta-only, `delta.enableChangeDataFeed`), the shared `table_changes()` / `readChangeFeed` APIs, the `_change_type`/`_commit_version`/`_commit_timestamp` metadata columns, batch (required starting version) vs streaming reads, archiving the transient feed for permanent history, out-of-range tolerance, and the column-mapping / row-filter / multi-statement-txn limitations.
5. **Reference — [Column mapping (rename & drop columns)](sources/databricks-docs/column-mapping/)** (captured notes) — the schema-evolution feature behind `ALTER TABLE … RENAME/DROP COLUMN`: metadata-only column rename (DBR 10.4 LTS+) / drop (11.3 LTS+) with no data rewrite, the `delta.columnMapping.mode` modes (`none`/`name`/`id`, `id` recommended but creation-only; `name` auto-set with UniForm), special-character column names, the reader-v2/writer-v5 protocol bump, what enabling it **breaks** (path-based reads use random partition prefixes, CDF across the change, streaming — fix via `schemaTrackingLocation`), and the expensive `none`-rewrite vs `DROP FEATURE` protocol downgrade. These rename/drop ops are exactly the *non-additive schema changes* CDF (#4) can't span.
6. **Reference — [Row tracking](sources/databricks-docs/row-tracking/)** (captured notes) — the row-level-lineage substrate behind automatic CDF (#4) and row-level concurrency: the two hidden fields `_metadata.row_id` (stable across MERGE/UPDATE) and `_metadata.row_commit_version`, `delta.enableRowTracking` (DBR 14.1+; Iceberg v3 has it built-in), the writer-protocol bump (one-way, blocks non-supporting writers), the slow backfill when enabling on existing tables, and the half-disable gotcha (`=false` doesn't remove the feature/protocol/fields). Required for some materialized-view incremental updates; its metadata fields can't be read from the CDF.
7. **Reference — [Schema evolution in Databricks](sources/databricks-docs/schema-evolution/)** (captured notes) — the *concept map* that unifies the mechanisms above (#5 column mapping) with `mergeSchema` / `overwriteSchema` / type widening. The page's key framing: schema evolution is **per-component, not a global switch** — each stage (connector → format parser → engine → data set) is configured independently, and an end-to-end pipeline only evolves cleanly if *every* stage agrees. Covers the five change-type taxonomy (new / rename / drop / type-widening / other-type-change) and which lever covers each on a Delta table (additive → `mergeSchema`; rename+drop → column mapping; broadening → type widening; arbitrary type change → `overwriteSchema` + full rewrite), plus the view `SCHEMA EVOLUTION` vs `SCHEMA TYPE EVOLUTION` distinction (see callout).
8. **Reference — [Upsert into a Delta Lake table using merge](sources/databricks-docs/merge/)** (captured notes) — the full `MERGE INTO` mechanics: basic upsert (`WHEN MATCHED UPDATE` / `WHEN NOT MATCHED INSERT`), the **`WHEN NOT MATCHED BY SOURCE`** clause (DBR 12.2 LTS+) for updating or deleting target rows with no source match (always add a condition to avoid a full-table rewrite; can't reference source columns), detailed clause semantics (evaluation order, last-clause-needs-no-condition rule, `updateAll()`/`insertAll()` schema requirements), the **deduplication pattern** (insert-only merge + date-bounded window + `foreachBatch` for streaming dedup), a pointer to `AUTO CDC` for SCD Type 1/2, and the **incremental sync pattern** — `WHEN NOT MATCHED BY SOURCE ... DELETE` with the same date filter on source and target to atomically propagate deletes for a bounded window. Also captures the DBR 16.0+ vs ≤15.4 LTS difference in duplicate-match detection (16.0+ considers both `ON` and `WHEN MATCHED` conditions; ≤15.4 uses `ON` only).
9. **Reference — [Selectively overwrite data with Delta Lake](sources/databricks-docs/selective-overwrite/)** (captured notes) — the four Delta selective-overwrite options, positioned as lighter alternatives to MERGE for batch replacement scenarios: **`REPLACE USING`** (recommended for most; replaces rows where specified columns compare equal, compute-independent, no session config — SQL DBR 16.3+, Python/Scala DBR 18.2+); **`REPLACE WHERE`** (predicate-based atomic overwrite, validates all written rows satisfy the predicate by default, empty source may delete rows — SQL DBR 12.2 LTS+, Python/Scala DBR 9.1 LTS+); **`REPLACE ON`** (like `REPLACE USING` but with a user-defined boolean expression, use when you need NULL-safe `<=>` matching — SQL DBR 17.1+, Python/Scala DBR 18.2+); **`partitionOverwriteMode=dynamic`** (legacy — replaces every touched partition, classic-only for SQL, risky if a row lands in the wrong partition). All four are atomic. Key distinction from MERGE: no per-row branching logic — reach for `REPLACE USING` when you know the key columns, `REPLACE WHERE` when you know the predicate window (e.g. a date partition); use MERGE only when you need `WHEN MATCHED`/`WHEN NOT MATCHED` clause logic. `replaceOn`/`replaceUsing` can't be combined with `replaceWhere`, `partitionOverwriteMode`, or `overwriteSchema` in Python/Scala.

> 📌 **Schema evolution is per-component, not one switch.** The [schema-evolution concept page](sources/databricks-docs/schema-evolution/) is the map; `mergeSchema` on a Delta sink **only adds new columns** — renaming needs [column mapping](sources/databricks-docs/column-mapping/), broadening needs type widening, and arbitrary type changes need `overwriteSchema` (full rewrite). Across a pipeline (Auto Loader → Delta, or Kafka → `from_avro` → Delta) **every** stage must be configured to evolve or the stream fails; streaming queries lock their schema at planning time and recover only by **fail-then-restart**. Materialized views are strictest — *any* schema change triggers a full recompute.

> 🆕 **Automatic CDF (2026, Public Preview)** is the modern default: it computes changes *at read time* from row-tracking metadata, so MERGE/UPDATE writes stay cheap and no per-table `delta.enableChangeDataFeed` is needed (DBR 18+, requires row tracking; Delta + Iceberg v3). Reader code (`table_changes`, `readChangeFeed`) is identical to legacy. Automatic upgrades (A2) can turn it on for you. Learn legacy enablement for the exam; expect automatic in practice.

> 📌 DCDE-SG covers Z-ORDER extensively. **Liquid Clustering** replaces Z-order (and partitioning) as the recommended layout strategy — GA for Delta on DBR 15.4 LTS+ (covered in A2). Both names appear on exams.

> 📌 In 2026, `OPTIMIZE` and `VACUUM` run **automatically** on Unity Catalog managed tables via Predictive Optimization (see A2). Learn the commands here for the exam and for external tables, but expect the platform to run them for you on managed tables in practice.

> ⚠️ **DBR 18 breaking changes:**
> - **NULL structs:** NULL structs are now stored as NULL (not as non-null structs with all-NULL fields) in MERGE, INSERT, and streaming with schema evolution. Test any MERGE statements that compared NULL struct fields.
> - **Time travel hard-errors:** Queries with `VERSION AS OF` or `TIMESTAMP AS OF` beyond the `deletedFileRetentionDuration` threshold now raise an error instead of a warning. Aggressive `VACUUM` (< 7 days) will block time travel.

**Milestone:** You can write a MERGE INTO for SCD logic, explain why `VACUUM` with a short retention window is dangerous, and enable and query Change Data Feed on a Delta table.

---

### ⬜ I6 — Lakeflow Jobs & Workflow Orchestration

**What it is:** Lakeflow Jobs (formerly Databricks Workflows): multi-task pipelines with dependencies, scheduling, retry logic, conditional branching, and task types (notebook, Python script, Lakeflow pipeline, SQL, dbt).

**Why you need it:** Notebooks and pipelines need to be orchestrated into reliable, schedulable production jobs; Jobs is how you do that on Databricks.

**How to learn it:**

1. **Official course — DA-DE Module 2, "Deploy Workloads with Lakeflow Jobs"** (~4 hrs) — Complete all labs including the multi-task job with notebook and pipeline tasks.
2. **Book chapter — DCDE-SG Ch 6, "Orchestrating Workflows with Databricks Jobs"** (~1 hr) — Job clusters vs all-purpose clusters for jobs, task dependencies, alerts.
3. **Interactive — Free Edition** (~2 hrs) — Build a 3-task job: Task 1 ingests data (Auto Loader), Task 2 runs a Lakeflow pipeline, Task 3 runs a SQL query. Add a failure alert via email.
4. **Reference — DB-DOCS: [Lakeflow Jobs](https://docs.databricks.com/aws/en/workflows/)** — Task type reference and retry configuration.
5. **Reference — [Serverless compute for jobs](sources/databricks-docs/serverless-jobs/)** (captured notes) — serverless is the **default compute** for jobs with supported task types (UC required; workload must support Standard access mode): five task types (notebook, Python script, dbt, Python wheel, JAR/PP), the Standard vs Performance-Optimized DBU trade-off, **auto-optimization** (auto-tune + retries, on by default — disable for non-idempotent tasks), and timeline-view + query-history debugging. Set an explicit timeout — serverless jobs have **no default execution timeout** and a 7-day hard max.

**Milestone:** You can build a multi-task Lakeflow Job with task dependencies, set up a schedule with a Quartz cron expression, add a failure notification, and explain when to use a job cluster vs an all-purpose cluster vs serverless for tasks.

---

### ⬜ I7 — Unity Catalog & Data Governance

**What it is:** Unity Catalog as the **complete data-governance solution**, spanning six pillars: **(1) access control** — three-level namespace (catalog.schema.table), metastore architecture, identity federation, hierarchical privilege model (`GRANT`/`REVOKE` from account down to rows/columns), row/column-level security, and **attribute-based access control (ABAC)**; **(2) discoverability** — Catalog Explorer, AI-generated comments, table insights, **entity relationship diagrams (ERD)** for FK-linked tables, and automatic **data lineage**; **(3) data quality monitoring** (see A6); **(4) collaboration/sharing** (OpenSharing/Clean Rooms/Marketplace — see A7); **(5) auditing** — audit logs surfaced via **system tables**; and **(6)** the legacy tools UC replaces (Hive-metastore table ACLs, IAM credential passthrough). UC governs structured **and** unstructured data plus AI assets (ML models), wherever the data lives.

**Why you need it:** Unity Catalog is mandatory for production Databricks deployments; all governance, sharing, and lineage flows through it.

**How to learn it:**

1. **Official course — DA-DG, "Get Started with Data Governance on Databricks"** (~3 hrs, free) — UC architecture, table/volume types, catalog & schema configuration, group-based access management, and fine-grained access controls: row-level security, column masking, and attribute-based access control (ABAC). Self-paced; complete all labs. (Replaces the retired "Data Management and Governance with Unity Catalog" course.)
2. **Book chapter — DCDE-SG Ch 8, "Implementing Data Governance"** (~2 hrs) — UC architecture, three-level namespace, identity management, implementing row and column security. Read all sections.
3. **Interactive — Free Edition or trial workspace** (~2 hrs) — Create a catalog, schema, and table in UC; grant SELECT to a second user; create a row filter and a column mask; inspect lineage in the Data Explorer.
4. **Reference — DB-DOCS: [Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)** — Privilege model and securable objects reference.
5. **Reference — [Data governance with Databricks (UC hub)](sources/databricks-docs/data-governance-hub/)** (captured notes) — the governance index mapping UC onto the six pillars above: the hierarchical access model + six access-control tasks (privileges, ABAC, identities, fine-grained row/column, external storage access, access from external platforms), the discoverability suite (Catalog Explorer / AI comments / table insights / lineage / ERD), data quality monitoring (anomaly detection + profiling), sharing (OpenSharing/Clean Rooms/Marketplace), auditing via system tables, and the two legacy tools UC replaces.

> 🆕 **Genie Ontology (announced DAIS 2026, Preview):** a self-improving **knowledge graph / semantic context layer** that sits on top of Unity Catalog and continuously learns your business — extracting and updating business meaning from Databricks data, dashboards, and queries plus 50+ connected apps (Google Drive, Jira, Slack, Confluence, SharePoint). It's grounded in the verified metric definitions in **Unity Catalog Metrics**, so AI agents (Genie) query agreed-upon definitions instead of guessing from raw schema; an **OntoRank** algorithm (PageRank for enterprise assets) ranks relevance by who created an asset, how often it's accessed, and how it connects to other concepts. For the DCDEA/DCDEP this is *awareness-only* — it's the context layer above the governance primitives (lineage, ERD, AI comments, metrics) you must still know by hand — but it explains where the discoverability/semantic story is heading. See the [Databricks blog](https://www.databricks.com/blog/unifying-data-and-governance-agentic-era-whats-new-azure-databricks). *(Also from DAIS 2026, on the same agentic thread: **Omnigent**, an open-source agentic model — purely AI/ML and tangential to the DE track, noted here only so the name is familiar.)*

**Milestone:** You can name the six governance pillars Unity Catalog covers; explain the three-level namespace; implement a `GRANT` for table-level access and explain when ABAC beats per-object grants; create a column mask using a SQL function; describe how Unity Catalog tracks data lineage automatically and what an ERD shows; and find an account's audit logs via system tables.

---

### ⬜ I8 — Databricks SQL & Analytics

**What it is:** SQL Warehouses (serverless and classic), Databricks SQL dashboards, scheduled queries, and alerts.

**Why you need it:** Data analysts and BI tools consume data through SQL Warehouses; as a data engineer you need to provision and configure them correctly.

**How to learn it:**

1. **Official course — DA-SQL, "SQL Analytics on Databricks"** (~4 hrs) — End-to-end: creating and sizing SQL Warehouses, SQL Editor, Unity Catalog data discovery, building dashboards, and setting alerts. Complete all hands-on exercises.
2. **Book chapter — DCDE-SG Ch 7, "Exploring Databricks SQL"** (~1.5 hrs) — Supplement for exam prep: sample questions, edge cases around SQL Warehouse config and dashboard behavior.
3. **Interactive — Databricks SQL UI** (~1.5 hrs) — Create a SQL Warehouse, write 3 queries against Gold tables from your Medallion pipeline, build a dashboard, and set an alert for a metric threshold.
4. **Reference — DB-DOCS: [Databricks SQL](https://docs.databricks.com/aws/en/sql/)** — Warehouse sizing and channel options.
5. **Reference — [SQL warehouse overview](sources/databricks-docs/sql-warehouse-overview/)** (captured notes) — what a SQL warehouse is (SQL-optimised compute, distinct from all-purpose/job clusters; renamed from "SQL endpoint" in 2023), the auto-created **Starter Warehouse**, auto-start on query, and that UC governs warehouse data access.
6. **Reference — [SQL warehouse types](sources/databricks-docs/sql-warehouse-types/)** (captured notes) — **Serverless > Pro > Classic**: Photon on all three; **Predictive IO** on serverless+pro; **Intelligent Workload Management (IWM)** serverless-only; serverless starts in 2–6 s (Databricks-managed) vs ~4 min for pro/classic (your AWS account); no credential passthrough on any type.

> 📌 **Pick the right warehouse type (current).** Use **Serverless** for almost everything — fastest startup, Predictive IO, and IWM (AI-driven queuing + rapid autoscaling). Use **Pro** only when serverless isn't in your region or you need custom networking (federation/hybrid). Use **Classic** only for entry-level interactive exploration. Gotcha: the UI defaults to Serverless but the **API defaults to Classic** — set the type explicitly when creating via API.

**Milestone:** You can create a serverless SQL Warehouse, name the three warehouse types and what each supports (Photon / Predictive IO / IWM), build a 3-widget dashboard, schedule a query to run daily, and set up an alert that emails when a row count drops below a threshold.

---

### ✅ Intermediate Checkpoint

You are ready to advance when you can:
- Build an end-to-end pipeline: Auto Loader ingest → Lakeflow Spark Declarative Pipeline (Bronze/Silver/Gold with expectations) → Lakeflow Job orchestration
- Implement CDC with `APPLY CHANGES INTO` for SCD Type 1 and Type 2
- Govern a catalog in Unity Catalog with row/column-level security and inspect lineage
- Pass a DCDEA practice exam with ≥80% correct

**Certification target:** **DCDEA** — validates B1–I8. Attempt now. Fee: $200, 45 questions, 90 min.

---

## Advanced

**Goal:** Tune Spark performance, design optimal storage layouts, handle enterprise ingestion, enforce data privacy, and deploy pipelines with CI/CD using Declarative Automation Bundles (DABs).
**Estimated time:** ~40 hrs

---

### ⬜ A1 — Spark Performance Tuning & the Spark UI

**What it is:** Reading the Spark UI (DAG, stages, tasks, executor metrics), diagnosing shuffle, skew, and spill, and applying fixes: broadcast joins, AQE, repartition strategies, and serialization. Plus the **platform optimization knobs** the Databricks Runtime exposes on top of open-source Spark — disk caching, dynamic file pruning, low shuffle merge, the cost-based optimizer, range join optimization, and Delta isolation-level tuning (see the "Platform optimization knobs" lessons below).

**Why you need it:** Production pipelines hit performance walls; knowing how to diagnose and fix them in the Spark UI is the most high-ROI advanced skill. Most Databricks Runtime optimizations are auto-on, but knowing *which* exist, *when* each fires, and *which* you can still tune by hand is what separates "the platform is slow" from a concrete fix.

**How to learn it:**

1. **Official course — DA-ADE Module 3, "Databricks Performance Optimization"** (~4 hrs) — Spark UI analysis lab, data skipping lab, join optimization lab. Complete all labs.
2. **Official course — Optimizing Apache Spark (Databricks Academy, self-paced)** — The "5 S's" framework: Skew, Spill, Shuffle, Storage, Serialization on production-scale 1TB+ datasets. Take this alongside or after DA-ADE Module 3 for the deepest coverage on this topic.
3. **Book chapter — UDEDW, performance chapters** (~2 hrs) — Shuffle optimization, serialization, caching strategy.
4. **Hands-on** (~3 hrs) — Take a deliberately slow join (1M rows × 1M rows without broadcast) and iteratively optimize it: add broadcast hint, enable AQE, fix skew with salting. Compare Spark UI before/after each change.
5. **Reference — DB-DOCS: [Spark UI guide](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide.html)** and **[AQE](https://docs.databricks.com/aws/en/optimizations/aqe.html)**
6. **Reference — captured Spark-UI & tuning notes** — the deep-dive notes behind this topic: [AQE](sources/databricks-docs/aqe/) (the four capabilities + config thresholds + how to read the adaptive plan), [SQL join hints](sources/databricks-docs/sql-join-hints/) (BROADCAST/SHUFFLE_HASH/MERGE/REBALANCE and how they interact with AQE), [optimize data workloads guide](sources/databricks-docs/optimize-data-workloads-guide/) (broadcast/shuffle-partition formulas), and the [Spark UI guide](sources/databricks-docs/spark-ui-guide/) plus its symptom-driven troubleshooting set — [long stage with high I/O](sources/databricks-docs/long-spark-stage-io/), [long stage / few tasks](sources/databricks-docs/long-spark-stage/), [long stage page](sources/databricks-docs/long-spark-stage-page/), [one long task (skew)](sources/databricks-docs/one-spark-task/), [slow stage, low I/O](sources/databricks-docs/slow-spark-stage-low-io/), [memory/OOM issues](sources/databricks-docs/spark-memory-issues/), [Spark rewriting all data](sources/databricks-docs/spark-rewriting-data/), [failing Spark jobs](sources/databricks-docs/failing-spark-jobs/), and [losing spot instances](sources/databricks-docs/losing-spot-instances/).

**Milestone:** You can open a Spark UI, identify a shuffle-heavy stage, apply a broadcast join hint, and explain what AQE's `coalescePartitions` and `skewJoin` do.

#### Platform optimization knobs

The Databricks Runtime layers its own optimizations on top of Apache Spark. Most are **enabled by default in DBR 10.4 LTS+** — you get them for free — but you must know which exist, when each helps, and which still take manual tuning. Source: the [Optimization recommendations](https://docs.databricks.com/aws/en/optimizations) hub ([captured notes](sources/databricks-docs/optimization-recommendations/)). These six are the gaps the rest of the path doesn't already teach (AQE → above; liquid clustering / predictive optimization → A2; Photon → E1).

##### Lesson 1 — Disk caching (formerly Delta / DBIO cache)

**What it is:** Databricks caches remote Parquet files (incl. Delta) onto worker **local SSDs** in a fast intermediate format, automatically on first read; successive reads of the same data are served locally. Distinct from Spark cache (`.cache()`/`.persist()`, in-memory, manual, any DataFrame/RDD). Disk cache auto-invalidates on file change — no manual cache busting. `CACHE SELECT` is ignored on SQL warehouses and DBR 14.2+ (an enhanced algorithm runs instead).

**When to use it:** Repeated reads of the same Parquet/Delta data — BI dashboards, ad-hoc/interactive analytics, iterative notebook development. The easy path is to pick an **SSD-backed (cache-accelerated) worker type** — those auto-enable and size it (uses ≤ half the local SSD). *Pitfall:* with autoscaling, a decommissioned worker loses its cache → re-reads from source.

**How to learn it:**

1. **Reference — DB-DOCS: [Disk caching](https://docs.databricks.com/aws/en/optimizations/disk-cache)** ([captured notes](sources/databricks-docs/disk-cache/)) — config flags (`spark.databricks.io.cache.enabled`, `.maxDiskUsage`, `.compression.enabled`) and the disk-vs-Spark-cache comparison table.
2. **Hands-on** (~30 min) — On an SSD-backed cluster, run a heavy scan-and-filter query twice; compare second-run time and check the Storage tab. Toggle `spark.conf.get("spark.databricks.io.cache.enabled")` and re-test.

**Milestone:** You can explain disk cache vs Spark cache (local SSD + automatic vs in-memory + manual), pick a cache-accelerated worker type, and predict the autoscaling cache-loss effect.

##### Lesson 2 — Dynamic file pruning (DFP)

**What it is:** A runtime optimization that pushes a join filter from a small (dimension) table into the scan of a large (fact) table, skipping data files that can't match — *before* reading them. Default-on (`spark.databricks.optimizer.dynamicFilePruning = true`). For `MERGE`/`UPDATE`/`DELETE`, DFP **requires Photon**; for `SELECT`, Photon makes it broader/more reliable (without Photon it may still apply depending on plan shape).

**When to use it:** Automatic — but it only triggers when the probe-side Delta table is **≥ 10 GB** (`deltaTableSizeThreshold`) and **≥ 10 files** (`deltaTableFilesThreshold`). Most effective on **non-partitioned tables / joins on non-partitioned columns**, and the benefit tracks how well-clustered the data is → **pair with liquid clustering** (A2). Star-schema fact×dim joins are the canonical win.

**How to learn it:**

1. **Reference — DB-DOCS: [Dynamic file pruning](https://docs.databricks.com/aws/en/optimizations/dynamic-file-pruning)** ([captured notes](sources/databricks-docs/dynamic-file-pruning/)) — the three config thresholds and the Photon requirement.
2. **Hands-on** (~30 min) — Join a >10 GB fact table to a filtered small dim; in the Spark UI scan node, read "files pruned" / bytes scanned. Cluster the fact table (A2) and re-measure.

**Milestone:** You can explain what DFP pushes down and when, name the size/file thresholds, state that MERGE/UPDATE/DELETE DFP needs Photon, and explain why liquid clustering amplifies it.

##### Lesson 3 — Low shuffle merge

**What it is:** An optimized `MERGE` implementation (GA, default-on **DBR 10.4 LTS+**) that processes **unmodified** rows in a streamlined, shuffle-free path instead of pushing them through the same shuffles as modified rows. Cuts shuffled data sharply, and **preserves existing data layout** (incl. liquid clustering / Z-order) on unmodified rows on a best-effort basis — reducing the need to re-`OPTIMIZE` after a `MERGE`.

**When to use it:** Automatic on DBR 10.4+ (the `spark.databricks.delta.merge.enableLowShuffle` flag is a no-op there). Nothing to enable — this lesson is about *reasoning*: MERGE rewrites whole files even to change a few rows, so low shuffle merge matters for any frequent-MERGE / CDC / SCD workload. *Caveat:* newly inserted/updated rows still may not be optimally laid out → periodic `OPTIMIZE` on clustered tables is still warranted.

**How to learn it:**

1. **Reference — DB-DOCS: [Low shuffle merge](https://docs.databricks.com/aws/en/optimizations/low-shuffle-merge)** ([captured notes](sources/databricks-docs/low-shuffle-merge/)) — the unmodified-row processing model and layout-preservation caveat.
2. **Tie-in** — Revisit your I4 CDC / I5 `MERGE INTO` work and explain why repeated merges degrade layout more slowly now.

**Milestone:** You can explain why MERGE rewrites unmodified rows at all, what low shuffle merge changes, and why you might still run `OPTIMIZE` after merges.

##### Lesson 4 — Cost-based optimizer (CBO)

**What it is:** Spark SQL's CBO uses **table + column statistics** to choose better plans — especially join order and strategy — for multi-join queries. Default-on (`spark.sql.cbo.enabled = true`). It's only as good as the stats: collect them with `ANALYZE TABLE … COMPUTE STATISTICS {FOR ALL COLUMNS}`, and refresh after writes. **Predictive optimization runs `ANALYZE` automatically** on UC managed tables (A2) — so on managed tables this is largely handled for you.

**When to use it:** Complex analytical queries with **multiple joins**. Diagnose via `EXPLAIN` — missing `rowCount` means absent stats; **DBR 16.0+** `EXPLAIN` prints a per-table `missing / partial / full` stats summary with a corrective `ANALYZE` command. The Spark SQL UI shows `est:` vs actual rows and the estimation-error factor.

**How to learn it:**

1. **Reference — DB-DOCS: [Cost-based optimizer](https://docs.databricks.com/aws/en/optimizations/cbo)** ([captured notes](sources/databricks-docs/cost-based-optimizer/), with annotated EXPLAIN-plan screenshots) — `ANALYZE`, reading `EXPLAIN` stats, the Spark SQL UI estimate lines.
2. **Hands-on** (~45 min) — Run a 3-table join with no stats, `EXPLAIN` it (note `est: N/A`), run `ANALYZE TABLE … COMPUTE STATISTICS FOR ALL COLUMNS`, re-`EXPLAIN`, and compare the estimation-error factor in the Spark SQL UI.

**Milestone:** You can collect table/column stats, read an `EXPLAIN` plan to spot missing stats, explain why `rowCount` drives multi-join plans, and state how predictive optimization keeps managed-table stats fresh.

##### Lesson 5 — Range join optimization

**What it is:** Speeds joins whose condition is a **point-in-interval** (`p BETWEEN start AND end`, inequalities) or **interval-overlap** join — otherwise executed as a slow nested loop. It splits the value domain into equal **bins** so only candidates in the same bin are compared. In **Databricks SQL it's automatic** (the optimal bin size is derived by sampling); elsewhere you tune it with a `/*+ RANGE_JOIN(relation, binSize) */` hint or `spark.databricks.optimizer.rangeJoin.binSize`. Applies to numeric/`DATE`/`TIMESTAMP` columns of the same type, `INNER` (or specific `OUTER`) joins.

**When to use it:** Slow joins on time windows, IP/number ranges, point-in-polygon/geo bucketing, "event falls within interval" lookups. *Pitfall:* if a numeric **equality** key sits alongside the range condition, the optimizer may bin it and hurt performance — **cast equality keys to `STRING`** to exclude them. For `DATE`, bin size = days; for `TIMESTAMP`, = seconds (fractions allowed). Choose bin size from the interval-length distribution (`APPROX_PERCENTILE`), starting near the 90th percentile.

**How to learn it:**

1. **Reference — DB-DOCS: [Range join optimization](https://docs.databricks.com/aws/en/optimizations/range-join)** ([captured notes](sources/databricks-docs/range-join/)) — the hint/session syntax, the `APPROX_PERCENTILE` bin-size method, and the numeric-equality-key pitfall.
2. **Hands-on** (~1 hr) — Join an events table to a time-windows table with a `BETWEEN`; measure runtime, add `/*+ RANGE_JOIN(windows, 60) */`, re-measure, then tune bin size via the percentile query.

**Milestone:** You can recognize a range join, add a `RANGE_JOIN` hint with a sensible bin size, explain how binning prunes candidates, and apply the cast-equality-key-to-`STRING` fix.

##### Lesson 6 — Delta isolation levels (opt-in write-serializable tuning)

**What it is:** Delta gives ACID guarantees with two isolation levels — **`WriteSerializable` (default)** and **`Serializable` (stricter)**. WriteSerializable allows slightly more concurrency; Serializable guarantees read-serializability at the cost of throughput on concurrent writes. Set per table: `ALTER TABLE … SET TBLPROPERTIES ('delta.isolationLevel' = 'Serializable')`. **Row-level concurrency** (tied to deletion vectors + row tracking, see [liquid-clustering](sources/databricks-docs/liquid-clustering/)) reduces conflicts independently of the level.

**When to use it:** Stick with the default `WriteSerializable` for almost everything — only raise to `Serializable` when an application genuinely needs read-serializability. *Pitfall:* metadata changes (protocol, table properties, schema) make **all concurrent writes fail** and **break streaming reads** until restarted — relevant whenever you flip this property on a live table.

**How to learn it:**

1. **Reference — DB-DOCS: [Isolation levels and write conflicts](https://docs.databricks.com/aws/en/optimizations/isolation-level)** ([captured notes](sources/databricks-docs/isolation-levels/)) plus the captured [transactions](sources/databricks-docs/transactions/) note for the broader concurrency/conflict model.
2. **Tie-in** — Connect to B4/I5: explain why a multi-writer pipeline rarely needs `Serializable` and what conflict it would actually prevent.

**Milestone:** You can explain `WriteSerializable` vs `Serializable`, set the table property, predict the concurrent-write/streaming impact of the metadata change, and state when row-level concurrency makes the level moot.

> ⚠️ **Deprecated — skip:** **Bloom filter indexes** are deprecated on Databricks. The docs say use **predictive I/O** (SQL warehouse Pro/Serverless, see [sql-warehouse-types](sources/databricks-docs/sql-warehouse-types/)) or **liquid clustering** (A2) instead. Know the name only so you recognize it in old material; don't build new tables around it.

---

### ⬜ A2 — Liquid Clustering & Storage Optimization

**What it is:** Liquid Clustering — the current recommended data layout strategy: cluster columns, incremental clustering, when to use it vs partitioning vs Z-order.

**Why you need it:** Inefficient data layout causes excessive file reads and slow queries; Liquid Clustering replaces both partitioning and Z-order — **GA for Delta on DBR 15.4 LTS+** (Public Preview for Iceberg on DBR 16.4 LTS+; managed Iceberg v3 features need DBR 18.0+) — and is now the default recommendation for all new tables, including streaming tables and materialized views.

**How to learn it:**

1. **Official course — DA-ADE Module 1, "Multi-flow pipelines and liquid clustering" section** (~1 hr) — Hands-on with clustering on a Lakeflow pipeline.
2. **Video — Databricks YouTube: search "Liquid Clustering Databricks 2025"** (~30 min) — Official Databricks engineering explanation of why Liquid Clustering supersedes Z-order.
3. **Interactive — Free Edition** (~2 hrs) — Create a 5M-row Delta table, run queries on an unclustured table (note scan size), add `CLUSTER BY (date, region)`, run `OPTIMIZE`, rerun queries, compare bytes scanned in Spark UI.
4. **Reference — DB-DOCS: [Liquid Clustering](https://docs.databricks.com/aws/en/tables/clustering)** and **[Predictive Optimization](https://docs.databricks.com/aws/en/optimizations/predictive-optimization)**
5. **Reference — [Use liquid clustering for tables](sources/databricks-docs/liquid-clustering/)** (captured notes) — the full LC reference: `CLUSTER BY` create/alter syntax (SQL + DataFrame APIs, keys mutable without rewrite, max 4 keys); `CLUSTER BY AUTO` automatic key selection (DBR 15.4 LTS+, UC managed, driven by predictive optimization); converting a partitioned table via `REPLACE PARTITIONED BY WITH CLUSTER BY` (DBR 18.1+); migrating-from-partition/Z-order key guidance; `OPTIMIZE` vs `OPTIMIZE FULL` (incremental vs force recluster); clustering-on-write size thresholds (lower for managed tables); and the writer-v7/reader-v3 protocol lock-in.
6. **Reference — [Predictive optimization for UC managed tables](sources/databricks-docs/predictive-optimization/)** (captured notes) — the deep dive behind the callout below: the three ops (`OPTIMIZE`/`VACUUM`/`ANALYZE`) and that PO's `OPTIMIZE` skips `ZORDER`; the account→catalog→schema inheritance model + `ALTER {CATALOG|SCHEMA} … {ENABLE|DISABLE|INHERIT} PREDICTIVE OPTIMIZATION`; the `delta.deletedFileRetentionDuration` (7-day default) `VACUUM` retention trap to set *before* enabling; serverless-jobs billing; the `system.storage.predictive_optimization_operations_history` observability table; and exclusions (external tables, OpenSharing recipients).

> 🆕 **Predictive Optimization (2026 default behavior):** For Unity Catalog **managed** tables, Databricks now autonomously runs `ANALYZE`, `OPTIMIZE`, and `VACUUM` on serverless compute — enabled by default for accounts created on/after 2024-11-11, with the rollout to older accounts completing ~August 2026. You still need to *understand* these operations (and choose `CLUSTER BY` keys — that part is not automated), but you no longer hand-schedule maintenance jobs on managed tables. Manual `OPTIMIZE`/`VACUUM` still matters for external tables and for reasoning about what the platform is doing.

**Milestone:** You can define Liquid Clustering on a new table with `CLUSTER BY`, run `OPTIMIZE` to apply it, explain why you'd choose Liquid Clustering over partitioning for a high-cardinality filter column, and describe when a partition is still preferable.

---

### ⬜ A3 — Lakeflow Connect & Enterprise Ingestion

**What it is:** Lakeflow Connect's managed connectors for ingesting from enterprise sources: relational databases (CDC via Debezium), SaaS (Salesforce, ServiceNow), and Kafka — without writing custom code.

**Why you need it:** Real enterprise data doesn't live in files; most pipelines require ingesting from operational databases or SaaS systems, and Lakeflow Connect handles the complexity.

**How to learn it:**

1. **Official course — DA-DE Module 1, "Enterprise Data Ingestion with LakeFlow Connect Managed Connectors"** (~2 hrs) — Complete the hands-on lab for a database connector.
2. **Official course — DA-ADE Module 1 advanced ingestion sections** (~1 hr) — Multiplex patterns and Kafka ingestion.
3. **Local repo — REPO-DLT** (~1 hr) — Study the `dms-dlt-cdc-demo` folder: this shows end-to-end AWS DMS → Lakeflow pipeline CDC ingestion from a relational database. Also look at the Fivetran integration example for SaaS ingestion patterns.
4. **Book chapter — BBDE, "How to Set Up Your First Federated Lakehouse"** (~1 hr) — Context on where managed ingestion fits in the architecture.
5. **Reference — [Managed connectors in Lakeflow Connect](sources/databricks-docs/lakeflow-connect-managed/)** (captured notes) — hub for all six connector types: **database/CDC** (MySQL/PostgreSQL/SQL Server — requires ingestion gateway + staging storage, gateway runs as its own continuous-task job), **query-based** (schedule-based direct queries, no gateway), **SaaS** (Salesforce/HubSpot/Jira/Workday — cursor-column or API-based), **file source** (Google Drive/SharePoint), **streaming** (RabbitMQ), **community** (no SLA). Architecture: Connection (UC securable with auth) + Ingestion pipeline (SDP on serverless) + Destination streaming tables; CDC adds gateway + staging. Incremental: full load on first run, then change tracking/CDC/cursor on subsequent runs. Networking: SaaS via API, cloud DBs via Private Link or VPC peering, on-premises via Direct Connect/ExpressRoute. Deploy with DABs for CI/CD. Automatic exponential-backoff retries; stores cursor position on manual-intervention errors.
6. **Reference — [What is Lakeflow Connect?](sources/databricks-docs/lakeflow-connect-overview/)** (captured notes) — the orienting hub: two service models (fully-managed vs custom pipeline), the **ETL stack layer model** (start most managed, drop down if unsupported — fully-managed connectors on top, then SDP below), four connector types (managed / community / standard / file upload), ingestion partners + DIY (dlt/Airbyte/Debezium), and the **ingestion alternatives** (Lakehouse Federation + OpenSharing for when you don't want to copy data). Key efficiency note: incremental reads + writes in Lakeflow Connect paired with incremental transformations downstream gives the biggest ETL performance gains.
7. **Reference — [Common patterns for managed ingestion pipelines](sources/databricks-docs/lakeflow-connect-common-patterns/)** (captured notes) — 12 advanced configuration techniques for managed connector pipelines: column selection (reduce egress), row filtering (SQL-like at source), full refresh (force complete re-sync), SCD Type 2 history tracking, multi-destination pipelines (fan-out to multiple schemas/catalogs from one pipeline), Run as identity (UC access control), source data lineage (end-to-end UC lineage from operational DB), TLS certificate validation (PITM protection for database connectors), pipeline tagging/maintenance/cost monitoring. Not all connectors support all patterns — check connector-specific docs.
8. **Reference — [Select columns to ingest](sources/databricks-docs/lakeflow-connect-column-selection/)** (captured notes) — `include_columns` (opt-in, freezes schema — future columns excluded) vs `exclude_columns` (opt-out, schema-forward — future columns auto-included). Set in `table_configuration` of a `table` or `report` object. DABs YAML + Notebook Python + CLI JSON examples for Google Analytics, Salesforce, and Workday (Workday uses `report` + `source_url` instead of `table` + `source_schema`/`source_table`).
9. **Reference — [Fully refresh target tables](sources/databricks-docs/lakeflow-connect-full-refresh/)** (captured notes) — three trigger interfaces (Lakehouse UI / Pipelines API / CLI). CDC-optimized full refresh: snapshot runs while table stays queryable with old data → atomic apply when snapshot completes (reduces PENDING_RESET). Important: gateway snapshots can't be resumed — pipeline updates during a snapshot cancel it. For DB connectors: **full refresh window** (`full_refresh_window.start_hour`/`days_of_week`/`time_zone_id` in `ingestion_definition`) to schedule snapshots; **auto full refresh policy** (`table_configuration.auto_full_refresh_policy.enabled`/`min_interval_hours`) to auto-trigger on DDL changes (truncate, schema change, column rename/add-with-default). Pipeline-level policy can be overridden per table.
10. **Reference — [History tracking / SCD Type 2](sources/databricks-docs/lakeflow-connect-scd/)** (captured notes) — `scd_type: SCD_TYPE_2` in `table_configuration` keeps a history of changes (`__START_AT`/`__END_AT` columns); default is `SCD_TYPE_1` (overwrite). DB connectors (SQL Server) require `sequence_by: <column>` (Timestamp/Date/Integer/Long/String). Note: source deletes/drops don't remove destination data even with SCD Type 1. Full refresh wipes all row versions — history restarts from refresh. GA: SCD 2 supported only for `users`/`pseudonymous_users` (not event tables). DABs/Notebook/CLI examples for GA, Salesforce, SQL Server, Workday. Distinct from the SDP `APPLY CHANGES INTO` / `AUTO CDC` SCD2 approach.
11. **Reference — [Create multi-destination pipelines](sources/databricks-docs/lakeflow-connect-multi-destination/)** (captured notes) — one pipeline → multiple `destination_catalog`/`destination_schema` targets; top-level `catalog`/`schema` on the pipeline resource = **event log location** (not default destination). Duplicate table names in the same destination schema are blocked — use `destination_table` to rename. Two patterns: multiple objects into different schemas; same object ingested N times with `destination_table` for schema-collision avoidance. Applies to GA, MySQL, Salesforce, SQL Server, Workday.
12. **Reference — [Name a destination table](sources/databricks-docs/lakeflow-connect-table-rename/)** (captured notes) — `destination_table` param overrides default (source table name) per `table`/`report` object; required when same object ingested into two tables in the same destination schema. UI: "Destination table" field on Source page of wizard. DABs YAML + Notebook Python + CLI JSON examples for GA, Salesforce, Workday (Workday uses `report` + `source_url`).
13. **Reference — [Monitor managed ingestion pipeline cost](sources/databricks-docs/lakeflow-connect-monitor-costs/)** (captured notes) — `system.billing.usage` with `billing_origin_product = 'LAKEFLOW_CONNECT'`; `usage_metadata` struct: `dlt_pipeline_id` + `uc_table_catalog/schema/name`; `usage_unit` = MILLISECOND or DBU. Maintenance charges accrue even when idle (infrastructure + change tracking). 8 SQL query patterns: monthly totals, most-expensive pipelines (JOIN `system.lakeflow.pipelines`), per-pipeline trend, dollar cost (JOIN `system.billing.list_prices`), budget-tag chargeback (`custom_tags`; API-only tagging), maintenance vs processing (0.1 DBU/hour threshold), MoM growth, cost-by-destination-catalog. Recommend AI/BI dashboard with pre-built cost monitoring template.
14. **Reference — [Common pipeline maintenance tasks](sources/databricks-docs/lakeflow-connect-pipeline-maintenance/)** (captured notes) — 8 ops: restart pipeline (`POST /api/2.0/pipelines/{id}/updates`), restart gateway (forces table discovery < 6h), full refresh, update schedule (**Jobs API** `POST /api/2.2/jobs/update` — not Pipelines API), alerts (auto-configured, customize via `PUT /api/2.0/pipelines/{id}`), staging file cleanup (auto after Jan 6 2025: delete at 25 days / physical removal at 30 days; pipelines without successful run > 25 days → data gaps → full refresh needed; pre-2025 pipelines require Support), specify-tables (table vs schema specification), verify ingestion (UI list view; Upserted/Deleted columns hidden by default). Was name-dropped in common-patterns. A3 still ⬜.
15. **Reference — [Apply tags to managed ingestion pipelines](sources/databricks-docs/lakeflow-connect-pipeline-tags/)** (captured notes, Public Preview) — `tags` key-value object in pipeline spec (API/CLI only); distinct from serverless usage policies (tags = pipeline resource metadata; usage policies = billing record labels). Propagate to `system.lakeflow.pipelines` + billing records → enables `custom_tags[:key]` cost-attribution queries (see ref #13). Was name-dropped in common-patterns + monitor-costs. A3 still ⬜.
16. **Reference — [Select rows to ingest (row filtering)](sources/databricks-docs/lakeflow-connect-row-filtering/)** (captured notes, Beta) — `table_configuration.row_filter` SQL WHERE-like string; requires `"channel": "PREVIEW"`. Supported: GA, Salesforce, ServiceNow, all query-based connectors; DB connectors (CDC/gateway) **not** supported. Applies during initial load + incremental updates. Salesforce: filter on primary key (`ID`) + cursor column only. ServiceNow: `AND` only (no `OR`); reference field filters applied post-fetch (source volume not reduced). GA: numeric columns must be **unquoted** (`event_timestamp >= 1712224270703246`) or server-side filtering is skipped → slow initial load. Operators: `AND`/`OR`(GA+SFDC only)/`=`/`!=`/`<`/`<=`/`>`/`>=` — no `LIKE`, no `IN`. Edge case: changing filter does not delete already-ingested rows that no longer match; full refresh only needed to pick up rows that previously didn't match. Absent from A3 before. A3 still ⬜.
17. **Reference — [Configure the Run as identity](sources/databricks-docs/lakeflow-connect-run-as/)** (captured notes) — default: pipeline runs as owner (user); recommendation: change to service principal so pipeline survives owner departure/access loss. UI-only: Advanced settings → Run as dropdown, during creation or via Edit pipeline. Was name-dropped in common-patterns. A3 still ⬜.
18. **Reference — [Managed connector FAQs](sources/databricks-docs/lakeflow-connect-faq/)** (captured notes) — key facts: schema evolution (new col → auto+NULL; deleted col → inactive not dropped; same-name reuse → pipeline fails; SFDC rename = delete+add; SQL Server rename = full refresh); multi-destination pipelines become **API-only** (can't edit in UI); concurrent update N+1 skipped if N still running; pipeline deletion **drops destination tables**; `ALTER STREAMING TABLE`/`ALTER MATERIALIZED VIEW` allowed for columns/tags/masks/row-filters but NOT schedule; SaaS pricing = serverless SDP DBUs only; DB connectors = classic + serverless possible; gateways **require classic compute** (no serverless-only workspaces); CDF auto-enabled on all destination tables. Absent from A3 before. A3 still ⬜.
19. **Reference — [Managed database connectors (CDC)](sources/databricks-docs/lakeflow-connect-cdc-overview/)** (captured notes) — 5-component architecture: Connection (UC securable) + Ingestion gateway (classic compute, **continuous** — reads before source change logs truncated) + Staging storage (UC volume, auto-purged 30 days, decouples gateway from pipeline schedule) + Ingestion pipeline (serverless) + Destination streaming tables. Key gotchas: pay for gateway classic compute **even when pipeline idle**; initial snapshot can fail on undersized gateway compute. SQL Server unique: also supports full-snapshot mode (MySQL/PostgreSQL CDC only). Cross-cloud supported. Was name-dropped in managed overview; ops detail absent. A3 still ⬜.
20. **Reference — [Query-based connectors](sources/databricks-docs/lakeflow-connect-query-based-overview/)** (captured notes, PP) — cursor-column (monotonically increasing timestamp/int) replaces CDC/binlog; high-water mark stored between runs; **no gateway, no staging volume**, runs on schedule. Two approaches: foreign-connection ingestion (`connection_name` + `cursor_column`) vs foreign-catalog ingestion (`ingest_from_uc_foreign_catalog: true` + `cursor_columns` + `primary_keys`; works with all Lakehouse Federation sources). Foreign-connection sources: Oracle/Teradata/SQL Server/MySQL/MariaDB/PostgreSQL. Compute: serverless (default); classic = Beta via DABs/API. SCD modes: SCD_TYPE_1 / SCD_TYPE_2 / **APPEND_ONLY** (unique to query-based). Deletion: soft (`deletion_condition`); hard (Beta, API only). Trade-off vs CDC: higher source DB load; captures latest state only (no intermediate row states). Was name-dropped in managed note. A3 still ⬜.
21. **Reference — [Monitor ingestion gateway progress with event logs](sources/databricks-docs/lakeflow-connect-gateway-event-logs/)** (captured notes) — `event_log('<pipeline-id>')` SQL function; two event types at METRICS level: `flow_progress` (row + byte **deltas**, liveness signal even with zero changes; CDC adds `discovery_latency_ms` + `batch_processing_time_ms` + `event_time.max`) and `operation_progress` (snapshot **% cumulative** + `estimated_completion_ms`); flow name suffix encodes phase (`_snapshot_flow` vs `_cdc_flow`). Configure via `pipelines.gateway.progressEventsEnabled` + `progressEventEmitFrequencySeconds` (default 300s, range 30–3600). CDC latency diagnosis: high `discovery_latency_ms` + low `batch_processing_time_ms` → source-side lag; both high → gateway bottleneck. ETA + CDC latency require May 2026+ gateway image (auto-deployed). Includes full SQL query library: snapshot progress board, stalled-snapshot detection, CDC freshness, throughput trend, bytes-per-row LOB detector.
11. **Reference — [File upload (Add data UI)](sources/databricks-docs/create-or-modify-table/)** (captured notes) — the manual/ad-hoc upload tool (not for production pipelines): New → Add or upload data → Create or modify a table. Up to 10 files, 2 GB total; CSV/TSV/JSON/Avro/Parquet/text only; no compressed files. Compute needed for preview (50 rows); SQL warehouse/serverless/dedicated only (not group clusters). Create new or overwrite existing managed Delta table in UC or Hive metastore. Format options: CSV delimiter/header/type-detection/multiline/merge-schema; JSON type-detection/multiline/comments/single-quotes/timestamp-inference. Multi-file upload appends rows — no join/merge. Column names can't contain commas/backslashes/unicode; uses column mapping under the hood.

**Milestone:** You can describe the difference between Lakeflow Connect Standard Connectors (file-based) and Managed Connectors (database/SaaS CDC), configure a managed connector for a database source, and explain when to use it vs Auto Loader.

---

### ⬜ A4 — Data Privacy, PII & Compliance

**What it is:** PII identification, data masking, pseudonymization, row/column-level security in Unity Catalog, audit logs, and Change Data Feed for right-to-deletion (GDPR delete propagation).

**Why you need it:** Regulatory requirements (GDPR, HIPAA, CCPA) are non-negotiable in production; privacy enforcement must be built into the lakehouse architecture.

**How to learn it:**

1. **Official course — DA-ADE Module 2, "Databricks Data Privacy"** (~4 hrs) — Covers all four hours: regulatory frameworks, pseudonymization, CDF-based delete propagation, PII masking. Complete the "Propagating Changes with CDF Lab".
2. **Book chapter — BBDE, relevant data privacy sections** (~1 hr) — Architecture patterns for PII handling.
3. **Reference — DB-DOCS: [Column masks](https://docs.databricks.com/aws/en/data-governance/unity-catalog/row-and-column-filters.html)** — SQL syntax for row filters and column masks.
4. **Reference — [Change data feed (CDF)](sources/databricks-docs/change-data-feed/)** (captured notes) — the mechanism behind CDF delete propagation: `_change_type = delete` events read via `table_changes()` / streaming `readChangeFeed` to cascade erasures downstream. **Caveat for this topic:** automatic CDF is **not supported on tables with row filters or column masks** — so a table that uses A4-style fine-grained access controls must use legacy CDF (`delta.enableChangeDataFeed`) for delete propagation.

**Milestone:** You can implement a column mask that returns `****` for non-owner users, apply a row filter that restricts data by region, and describe how Change Data Feed enables cascaded deletes for GDPR right-to-erasure.

---

### ⬜ A5 — Declarative Automation Bundles (DABs) & CI/CD

**What it is:** Declarative Automation Bundles (DABs) — formerly "Databricks Asset Bundles", renamed March 2026: define Databricks resources (jobs, pipelines, clusters, permissions) as YAML + code, deploy across dev/staging/prod with variable substitution, and integrate with GitHub Actions. CLI commands (`databricks bundle`) are unchanged.

**Why you need it:** Manual deployment of notebooks and jobs doesn't scale; DABs is the IaC standard for Databricks that enables reproducible, versioned deployments.

**How to learn it:**

1. **Official course — DA-ADE Module 4, "Automated Deployment with Declarative Automation Bundles"** (~4 hrs) — DABs fundamentals, VS Code integration, multi-environment config, GitHub Actions integration. Complete all labs.
2. **Official course — DA-DE Module 4, "DevOps Essentials for Data Engineering"** (~4 hrs) — Git integration, modularizing PySpark code, unit testing PySpark. Complete the unit testing lab.
3. **Reference — DB-DOCS: [Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/)** — Bundle YAML schema and CLI commands.

**Milestone:** You can create a DAB project with `databricks bundle init`, define a job and pipeline in YAML, deploy to dev and prod environments with different cluster sizes via variable substitution, and run the deployment from a GitHub Actions workflow.

---

### ⬜ A6 — Production Pipeline Operations & Observability

**What it is:** Monitoring Lakeflow Spark Declarative Pipelines (expectations metrics, event log), Lakeflow Jobs (run history, failure alerting), Databricks observability features (system tables, audit logs), and **Unity Catalog data quality monitoring** — anomaly detection across all tables in a catalog/schema plus statistical profiling of an individual table (Databricks recommends governing quality this way, distinct from pipeline expectations which only gate in-flight rows).

**Why you need it:** Production pipelines fail; you need dashboards and alerts that tell you what broke, when, and why — before your users notice.

**How to learn it:**

1. **Official course — DA-ADE Module 3, Spark UI analysis and monitoring sections** (~2 hrs) — Spark UI for production pipeline diagnosis.
2. **Book chapter — BBDE, "Orchestrating Data Analytics With Databricks Workflows"** (~1 hr) — Operational patterns for production job management.
3. **Interactive** (~2 hrs) — Create a Lakeflow pipeline with a deliberate expectation failure; inspect the event log and metrics; build a SQL query using `event_log(table(your_streaming_table))` to find quarantined rows; wire a Databricks SQL alert to the count.
4. **Reference — DB-DOCS: [Pipeline event log](https://docs.databricks.com/aws/en/dlt/observability.html)** and **[System tables](https://docs.databricks.com/aws/en/admin/system-tables/)**

> 🆕 **Genie ZeroOps (announced DAIS 2026):** a background AI agent that monitors data/AI assets, detects failures, and runs root-cause analysis using data-quality metrics, error logs, and Unity Catalog lineage. The manual `event_log()` + SQL-alert workflow below is still the foundation — and what you must be able to do by hand — but know that the platform direction is autonomous, agent-driven monitoring on top of these same signals.

**Milestone:** You can use `event_log(table(...))` to query the last 5 expectation violations for a Lakeflow pipeline, build a Databricks SQL alert on a system table metric, and describe the difference between pipeline-level and job-level monitoring.

---

### ⬜ A7 — Lakehouse Federation, External Access & OpenSharing

**What it is:** Three directions of UC data interoperability — (1) **Lakehouse Federation** for querying external databases (PostgreSQL, MySQL, Redshift) *from* Unity Catalog without data movement (external → UC, inbound); (2) **External access** — letting trusted external engines/clients *inside your org* read (and increasingly write) UC tables via UC's open APIs: the **Unity REST API** (Delta clients), the **Iceberg REST catalog** (Spark, Flink, Trino, Snowflake), **credential vending** (external clients inherit UC privileges via temporary creds), and **compatibility mode** (read-only via a cloned copy for clients without REST-API support) (UC → external engine, outbound reads); and (3) **OpenSharing** (formerly Delta Sharing, renamed June 2026, now a Linux Foundation project) — the open, zero-copy sharing protocol *across organizations*, extending beyond Delta/Iceberg tables to AI models, agent skills, and unstructured data, regardless of whether the recipient uses Databricks.

**Why you need it:** Real data engineering involves data that lives outside Databricks — and tools (BI, Trino, Snowflake) that need to read UC data without going through Databricks compute. Federation, external access, and OpenSharing solve the inbound-query, in-org-engine-read, and cross-org-sharing problems respectively, all without copying data. OpenSharing also underpins Databricks Marketplace and Clean Rooms, so understanding it explains how cross-org data products and privacy-safe collaboration work. (DCDEP tests "Data Sharing & Federation" at 5%.)

**How to learn it:**

1. **Official course — DA-DIUC, "Data Interoperability with Unity Catalog"** (~4 hrs) — Covers both Lakehouse Federation (Foreign Catalogs) and Delta/Iceberg interoperability with OpenSharing. The authoritative course for this topic; complete all labs before the hands-on exercise below.
2. **Book chapter — BBDE, "How to Set Up Your First Federated Lakehouse"** (~1 hr) — Architecture walkthrough and setup guide.
3. **Video — Databricks YouTube: search "OpenSharing Databricks 2026"** (~30 min) — Official explanation of the OpenSharing open protocol (search "Delta Sharing" if no results — same content, renamed June 2026).
4. **Reference — DB-DOCS: [Lakehouse Federation](https://docs.databricks.com/aws/en/query-federation/)**, **[External access](https://docs.databricks.com/aws/en/external-access/)**, and **[OpenSharing / Delta Sharing](https://docs.databricks.com/aws/en/delta-sharing/)**
5. **Reference — [Access Databricks data using external systems](sources/databricks-docs/external-access/)** (captured notes) — the external-access map: the per-UC-object access-pattern table (managed/external/foreign tables, MVs, volumes), Unity REST API vs Iceberg REST catalog, credential vending, compatibility-mode read-only clones, the Beta on managed-table writes from Delta clients, and the un-governed-cloud-storage caveats for external tables/volumes (`MSCK REPAIR TABLE`, R2 for multi-writer).
6. **Reference — [Work with foreign tables](sources/databricks-docs/foreign-tables/)** (captured notes) — the inbound-federation end-product: **foreign tables** registered in a UC foreign catalog via **query federation** (JDBC to PostgreSQL/MySQL) or **catalog federation** (Hive Metastore/AWS Glue/Snowflake Horizon). Read-only (except an internal federated HMS), no UC transactional guarantees, most optimizations require a managed table — so Databricks frames them as a migration stopgap (`convert-foreign-managed`, or replicate via materialized views). Also captured in B4 as the third table type.
7. **Interactive** (~1.5 hrs) — Configure a Foreign Catalog connection to a PostgreSQL external database; run a federated query; read a UC managed Iceberg table from an external engine (e.g. Trino or OSS Spark) via the Iceberg REST catalog with credential vending; then create an OpenShare and share a table with an external recipient.

> 🆕 **On-prem / hybrid OpenSharing — the Databricks Storage Ecosystem (announced June 2026):** OpenSharing now reaches *inward* to data that never leaves your premises. The **Databricks Storage Ecosystem** natively connects hybrid and on-premises storage to Databricks over the OpenSharing protocol, so you can run **Serverless Compute, Genie, and LLMs directly against on-prem datasets with zero copy** — no lift-and-shift, no duplicate file. Launch storage partners offering a managed OpenSharing service: **Everpure, MinIO, Qumulo** (more coming — Cohesity, Commvault, HPE, NetApp, Nutanix, Rubrik, VAST Data). This is the "Databricks meets your data where it lives" direction — pairs with **ZeroBus** (I1) for *pushing* on-prem events to the cloud, whereas the Storage Ecosystem *governs and queries on-prem data in place*. Awareness-only for the certs, but it rounds out the interop picture beyond the three cross-org/in-org directions above. See the [Databricks blog](https://www.databricks.com/blog/announcing-databricks-storage-ecosystem-governing-enterprise-data-estate-wherever-it-lives).

> 🆕 **Reverse ETL — the outbound-to-operational direction (DAIS 2026):** the three directions above move data *in* (Federation), *across engines in-org* (external access), or *across orgs* (OpenSharing). **Reverse ETL** is the fourth, operational direction: pushing governed Lakehouse data *back out* to the SaaS/operational tools where it gets acted on — e.g. syncing a Gold audience table to **Google Ads**, Salesforce, or a marketing platform. As the Lakehouse becomes the single source of truth, reverse ETL is how that truth reaches the systems of action without standing up a separate reverse-ETL vendor (Hightouch/Census-style). This is real DE territory — the DCDEP tests "Data Sharing & Federation" (5%), and outbound activation is its operational mirror. The headline driver announced alongside it is **CustomerLake** (a Databricks-native **customer data platform / CDP**): build your own campaign + master-record layer on the Lakehouse instead of buying a SaaS CDP, with reverse ETL as the activation step that pushes those segments to ad/marketing tools. (CustomerLake itself is a vertical *solution*, so it's awareness-only for the certs — but it's the canonical use case that makes reverse ETL click.)

**Milestone:** You can distinguish the three directions — Federation (external DB → UC), external access (external engine → UC table), OpenSharing (cross-org share); explain when to use each; name the two open APIs UC exposes (Unity REST API for Delta clients, Iceberg REST catalog for Iceberg clients) and what credential vending and compatibility mode do; configure a federated connection; name what OpenSharing adds beyond table sharing (AI models, agent skills, unstructured data) over the older Delta Sharing scope; and explain **Reverse ETL** as the fourth, outbound-to-operational direction (pushing governed Lakehouse data to SaaS/ad tools) and how a **CustomerLake/CDP** use case drives it.

---

### ✅ Advanced Checkpoint

You are ready to advance when you can:
- Diagnose and fix a slow Spark job using the Spark UI (identify shuffle, apply broadcast join, explain AQE)
- Deploy a full pipeline (job + Lakeflow pipeline) using DABs to two environments with different configs
- Implement PII masking and CDF-based delete propagation
- Pass a DCDEP practice exam with ≥75% correct

**Certification target:** **DCDEP** — validates I1–A7. Attempt now. Fee: $200, 59 questions, 120 min.

---

## Expert

**Goal:** Architect end-to-end lakehouse systems at scale: optimize cost, design advanced streaming, automate with the SDK, and own the full DevOps lifecycle.
**Estimated time:** ~35 hrs

---

### ⬜ E1 — Photon Engine & Cluster Cost Optimization

**What it is:** Databricks' vectorized C++ query engine (Photon), when it accelerates workloads, instance type selection (memory-optimized vs compute-optimized vs GPU), autoscaling strategies, and spot/preemptible instance policies.

**Why you need it:** Compute is 60–80% of Databricks costs; wrong instance types and always-on clusters are the primary source of waste.

**How to learn it:**

1. **Official course — DA-ADE Module 3, "Cluster instance type selection" and "Photon acceleration" sections** (~1 hr)
2. **Video — Databricks YouTube: search "Photon engine Databricks deep dive"** (~30 min)
3. **Hands-on** (~2 hrs) — Run the same heavy aggregation workload on a Standard cluster vs a Photon-enabled cluster. Compare runtime and DBU cost. Then reconfigure the cluster as memory-optimized vs compute-optimized for a shuffle-heavy vs CPU-heavy workload.
4. **Reference — DB-DOCS: [Photon](https://docs.databricks.com/aws/en/compute/photon.html)** and **[Cluster instance types](https://docs.databricks.com/aws/en/compute/cluster-config-best-practices.html)**
5. **Reference — [Photon](sources/databricks-docs/photon/)** (captured notes) — the C++ vectorised engine deep-dive: columnar/SIMD batch processing, **transparent fallback** to Spark for unsupported ops, default-on for serverless + SQL warehouses (toggle `runtime_engine=PHOTON` on classic), what it accelerates (hash joins, native Parquet writer for MERGE/UPDATE/DELETE/CTAS) vs what falls back (UDFs, RDD/Dataset, stateful streaming, sub-2-s queries), the **Predictive IO and MERGE/UPDATE/DELETE dynamic-file-pruning both require Photon** gate, and the orange/purple operators that show Photon in the Spark UI / query profile.
6. **Reference — [Compute pools (instance pools)](sources/databricks-docs/compute-pools/)** (captured notes) — pre-warmed idle VMs that cut cluster start/autoscale time: **no DBU while idle** (cloud VM billing still applies), the "Allow pool creation" entitlement (non-admins via CLI/API only), autoscaling constraints (pool idle ≥ min workers; max size ≤ pool capacity), never use a spot pool for the driver, and irreversible deletion.

**Milestone:** You can explain which query types Photon accelerates (SQL aggregations, sorts, joins) vs what it doesn't (Python UDFs), state which features require Photon (Predictive IO, MERGE/UPDATE/DELETE DFP), choose the right instance family for a given workload, use an instance pool to cut startup time, and configure spot instance fallback with a reasonable on-demand percentage.

---

### ⬜ E2 — Advanced Streaming Patterns

**What it is:** Multiplex streaming (fan-out from a single Kafka topic to multiple tables), stateful streaming operations (stream-stream joins, session windows), late data handling with watermarks, and continuous execution mode.

**Why you need it:** Simple append streaming is straightforward; stateful and fan-out patterns are where production streaming systems get complex and expensive if done wrong.

**How to learn it:**

1. **Official course — DA-ADE Module 1, "Multiplex streaming patterns with Delta sinks"** (~2 hrs) — The multiplex pattern with routing logic; complete the hands-on build.
2. **Video — Databricks YouTube: search "Structured Streaming stateful operations 2026"** (~1 hr) — Stream-stream joins and session windows.
3. **Hands-on** (~3 hrs) — Build a multiplex streaming pipeline: single Auto Loader source → route to 3 different Delta tables based on `event_type`; add a watermark and windowed aggregation. Inspect state store size in Spark UI.
4. **Reference — DB-DOCS: [Structured Streaming state management](https://docs.databricks.com/aws/en/structured-streaming/stateful-streaming.html)**

**Milestone:** You can build a fan-out streaming pipeline that routes events from one source to multiple targets, explain why stream-stream joins require watermarks on both streams, and describe when to use `Trigger.Continuous` vs `AvailableNow`.

---

### ⬜ E3 — DevOps: Testing, GitHub Actions & Multi-Environment Deployment

**What it is:** Unit testing PySpark transformations with pytest, integration testing Lakeflow pipelines with `nutter` or DLT test tables, GitHub Actions CI pipelines for automated test + bundle deploy.

**Why you need it:** At scale, manual testing breaks down; automated tests and CI/CD are what separate reliable production pipelines from fragile ones.

**How to learn it:**

1. **Official course — DA-DE Module 4, "Unit Testing for PySpark" and "Integration Testing with Lakeflow Spark Declarative Pipelines and Lakeflow Jobs" labs** (~2 hrs) — Write and run PySpark unit tests; run integration tests via Lakeflow Jobs.
2. **Official course — DA-ADE Module 4, "GitHub Actions automation pipeline integration"** (~2 hrs) — Full CI/CD loop with DABs and GitHub Actions.
3. **Local repo — REPO-NBP** (~1 hr) — A concrete before/after modularization example on COVID hospitalization data. Read in this order: (1) `notebooks/covid_eda_raw.py` — monolithic notebook with inline pandas transforms and a Delta write; (2) `notebooks/covid_eda_modular.py` — same logic refactored to import from the shared `covid_analysis/transforms.py` module (`filter_country`, `pivot_and_clean`, `clean_spark_cols`, `index_to_col`); (3) `tests/transforms_test.py` — 4 pytest tests using `@pytest.fixture` and pandas DataFrames, one test per function; (4) `notebooks/run_unit_tests.py` — the key pattern: `%pip install`, `dbutils.library.restartPython()`, then `pytest.main([".", "-p", "no:cacheprovider"])` to run all tests inside a Databricks notebook; (5) `.github/workflows/databricks_pull_request_tests.yml` — GitHub Actions using `databricks/run-notebook@main` to run `run_unit_tests.py` on an existing cluster on every PR.
4. **Hands-on** (~3 hrs) — Set up a GitHub repo with a DAB project; write 3 pytest unit tests for a transformation function; add a GitHub Actions workflow that runs tests on PR and deploys to dev on merge to main.
5. **Reference — DB-DOCS: [Testing Databricks Assets](https://docs.databricks.com/aws/en/dev-tools/testing.html)**
6. **Reference — DB-DOCS: [Databricks Container Services (dedicated)](https://docs.databricks.com/aws/en/compute/custom-containers)** and **[for standard compute](https://docs.databricks.com/aws/en/compute/custom-containers-standard)** — enabling DCS, supported registries, and the launch sequence (VM → pull image → create container → copy DBR code → run init scripts).

> 🆕 **Runtime as code — custom container runtimes (Databricks Container Services):** the missing third leg of "everything as code." DABs (A5) is *artifacts* as code, Terraform (E7) is *infra* as code, and DCS is the **runtime** as code — you ship a Docker image instead of running `pip install` on a live cluster. Build `FROM` an official `databricksruntime/*` base image (12 of them on [Docker Hub](https://hub.docker.com/u/databricksruntime) — `standard`, `minimal`, `python`, `rbase`, `gpu-pytorch`, etc.; start from **`minimal`** when you want full control), then build → scan → version → promote the image through environments exactly like app code, so the image *is* the audit artifact. This solves what pip can't: regulated/air-gapped clusters that mustn't download at runtime, native binaries (e.g. the DuckDB CLI), baked-in enterprise root CAs, pinned private wheels, and DB client drivers. Operational gotchas worth memorizing: (1) a workspace admin must enable it — `databricks workspace-conf set-status --json '{"enableDcs": "true"}'` — then set the **Docker Image URL** in the cluster's Advanced settings; (2) **access mode matters** — the classic path is **Dedicated** (single-user), and there's now a **separate Standard-compute variant of DCS that expects a *different* base image**, so a Dedicated image will fail to launch on Standard and vice-versa; (3) credentials never go in the image — keep them in secrets. *For the certs this is awareness-level (DCDEP touches "Debugging & Deploying" at 10%), but it's core platform-engineering knowledge for regulated and offline deployments.* (Walkthrough: [SunnyData / Hubert Dudek](https://www.sunnydata.ai/blog/databricks-custom-container-runtimes).)

**Milestone:** You can write pytest unit tests for a PySpark function that mock the Spark session, configure a GitHub Actions workflow that runs tests and deploys a DAB bundle, describe the difference between unit testing a transformation function and integration-testing a full pipeline, and explain when a **custom container runtime (DCS)** is the right tool — naming the `enableDcs` toggle and the Dedicated-vs-Standard base-image gotcha.

---

### ⬜ E4 — Cost Management & FinOps on Databricks

**What it is:** DBU types (All-Purpose, Jobs, Pipeline, SQL, Serverless), system tables for cost attribution (`system.billing.usage`), cluster policies, budget alerts, and cost optimization patterns.

**Why you need it:** Databricks can become expensive fast without discipline; FinOps is the difference between a project that scales and one that gets shut down.

**How to learn it:**

1. **Video — Databricks YouTube: search "Databricks cost optimization FinOps 2026"** (~1 hr)
2. **Hands-on** (~2 hrs) — Query `system.billing.usage` to build a cost-by-workspace-and-job dashboard in Databricks SQL. Identify the top 3 cost drivers. Configure a cluster policy that caps max workers and enforces auto-termination.
3. **Reference — DB-DOCS: [System tables billing](https://docs.databricks.com/aws/en/admin/system-tables/billing.html)** and **[Cluster policies](https://docs.databricks.com/aws/en/compute/cluster-policies.html)**
4. **Book chapter — BBDE relevant FinOps sections** (~30 min)

**Milestone:** You can query `system.billing.usage` to attribute DBU cost by job and workspace, create a cluster policy that enforces auto-termination and max worker count, and explain the DBU cost difference between All-Purpose compute and Jobs compute for the same workload.

---

### ⬜ E5 — End-to-End Lakehouse Architecture Design

**What it is:** Designing a full production lakehouse: storage topology (zones, catalogs), SLA-based pipeline design, multi-tenancy, disaster recovery, and the trade-offs between batch, micro-batch, and streaming for each layer.

**Why you need it:** Individual skills don't automatically compose into a coherent architecture; this topic synthesizes everything into system-level design judgment.

**How to learn it:**

1. **Book — BBDE, all case study chapters** (~3 hrs) — Read the financial services batch processing pattern, the federated lakehouse setup, and the DevOps best practices chapter. These show full architectures, not isolated features.
2. **Book — UDEDW, "Data Modeling and Storage" chapter** (~1.5 hrs) — Storage design decisions and their trade-offs.
3. **Local repo — REPO-TF** (~2 hrs) — Browse the `aws_fs_lakehouse` (financial services) and `aws_uc` (Unity Catalog) modules to see how a production-grade lakehouse is laid out in Terraform. You don't need to run it — read the module structure to understand what a real deployment includes (VPC, UC metastore, workspace, cluster policies, IAM).
4. **Hands-on capstone** (~6 hrs) — Design and build a complete Lakehouse: 2 source systems (file + database CDC), Auto Loader + Lakeflow Connect ingestion, 3-layer Medallion Lakeflow pipeline with expectations, Lakeflow Jobs orchestration, Unity Catalog governance, DABs CI/CD deployment. Document architecture decisions.
5. **Reference — DB-DOCS: [Data architecture best practices](https://docs.databricks.com/aws/en/lakehouse-architecture/)**

**Milestone:** You can draw an architecture diagram for a production lakehouse covering ingestion, storage, transformation, governance, orchestration, and CI/CD — and defend the key design decisions (batch vs streaming per layer, partitioning strategy, SLA management).

---

### ⬜ E6 — Databricks SDK & API Automation

**What it is:** The Databricks SDK for Python: programmatically managing clusters, jobs, pipelines, secrets, permissions, and workspace state — beyond what YAML configuration covers.

**Why you need it:** Complex automation (dynamic job creation, workspace provisioning, metadata-driven pipeline generation) requires code, not just config.

**How to learn it:**

1. **Official course — DA-DE Module 4, "From Idea to Code: Building With the Databricks SDK for Python" section** (~1 hr)
2. **Book chapter — BBDE, "Building With the Databricks SDK for Python"** (~1 hr)
3. **Hands-on** (~3 hrs) — Write a Python script using the SDK that: lists all jobs in a workspace, retrieves the last run status for each, sends a Slack notification for any job with `FAILED` status. Then add a function that dynamically creates a job from a template YAML.
4. **Reference — DB-DOCS: [Databricks SDK for Python](https://docs.databricks.com/aws/en/dev-tools/sdk-python.html)** and the [GitHub repo](https://github.com/databricks/databricks-sdk-py).

**Milestone:** You can use the Databricks SDK to list, create, and trigger a job programmatically, retrieve its run status, and explain when to use the SDK vs DABs (SDK = runtime automation; DABs = deployment-time config).

---

### ✅ E7 — Databricks Infrastructure as Code with Terraform

**What it is:** Using the Databricks Terraform provider to provision AWS workspaces (VPC, IAM, S3, `databricks_mws_*` resources), set up Unity Catalog objects programmatically, manage cluster policies and permissions at scale — and Terragrunt for DRY, multi-environment IaC deployments.

**Why you need it:** DABs (A5) handles the application layer — pipelines and jobs. Terraform handles the platform layer — workspaces, networking, Unity Catalog metastores, and shared resources. Understanding both, and where each starts and stops, is what separates a data engineer who can deploy a pipeline from one who can provision the entire platform.

**How to learn it:**

1. **Specialist session — SPEC-TF** (~3 hrs) — 100-page official Databricks session covering the complete picture: architecture, AWS workspace provisioning, Unity Catalog setup, Terragrunt, the Terraform vs DABs split, and Terraform CI/CD. Read cover to cover before anything else.
2. **Reference — DB-DOCS: [Terraform on Databricks](https://docs.databricks.com/aws/en/dev-tools/terraform/)** (~1 hr) — Official provider docs; focus on the AWS workspace provisioning guide and Unity Catalog resource reference.
3. **Local repo — REPO-TF** (~1.5 hrs) — Browse the `aws_fs_lakehouse` and `aws_uc` modules. Focus on: how account-level resources (`databricks_mws_*`, `databricks_metastore`) are separated from workspace-level resources (`databricks_catalog`, `databricks_grants`, `databricks_cluster_policy`). Note the separate Terraform state files for each layer.
4. **Hands-on: AWS workspace + UC** (~4 hrs) — Provision a Databricks workspace on AWS from scratch: VPC + private subnets, IAM cross-account role, S3 root bucket, `databricks_mws_networks` → `databricks_mws_credentials` → `databricks_mws_storage_configurations` → `databricks_mws_workspaces`. Then switch to workspace provider and add UC: `databricks_metastore` (no `storage_root` — best practice from SPEC-TF), `databricks_metastore_assignment`, `databricks_catalog`, `databricks_schema`, `databricks_grants`.
5. **Local repo — REPO-SRA** (~2 hrs) — Read the AWS SRA after the hands-on above. Compare your basic deployment to what a hardened deployment adds: two Private Link VPC endpoints (REST + SCC relay), S3/STS/Kinesis VPC endpoints with restrictive policies, two CMK keys (workspace storage + managed services), Network Connectivity Configuration, disabled legacy DBFS/access settings, and the Security Analysis Tool. This is the difference between "it works" and "it passes a security audit".
6. **Hands-on: Terragrunt** (~2 hrs) — Refactor into a Terragrunt layout: `root.hcl` with S3 remote state (`remote_state` block), separate `account-config/`, `workspace/`, `unity-catalog/` units with `terragrunt.hcl` per unit, `environment.hcl` per stage (dev/prod). Run `terragrunt run --all apply` and confirm dependency ordering.
7. **Hands-on: CI/CD** (~1 hr) — Wire deployment into GitHub Actions using REPO-TF-EX's `cicd-pipelines` as a reference: `terraform fmt` + `validate` + `plan` on PR, `apply` on merge to main. Store Terraform state in S3 with DynamoDB locking.
8. **Reference: REPO-TF-PROVIDER** — When a Terraform resource behaves unexpectedly (plan shows diff you can't explain, an attribute isn't in the docs), look it up in the provider source. The `mws/` directory covers MWS workspace resources; `catalog/` covers Unity Catalog. Reading the Go struct tags is faster than filing a GitHub issue.

> **Terraform vs DABs — the canonical split (from SPEC-TF p.89):**
> - **Terraform:** workspace provisioning + cloud infra, Unity Catalog metastore/catalogs/grants, cluster policies, shared SQL warehouses, user/group/service principal management
> - **DABs (A5):** pipelines, jobs, notebooks — project-level artifacts, environment promotion, developer-owned CI/CD

> **Key Databricks-specific Terraform gotchas (from SPEC-TF):**
> - AWS workspace provisioning is an account-level operation — use `provider = databricks.mws` (MWS endpoint), not the workspace endpoint.
> - `databricks_mws_credentials` has a circular dependency on IAM: the IAM role trust policy needs the Databricks `external_id`, which isn't known until after the credential is created. The official workaround uses a two-phase `depends_on`.
> - Create `databricks_metastore` without `storage_root` to ensure full storage isolation between catalogs.
> - Keep account-level and workspace-level resources in **separate Terraform state files**.
> - `databricks_grants` is authoritative (replaces all grants); `databricks_grant` is per-principal. Never mix both for the same object.

**Milestone:** You can provision a Databricks workspace on AWS entirely from Terraform (`databricks_mws_*`), set up a Unity Catalog metastore and catalog with grants, organize code into Terragrunt stacks with separate state per layer, and explain the Terraform vs DABs split: what each tool owns and why.

---

### ⬜ E8 — LTAP & Lakebase: Unified Transactional-Analytical Architecture

**What it is:** LTAP (Lake Transactional/Analytical Processing) — an architecture that unifies OLTP and OLAP on a single copy of data in open lake storage (Delta/Iceberg), eliminating the ETL layer between operational and analytical systems. Built on **Lakebase** (serverless Postgres on object storage) + the Lakehouse, both sharing Unity Catalog governance.

**Why you need it:** CDC pipelines between operational databases and the lakehouse are brittle and lag-prone; LTAP eliminates this layer entirely. As AI agents increasingly require real-time access to data, the traditional OLTP↔OLAP gap becomes a critical bottleneck — LTAP is how Databricks solves it architecturally.

**How to learn it:**

1. **Press release — LTAP launch** (~30 min) — Read the official announcement: what LTAP is, why HTAP failed (collapsed workload isolation), why zero-ETL was insufficient (hid pipelines rather than eliminated them), and the three defining LTAP properties. [databricks.com/company/newsroom/press-releases/databricks-launches-ltap-first-lake-transactionalanalytical](https://www.databricks.com/company/newsroom/press-releases/databricks-launches-ltap-first-lake-transactionalanalytical)
2. **Reference — DB-DOCS: [Lakebase](https://docs.databricks.com/aws/en/lakebase/)** (~1.5 hrs) — Serverless Postgres on object storage: architecture, git-style branching and snapshots, cross-cloud/cross-region disaster recovery, autonomous database operations, and Unity Catalog integration.
3. **Video — Databricks YouTube: search "LTAP Lakebase Databricks 2026"** (~30 min) — Official architecture walkthrough of how Lakebase and the Lakehouse share a unified storage layer.
4. **Hands-on** (~2 hrs) — Provision a Lakebase instance; write rows to a Postgres table; query the same data from a Databricks notebook via Unity Catalog without copying it. Compare this to a CDC-based approach (I4) and note what the pipeline layer you eliminated looked like.
5. **Reference — DB-DOCS: [Lakebase DR & branching](https://docs.databricks.com/aws/en/lakebase/)** — Cross-region failover, snapshot-based experimentation, autonomous health management.

> **Three defining LTAP properties:**
> 1. **Unified governance** — all operational, analytical, and streaming data in open formats (Delta/Iceberg) under a single Unity Catalog
> 2. **Independent scaling** — Postgres ACID for transactional workloads; Lakehouse scale for analytical workloads; no performance tradeoffs
> 3. **No ETL** — data stored in one place; no copy, no CDC pipeline, no shadow infrastructure

**Milestone:** You can explain the three LTAP properties, contrast LTAP with HTAP and zero-ETL, provision a Lakebase instance, and query operational Postgres data from the Lakehouse through Unity Catalog without a CDC pipeline or data copy.

---

### ⬜ E9 — LakehouseRT: Real-Time Analytics on Open Data

**What it is:** Lakehouse//RT — a new Databricks compute engine (Reyden) that delivers sub-100 millisecond analytical queries directly on Delta Lake and Iceberg tables, eliminating the need for separate real-time serving infrastructure (Druid, Pinot, ClickHouse, etc.). All queries run within Unity Catalog governance; no data copies, no ingestion pipelines to a serving layer, no proprietary formats.

**Why you need it:** Most production stacks maintain two parallel systems — the lakehouse for pipelines and a specialized serving layer for low-latency dashboards and AI agent queries. LakehouseRT collapses this into one: same data, same governance, same open formats — just served at operational latency. With LTAP (E8) eliminating ETL for writes and LakehouseRT eliminating separate serving for reads, the full real-time lakehouse architecture becomes coherent.

**How to learn it:**

1. **Press release — LakehouseRT launch** (~20 min) — What Reyden is, the "serving layer trap" (vendor lock-in, data copies, fragmented governance), the sub-100ms at 12,000 QPS performance claim, and the Unity Catalog governance guarantee. [databricks.com/company/newsroom/press-releases/databricks-launches-lakehousert-bring-real-time-analytics-directly](https://www.databricks.com/company/newsroom/press-releases/databricks-launches-lakehousert-bring-real-time-analytics-directly)
2. **Reference — DB-DOCS: [Lakehouse//RT](https://docs.databricks.com/aws/en/lakehousert/)** (~1 hr) — How to enable LakehouseRT compute, supported query patterns, latency guarantees, and configuration options.
3. **Video — Databricks YouTube: search "LakehouseRT Reyden Databricks 2026"** (~30 min) — Official architecture deep-dive into Reyden's asynchronous execution model.
4. **Hands-on** (~2 hrs) — Run the same analytical query against a Serverless SQL Warehouse and against LakehouseRT compute; compare latency. Query a live streaming Delta table (from E2) with LakehouseRT; confirm Unity Catalog audit logs apply uniformly across both compute types.
5. **Reference — DB-DOCS: [Reyden execution model](https://docs.databricks.com/aws/en/lakehousert/)** — How fully asynchronous execution differs from Photon's vectorized synchronous model.

> **Contrast with Photon (E