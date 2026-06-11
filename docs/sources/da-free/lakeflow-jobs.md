# M2-04: Creating a Simple Lakeflow Job

> **Source:** DA-FREE v3.1.1 — `M2 - Using Databricks for Data Engineering/DEWD00 - 04-Creating a Simple Databricks Job.ipynb` + `04A-Task 1 - Setup - Bronze.ipynb` + `04B-Task 2 - Silver - Gold.ipynb`
> **Added:** 2026-06-11
> **Tags:** lakeflow-jobs, orchestration, scheduling, serverless, I6
> **Type:** notebook

> 📌 **Full explained chapter:** [[ch08-lakeflow-jobs]]

## Summary

Creates a two-task Lakeflow Job that runs the Medallion pipeline from the previous notebook: Task 1 (Setup-Bronze) creates the bronze table via COPY INTO; Task 2 (Silver-Gold) transforms to silver and aggregates to gold. Covers the Jobs UI, task dependency configuration, scheduling options, serverless compute for jobs, and reviewing job run results.

## Key points

- **Lakeflow Jobs** (formerly Databricks Workflows) is the orchestration layer for scheduling all Databricks workloads.
- A job is created with one task, then additional tasks are added.
- Task 2 declares `Depends on: Setup-Bronze` → `Run if: All succeeded`.
- Serverless compute for jobs is the default; starts faster than classic clusters.
- **Performance Optimized Mode** reduces cold-start to ~30s (vs 4-6 min for Standard serverless).
- Scheduling uses a cron UI; the UI output is editable cron syntax.
- Job run history is on the **Runs** tab; each task's notebook output is inspectable.

## Notes

### Job structure: two tasks, one dependency

```
Job: <job_name>
├── Task 1: Setup-Bronze
│   └── Notebook: DEWD00 - 04A-Task 1 - Setup - Bronze
│       Compute: Serverless
└── Task 2: Silver-Gold
    └── Notebook: DEWD00 - 04B-Task 2 - Silver - Gold
        Compute: Serverless
        Depends on: Setup-Bronze
        Run if dependencies: All succeeded
```

Task 2 only runs if Task 1 succeeds. If Task 1 fails, Task 2 is skipped.

### Task 1 notebook (Setup-Bronze)

```python
spark.sql(f'USE CATALOG {DA.catalog_name}')
spark.sql(f'USE SCHEMA {DA.schema_name}')
```

```sql
CREATE TABLE IF NOT EXISTS current_employees_bronze_job (
  ID INT,
  FirstName STRING,
  Country STRING,
  Role STRING
);
```

```python
spark.sql(f'''
  COPY INTO current_employees_bronze_job
  FROM '/Volumes/dbacademy/{DA.schema_name}/myfiles/'
  FILEFORMAT = CSV
  FORMAT_OPTIONS (
    'header' = 'true',
    'inferSchema' = 'true'
  )
''').display()
```

No new patterns here — same COPY INTO shown in [[ingesting-data]]. The key difference is this notebook runs inside a Job task, not interactively.

### Task 2 notebook (Silver-Gold)

Same medallion transformations as [[medallion-architecture]], but targeting `_job` suffixed tables:

```sql
CREATE OR REPLACE TABLE current_employees_silver_job AS
SELECT
  ID, FirstName, Country,
  upper(Role) AS Role,
  current_timestamp() AS CurrentTimeStamp,
  date(CurrentTimeStamp) AS CurrentDate
FROM current_employees_bronze_job;

CREATE OR REPLACE TEMP VIEW temp_view_total_roles_job AS
SELECT Role, count(*) AS TotalEmployees
FROM current_employees_silver_job
GROUP BY Role;

CREATE TABLE IF NOT EXISTS total_roles_gold_job (
  Role STRING, TotalEmployees INT
);

INSERT OVERWRITE TABLE total_roles_gold_job
SELECT * FROM temp_view_total_roles_job;
```

### Creating a job: step-by-step

```
Jobs & Pipelines → Create → Job
→ Enter job name (from DA.print_lakeflow_job_info())

Task 1 (Setup-Bronze):
  Task name: Setup-Bronze
  Type: Notebook
  Source: Workspace
  Path: <navigate to DEWD00 - 04A-Task 1 - Setup - Bronze>
  Compute: Serverless
  → Create task

Task 2 (Silver-Gold):
  Add task → Notebook
  Task name: Silver-Gold
  Source: Workspace
  Path: <navigate to DEWD00 - 04B-Task 2 - Silver - Gold>
  Compute: Serverless
  Depends on: Setup-Bronze
  Run if dependencies: All succeeded
  → Create task
```

### Serverless compute modes for jobs

| Mode | Start time | Cost |
|------|-----------|------|
| Performance Optimized | ~30s | Higher |
| Standard | 4–6 min | ~70% cheaper |

The notebook instructs: enable **Performance Optimized Mode** in Job Details for faster startup during development/testing.

**Jobs vs All-Purpose billing:** Job compute (classic or serverless) is billed at a lower DBU rate than All-Purpose clusters. A warning appears when selecting an All-Purpose cluster for a job task.

### Scheduling

```
Job details → Schedules & Triggers → Add trigger
→ Trigger type: None (Manual) | Scheduled | Continuous | File arrival

Scheduled → cron UI with:
  - Every N minutes/hours/days/weeks/months
  - Day-of-week selector
  - Time and timezone
→ "Show cron syntax" to see/edit the underlying cron expression
→ Cancel to return without saving
```

Cron syntax example: `0 0 * * ?` = midnight UTC every day.

### Reviewing a job run

```
Job details → Runs tab
→ Click Start time timestamp to open the run
→ Click a task to see its notebook output
→ Status: Pending | Running | Succeeded | Failed | Skipped
```

Each task shows its notebook output exactly as it would in interactive mode — cell outputs, `display()` results, errors.

### Task types available in Lakeflow Jobs

From the task Type dropdown (noted in the notebook):

- Notebook
- Python script
- SQL
- dbt
- Lakeflow Spark Declarative Pipeline (formerly Delta Live Tables)
- JAR
- Spark Submit
- ...and more

> **Note from the notebook:** You could use a Lakeflow Spark Declarative Pipeline for this data engineering task. Declarative Pipelines can be scheduled within a Lakeflow Job as additional tasks.

## Related sources

- [[medallion-architecture]] — the same Bronze/Silver/Gold pattern run interactively
- [[ingesting-data]] — COPY INTO details used in Task 1
- [[ch08-lakeflow-jobs]] — full explanatory chapter
