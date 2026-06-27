# Unit Testing in Notebooks

> **Source:** [docs.databricks.com/aws/en/notebooks/testing](https://docs.databricks.com/aws/en/notebooks/testing)
> **Added:** 2026-06-17
> **Source updated:** 2025-01-21
> **Tags:** notebooks, testing, pytest, testthat, scalatest, sql, CI-CD, B1
> **Type:** documentation

A guide to unit testing notebook code across **Python (pytest), R (testthat), Scala (ScalaTest), and SQL (`SELECT if`)**. The pattern across all four: keep functions in workspace files (or a separate notebook for Scala), write tests against **fake data** (never production), and trigger test runs from notebook cells; CI/CD via GitHub Actions is supported. Functions should return "a single predictable outcome of a single data type." Out of scope: stubs, mocks, harnesses, and integration/system/acceptance testing.

> "In general, it is a best practice to not run unit tests against functions that work with data in production." · "Databricks recommends storing functions and their unit tests outside of notebooks" (Python/R) — for Scala, "include functions in one notebook and their unit tests in a separate notebook."

| Language | Functions | Tests |
|---|---|---|
| Python | `myfunctions.py` (workspace file) | `test_myfunctions.py` (workspace file) |
| R | `myfunctions.r` (workspace file) | `test_myfunctions.r` (workspace file) |
| Scala | `myfunctions` notebook | separate notebook (`%run ./myfunctions`) |
| SQL | UDFs registered in the session | notebook cells (`SELECT if(...)`) |

## Python — pytest

`myfunctions.py` (workspace file — must create its own `SparkSession`; notebooks get one by default):

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
spark = SparkSession.builder.appName('integrity-tests').getOrCreate()

def tableExists(tableName, dbName):
    return spark.catalog.tableExists(f"{dbName}.{tableName}")

def columnExists(dataFrame, columnName):
    return columnName in dataFrame.columns

def numRowsInColumnForValue(dataFrame, columnName, columnValue):
    return dataFrame.filter(col(columnName) == columnValue).count()
```

`test_myfunctions.py` (fake data via `spark.createDataFrame`, not production):

```python
from myfunctions import *
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, StringType
spark = SparkSession.builder.appName('integrity-tests').getOrCreate()

schema = StructType([StructField("clarity", StringType(), True), StructField("price", IntegerType(), True)])  # abridged
df = spark.createDataFrame([("SI2", 326), ("SI1", 326)], schema)

def test_tableExists():            assert tableExists("diamonds", "default") is True
def test_columnExists():           assert columnExists(df, "clarity") is True
def test_numRowsInColumnForValue(): assert numRowsInColumnForValue(df, "clarity", "SI2") > 0
```

Notebook cells to run it:

```python
%pip install pytest
```
```python
import pytest, sys
sys.dont_write_bytecode = True                      # readonly filesystem
retcode = pytest.main([".", "-v", "-p", "no:cacheprovider"])
assert retcode == 0, "The pytest invocation failed. See the log for details."
```

`-v` = verbose, `-p no:cacheprovider` skips `.pytest_cache` (readonly filesystem).

## R — testthat

`myfunctions.r` defines `table_exists`, `column_exists`, `num_rows_in_column_for_value` over SparkR; `test_myfunctions.r` uses `testthat` with `createDataFrame` fake data:

```r
library(testthat); source("myfunctions.r")
df <- createDataFrame(list(list("SI2", as.integer(326)), list("SI1", as.integer(326))),
                      structType(structField("clarity", "string"), structField("price", "integer")))
test_that("The table exists.", { expect_true(table_exists("diamonds", "default")) })
test_that("The column exists.", { expect_true(column_exists(df, "clarity")) })
```

Run it:

```r
install.packages("testthat")
library(testthat); source("myfunctions.r"); test_dir(".", reporter = "tap")
```

## Scala — ScalaTest

Functions live in a separate `myfunctions` notebook; the test notebook `%run`s it, then defines an `AsyncFunSuite`:

```scala
%run ./myfunctions
```
```scala
import org.scalatest._
class DataTests extends AsyncFunSuite {
  val df = spark.createDataFrame(Seq(Row(1, "SI2", 326), Row(2, "SI1", 326)).asJava, schema)  // schema abridged
  test("The table exists") { assert(tableExists("diamonds", "default") == true) }
  test("The column exists") { assert(columnExists(df, "clarity") == true) }
  test("There is at least one matching row") { assert(numRowsInColumnForValue(df, "clarity", "SI2") > 0) }
}
nocolor.nodurations.nostacks.stats.run(new DataTests)   // suppresses ANSI color + timing for clean output
```

## SQL — `SELECT if` pattern

No external framework — `SELECT if(udf_call, printf("PASS:…"), printf("FAIL:…"))` against a view from real or fake data:

```sql
USE CATALOG main; USE SCHEMA default;
CREATE VIEW view_diamonds AS SELECT * FROM diamonds;

SELECT if(table_exists("main", "default", "view_diamonds"),
          printf("PASS: table exists."), printf("FAIL: table does not exist."));
SELECT if(column_exists("main", "default", "view_diamonds", "clarity"),
          printf("PASS: column exists."), printf("FAIL: column missing."));
SELECT if(num_rows_for_clarity_in_diamonds("VVS2") > 0,
          printf("PASS: ≥1 row with clarity=VVS2."), printf("FAIL: no rows."));
```

The SQL UDFs (`table_exists`, etc.) must be pre-registered (defined elsewhere).

## CI/CD integration

> "set up a continuous integration and continuous delivery or deployment (CI/CD) system, such as GitHub Actions, to automatically run your unit tests whenever your code changes."

See [[notebook-best-practices]] for a worked GitHub Actions example.

Related: [[notebooks-overview]], [[notebook-best-practices]], [[notebook-debugger]], [[ch01-getting-started-with-databricks]].
