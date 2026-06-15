# Page map — Databricks Certified Data Engineer Associate Study Guide

Derar Alhussein, O'Reilly, 1st Edition (February 2025). Working file — not in nav.

Reflowable O'Reilly ebook PDF (small pages, ~13 lines each). PDF page numbers only; no stable printed page offset.

| Chapter | Title | PDF start | PDF end |
| --- | --- | --- | --- |
| 1 | Getting Started with Databricks | 20 | 113 |
| 2 | Managing Data with Delta Lake | 114 | 168 |
| 3 | Mastering Relational Entities | 169 | 230 |
| 4 | Transforming Data with Spark | 231 | 314 |
| 5 | Processing Incremental Data | 315 | 398 |
| 6 | Building Production Pipelines | 399 | 504 |
| 7 | Exploring Databricks SQL | 505 | 552 |
| 8 | Implementing Data Governance (Unity Catalog) | 553 | 636 |
| 9 | Certification Overview | 637 | end |

Extract a chapter with:

```bash
pdftotext -f <start> -l <end> -layout "/c/opt/learn/databricks/books/DCDE-SG.pdf" \
  "docs/sources/dcde-sg/pdf-cache/<NN>-<slug>.txt"
```
