# Ch 4 — Bringing Data Intelligence to the Data Lakehouse

> **Source:** Kaplan & Kara, *The Data Lakehouse For Dummies* (Wiley, 2nd Databricks Special Ed., © 2026) — Chapter 4, PDF pp. 21–26.
> **Added:** 2026-06-20
> **Tags:** data-intelligence, ai-bi-genie, agent-bricks, rag, databricks-apps, mosaic-ai, unity-catalog
> **Type:** book

> *Why "almost every company has a lakehouse" isn't enough, and how GenAI-driven data intelligence — Genie, AI Assistant, Agent Bricks, Apps — closes the remaining gaps.*

> 📎 **Overlaps:** this is the booklet's condensed version of [[ch04-building-ai-applications]] (DIP §4) plus the [[ch01-understanding-data-intelligence]] (DIP §1) definition of data intelligence. Component taxonomy in [[ch03-databricks-platform]] (DIP §3).

---

## 1. The remaining challenges (even with a lakehouse)

Lakehouses unified data, but gaps persist:

- Business users **bottlenecked by technical staff** to build dashboards when they just want to *talk* to data.
- **Discovery is hard** — finding the right table/column among tens of thousands needs heavy curation.
- GenAI amplifies **security/privacy/accuracy** concerns about LLMs.
- Companies want intelligence on **their own** data estate, with **their own** business terms — not diluted by general-purpose LLMs.

Root cause: platforms lack a fundamental understanding of *organizational* data and its usage. **GenAI** is the tool to fix exactly this.

---

## 2. Introducing data intelligence

**Data intelligence** = using AI to deeply understand the **semantics** of your enterprise data (governed by your data), then automatically analyzing it, optimizing workflows, and unlocking new capabilities. It enables:

- **Natural language** — converse with your own data; anyone can use it.
- **Semantic cataloging & discovery** — understands your data model, metrics, KPIs; surfaces discrepancies.
- **Automated management & optimization** — learns usage patterns, improves layout/partitioning/indexing without manual tuning.
- **Enhanced governance & privacy** — auto-detect/classify/prevent misuse of sensitive data via natural language.
- **First-class AI app support** — uses the business's own terminology/metrics for accurate results; no brittle prompt-engineering hacks.

---

## 3. The Databricks Data Intelligence Platform

Built on the lakehouse (unified governance, open format-agnostic storage, one platform spanning ETL/SQL/ML/AI/BI), it adds AI-powered capabilities:

- **AI/BI Genie** — talk to your data in business context via AI/BI dashboards; business users self-serve insights without waiting on BI teams, governed with human guidance.
- **Platform optimization** — auto-adjusts column indexing, partition layout → better performance, lower cost.
- **Enhanced governance** — UC auto-generates descriptions/tags for tables/columns → better semantic search + AI quality.
- **AI Assistant** — coding/debugging help (Python, SQL); **Agent mode** plans + automates multistep solutions; **Data Science Agent** for advanced analytics.
- **Query performance** — uses data predictions for optimal query planning → fast, low-cost queries.
- **Efficient scaling** — predicts workload needs for optimal ETL/orchestration autoscaling.

---

## 4. Building agent systems

Data intelligence platforms simplify enterprise AI apps, especially **agent systems** = lakehouse + AI agents that understand your data. Databricks builds/deploys/manages AI apps and agents (RAG pipelines, vector indexes) **without duplicating data**. **Agent Bricks** adds prebuilt, production-ready agents optimized on your data.

The unified platform supports:

- **Agents that reason over your data** — securely connect enterprise data to agents (incl. Agent Bricks); auto-generate **vector indexes** and ML features from production data — no duplication. Customize models: build RAG apps, fine-tune open-source LLMs, train custom LLMs and classical ML.
- **Custom evaluation** — built-in agent evaluation; mix open-source + commercial GenAI + ML models; **AI-assisted judges** grade responses, human experts give peer feedback; trace root cause → fix → redeploy.
- **Unified governance** — end-to-end governance for agents, incl. models hosted *outside* Databricks; UC enforces access controls, rate limits (cost), harmful-content prevention, lineage from data → models.

> 💡 **Why compound systems beat a single LLM:** combining many models (LLMs + classical ML + tools), retrievers, and vector databases yields higher-quality, safer, more governed outputs than one model alone (Figure 4-1).

### Accelerators: Apps + Agent Bricks

- **Databricks Apps** — quickly build secure data/AI apps on your own data estate. Runs on **serverless**, powered by data intelligence, secured/governed out of the box, open Python ecosystem (**Dash, Streamlit, Gradio**). The architectural shift: **move the app to where the data and AI live**, not the data to the app.
- **Agent Bricks** — research-backed automation to build/evaluate/optimize agent systems grounded on your data: custom evals, swap models as the market evolves, balance cost vs. quality, stitch multiple agents. Examples: extract insights from docs, build Q&A agents, create custom LLMs. Governed by **Unity Catalog** + **AI Gateway**. "Focus on value, not infrastructure."

---

## Summary

A lakehouse alone leaves business users dependent on technical staff and struggling to discover data. **Data intelligence** layers GenAI that understands your data's semantics — surfaced through **Genie, AI Assistant, Agent Bricks, and Apps**, all governed by UC + AI Gateway — to democratize data and ship governed AI agents without duplicating data.

## References

- Source: PDF pp. 21–26. Figure 4-1 (agent systems on the platform) not reproduced.
- Related: [[05-ten-reasons]], [[ch04-building-ai-applications]] (DIP), [[ch01-understanding-data-intelligence]] (DIP).
