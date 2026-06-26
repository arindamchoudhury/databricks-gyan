# Debug notebooks (interactive debugger)

> **Source:** [docs.databricks.com/aws/en/notebooks/debugger](https://docs.databricks.com/aws/en/notebooks/debugger)
> **Added:** 2026-06-14
> **Source updated:** 2026-06-16
> **Tags:** notebooks, debugging, variable-explorer, python, B1
> **Type:** documentation

> 📌 **Version note:** reflects the page as of 2026-06-14. Requirements quote minimum runtimes (DBR 13.3/14.3 LTS); current runtimes are DBR 18 / 17.3 LTS, so any supported cluster qualifies.

Databricks has a built-in **interactive debugger** for **Python notebooks** — breakpoints, step-through execution, a variable explorer, and a debug console — instead of relying on `pdb`/`%debug`. This page is *only* about that visual debugger (it doesn't mention `pdb`, `%debug`, `%pdb`, post-mortem debugging, or `breakpoint()`). It's enabled per-user via a Developer setting.

## Requirements

One of: **Serverless compute**; **Standard access mode** on DBR **14.3 LTS+**; **Dedicated access mode** on DBR **13.3 LTS+**; or **No Isolation Shared** on DBR **13.3 LTS+**. Enable it via Username (top-right) → **Settings** → **Developer** → toggle **Python Notebook Interactive Debugger** on.

## Start debugging

Menu **Run > Debug cell**; keyboard **Option/Alt + Shift + D**; the cell menu's **Debug cell**; or, after an exception, the **Debug** button in the error output (debug from the failure).

[![Debug cell item in the cell run menu](assets/notebook-debugger/02-debug-cell-menu.png)](assets/notebook-debugger/02-debug-cell-menu.png)

## Debugging actions

Click the **cell gutter** to add/remove breakpoints — execution pauses *before* the breakpointed line. The toolbar sets/removes breakpoints, shows variable values, **steps through** code, and **steps into / out of** functions. Stepping through a function shows its local variables marked **`[local]`**.

[![Adding and removing breakpoints in the cell gutter](assets/notebook-debugger/01-breakpoints.gif)](assets/notebook-debugger/01-breakpoints.gif)

## Step into workspace files

Requires **"Enable tabs for notebooks and files"** on. The **step-in** icon opens the referenced workspace file in a **new tab** and continues debugging there.

[![Stepping into a workspace file during a debug session](assets/notebook-debugger/05-step-into-workspace-file.gif)](assets/notebook-debugger/05-step-into-workspace-file.gif)

> ⚠️ "The debugger can only step into functions defined in files in the workspace. Stepping into Python libraries or other notebooks is not yet supported."

> 💡 **Stale-module gotcha:** if you edit an external file after it's imported, the session may keep using the old module. Use **autoreload** for Python modules on **DBR 18.0+** or **serverless environment version 4+** so edits to imported modules take effect during debugging.

## Debug console

Appears at the bottom when paused and runs Python in the current frame. **Enter** = single-line, **Shift + Enter** = multi-line; **15-second timeout**; **no `display()`** (use `df.show()` / `df.head()`). Code in the main notebook does **not** run during a debug session — only console code.

[![Debug console running code in the current frame while paused at a breakpoint](assets/notebook-debugger/03-debug-console.gif)](assets/notebook-debugger/03-debug-console.gif)

## Variable explorer

A right-sidebar panel listing variable values while paused. Click **Inspect** on a variable to run debug-console code showing its contents; a **search box** filters the list.

[![Variable explorer panel showing live variable values during a debug session](assets/notebook-debugger/04-variable-explorer.png)](assets/notebook-debugger/04-variable-explorer.png)

## Debug with Genie Code

**Genie Code** (the AI assistant) offers context-aware debugging help during a session.

## Limitations

- **Variable update timing:** on DBR 12.2 LTS+, variables update *during* cell execution; on earlier runtimes only *after* the cell completes.
- Step-into is limited to **workspace files** (no libraries / other notebooks). Sessions auto-terminate after **30 min** idle.

Related: [[notebooks-overview]], [[serverless-notebooks]], [[ch01-getting-started-with-databricks]], [[workspace-walkthrough]].
