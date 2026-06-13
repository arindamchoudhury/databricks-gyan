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
extra_javascript = ["javascripts/sidebar-toggle.js"]
```

**Sidebar collapse toggle** (`docs/javascripts/sidebar-toggle.js` + `docs/stylesheets/extra.css`):
- Both sidebars are `position: sticky` so they float in place as the main content scrolls
- Adds a ◀/▶ button to each sidebar; click to collapse/expand
- Collapsed state persists in `localStorage` across page navigations
- Left nav uses key `sidebar-nav-collapsed`, right TOC uses `sidebar-toc-collapsed`
- To remove: delete both files and remove the `extra_css`/`extra_javascript` lines from `zensical.toml`
