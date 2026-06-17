# Lakeguard

> **Source:** [docs.databricks.com/aws/en/compute/lakeguard](https://docs.databricks.com/aws/en/compute/lakeguard)
> **Added:** 2026-06-16
> **Source updated:** 2025-11-05
> **Tags:** compute, lakeguard, security, isolation, standard-compute, spark-connect, UDF, B1
> **Type:** documentation

## Summary

Lakeguard is the set of technologies Databricks uses to enforce code isolation and data filtering on multi-user shared compute — standard classic compute, serverless compute, and SQL warehouses. It replaces the classic Spark model (shared JVM, privileged machine access) with container-sandboxed client processes connected via Spark Connect. UDFs are sandboxed separately on executors with egress network isolation. Data filtering prevents cross-user leakage through row/column security policies.

## Key points

- **Lakeguard** = code isolation + data filtering layer on all multi-user Databricks compute.
- Applies to: standard classic compute, serverless compute, SQL warehouses.
- **Two mechanisms**: Spark Connect (client ↔ driver decoupling) + container sandboxing (per-user isolated containers).
- **Spark Connect behavioral change**: defers analysis and name resolution to *execution time* — errors that surfaced at plan time may now surface later.
- **UDF egress isolation**: network traffic from UDFs is isolated to prevent unauthorized external access.
- **UDF scope**: isolated on standard compute and for Python UDFs on serverless/SQL warehouses. Scala/Java UDFs on serverless/SQL warehouses may not have equivalent isolation.
- **Data filtering**: prevents over-fetch leakage when row/column-level filters are applied.

## Notes

### The problem: classic Spark architecture

In traditional Spark, "user applications share a JVM with privileged access to the underlying machine." On shared compute, this means one user's process can potentially access another user's data or interfere with their execution.

### Lakeguard architecture

"Lakeguard isolates all user code using secure containers. This allows multiple workloads to run on the same compute resource while maintaining strict isolation between users."

Boundaries enforced: user ↔ user, user ↔ Spark driver, user ↔ Spark executors.

### Spark client isolation

Two components working together:

**Spark Connect**

"Lakeguard uses Spark Connect to decouple client applications from the driver. Client applications and drivers no longer share the same JVM or classpath."

> ⚠️ "Spark Connect defers analysis and name resolution to execution time, which may change the behavior of your code." Plan-time errors (e.g., referencing a nonexistent column) may not surface until the query actually runs. See also [[serverless-limitations]] which lists Spark Connect as the only supported API surface on serverless.

**Container sandboxing**

"Each client application runs in its own isolated container environment." Each user's notebook/query process is walled off from others — no shared memory, no shared classpath.

### UDF isolation

UDFs run on Spark executors and could in theory exfiltrate data or cross-contaminate. Lakeguard addresses this by:

- **Sandboxing** the UDF execution environment on executors.
- **Isolating egress network traffic** from UDFs to prevent unauthorized external access.
- **Replicating** the client's container environment into the UDF sandbox, so UDFs see consistent libraries.

**Scope of UDF isolation**:

| Surface | Python UDFs | Scala/Java UDFs |
|---|---|---|
| Standard classic compute | Isolated | Isolated |
| Serverless compute | Isolated | May not be equivalent |
| SQL warehouses | Isolated | May not be equivalent |

### Data filtering

Lakeguard prevents users from "accessing data resulting from over-fetching when queries include row- or column-level filters." Without isolation, a Spark engine that fetches more rows than a filter allows could expose those rows to another user sharing the same executor. Lakeguard enforces filter boundaries at the isolation layer.

## Open questions

- ❓ What specific code behavior changes are caused by Spark Connect deferring name resolution? Are there documented examples?
- ❓ Do Scala/Java UDFs on serverless/SQL warehouses have any isolation, or are they fully unrestricted?

## Related sources

- [[standard-compute-overview]] — standard compute uses Lakeguard; this page is the technical detail behind that security claim.
- [[serverless-limitations]] — Spark Connect is the only API surface on serverless; Lakeguard is why.
- [[dedicated-compute-overview]] — dedicated compute does NOT use Lakeguard (single-user; no isolation needed); that's why it can expose RDD APIs and privileged access.
- [[classic-compute-configure]] — access mode setting controls whether Lakeguard applies (Standard mode) or not (Dedicated mode).
