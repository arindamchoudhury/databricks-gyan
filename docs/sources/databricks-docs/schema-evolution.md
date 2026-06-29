# Schema evolution in Databricks

> **Source:** [docs.databricks.com/aws/en/data-engineering/schema-evolution](https://docs.databricks.com/aws/en/data-engineering/schema-evolution)
> **Added:** 2026-06-27
> **Source updated:** 2026-06-11
> **Tags:** data-engineering, schema-evolution, mergeSchema, auto-loader, structured-streaming, streaming-tables, materialized-views, delta, views, type-widening, column-mapping, from_json, from_avro, I1, I2, I5
> **Type:** documentation

**Schema evolution** is a system's ability to adapt to changes in data structure over time — common with semi-structured data, event streams, and third-party sources. The page's key framing: schema evolution is **not one feature but a property each component handles independently**, so an end-to-end pipeline only evolves cleanly if *every* stage along the path is configured to. There is no global switch.

Five change types recur throughout the page (the columns of every support matrix below):

- **New columns** — added fields (optionally with a backfill value).
- **Column renaming** — e.g. `name` → `full_name`.
- **Dropped columns** — removing a column from the schema.
- **Type widening** — a column's type broadens, e.g. `INT` → `DOUBLE`.
- **Other type changes** — any non-widening type change, e.g. `INT` → `STRING` (the hardest case — almost always needs a full rewrite/refresh).

## Components

Schema evolution involves four independent component categories. Each is configured separately; the diagram on the source page shows data flowing **connectors → format parsers → engines → data sets**, with each box owning its own schema decision:

1. **Connectors** — ingest from external sources: Auto Loader, Kafka, Kinesis, Lakeflow connectors.
2. **Format parsers** — decode raw bytes: `from_json`, `from_avro`, `from_xml`, `from_protobuf`.
3. **Engines** — execute queries: Structured Streaming.
4. **Data sets** — persist/serve: streaming tables, materialized views, Delta tables, views.

> 📌 **The two-schema mental model (Auto Loader → Delta).** There are *two* persisted schemas: the one Auto Loader tracks in its schema location, and the target Delta table's schema. In steady state they match. When Auto Loader evolves its schema from incoming data, the Delta table **must** evolve too or the query fails — fix by either (a) enabling schema evolution / running DDL on the target, or (b) fully rewriting the target. This "each stage must agree" pattern generalizes to every component pair in the pipeline.

## Support by connector

| Connector | New cols | Rename | Drop | Type widening | Other type change |
|---|---|---|---|---|---|
| **Auto Loader** | ✅ restart¹ | ✅ as new col²; old col → NULL; restart | ✅ soft delete (new rows NULL) | ✅ DBR 16.4+ via `addNewColumnsWithTypeWidening` | ❌ → `rescuedDataColumn` (mode `rescue`) else manual |
| **Delta connector** | ✅ auto w/ `mergeSchema`, else restart (no rewrite) | ✅ `mergeSchema`, else `spark…allowSourceColumnRename` | ✅ `mergeSchema`, else `spark…allowSourceColumnDrop` | ✅ DBR 16.4 LTS+ w/ `mergeSchema` + target type widening | ❌ |
| **SaaS & CDC connectors** | ✅ auto-restart | ✅ auto-restart (as new col) | ✅ soft delete | ❌ full refresh | ❌ full refresh |
| **Kinesis / Kafka / Pub-Sub / Pulsar** | ↪ format parser | ↪ format parser | ↪ format parser | ↪ format parser | ↪ format parser |

¹ Behavior depends on `cloudFiles.schemaEvolutionMode`; auto-evolution makes the stream **fail once, then succeed on restart** with the evolved schema. Knobs: `schemaHints` (pin specific columns), immutable `schema`, `rescuedDataColumn`.
² Renamed column is treated as a brand-new column; the old name back-fills `NULL` for new rows.

The message-bus connectors (Kafka/Kinesis/Pub-Sub/Pulsar) do **no** native evolution — each returns a binary blob, so all schema handling is delegated to the format parser that decodes it.

## Support by format parser

| Parser | Schema evolution? |
|---|---|
| **`from_json`** | ❌ standalone (update schema manually). ✅ *inside Lakeflow SDP* via `schemaLocationKey` + `schemaEvolutionMode` — then behaves like Auto Loader for all five change types. |
| **`from_avro` / `from_protobuf`** | No evolution *in the function itself*. ✅ all five types **with Confluent Schema Registry**; otherwise the user supplies and maintains the schema manually. Evolution is owned by the engine + Schema Registry. |
| **`from_csv` / `from_xml`** | ❌ none of the five types. |

## Support by engine

**Structured Streaming.** A streaming query's schema is **locked at planning time** and every micro-batch reuses that plan without re-planning. If the source schema changes mid-run, the query **fails by design** and you must restart it so Spark re-plans against the new schema — and the data set the stream writes to must itself support evolution. All five change types are "supported" only in this fail-then-restart sense.

## Support by data set

| Data set | New cols | Rename | Drop | Type widening | Other type change |
|---|---|---|---|---|---|
| **Streaming tables** | ✅ auto-restart | ✅ auto-restart (as new col) | ✅ soft delete (NULL) | ✅ enable at pipeline or table level | ❌ full refresh |
| **Materialized views** | 🔁 full recompute | 🔁 full recompute | 🔁 full recompute | 🔁 full recompute | 🔁 full recompute |
| **Delta tables** | ✅ auto w/ merge schema evolution (no rewrite) | ✅ `ALTER TABLE` DDL + [[column-mapping]] (no rewrite) | ✅ `ALTER TABLE` DDL + [[column-mapping]] (no rewrite) | ✅ auto w/ [type widening](https://docs.databricks.com/aws/en/tables/features/type-widening) + merge schema evolution; or DDL | ✅ **but requires full rewrite** via `overwriteSchema` |
| **Views** | ✅ `SCHEMA EVOLUTION` (no explicit `column_list`) | ✅ `SCHEMA EVOLUTION` | ✅ `SCHEMA EVOLUTION` | ✅ `SCHEMA TYPE EVOLUTION` (or `SCHEMA EVOLUTION`) | ✅ `SCHEMA TYPE EVOLUTION` (or `SCHEMA EVOLUTION`) |

Notes on the data-set row semantics:

- **Streaming tables** turn on *merge schema evolution* by default — schema updates need no manual restart, but arbitrary (non-additive) changes still force a **full refresh**.
- **Materialized views** are the strictest: *any* schema or defining-query change triggers a **full recompute**, full stop.
- **Delta tables** are the most configurable — four levers: **merge schema evolution**, **column mapping** (rename/drop as metadata-only), **type widening**, and **`overwriteSchema`** (the escape hatch for arbitrary type changes, at the cost of a full data rewrite).
- **Views** distinguish two modes: `SCHEMA TYPE EVOLUTION` (type changes only) vs `SCHEMA EVOLUTION` (a **superset** — type changes *plus* new/renamed/dropped columns). A view with an explicit `column_list` that no longer matches, or an unparseable query, becomes **invalid** and unqueryable.

## End-to-end example (Kafka + Avro → Delta)

The page's worked example ingests a Confluent-Schema-Registry Avro Kafka topic into a managed Delta bronze table, showing that **three** separate evolution knobs must line up across the pipeline:

1. **Connector** (Kafka) — none; returns a binary blob.
2. **Format parser** (`from_avro` with Schema Registry) — `avroSchemaEvolutionMode = "restart"` (fail-fast so a restart adopts new fields), `mode = "FAILFAST"`.
3. **Data set** (Delta write) — `.option("mergeSchema", "true")` on the `writeStream` (additive columns only — rename/drop/type changes still need their own handling), with `spark.databricks.delta.schema.autoMerge.enabled` as the session-level equivalent. Uses `trigger(availableNow=True)` for UC/Databricks-SQL.

The key lesson the example drives home: `mergeSchema` on the Delta sink **only adds new columns** — renaming, dropping, and type changes each require their own mechanism ([[column-mapping]], [type widening](https://docs.databricks.com/aws/en/tables/features/type-widening), `overwriteSchema`) at the appropriate stage.

## How this connects to the captured table-feature notes

This concept page is the **map**; the per-feature notes are the **territory**:

- Additive evolution on Delta = "merge schema evolution" / `mergeSchema` / `autoMerge`.
- Rename + drop without rewrite = [[column-mapping]] (the metadata-only mechanism, plus the `schemaTrackingLocation` needed to keep streams alive across non-additive changes).
- `INT`→`DOUBLE`-style broadening = [type widening](https://docs.databricks.com/aws/en/tables/features/type-widening).
- Non-additive changes are exactly what [[change-data-feed]] (legacy) can't span, and why [[row-tracking]] / schema tracking exist.

Related: [[column-mapping]], [type widening](https://docs.databricks.com/aws/en/tables/features/type-widening), [[change-data-feed]], [[row-tracking]], [[batch-vs-streaming]], [[materialized-views]], [[tables-concepts]].
