# Losing Spot Instances

> **Source:** [docs.databricks.com/aws/en/optimizations/spark-ui-guide/losing-spot-instances](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/losing-spot-instances)
> **Added:** 2026-06-17
> **Source updated:** 2024-07-16
> **Tags:** spark, spark-ui, debugging, spot-instances, AWS, executors, B2, B16
> **Type:** documentation

## Summary

Very sparse sub-page of the Spark UI Guide series, reached from [[failing-spark-jobs]] when the Event log shows spot instance reclaim. Root cause: using an instance type with a high AWS reclaim rate. Three options.

## Key points

- Losing spot instances = cloud provider reclaiming VMs, not a Spark bug.
- High reclaim rate is instance-type specific — check AWS Spot Instance Advisor before picking a type.
- Fastest fix: switch to on-demand (stop using spot).

## Notes

> "If you're losing spot instances, you may be using an instance type that has a high reclaim rate."

**Three options:**

| Option | When to use |
|---|---|
| **Change instance type** | Check [AWS Spot Instance Advisor](https://aws.amazon.com/ec2/spot/instance-advisor/) for reclaim frequency; switch to a type with < 5% reclaim rate |
| **Stop using spot instances** | When job SLA cannot tolerate interruption |
| **Review Databricks spot optimization guidance** | For balancing cost vs. reliability |

## Related sources

- [[failing-spark-jobs]] — escalation source; spot reclaim is one of the three executor-loss causes
- [[spark-ui-guide]] — parent guide
