# ipywidgets in Notebooks

> **Source:** [docs.databricks.com/aws/en/notebooks/ipywidgets](https://docs.databricks.com/aws/en/notebooks/ipywidgets)
> **Added:** 2026-06-17
> **Source updated:** 2024-06-27
> **Tags:** notebooks, ipywidgets, python, interactive, visualization, B1
> **Type:** documentation

## Summary

ipywidgets are interactive Python UI controls (30+ types: sliders, checkboxes, buttons, tabs, accordions, grids) that run inside notebook cells. GA on DBR 13.0+. Key trade-off vs Databricks widgets: richer UI controls but **cannot pass parameters between notebooks or to jobs**. Recommended for Python-only interactive data exploration.

## Key points

- **GA on DBR 13.0+**; preview on DBR 11.0–12.2 LTS; **some controls broken on DBR 15.0**.
- Browser must reach `databricks-dev-cloudfront.dev.databricks.com` — blocked corporate proxies will break rendering.
- Default comm port 6062; change via Spark config at **cluster creation time** (not after).
- **Cannot** pass params between notebooks or to jobs — use Databricks widgets for that.
- Databricks recommends ipywidgets for Python; for R/Scala/SQL use `dbutils.widgets` instead.
- Third-party extras (ipyleaflet, bqplot, VegaFusion) = best-effort support only; some unsupported.

## Notes

### Version matrix

| Feature | Minimum DBR |
|---|---|
| ipywidgets (preview) | 11.0 |
| ipywidgets (GA) | 13.0 |
| Unity Catalog table access | 12.1 (UC-enabled cluster) |
| Port configuration | 11.3 LTS |
| Known breakage | 15.0 — some widgets do not work |

### Browser requirement

> "your browser must be able to access the `databricks-dev-cloudfront.dev.databricks.com` domain"

Widgets communicate via this domain. Corporate firewall/proxy blocking it = widgets silently fail.

### Port configuration

Default: **6062**. Conflicts with tools like Datadog can be resolved by setting an alternate port:

```
spark.databricks.driver.ipykernel.commChannelPort <port-number>
```

> ⚠️ "The Spark config must be set when the cluster is created." Cannot be changed on a running cluster.

### ipywidgets vs Databricks widgets

| Capability | ipywidgets | Databricks widgets (`dbutils.widgets`) |
|---|---|---|
| Languages | Python only | Python, Scala, R, SQL |
| UI richness | 30+ control types | 4 types (text, dropdown, combobox, multiselect) |
| Pass params to jobs | ❌ No | ✅ Yes |
| Pass params between notebooks | ❌ No | ✅ Yes (`%run $X="10"`) |
| Recommended for | Python interactive exploration | Cross-language, job params, dashboard params |

### Code examples

**Interactive histogram with `@interact` decorator**

```python
import ipywidgets as widgets
from ipywidgets import interact

sparkDF = spark.read.csv(
    "/databricks-datasets/bikeSharing/data-001/day.csv",
    header="true", inferSchema="true"
)

# (bins=(3, 10)) defines an integer slider widget allowing values between 3 and 10.
@interact(bins=(3, 10))
def plot_histogram(bins):
    pdf = sparkDF.toPandas()
    pdf.hist(column='temp', bins=bins)
```

The `@interact` decorator auto-creates a slider from the tuple argument — no explicit widget construction needed.

**IntSlider**

```python
import ipywidgets as widgets

int_slider = widgets.IntSlider(max=10, value=5)
int_slider
```

Display by returning the widget as the last expression in the cell.

**Button with Unity Catalog query (DBR 12.1+)**

```python
import ipywidgets as widgets

button = widgets.Button(description="Load dataframe sample")
output = widgets.Output()

def load_sample_df(table_name):
    return spark.sql(f"SELECT * FROM {table_name} LIMIT 1000")

def on_button_clicked(_):
    with output:
        output.clear_output()
        df = load_sample_df('<catalog>.<schema>.<table>')
        print(df.toPandas())

button.on_click(on_button_clicked)
display(button, output)
```

`widgets.Output()` captures cell output inside the callback; `with output:` + `output.clear_output()` replaces previous output on each click.

### Third-party widget ecosystem

Databricks provides **best-effort support** for:

- **ipyleaflet** — interactive maps
- **bqplot** — 2D plotting
- **VegaFusion** — scalable Vega/Altair rendering

Some third-party widgets are explicitly unsupported. No list given in docs.

## Quotes worth keeping

> "ipywidgets are visual elements that allow users to specify parameter values in notebook cells."

> "You can use Databricks widgets to pass parameters between notebooks and to pass parameters to jobs; ipywidgets do not support these scenarios."

> "Some ipywidgets do not work in Databricks Runtime 15.0."

## Open questions

- ❓ Which specific widgets are broken on DBR 15.0? The docs say "some" without listing them.
- ❓ Is `widgets.Output()` the only way to display dynamic content from button callbacks, or can `display()` be called directly inside the handler?
- ❓ Do ipywidgets work on serverless compute, or only classic clusters?

## Related sources

- [[notebook-widgets]] — Databricks native widgets (`dbutils.widgets`); supports cross-notebook param passing and jobs; use for non-Python languages
- [[notebooks-overview]] — hub page; ipywidgets covered under Develop and run notebooks
- [[notebook-dashboards]] — dashboard widgets at top are Databricks widgets, not ipywidgets
