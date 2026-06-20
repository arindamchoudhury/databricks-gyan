# Page map — The Data Intelligence Platform For Dummies (2nd Databricks Special Edition)

Ari Kaplan & Amit Kara, John Wiley & Sons, 2nd Databricks Special Edition (© 2026). Working file — not in nav.

PDF-to-print offset: **+6** (PDF page 7 = printed page 1). Thin marketing/overview booklet; content runs PDF 7–51.

| Chapter | Title | PDF start | PDF end | Printed |
| --- | --- | --- | --- | --- |
| — | Introduction | 7 | 8 | 1–2 |
| 1 | Understanding Data Intelligence | 9 | 18 | 3–12 |
| 2 | Exploring the Lakehouse as the Foundation for Data and AI | 19 | 28 | 13–22 |
| 3 | Getting Started with the Databricks Data Intelligence Platform | 29 | 38 | 23–32 |
| 4 | Building AI Applications on the Databricks Data Intelligence Platform | 39 | 48 | 33–42 |
| 5 | Ten Reasons Why You Need a Data Intelligence Platform | 49 | 51 | 43–45 |

Extract a chapter with:

```bash
pdftotext -f <start> -l <end> -layout \
  "/c/opt/learn/databricks/books/The-Data-Intelligence-Platform-For-Dummies-2nd-Databricks-Special-Edition.pdf" \
  "docs/sources/dip-dummies/pdf-cache/<NN>-<slug>.txt"
```
