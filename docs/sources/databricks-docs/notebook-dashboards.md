# Dashboards in Notebooks

> **Source:** [docs.databricks.com/aws/en/notebooks/dashboards](https://docs.databricks.com/aws/en/notebooks/dashboards)
> **Added:** 2026-06-17
> **Source updated:** 2026-06-17
> **Tags:** notebooks, dashboards, visualization, AI-BI, scheduling, sharing, B1
> **Type:** documentation

## Summary

Databricks notebooks support two distinct dashboard types: **notebook dashboards** (notebook-cell-output-bound presentations) and **AI/BI dashboards** (recommended for org-wide sharing, SQL-only). Dashboards can be scheduled, shared, and presented fullscreen.

## Key points

- Two types: **Notebook dashboards** (any cell output) vs **AI/BI dashboards** (SQL cell visualizations only).
- Databricks recommends **AI/BI dashboards** for organizational sharing.
- Notebook dashboards are **coupled to cell outputs** — clearing outputs clears the dashboard.
- Notebook dashboards support two layout modes: **Stack** (aligned grid) and **Float** (free drag).
- Both types can be **scheduled** via a notebook job; scheduling triggers notebook execution to refresh plots.
- Both types support **fullscreen presentation mode**.

## Notes

### Two dashboard types compared

| Feature | Notebook Dashboard | AI/BI Dashboard |
|---|---|---|
| Source cells | Any cell output | SQL cells only |
| Recommended for org sharing | No | Yes (Databricks recommendation) |
| Create via | "Add to notebook dashboard >" | "Add to dashboard" dialog |
| Tied to cell outputs | Yes — clearing outputs clears dashboard | N/A |

### Creating a notebook dashboard

From a cell's output menu:

> "Select **Add to notebook dashboard >**. If you select **Add to new notebook dashboard**, the new dashboard is automatically displayed."

### Creating an AI/BI dashboard

From a SQL cell's output menu:

> "Select **Add to dashboard**. In the **Add to dashboard** dialog, select **Create a new dashboard** or **Add to existing dashboard**."

### Critical limitation — notebook dashboards

> "Content in notebook dashboards are tied to the output of notebook cells. If you clear the cell output, the dashboard content is also cleared."

This is the main gotcha: `Clear outputs` in a notebook silently wipes all notebook dashboard content.

### Layout and sizing (notebook dashboards)

**Layout modes**

- **Stack** — items snap to an aligned grid
- **Float** — items move freely; drag anywhere on canvas

**Resize**

> "To resize an item, click [corner resize icon] at the lower-right corner and move your cursor until the item is the size you want."

**Move** — click and drag any item.

**Add a title to a plot**

> "Select the Settings icon. The **Configure Dashboard Element** dialog appears. In the dialog, click **Show Title**, enter a title for the plot, and click **Save**."

### Navigation

- Dashboard icon (top-right of notebook) lists all dashboards associated with the notebook.
- Switch between notebook view and dashboard view via that icon.
- Hover over a plot → "new window" icon → jumps to the source cell in the notebook.

### Scheduling

> "Click **Schedule** to create a scheduled job for the notebook that generates the dashboard plots."

Scheduling creates a Lakeflow job that re-runs the notebook on a timer. "View last successful run" shows the most recently refreshed state.

### Presentation mode

> "To present a dashboard, click **Fullscreen**. To return to the interactive dashboard, click **Exit** in the upper-left corner or press the `Esc` key."

### Deleting a dashboard

"Delete this dashboard" removes it entirely (does not affect the notebook or its outputs).

## Quotes worth keeping

> "Content in notebook dashboards are tied to the output of notebook cells. If you clear the cell output, the dashboard content is also cleared."

> "Only visualizations from SQL cells can be added to AI/BI dashboards."

## Open questions

- ❓ Do AI/BI dashboards support scheduling the same way (notebook job trigger), or do they have a separate refresh mechanism?
- ❓ Can notebook dashboards be shared with non-Databricks users (public link), or only within the workspace?
- ❓ What is the difference between notebook dashboard scheduling and Lakeflow Jobs scheduling — are they the same underlying mechanism?

## Related sources

- [[notebooks-overview]] — hub page; "Dashboards in notebooks" is listed as a collaborate/share topic
- [[lakeflow-jobs]] — scheduling a dashboard triggers a notebook job; see jobs notes for scheduling mechanics
- [[workspace-walkthrough]] — DA-FREE M1; covers the notebook UI that dashboards live inside
