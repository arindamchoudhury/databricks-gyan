# dbldatagen — Databricks Labs Data Generator

> **Source:** [github.com/databrickslabs/dbldatagen](https://github.com/databrickslabs/dbldatagen)
> **Added:** 2026-07-02
> **Source updated:** 2026-07-02 (last push)
> **Tags:** synthetic-data, testing, pyspark, delta-live-tables, faker, unity-catalog, E3
> **Type:** other (OSS library, Databricks Labs)

Python/PySpark library for generating synthetic data inside a Databricks environment — testing, benchmarking, demos, POCs. 476★, actively maintained, not archived.

## Project description

You define a **data generation specification in code** that controls how synthetic data is produced — either against an existing schema or fully ad-hoc. No dependencies beyond what's already in the Databricks Runtime. Output is a Spark DataFrame, so it's usable from Scala/R/SQL too by defining a view over it.

## Feature summary

- Generates synthetic data at scale — billions of rows in minutes on an appropriately sized cluster.
- **Repeatable, predictable** data — supports multi-table generation with consistent primary/foreign keys across tables (CDC, merge, join scenarios).
- Covers all Spark SQL primitive types; output is a Spark DataFrame you persist, export, or feed into other computation.
- Date/timestamp/numeric ranges; discrete numeric and text values.
- Values generated at random or **derived from other fields** (via hash or the underlying value itself).
- Configurable distributions and per-value weights.
- Generates arrays (ML-style feature arrays).
- Conform to an existing schema, or generate independent of one.
- SQL expressions inside the spec; plugin mechanism for third-party generators like **Faker**.
- Usable as a synthetic-data **source inside a Lakeflow Declarative Pipeline** (still named "Delta Live Tables" in the README).
- Experimental: generate data-gen code *from* an existing schema/data sample.
- Ships standard datasets for quick generation without writing a spec.

## Installation

```commandline
pip install dbldatagen
```

Inside a Databricks notebook:

```commandline
%pip install dbldatagen
```

Works in a notebook, inside a Lakeflow Declarative Pipeline, and even on Free/Community Edition.

## Compatibility

Requires **PySpark 3.4.1 + Python 3.10.12 or later** — compatible with **DBR 13.3 LTS and later**. This version also supports Unity Catalog.

> ❓ **README is stale on the runtime floor.** 13.3 LTS predates the account-wide UC-only-workspace rollout covered in [[legacy-features]] (2026-09-30) — worth re-checking dbldatagen's DBR 18 / Spark 4.1 compatibility before relying on the README's version claim as current.

Older releases had a UC access-mode gotcha: on Databricks runtimes **before 13.2**, UC `Shared` access mode blocked third-party libraries and Python UDFs, so dbldatagen needed `Single User` or `No Isolation Shared` (or `Custom`, depending on settings) instead. From runtime **13.2 onward**, `Shared` access mode works. *This version's 13.3 LTS floor exists specifically to sidestep that issue.*

## Using the data generator

Fastest path — one of the built-in standard datasets:

```python
import dbldatagen as dg
df = dg.Datasets(spark, "basic/user").get(rows=1000_000).build()
num_rows = df.count()
```

Fully custom spec via `DataGenerator`:

```python
import dbldatagen as dg
from pyspark.sql.types import IntegerType, FloatType, StringType
column_count = 10
data_rows = 1000 * 1000
df_spec = (dg.DataGenerator(spark, name="test_data_set1", rows=data_rows,
                                                  partitions=4)
           .withIdOutput()
           .withColumn("r", FloatType(),
                            expr="floor(rand() * 350) * (86400 + 3600)",
                            numColumns=column_count)
           .withColumn("code1", IntegerType(), minValue=100, maxValue=200)
           .withColumn("code2", IntegerType(), minValue=0, maxValue=10)
           .withColumn("code3", StringType(), values=['a', 'b', 'c'])
           .withColumn("code4", StringType(), values=['a', 'b', 'c'],
                          random=True)
           .withColumn("code5", StringType(), values=['a', 'b', 'c'],
                          random=True, weights=[9, 1, 1])
           )

df = df_spec.build()
num_rows = df.count()
```

`withColumn` reads as a declarative per-column mini-spec: fixed range (`code1`/`code2`), a discrete value set taken in order (`code3`), taken randomly (`code4`), and taken randomly with weights so `'a'` is 9x more likely than `'b'` or `'c'` (`code5`).

## Spark and Databricks Runtime compatibility

Targets recent LTS releases from 13.3 LTS onward, plus Delta Live Tables `current` and `preview` runtimes. Doesn't pin/install dependent-package versions (`numpy`, `pandas`, `pyarrow`, `pyparsing`) — deliberately, to avoid clobbering the DBR's curated package set — so a Pyspark API change in a newer DBR could still break it even though nothing is formally dropped.

## License and support

Licensed under the **Databricks License** (not Apache/MIT) — scope-of-use clause restricts it to use "in connection with your use of the Databricks Services." Fine for work inside Databricks; not a general-purpose OSS Spark library for use outside the platform.

> ⚠️ **No SLA.** Databricks Labs projects are "provided for your exploration only... not formally supported by Databricks with Service Level Agreements... provided AS-IS." File issues on the GitHub repo; no formal response guarantee.

---
Related: [[legacy-features]] — the DBR-13.3-LTS floor this library targets sits right at the same legacy-runtime cutoff Databricks is deprecating account-wide by 2026-09-30.
