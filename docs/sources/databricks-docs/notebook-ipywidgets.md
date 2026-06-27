# ipywidgets in Notebooks

> **Source:** [docs.databricks.com/aws/en/notebooks/ipywidgets](https://docs.databricks.com/aws/en/notebooks/ipywidgets)
> **Added:** 2026-06-17
> **Source updated:** 2024-06-27
> **Tags:** notebooks, ipywidgets, python, interactive, visualization, B1
> **Type:** documentation

> "ipywidgets are visual elements that allow users to specify parameter values in notebook cells."

ipywidgets are interactive **Python** UI controls (30+ types: sliders, checkboxes, buttons, tabs, accordions, grids) that run inside notebook cells. GA on **DBR 13.0+**. The key trade-off vs Databricks widgets: richer UI controls but "ipywidgets do not support" passing parameters between notebooks or to jobs. Recommended for Python-only interactive exploration; for R/Scala/SQL use `dbutils.widgets` instead.

| Feature | Minimum DBR |
|---|---|
| ipywidgets (preview) | 11.0 |
| ipywidgets (GA) | 13.0 |
| Unity Catalog table access | 12.1 (UC-enabled cluster) |
| Port configuration | 11.3 LTS |
| Known breakage | 15.0 — "some ipywidgets do not work" |

## Browser requirement

> "your browser must be able to access the `databricks-dev-cloudfront.dev.databricks.com` domain"

A corporate firewall/proxy blocking it = widgets silently fail.

## Port configuration

Default comm port **6062**; resolve conflicts (e.g. Datadog) with `spark.databricks.driver.ipykernel.commChannelPort <port-number>`.

> ⚠️ "The Spark config must be set when the cluster is created." It can't be changed on a running cluster.

## ipywidgets vs Databricks widgets

| Capability | ipywidgets | Databricks widgets (`dbutils.widgets`) |
|---|---|---|
| Languages | Python only | Python, Scala, R, SQL |
| UI richness | 30+ control types | 4 types |
| Pass params to jobs | ❌ No | ✅ Yes |
| Pass params between notebooks | ❌ No | ✅ Yes (`%run $X="10"`) |
| Recommended for | Python interactive exploration | Cross-language, job params, dashboard params |

## Code examples

```python
# Interactive histogram with the @interact decorator (auto-creates a slider from the tuple)
import ipywidgets as widgets
from ipywidgets import interact
sparkDF = spark.read.csv("/databricks-datasets/bikeSharing/data-001/day.csv", header="true", inferSchema="true")

@interact(bins=(3, 10))
def plot_histogram(bins):
    pdf = sparkDF.toPandas()
    pdf.hist(column='temp', bins=bins)

# IntSlider — display by returning the widget as the last expression
int_slider = widgets.IntSlider(max=10, value=5)
int_slider

# Button with a Unity Catalog query (DBR 12.1+); Output() captures callback output
button = widgets.Button(description="Load dataframe sample")
output = widgets.Output()
def on_button_clicked(_):
    with output:
        output.clear_output()
        print(spark.sql("SELECT * FROM <catalog>.<schema>.<table> LIMIT 1000").toPandas())
button.on_click(on_button_clicked)
display(button, output)
```

## Third-party widget ecosystem

Databricks provides **best-effort support** for **ipyleaflet** (interactive maps), **bqplot** (2D plotting), and **VegaFusion** (scalable Vega/Altair rendering). Some third-party widgets are explicitly unsupported (no list given).

Related: [[notebook-widgets]], [[notebooks-overview]], [[notebook-dashboards]].
