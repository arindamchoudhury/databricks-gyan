#!/usr/bin/env python3
"""
check-docs-freshness.py

Scan docs/sources/ for Markdown notes with **Source:** and **Source updated:**
metadata. Fetch each live page (static HTTP) and try to extract the current
"Last updated" date. Report STALE / OK / NEEDS-CLAUDE.

JavaScript-rendered pages (e.g. Databricks docs) will show NEEDS-CLAUDE —
static HTTP cannot execute JS. Those entries print a ready-to-paste Claude prompt.

Usage:
    python scripts/check-docs-freshness.py
    python scripts/check-docs-freshness.py --course databricks-docs
    python scripts/check-docs-freshness.py --skip-fetch
"""

import argparse
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

ROOT        = Path(__file__).parent.parent
SOURCES_DIR = ROOT / "docs" / "sources"

# Patterns tried against raw (static) HTML.
# Databricks docs are Next.js-rendered; "Last updated" is injected by JS and
# will not be found here — those notes surface as NEEDS-CLAUDE.
DATE_PATTERNS = [
    re.compile(r'last[_\-\s]?updated[\s"=>:]+(\w+ \d{1,2},?\s+\d{4})', re.IGNORECASE),
    re.compile(r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})',             re.IGNORECASE),
    re.compile(r'article:modified_time[^>]+content="(\d{4}-\d{2}-\d{2})"', re.IGNORECASE),
    re.compile(r'data-last-updated="(\d{4}-\d{2}-\d{2})"',               re.IGNORECASE),
]

URL_RE      = re.compile(r'\*\*Source:\*\*\s*\[[^\]]*\]\((https?://[^)]+)\)')
CAPTURED_RE = re.compile(r'\*\*Source updated:\*\*\s*(\d{4}-\d{2}-\d{2})')

SKIP_NAMES  = {"index.md", "page-map.md"}

RED    = "\033[31m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
GREEN  = "\033[32m"
DARK   = "\033[90m"
RESET  = "\033[0m"

STATUS_COLOR = {
    "STALE":        RED,
    "MISSING-DATE": YELLOW,
    "FETCH-ERROR":  YELLOW,
    "NEEDS-CLAUDE": CYAN,
    "OK":           GREEN,
    "SKIPPED":      DARK,
}


def _parse_date(raw: str) -> str:
    for fmt in ("%b %d, %Y", "%B %d, %Y", "%b %d %Y", "%B %d %Y"):
        try:
            return datetime.strptime(raw.replace(",", ""), fmt.replace(",", "")).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return raw  # already ISO or unparseable


def get_live_date(url: str) -> str | None:
    """Fetch page; return normalised date string, None (not found), or 'ERROR: ...'."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as exc:
        return f"ERROR: {str(exc)[:70]}"

    for pat in DATE_PATTERNS:
        m = pat.search(html)
        if m:
            return _parse_date(m.group(1).strip())

    return None  # date not in static HTML (JS-rendered)


def scan(sources_dir: Path, course: str, skip_fetch: bool) -> list[dict]:
    search_root = sources_dir / course if course else sources_dir
    if not search_root.exists():
        print(f"ERROR: directory not found: {search_root}", file=sys.stderr)
        sys.exit(1)

    files = sorted(f for f in search_root.rglob("*.md") if f.name not in SKIP_NAMES)

    results = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")

        url_m  = URL_RE.search(text)
        date_m = CAPTURED_RE.search(text)
        url      = url_m.group(1)  if url_m  else None
        captured = date_m.group(1) if date_m else None

        if not url:
            continue  # not a source note with a URL

        live = get_live_date(url) if not skip_fetch else None

        if not captured:
            status = "MISSING-DATE"
        elif skip_fetch:
            status = "SKIPPED"
        elif live and live.startswith("ERROR:"):
            status = "FETCH-ERROR"
        elif live is None:
            status = "NEEDS-CLAUDE"
        elif captured == live:
            status = "OK"
        else:
            status = "STALE"

        results.append({
            "note":     f.name,
            "captured": captured or "(none)",
            "live":     live or "-",
            "status":   status,
            "url":      url,
        })

    return results


def print_table(results: list[dict]) -> None:
    cols   = ["note", "captured", "live", "status"]
    widths = {c: max(len(c), max(len(r[c]) for r in results)) for c in cols}
    header = "  ".join(c.upper().ljust(widths[c]) for c in cols)
    print(header)
    print("-" * len(header))
    for r in results:
        color = STATUS_COLOR.get(r["status"], "")
        row   = "  ".join(r[c].ljust(widths[c]) for c in cols)
        print(f"{color}{row}{RESET}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--course",      default="", help="Course folder to scan (default: all)")
    parser.add_argument("--skip-fetch",  action="store_true", help="Skip HTTP; report metadata only")
    args = parser.parse_args()

    results = scan(SOURCES_DIR, args.course, args.skip_fetch)
    if not results:
        print("No notes with Source URL metadata found.")
        sys.exit(0)

    print_table(results)
    print()

    stale   = [r for r in results if r["status"] == "STALE"]
    missing = [r for r in results if r["status"] == "MISSING-DATE"]
    errors  = [r for r in results if r["status"] == "FETCH-ERROR"]
    needs   = [r for r in results if r["status"] == "NEEDS-CLAUDE"]
    ok      = [r for r in results if r["status"] == "OK"]

    if stale:
        print(f"{RED}=== STALE ({len(stale)}) ==={RESET}")
        for r in stale:
            print(f"  {r['note']}")
            print(f"    Captured: {r['captured']}  |  Live: {r['live']}")
            print(f"    {r['url']}")
        print()

    if missing:
        print(f"{YELLOW}=== Missing 'Source updated' field ({len(missing)}) ==={RESET}")
        for r in missing:
            print(f"  {r['note']}")
            if r["live"] != "-":
                print(f"    Live date: {r['live']} — add to note metadata")
            print(f"    {r['url']}")
        print()

    if errors:
        print(f"{YELLOW}=== Fetch errors ({len(errors)}) ==={RESET}")
        for r in errors:
            print(f"  {r['note']}: {r['live']}")
        print()

    if needs:
        print(f"{CYAN}=== Needs Claude verification ({len(needs)}) ==={RESET}")
        print("  Page date is JavaScript-rendered — not in static HTML.")
        print()
        print("  Paste into Claude Code:")
        print("  " + "-" * 55)
        print("  For each URL below, fetch the live page and extract the")
        print("  'Last updated' date. Compare it to the captured date and")
        print("  report which notes are stale.")
        print()
        for r in needs:
            print(f"  Note: {r['note']} | captured {r['captured']}")
            print(f"  URL:  {r['url']}")
            print()
        print("  " + "-" * 55)
        print()

    if ok and not stale and not needs and not missing:
        print(f"{GREEN}All {len(ok)} pages confirmed up to date.{RESET}")


if __name__ == "__main__":
    main()
