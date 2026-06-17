# Notebooks Overview

> **Source:** [docs.databricks.com/aws/en/notebooks/](https://docs.databricks.com/aws/en/notebooks/)
> **Added:** 2026-06-17
> **Source updated:** 2026-06-17
> **Tags:** notebooks, python, sql, scala, R, EDA, ML, collaboration, B1
> **Type:** documentation

## Summary

Hub page for Databricks notebooks documentation. Notebooks are described as "the primary tool for creating data science and machine learning workflows on Databricks." The page is a navigation index organized into four areas: develop/run, collaborate/share, debug/optimize, and tutorials.

## Key points

- Notebooks support four languages: **Python, SQL, Scala, R** — all with syntax highlighting and IntelliSense.
- Compute is flexible — notebooks can run on serverless, classic, or SQL warehouse compute (see [[serverless-notebooks]]).
- Databricks embeds an AI assistant (**Genie Code / Data Science Agent**) that can orchestrate multi-step data science workflows from a single prompt.
- Notebooks support real-time collaboration, comments, and sharing.
- Interactive dashboards can be built directly from notebook cell results.
- An interactive visual debugger is available (see [[notebook-debugger]]).
- Unit testing is a first-class topic in the docs.

## Notes

### Documentation structure

**Get started tutorials**

- Query and visualize data from a notebook — SQL, Python, Scala, R against Unity Catalog
- Import and visualize CSV data — CSV → Unity Catalog → DataFrame → visualization
- EDA techniques — Python-based exploratory data analysis
- End-to-end classic ML models — data loading, visualization, hyperparameter tuning, MLflow

**Develop and run notebooks**

- Basic editing — cell types, keyboard shortcuts, essential features
- Develop code — Python, SQL, Scala, R; syntax highlighting; IntelliSense
- Run notebooks — flexible compute options, execution controls
- Use the Data Science Agent — Genie Code Agent mode for orchestrating multi-step workflows from a prompt

**Collaborate and share**

- Import and export — multiple export formats; import from external sources
- Collaborate — sharing, comments, real-time co-editing
- Dashboards — interactive dashboards from notebook results

**Debug and optimize**

- Code help using Genie Code — AI-assisted debugging and code writing
- Debug notebooks — interactive debugger (see [[notebook-debugger]])
- Unit testing — strategies for validating notebook code

**Popular pages (highlighted by Databricks)**

- Databricks widgets — interactive input parameters for notebooks and dashboards
- Notebook outputs and results — cell outputs, results tables, filters, data download
- Orchestrate notebooks and modularize code — notebook workflow orchestration, code modularization
- Best practices — recommended practices for efficient, maintainable notebooks

## Open questions

- ❓ Does "Data Science Agent" (Genie Code Agent mode) require a specific compute type or tier?
- ❓ What export formats are supported for notebooks (IPYNB, HTML, PDF, DBC, source)?
- ❓ Are dashboards from notebooks different from Databricks SQL Dashboards?

## Related sources

- [[notebook-debugger]] — detailed notes on the interactive Python debugger (breakpoints, variable explorer, debug console)
- [[serverless-notebooks]] — serverless compute for notebooks; covers query insights and auto-suspend
- [[workspace-walkthrough]] — DA-FREE M1; hands-on intro to the notebook UI
- [[ch01-getting-started-with-databricks]] — DCDE-SG Ch 1; covers notebook fundamentals and cluster access modes
