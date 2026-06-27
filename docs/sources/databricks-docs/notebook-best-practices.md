# Notebook Best Practices (Software Engineering)

> **Source:** [docs.databricks.com/aws/en/notebooks/best-practices](https://docs.databricks.com/aws/en/notebooks/best-practices)
> **Added:** 2026-06-17
> **Source updated:** 2026-06-16
> **Tags:** notebooks, best-practices, git, testing, CI-CD, modularization, jobs, B1
> **Type:** documentation

An end-to-end walkthrough applying software-engineering discipline to a Databricks notebook, using a COVID-19 analysis notebook as the running example: Git branching → shared module extraction → pytest → Lakeflow job with task dependencies → optional GitHub Actions CI/CD. The headline rule: **never use the notebook schedule button** — always create a job pointing at the committed version.

| Step | What | Key action |
|---|---|---|
| 1 | Git setup | Connect GitHub credentials; create Git folder/repo in workspace |
| 2 | Import & run notebook | Branch → import → run → check in |
| 3 | Extract shared module | Move functions to `covid_analysis/transforms.py`; pin deps |
| 4 | Add tests | Write pytest in `tests/transforms_test.py`; check in |
| 5 | Create job | Two tasks: test notebook → main notebook (dependency) |
| 6 (optional) | CI/CD | Service principal; GitHub Actions workflow on PR |
| 7 (optional) | Trigger tests | Push → PR → Actions runs tests automatically |

## The principles

- **Work in Git branches** — "this branch enables you to work on files and code independently from your repo's `main` branch, which is a software engineering best practice." Every step branches before changing anything.
- **Extract reusable logic into workspace files** (e.g. `covid_analysis/transforms.py`) so functions can be reused and "more easily test[ed]… which… can raise the overall quality of your code."
- **Pin dependency versions** — "declaring dependencies improves reproducibility by using precisely defined versions of libraries."
- **Test with pytest against fake data** in `tests/testdata.csv`, not production.
- **Two-task job** — test task → main notebook task; the dependency enforces tests-pass-before-run.

> ⚠️ **The schedule-button anti-pattern:** "the schedule button creates a job by using the latest **working** copy of the notebook in the workspace repo. Instead, Databricks recommends… a job that uses the latest **committed** version." Working copy = uncommitted edits included; committed = only what's in Git.

> **CI/CD security:** "For security reasons, Databricks discourages you from giving your Databricks workspace user's personal access token to GitHub… Notebooks are run with all of the workspace permissions of the identity that is associated with the token, so Databricks recommends using a service principal."

## The example module — `covid_analysis/transforms.py`

Four pandas transformation functions (operate on pandas DataFrames, not Spark):

```python
import pandas as pd

def filter_country(pdf, country="USA"):
    return pdf[pdf.iso_code == country]

def pivot_and_clean(pdf, fillna):
    pdf["value"] = pd.to_numeric(pdf["value"])
    return pdf.fillna(fillna).pivot_table(values="value", columns="indicator", index="date")

def clean_spark_cols(pdf):
    pdf.columns = pdf.columns.str.replace(" ", "_")
    return pdf

def index_to_col(df, colname):
    df[colname] = df.index
    return df
```

## The example tests — `tests/transforms_test.py`

pytest with **fixtures** loading test CSV data (not production):

```python
import pytest, pandas as pd
from covid_analysis.transforms import *

@pytest.fixture
def raw_input_df() -> pd.DataFrame:
    return pd.read_csv('tests/testdata.csv')

def test_filter(raw_input_df):
    assert filter_country(raw_input_df).iso_code.drop_duplicates()[0] == "USA"

def test_pivot(raw_input_df):
    assert pivot_and_clean(raw_input_df, 0)["Daily ICU occupancy"][0] == 0
```

## GitHub Actions CI/CD workflow

Triggers on every PR; runs the test notebook on an existing cluster via `databricks/run-notebook@main`, pinned to the PR head SHA:

```yaml
name: Run pre-merge Databricks tests
on:
  pull_request:
jobs:
  unit-test-notebook:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v2
      - uses: databricks/run-notebook@main
        with:
          databricks-token: <your-access-token>
          local-notebook-path: notebooks/run_unit_tests.py
          existing-cluster-id: <your-cluster-id>
          git-commit: '${{ github.event.pull_request.head.sha }}'
          run-name: 'EDA transforms helper module unit tests'
```

Related: [[notebook-testing]], [[notebook-share-code]], [[notebook-workflows]], [[lakeflow-jobs]], [[notebook-best-practices]].
