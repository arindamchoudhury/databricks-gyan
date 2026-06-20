# Page map — The Data Lakehouse For Dummies (2nd Databricks Special Edition)

Ari Kaplan & Amit Kara, John Wiley & Sons, 2nd Databricks Special Edition (© 2026). Working file — not in nav.

PDF-to-print offset: **+5** (PDF page 8 = printed page 3). Thin marketing/overview booklet; content runs PDF 6–34 (Introduction PDF 6–7, chapters PDF 8–34).

| Chapter | Title | PDF start | PDF end | Printed |
| --- | --- | --- | --- | --- |
| — | Introduction | 6 | 7 | 1–2 |
| 1 | Making the Case for Data Lakehouses | 8 | 13 | 3–8 |
| 2 | Explaining Data Lakehouses | 14 | 19 | 9–14 |
| 3 | Understanding the Underlying Technology | 20 | 25 | 15–20 |
| 4 | Bringing Data Intelligence to the Data Lakehouse | 26 | 31 | 21–26 |
| 5 | Ten Reasons Why You Need a Data Lakehouse | 32 | 34 | 27–29 |

Extract a chapter with:

```bash
pdftotext -f <start> -l <end> -layout \
  "/c/opt/learn/databricks/books/the-data-lakehouse-dummies-2nd-databricksse.pdf" \
  "docs/sources/lakehouse-dummies/pdf-cache/<NN>-<slug>.txt"
```
