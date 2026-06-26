# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Commands

```bash
# Recommended: Docker with live-reload (port 8001 to avoid conflict with spark notes)
docker compose up          # http://localhost:8000; auto-rebuilds on docs/ or zensical.toml changes

# Local Python alternative
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install zensical
zensical serve
```

## Architecture

Zensical static site. Content in `docs/` as Markdown. `zensical.toml` holds all nav — **every new page must be added to nav or it won't appear**.

Book chapters live in `docs/book/`. One chapter per learning-path topic. The book skill (`databricks-book`) writes these.

Reading notes from doc-site pages live in `docs/sources/databricks-docs/`. The `research-notes` skill writes these; nav is grouped by each page's own breadcrumb (see research-notes "Documentation-site sources" rule).

**Note structure is dynamic — mirror the source page, don't impose a skeleton.** A note's body should follow the *page's own* headings/sections (and its tables, images, and order), not a fixed `Summary / Key points / Notes / Quotes worth keeping / Related sources` template. Keep only the metadata header (Source / Added / Source updated / Tags / Type) and a light trailing line of `[[wikilink]]` cross-references; everything between is shaped by the page. A short page gets a short note; a page with four sections gets four sections.

## Doc-coverage requests

When a docs URL is shared with a coverage question ("do we have this in the learning path?", "is X covered?"), run **research-notes flavor 5**: classify coverage (absent / name-dropped / covered), and unless already fully covered, fetch (`scripts/fetch_page.py`, not WebFetch) → write the note → wire in by breadcrumb → fold into `docs/learning-path.md` (learning-path Phase 5: add reference, callout if new distinction, bump the header changelog) → validate TOML + commit. **Do not stop at reporting coverage — "name-dropped in a feature list" counts as a gap, not coverage.** Adding a note ≠ topic completion; leave the topic's ⬜/✅ status unless a chapter was written.

## Current stable version

Databricks Runtime 18 (released 2026-06-10) — Apache Spark 4.1.0.
Databricks Runtime 17.3 LTS (released 2025-10-22) — Apache Spark 4.0.0.

Key naming notes (use the new names in all content):
- Delta Live Tables (DLT) is now **Lakeflow Spark Declarative Pipelines** as of DAIS 2025.
- Delta Sharing is now **OpenSharing** as of June 2026 (announced 2026-06-10; same open protocol, now a Linux Foundation project extended to AI models, agent skills, and unstructured data). Use "OpenSharing" in new content; "Databricks-to-Databricks" remains the term for the DB↔DB sub-protocol. Keep "Delta Sharing" only in point-in-time release notes dated before June 2026.

## `[project.theme]` intentionally absent — Zensical 0.0.x raises an error if set.

## Site customisation

Custom CSS and JS are loaded via `zensical.toml`:

```toml
extra_css = ["stylesheets/extra.css"]
extra_javascript = ["javascripts/sideba