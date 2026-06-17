# Unit Testing in Notebooks

> **Source:** [docs.databricks.com/aws/en/notebooks/testing](https://docs.databricks.com/aws/en/notebooks/testing)
> **Added:** 2026-06-17
> **Source updated:** 2026-06-17
> **Tags:** notebooks, testing, pytest, testthat, scalatest, sql, CI-CD, B1
> **Type:** documentation

## Summary

Databricks docs guide for unit testing notebook code across Python (pytest), R (testthat), Scala (ScalaTest), and SQL (`SELECT if`). The pattern across all four: keep functions in workspace files (or a separate notebook for Scala), write tests against fake data, and trigger test runs from notebook cells. CI/CD via GitHub Actions is supported.

## Key points

- **Python/R:** store functions and tests as workspace files (`.py`/`.r`); not in notebook cells.
- **Scala:** functions in one notebook; tests in a second notebook that `%run`s the first.
- **SQL:** no separate file; use `SELECT if(udf(...), printf("PASS:..."), printf("FAIL:..."))` pattern.
- **Never test against production data.** Create fake DataFrames in test setup.
- Functions should return **a single predictable outcome of a single data type**.
- CI/CD (e.g. GitHub Actions) can auto-run tests on every code change.
- Out of scope: stubs, mocks, test harnesses, integration/system/acceptance/non-functional testing.

## Notes

### Storage patterns

| Language | Functions | Tests |
|---|---|---|
| Python | `myfunctions.py` (workspace file) | `test_myfunctions.py` (workspace file) |
| R | `myfunctions.r` (workspace file) | `test_myfunctions.r` (workspace file) |
| Scala | `myfunctions` notebook | separate notebook (`%run ./myfunctions`) |
| SQL | UDFs registered in the session | notebook cells (`SELECT if(...)`) |

### Python — pytest

**myfunctions.py** (workspace file — must create its own `SparkSession`; notebooks get one by default)

```python
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
                    .appName('integrity-tests') \
                    .getOrCreate()

def tableExists(tableName, dbName):
  return spark.catalog.tableExists(f"{dbName}.{tableName}")

def columnExists(dataFrame, columnName):
  if columnName in dataFrame.columns:
    return True
  else:
    return False

def numRowsInColumnForValue(dataFrame, columnName, columnValue):
  df = dataFrame.filter(col(columnName) == columnValue)
  return df.count()
```

**test_myfunctions.py** (fake data — not production)

```python
import pytest
import pyspark
from myfunctions import *
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, StringType

tableName    = "diamonds"
dbName       = "default"
columnName   = "clarity"
columnValue  = "SI2"

spark = SparkSession.builder \
                    .appName('integrity-tests') \
                    .getOrCreate()

schema = StructType([ \
  StructField("_c0",     IntegerType(), True), \
  StructField("carat",   FloatType(),   True), \
  StructField("cut",     StringType(),  True), \
  StructField("color",   StringType(),  True), \
  StructField("clarity", StringType(),  True), \
  StructField("depth",   FloatType(),   True), \
  StructField("table",   IntegerType(), True), \
  StructField("price",   IntegerType(), True), \
  StructField("x",       FloatType(),   True), \
  StructField("y",       FloatType(),   True), \
  StructField("z",       FloatType(),   True), \
])
data = [ (1, 0.23, "Ideal",   "E", "SI2", 61.5, 55, 326, 3.95, 3.98, 2.43 ), \
         (2, 0.21, "Premium", "E", "SI1", 59.8, 61, 326, 3.89, 3.84, 2.31 ) ]
df = spark.createDataFrame(data, schema)

def test_tableExists():
  assert tableExists(tableName, dbName) is True

def test_columnExists():
  assert columnExists(df, columnName) is True

def test_numRowsInColumnForValue():
  assert numRowsInColumnForValue(df, columnName, columnValue) > 0
```

**Notebook cells to run pytest**

```python
%pip install pytest
```

```python
import pytest
import sys

# Skip writing pyc files on a readonly filesystem.
sys.dont_write_bytecode = True

retcode = pytest.main([".", "-v", "-p", "no:cacheprovider"])

# Fail the cell execution if there are any test failures.
assert retcode == 0, "The pytest invocation failed. See the log for details."
```

Key flags: `-v` verbose, `-p no:cacheprovider` skips `.pytest_cache` (readonly filesystem). `sys.dont_write_bytecode = True` also needed for readonly filesystem.

### R — testthat

**myfunctions.r**

```r
library(SparkR)

table_exists <- function(table_name, db_name) {
  tableExists(paste(db_name, ".", table_name, sep = ""))
}

column_exists <- function(dataframe, column_name) {
  column_name %in% colnames(dataframe)
}

num_rows_in_column_for_value <- function(dataframe, column_name, column_value) {
  df = filter(dataframe, dataframe[[column_name]] == column_value)
  count(df)
}
```

**test_myfunctions.r**

```r
library(testthat)
source("myfunctions.r")

table_name   <- "diamonds"
db_name      <- "default"
column_name  <- "clarity"
column_value <- "SI2"

# fake data
schema <- structType(
  structField("_c0",     "integer"), structField("carat",   "float"),
  structField("cut",     "string"),  structField("color",   "string"),
  structField("clarity", "string"),  structField("depth",   "float"),
  structField("table",   "integer"), structField("price",   "integer"),
  structField("x",       "float"),   structField("y",       "float"),
  structField("z",       "float"))
data <- list(list(as.integer(1), 0.23, "Ideal",   "E", "SI2", 61.5, as.integer(55), as.integer(326), 3.95, 3.98, 2.43),
             list(as.integer(2), 0.21, "Premium", "E", "SI1", 59.8, as.integer(61), as.integer(326), 3.89, 3.84, 2.31))
df <- createDataFrame(data, schema)

test_that("The table exists.", {
  expect_true(table_exists(table_name, db_name))
})
test_that("The column exists in the table.", {
  expect_true(column_exists(df, column_name))
})
test_that("There is at least one row in the query result.", {
  expect_true(num_rows_in_column_for_value(df, column_name, column_value) > 0)
})
```

**Notebook cells to run testthat**

```r
install.packages("testthat")
```

```r
library(testthat)
source("myfunctions.r")
test_dir(".", reporter = "tap")
```

### Scala — ScalaTest

Functions live in a separate `myfunctions` notebook. Tests use `%run` to import them.

**Test notebook, cell 1**

```scala
%run ./myfunctions
```

**Test notebook, cell 2** (AsyncFunSuite pattern)

```scala
import org.scalatest._
import org.apache.spark.sql.types.{StructType, StructField, IntegerType, FloatType, StringType}
import scala.collection.JavaConverters._

class DataTests extends AsyncFunSuite {
  val tableName   = "diamonds"
  val dbName      = "default"
  val columnName  = "clarity"
  val columnValue = "SI2"

  val schema = StructType(Array(
    StructField("_c0", IntegerType), StructField("carat", FloatType),
    StructField("cut", StringType),  StructField("color", StringType),
    StructField("clarity", StringType), StructField("depth", FloatType),
    StructField("table", IntegerType), StructField("price", IntegerType),
    StructField("x", FloatType), StructField("y", FloatType), StructField("z", FloatType)
  ))
  val data = Seq(
    Row(1, 0.23, "Ideal",   "E", "SI2", 61.5, 55, 326, 3.95, 3.98, 2.43),
    Row(2, 0.21, "Premium", "E", "SI1", 59.8, 61, 326, 3.89, 3.84, 2.31)
  ).asJava
  val df = spark.createDataFrame(data, schema)

  test("The table exists") {
    assert(tableExists(tableName, dbName) == true)
  }
  test("The column exists") {
    assert(columnExists(df, columnName) == true)
  }
  test("There is at least one matching row") {
    assert(numRowsInColumnForValue(df, columnName, columnValue) > 0)
  }
}

nocolor.nodurations.nostacks.stats.run(new DataTests)
```

The runner call `nocolor.nodurations.nostacks.stats.run(...)` suppresses ANSI color codes and timing output for clean notebook output.

### SQL — SELECT if pattern

SQL testing uses `SELECT if(udf_call, printf("PASS:..."), printf("FAIL:..."))` — no external framework needed. Tests against a view created from real or fake data.

**Setup cell**

```sql
USE CATALOG main;
USE SCHEMA default;

CREATE VIEW view_diamonds AS
SELECT * FROM diamonds;
```

**Test cells**

```sql
SELECT if(table_exists("main", "default", "view_diamonds"),
          printf("PASS: The table 'main.default.view_diamonds' exists."),
          printf("FAIL: The table 'main.default.view_diamonds' does not exist."));

SELECT if(column_exists("main", "default", "view_diamonds", "clarity"),
          printf("PASS: The column 'clarity' exists in the table 'main.default.view_diamonds'."),
          printf("FAIL: The column 'clarity' does not exists in the table 'main.default.view_diamonds'."));

SELECT if(num_rows_for_clarity_in_diamonds("VVS2") > 0,
          printf("PASS: The table 'main.default.view_diamonds' has at least one row where the column 'clarity' equals 'VVS2'."),
          printf("FAIL: The table 'main.default.view_diamonds' does not have at least one row where the column 'clarity' equals 'VVS2'."));
```

SQL UDFs (`table_exists`, `column_exists`, `num_rows_for_clarity_in_diamonds`) must be pre-registered; the docs show the test cell structure but define the UDFs elsewhere.

### CI/CD integration

> "set up a continuous integration and continuous delivery or deployment (CI/CD) system, such as GitHub Actions, to automatically run your unit tests whenever your code changes."

No further detail on the mechanics; GitHub Actions is the named example.

## Quotes worth keeping

> "In general, it is a best practice to not run unit tests against functions that work with data in production."

> "Databricks recommends storing functions and their unit tests outside of notebooks." (Python/R)

> "Databricks recommends including functions in one notebook and their unit tests in a separate notebook." (Scala)

## Open questions

- ❓ Where are the SQL UDFs (`table_exists`, `column_exists`) defined? The docs show the test cells but not the UDF creation — are these built-in Databricks SQL functions or user-defined?
- ❓ Does the pytest run in the notebook have access to workspace files in the same directory automatically, or does a specific working-directory setup need to happen?
- ❓ For Scala, is `AsyncFunSuite` (async test suite) required, or can `FunSuite` (sync) be used? The example uses async without explanation.

## Related sources

- [[notebooks-overview]] — hub page; "Unit testing" is listed under "Debug and optimize"
- [[notebook-debugger]] — interactive debugger for runtime debugging; complementary to unit tests
- [[ch01-getting-started-with-databricks]] — DCDE-SG Ch 1; covers workspace files and notebooks where test files are stored
