# Share Code Between Notebooks (Workspace Files)

> **Source:** [docs.databricks.com/aws/en/notebooks/share-code](https://docs.databricks.com/aws/en/notebooks/share-code)
> **Added:** 2026-06-17
> **Source updated:** 2026-06-16
> **Tags:** notebooks, workspace-files, modularization, python, git, B1
> **Type:** documentation

> ⚠️ **Capture note:** code examples on this page are rendered as images, not text — import syntax isn't extractable via fetch. The patterns (`import mymodule`, `from mymodule import func`) are standard Python.

The operational how-to for creating Python **workspace files** and importing them into notebooks (requires **DBR 11.3 LTS+**). Files live in the Databricks workspace, use standard Python `import`, sync to Git via Repos, and are the **recommended** modularization approach over `%run`.

## Creating a workspace file

**Workspace sidebar** → **Create** → **File** → name it ending in `.py`. The file **auto-saves** on every edit.

[![File that defines functions](assets/notebook-share-code/01.png)](assets/notebook-share-code/01.png)

## Importing into a notebook

Standard Python `import` — Databricks adds the workspace directory to `sys.path` so same-folder files import by name:

```python
import mymodule
from mymodule import my_function
```

[![Import file into notebook](assets/notebook-share-code/02.png)](assets/notebook-share-code/02.png)

## Cross-folder imports

> "If a helper file is in another folder, you must use the full file path."

Get it via the file's kebab menu (⋮) → **Copy URL/path** → **Full path**, then add the directory to `sys.path` or use the full dotted module path.

[![Import file from another folder into a notebook](assets/notebook-share-code/03.png)](assets/notebook-share-code/03.png)

## Running, managing, Git

- **Run a file directly:** Shift+Enter (whole cell) / Shift+Ctrl+Enter (selected lines).
- **Management:** delete/rename via the Workspace menu; per-file access control requires **Premium plan+**.
- **Git:** "You can also use a Databricks repo to sync your files with a Git repository" — same commit/push/pull workflow as notebooks in Repos.
- **Orchestration:** "Databricks also supports multi-task jobs which allow you to combine notebooks into workflows with complex dependencies" — workspace files handle reuse within a notebook; jobs handle multi-notebook pipelines.

Related: [[notebook-workflows]], [[notebook-testing]], [[notebooks-overview]].
