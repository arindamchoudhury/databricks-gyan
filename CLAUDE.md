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

Reading notes from doc-site pages live in `docs/sources/databricks-docs/`. The `research-notes` skill writes these.

**Nav placement for `docs.databricks.com` pages: mirror the page's breadcrumb verbatim, to full depth.** The site is Docusaurus, which generates the breadcrumb from the same `sidebars.js` that renders the sidebar — the two cannot disagree. So the generic research-notes warning that "a breadcrumb is not an information architecture" (written from HashiCorp docs, where it *is* lossy) **does not apply here**. `scripts/fetch_page.py` writes the trail as a `=== Breadcrumb ===` line at the top of `cache/web/<slug>.txt`; read it and use it.

Two rules that follow, both learned by getting them wrong:

- **Create the intermediate nav group even when it holds a single note.** The source's tree beats research-notes' "don't bury one note under an empty header" heuristic. `Schedule refreshes` was first filed flat for exactly that reason; it belongs under `Data engineering › Lakeflow Spark Declarative Pipelines › Standalone pipelines`.
- **Don't reach for `fetch_nav.py` on this site.** It works (rung 3, `ul.theme-doc-sidebar-menu`, ~5s), but the breadcrumb is already in the cache file and is the same signal. If you do run it, never add an "expand collapsed categories" pass — the ancestor chain is already expanded and the rest are off-screen, so every click fails actionability and burns ~50s for zero new links.

**Note structure is dynamic — mirror the source page, don't impose a skeleton.** A note's body should follow the *page's own* headings/sections (and its tables, images, and order), not a fixed `Summary / Key points / Notes / Quotes worth keeping / Related sources` template. Keep only the metadata header (Source / Added / Source updated / Tags / Type) and a light trailing line of `[[wikilink]]` cross-references; everything between is shaped by the page. A short page gets a short note; a page with four sections gets four sections.

## Doc-coverage requests

When a docs URL is shared with a coverage question ("do we have this in the learning path?", "is X covered?"), run **research-notes flavor 5**: classify coverage (absent / name-dropped / covered), and unless already fully covered, fetch (`scripts/fetch_page.py`, not WebFetch) → write the note → wire in by breadcrumb → fold into `docs/learning-path.md` (learning-path Phase 5: add reference, callout if new distinction, bump the header changelog) → validate TOML + commit. **Do not stop at reporting coverage — "name-dropped in a feature list" counts as a gap, not coverage.** Adding a note ≠ topic completion; leave the topic's ⬜/✅ status unless a chapter was written.

## Current stable version

Databricks Runtime 18 (released 2026-06-10) — Apache Spark 4.1.0.
Databricks Runtime 17.3 LTS (released 2025-10-22) — Apache Spark 4.0.0.

Key naming notes (use the new names in all content):
- Delta Live Tables (DLT) is now **Lakeflow Spark Declarative Pipelines** as of DAIS 2025.
- Delta Sharing is now **OpenSharing** as of June 2026 (announced 2026-06-10; same open protocol, now a Linux Foundation project extended to AI models, agent skills, and unstructured data). Use "OpenSharing" in new content; "Databricks-to-Databricks" remains the term for the DB↔DB sub-protocol. Keep "Delta Sharing" only in point-in-time release notes dated before June 2026.

## Site customisation

**Dark mode** (`[[project.theme.palette]]` in `zensical.toml`) — light "default" + dark "slate" schemes with a sun/moon toggle next to search. Verified working on the pinned `zensical>=0.0.30,<0.1` range (container resolves to 0.0.46): clean build, toggle renders, confirmed against [zensical.org/docs/setup/colors](https://zensical.org/docs/setup/colors/). Note: `theme.palette` became a **list** (breaking change) in [zensical 0.0.34](https://github.com/zensical/zensical/releases/tag/v0.0.34) — pre-0.0.34 it was a single dict with no toggle support. If a future pin drops below 0.0.34, this config needs the old single-dict form instead.

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
