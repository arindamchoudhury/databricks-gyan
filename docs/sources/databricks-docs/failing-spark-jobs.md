# Failing Jobs or Executors Removed

> **Source:** [docs.databricks.com/aws/en/optimizations/spark-ui-guide/failing-spark-jobs](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/failing-spark-jobs)
> **Added:** 2026-06-17
> **Source updated:** 2026-03-06
> **Tags:** spark, spark-ui, debugging, executors, memory, spot-instances, autoscaling, B2, B16
> **Type:** documentation

A sub-page of the Spark UI Guide series covering the three causes of executor removal, with step-by-step navigation for diagnosing failing jobs and failing executors. The terminal escalation: if no other cause applies, assume a memory issue.

## Three causes of executor removal

| Cause | Is it an error? | Next step |
|---|---|---|
| **Autoscaling** | No — expected | Nothing needed |
| **Spot instance reclaim** | No — cloud provider taking VMs back | → [[losing-spot-instances]] |
| **OOM (out of memory)** | Yes | → [[spark-memory-issues]] |

## Diagnosing failing jobs

Click the failing job → job detail, then scroll to the failed stage and read the **failure reason**; click the stage-description link for more detail, then scroll further for per-task failure reasons.

[![Jobs list with failed entries](assets/failing-spark-jobs/01-failing-jobs.png)](assets/failing-spark-jobs/01-failing-jobs.png)
[![Failure reason below the stage timeline](assets/failing-spark-jobs/02-failed-stage-reason.png)](assets/failing-spark-jobs/02-failed-stage-reason.png)
[![Stage description link expands error context](assets/failing-spark-jobs/03-failed-stage-description.png)](assets/failing-spark-jobs/03-failed-stage-description.png)
[![Per-task failure reasons](assets/failing-spark-jobs/04-failed-tasks.png)](assets/failing-spark-jobs/04-failed-tasks.png)

## Diagnosing failing executors

Check the compute's **Event log** first — spot reclaim → [[losing-spot-instances]]; autoscaling resize → expected. If there's no explanation, go to **Spark UI → Executors tab** and get logs from the failed executors (stderr/stdout often has the root cause).

[![Cluster Event log](assets/failing-spark-jobs/05-event-log.png)](assets/failing-spark-jobs/05-event-log.png)
[![Executors tab](assets/failing-spark-jobs/06-executors-tab.png)](assets/failing-spark-jobs/06-executors-tab.png)
[![Failed executors with log links](assets/failing-spark-jobs/07-failed-executors.png)](assets/failing-spark-jobs/07-failed-executors.png)

## Escalation

> "If you've gotten this far, the likeliest explanation is a memory issue."

→ See [[spark-memory-issues]].

Related: [[spark-ui-guide]], [[losing-spot-instances]], [[spark-memory-issues]], [[optimize-data-workloads-guide]].
