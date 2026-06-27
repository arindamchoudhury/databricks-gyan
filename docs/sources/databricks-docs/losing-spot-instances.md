# Losing Spot Instances

> **Source:** [docs.databricks.com/aws/en/optimizations/spark-ui-guide/losing-spot-instances](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/losing-spot-instances)
> **Added:** 2026-06-17
> **Source updated:** 2024-07-16
> **Tags:** spark, spark-ui, debugging, spot-instances, AWS, executors, B2, B16
> **Type:** documentation

A sparse sub-page of the Spark UI Guide series, reached from [[failing-spark-jobs]] when the Event log shows spot-instance reclaim. The root cause is using an instance type with a high AWS reclaim rate — this is the cloud provider reclaiming VMs, not a Spark bug.

> "If you're losing spot instances, you may be using an instance type that has a high reclaim rate."

| Option | When to use |
|---|---|
| **Change instance type** | Check the [AWS Spot Instance Advisor](https://aws.amazon.com/ec2/spot/instance-advisor/) for reclaim frequency; switch to a type with < 5% reclaim rate |
| **Stop using spot instances** | When the job SLA can't tolerate interruption |
| **Review Databricks spot optimization guidance** | For balancing cost vs reliability |

Related: [[failing-spark-jobs]], [[spark-ui-guide]].
