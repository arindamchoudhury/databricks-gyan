# Databricks Data Engineering — Learning Notes

Personal notes site for learning Databricks Data Engineering.

## Run the site

```bash
docker compose up    # http://localhost:8000
```

## Skills

| Command | What it does |
|---|---|
| `/databricks-release-notes` | Fetch new Databricks release notes, update `docs/release-notes/`, flag learning path changes |
| `/databricks-book` | Write a book chapter after finishing a topic (e.g. "I finished B1") |

## Structure

```
docs/
  learning-path.md     # 27-topic learning path with study resources
  book/                # one chapter per completed topic
  release-notes/       # platform, runtime, Lakeflow, SQL, DABs, serverless notes
  reference/           # glossary, resources
```
