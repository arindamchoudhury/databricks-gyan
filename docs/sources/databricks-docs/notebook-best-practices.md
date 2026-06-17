# Notebook Best Practices (Software Engineering)

> **Source:** [docs.databricks.com/aws/en/notebooks/best-practices](https://docs.databricks.com/aws/en/notebooks/best-practices)
> **Added:** 2026-06-17
> **Source updated:** 2026-06-17
> **Tags:** notebooks, best-practices, git, testing, CI-CD, modularization, jobs, B1
> **Type:** documentation

## Summary

End-to-end walkthrough applying software engineering discipline to a Databricks notebook: Git branching → shared module extraction → pytest → Lakeflow job with task dependencies → optional GitHub Actions CI/CD. Uses a COVID-19 analysis notebook as the running example. Key rule: **never use the notebook schedule button** — always create a job pointing at the committed version.

## Key points

- Work in **Git branches** for all changes — never directly on `main`.
- Extract reusable logic into **workspace files** (e.g. `covid_analysis/transforms.py`), not notebook cells.
- Test functions with **pytest** against **fake/test data** in `tests/testdata.csv` — not production.
- Create a **two-task Lakeflow job**: test task → main notebook task (dependency enforces tests-pass-before-run).
- **Never use the notebook schedule button** — it runs the latest _working_ copy; a job uses the latest _committed_ version.
- For CI/CD: use a **service principal token**, not a personal access token.
- Declare **pinned dependency versions** for reproducibility.

## Notes

### The seven-step workflow

| Step | What | Key action |
|---|---|---|
| 1 | Git setup | Connect GitHub credentials; create Git folder/repo in workspace |
| 2 | Import & run notebook | Branch → import → run → check in |
| 3 | Extract shared module | Move functions to `covid_analysis/transforms.py`; pin deps |
| 4 | Add tests | Write pytest in `tests/transforms_test.py`; check in |
| 5 | Create job | Two tasks: test notebook → main notebook (dependency) |
| 6 (optional) | CI/CD | Service principal; GitHub Actions workflow on PR |
| 7 (optional) | Trigger tests | Push change to branch → PR → Actions runs tests automatically |

### Why branches

> "This branch enables you to work on files and code independently from your repo's `main` branch, which is a software engineering best practice."

Every step in the walkthrough creates a new branch before changing anything.

### Why shared modules

> "This enables you to use these functions with other similar notebooks, which can speed up future coding and help ensure more predictable and consistent notebook results."

> "Sharing this code also enables you to more easily test these functions, which as a software engineering best practice can raise the overall quality of your code as you go."

### Why pin dependencies

> "Declaring dependencies improves reproducibility by using precisely defined versions of libraries."

### The schedule button anti-pattern

> "Databricks does not recommend that you use the schedule button in the notebook...to schedule a job to run this notebook periodically. This is because the schedule button creates a job by using the latest **working** copy of the notebook in the workspace repo. Instead, Databricks recommends that you follow the preceding instructions to create a job that uses the latest **committed** version of the notebook in the repo."

The distinction: **working copy** = unsaved/uncommitted edits included. **Committed version** = only what's in Git.

### CI/CD security: service principal over PAT

> "For security reasons, Databricks discourages you from giving your Databricks workspace user's personal access token to GitHub."

> "Databricks recommends using a service principal...Notebooks are run with all of the workspace permissions of the identity that is associated with the token, so Databricks recommends using a service principal."

### The example module: covid_analysis/transforms.py

Four pandas transformation functions (all operate on pandas DataFrames, not Spark):

```python
import pandas as pd

def filter_country(pdf, country="USA"):
    pdf = pdf[pdf.iso_code == country]
    return pdf

def pivot_and_clean(pdf, fillna):
    pdf["value"] = pd.to_numeric(pdf["value"])
    pdf = pdf.fillna(fillna).pivot_table(
        values="value", columns="indicator", index="date"
    )
    return pdf

def clean_spark_cols(pdf):
    pdf.columns = pdf.columns.str.replace(" ", "_")
    return pdf

def index_to_col(df, colname):
    df[colname] = df.index
    return df
```

### The example test file: tests/transforms_test.py

pytest with **fixtures** loading test CSV data (not production):

```python
import pytest
import pandas as pd
import numpy as np
from covid_analysis.transforms import *

@pytest.fixture
def raw_input_df() -> pd.DataFrame:
    return pd.read_csv('tests/testdata.csv')

@pytest.fixture
def colnames_df() -> pd.DataFrame:
    df = pd.DataFrame(
        data=[[0,1,2,3,4,5]],
        columns=[
            "Daily ICU occupancy",
            "Daily ICU occupancy per million",
            "Daily hospital occupancy",
            "Daily hospital occupancy per million",
            "Weekly new hospital admissions",
            "Weekly new hospital admissions per million"
        ]
    )
    return df

def test_filter(raw_input_df):
    filtered = filter_country(raw_input_df)
    assert filtered.iso_code.drop_duplicates()[0] == "USA"

def test_pivot(raw_input_df):
    pivoted = pivot_and_clean(raw_input_df, 0)
    assert pivoted["Daily ICU occupancy"][0] == 0

def test_clean_cols(colnames_df):
    cleaned = clean_spark_cols(colnames_df)
    cols_w_spaces = cleaned.filter(regex=(" "))
    assert cols_w_spaces.empty == True

def test_index_to_col(raw_input_df):
    raw_input_df["col_from_index"] = raw_input_df.index
    assert (raw_input_df.index == raw_input_df.col_from_index).all()
```

Test data lives in `tests/testdata.csv` — a small CSV fixture, not a live table.

### GitHub Actions CI/CD workflow

Triggers on every pull request; runs the test notebook on an existing cluster using `databricks/run-notebook@main`:

```yaml
name: Run pre-merge Databricks tests
on:
  pull_request:
env:
  DATABRICKS_HOST: https://<your-workspace-instance-name>
jobs:
  unit-test-notebook:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Checkout repo
        uses: actions/checkout@v2
      - name: Run test notebook
        uses: databricks/run-notebook@main
        with:
          databricks-token: <your-access-token>
          local-notebook-path: notebooks/run_unit_tests.py
          existing-cluster-id: <your-cluster-id>
          git-commit: '${{ github.event.pull_request.head.sha }}'
          access-control-list-json: >
            [{ "group_name": "users", "permission_level": "CAN_VIEW" }]
          run-name: 'EDA transforms helper module unit tests'
```

`git-commit` pins the run to the PR head SHA — not the default branch.

## Quotes worth keeping

> "Databricks does not recommend that you use the schedule button in the notebook...This is because the schedule button creates a job by using the latest **working** copy of the notebook in the workspace repo."

> "For security reasons, Databricks discourages you from giving your Databricks workspace user's personal access token to GitHub."

> "Notebooks are run with all of the workspace permissions of the identity that is associated with the token, so Databricks recommends using a service principal."

## Open questions

- ❓ The test functions use pandas DataFrames (not Spark). For Spark-native transformations, would the same pytest pattern work with `SparkSession` fixtures, or does the `notebook-testing` page cover that?
- ❓ `databricks/run-notebook@main` — is this an official Databricks GitHub Action? Is `@main` stable or should it be pinned to a SHA?
- ❓ The job in step 5 uses an existing all-purpose cluster. Should production jobs use job clusters instead for isolation and cost reasons?

## Related sources

- [[notebook-testing]] — the detailed pytest reference; this page shows a real-world example using the same pytest pattern
- [[notebook-share-code]] — the workspace file creation UI mechanics; step 3 of this walkthrough uses that
- [[notebook-workflows]] — `dbutils.notebook.run()` and `%run`; this page uses Lakeflow Jobs instead (the recommended approach)
- [[lakeflow-jobs]] — DA-FREE M2-04; hands-on intro to the jobs UI used in step 5
