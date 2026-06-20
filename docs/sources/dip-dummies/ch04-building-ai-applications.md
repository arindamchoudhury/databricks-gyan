# Ch 4 — Building AI Applications on the Databricks Data Intelligence Platform

> **Source:** Kaplan & Kara, *The Data Intelligence Platform For Dummies* (Wiley, 2nd Databricks Special Ed., © 2026) — Chapter 4, PDF pp. 39–48.
> **Added:** 2026-06-20
> **Tags:** agent-bricks, mlops, llmops, model-serving, mcp, ai-bi, databricks-apps, lakehouse-monitoring
> **Type:** book

> *The AI-development story: why building production agents is hard, the MLOps/LLMOps model lifecycle (refine → explain → deploy → govern → monitor drift), then Agent Bricks for building/evaluating/governing agents, MCP for connectivity, AI/BI for self-serve insight, and Databricks Apps. Closes with the "putting it all together" business pitch.*

> 📎 **Overlaps:** Agent Bricks and AI/BI introduced in [[ch03-databricks-platform]]; this chapter is the deeper cut.

---

## 1. Why building AI apps is hard

Three "hard" problems for production agents (esp. in financial/customer-facing risk paths):

- **Building/standardizing without knowing what agents do** — how to evaluate on *your* questions? what metrics? human + LLM judges? data drift?
- **Measuring/improving AI quality** — a "zoo" of optimization techniques, new models weekly; which is right?
- **Governing/scaling safely** — cost-vs-quality balance is painful trial and error; does cost scale prohibitively?

Answer: a suite of features spanning the AI development lifecycle.

---

## 2. Model management — MLOps / LLMOps

The model lifecycle Databricks supports end-to-end:

| Stage | Point |
|---|---|
| **Refining models** | Built on lakehouse data (quality data → quality models). E.g. linear regression for optimal price, logistic regression for loan approval. |
| **Explainability & transparency** | Business needs visibility into which features drove a decision; without it, models are black boxes and go unused. Databricks gives **lineage tracking** raw data → result. |
| **Deploying models** | Data scientist/ML engineer deploys via a **model serving endpoint** (low expertise needed); workflows move model dev → staging → production. |
| **Model governance** | As model count grows to hundreds/thousands, govern lifecycle via **UC** — only the right people promote to prod, only allowed users access training data. **UC audit logs + system tables** record who ran which model with what data, when. |
| **Monitoring & data drift** | Data changes over time (**data drift**) degrades accuracy. Dashboards + system tables show model health/failures; set metrics in dev, custom metrics via **lakehouse monitoring**. |

---

## 3. Developing AI applications

Key AI features the platform offers for app-building:

- **Customizing agent training** on proprietary data → domain-aligned outputs.
- **Reducing dev cost** — democratizes to non-technical users, makes technical users more efficient.
- **Comprehensive model support** — unified deploy/govern/query for models + agents.
- **Security & governance** — IP stays in your control via native UC; choose exactly what data the app sees.
- **Complete control** — own both models and data; build independent GenAI solutions.
- **Future-proofing** — Databricks framework + research team let you swap in the best new models as needs evolve.

---

## 4. Agent Bricks

Framework that simplifies building/optimizing **AI agent systems** (single or multi-agent) on your enterprise data. Full suite to **build, tune, evaluate, deploy** via reusable composable blocks.

Three capabilities:

1. **Build any agent any way** — custom-code agents (any framework/model), declarative agents (NL prompts), **AI functions** (intelligence directly in SQL).
2. **Evaluate & optimize quality** — measure every interaction; optimize accuracy/latency/cost; **built-in LLM judges** for continuous improvement.
3. **Govern & scale securely** — UC gives centralized access control + audits over agents, data, models, and external tools.

Workflow: define the high-level outcome via prompt → Databricks creates LLM judges + evaluations, optimizes with latest models/techniques, helps pick the quality/cost balance, learns from human feedback, repeat.

Example agents Agent Bricks targets:

- **Information extraction** — unstructured (PDFs/images) → structured fields.
- **Knowledge assistant** — high-quality **RAG** grounded in authoritative sources.
- **Supervisor of multiple agents** — orchestrates planners/executors/retrievers for complex workflows (supply chain, multichannel engagement).
- **Custom LLM agents** — translation, sentiment analysis with business context.
- **Customer support automation** — chatbots with citations + escalation.
- **Sales & marketing** — lead qualification, personalized comms, campaign optimization.
- **Data analysis & reporting** — multi-source collect/process/analyze → insights/reports.
- **Task automation** — scheduling, inventory, order processing, workflow coordination.
- **Classical AI agents** — fraud detection, demand forecasting, churn prediction.

> 💭 (mine): the bookstore recommender example shows the value-add over a vanilla recommender — Agent Bricks lets you encode business rules in NL ("don't recommend the sequel if they didn't read part 1").

### MCP — agent connectivity
- The roadblock to agent connectivity has been **data silos** — every tool (Salesforce, Slack, Teams, GitHub, Google Drive) needs a custom connector per framework.
- **Model Context Protocol (MCP)** = the open standard solving it — a universal way to connect agents to data/tools (built-in, third-party, or your own proprietary APIs).

---

## 5. Self-serve insight & apps

- **AI/BI** — two capabilities: **Genie** (talk with your data in business context) and **Dashboards** (business users self-serve AI-driven insight without BI teams). Detail in [[ch03-databricks-platform]].
- **Databricks Apps** — fast, secure way to build data/AI apps on the platform; architectural shift of *moving apps to where data/AI live* (not data to the app). Runs on **serverless compute**, one-click **Lakebase** integration as transactional engine, UC resource-level governance, 100% open source, works with popular Python/JS frameworks (React, JavaScript, Shiny) and vibe-coding tools.

---

## 6. Putting it all together

The platform helps organizations:

- **Reduce costs / consolidate data** — break silos, free budget for innovation.
- **Simplify governance & security** — one unified model = compliant, high-quality data.
- **Operationalize AI** — remove technical barriers for scalable, data-driven innovation everywhere.

---

## Summary

The AI-app lifecycle: data quality → model refine/explain/deploy/govern/monitor (MLOps/LLMOps with UC + lakehouse monitoring) → Agent Bricks to build/evaluate/govern agents (with MCP for connectivity) → surface via AI/BI and Databricks Apps. UC + lineage + system tables provide the governance spine throughout.

## References

- Source: PDF pp. 39–48. Figure 4-1 (Agent Bricks flow) not reproduced.
- External: AI/BI Genie (`databricks.com/product/business-intelligence/ai-bi-genie`), AI/BI Dashboards (`databricks.com/product/business-intelligence/ai-bi-dashboards`).
- Related: [[ch03-databricks-platform]], [[ch05-ten-reasons]].
