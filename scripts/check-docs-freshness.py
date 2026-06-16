#!/usr/bin/env python3
"""
check-docs-freshness.py

Scan docs/sources/ for Markdown notes with **Source:** and **Source updated:**
metadata. Fetch each live page and compare the "Last updated" date.

Strategy:
  1. Static HTTP fetch (fast, works for plain HTML sites).
  2. Playwright headless browser fallback for JS-rendered pages (e.g. Databricks
     docs). Requires: pip install playwright && playwright install chromium

Usage:
    python scripts/check-docs-freshness.py
    python scripts/check-docs-freshness.py --course databricks-docs
    python scripts/check-docs-freshness.py --skip-fetch

Install Playwright for JS-rendered pages (e.g. Databricks docs):
    pip install playwright && playwright install chromium
"""

import argparse
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

ROOT        = Path(__file__).parent.parent
SOURCES_DIR = ROOT / "docs" / "sources"

# Applied to both raw HTML (static fetch) and rendered text (Playwright).
DATE_PATTERNS = [
    re.compile(r'last[_\-\s]?updated\s+(?:on\s+)?(\w+ \d{1,2},?\s+\d{4})', re.IGNORECASE),
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
    "STALE":          RED,
    "MISSING-DATE":   YELLOW,
    "FETCH-ERROR":    YELLOW,
    "NO-PLAYWRIGHT":  CYAN,
    "UNKNOWN":        DARK,
    "OK":             GREEN,
    "SKIPPED":        DARK,
}


def _parse_date(raw: str) -> str:
    for fmt in ("%b %d, %Y", "%B %d, %Y", "%b %d %Y", "%B %d %Y"):
        try:
            return datetime.strptime(raw.replace(",", ""), fmt.replace(",", "")).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return raw  # already ISO or unparseable


def _search_date(text: str) -> str | None:
    for pat in DATE_PATTERNS:
        m = pat.search(text)
        if m:
            return _parse_date(m.group(1).strip())
    return None


def probe_url(url: str) -> None:
    """Fetch url with Playwright and print body text context for debugging."""
    if not PLAYWRIGHT_AVAILABLE:
        print("Playwright not installed. Run: pip install playwright && playwright install chromium")
        return
    print(f"Probing: {url}\n")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=30_000)
        try:
            page.wait_for_selector("text=Last updated", timeout=8_000)
            print("✓ 'Last updated' selector found\n")
        except Exception:
            print("✗ 'Last updated' selector timed out\n")
        text = page.inner_text("body")
        browser.close()

    # Show context around "updated"
    idx = text.lower().find("updated")
    if idx >= 0:
        snippet = text[max(0, idx - 30): idx + 100]
        print(f"Context around 'updated':\n  {repr(snippet)}\n")
    else:
        print("'updated' not found in body text\n")

    # Show any date-like strings: "Mon DD, YYYY" or "Month DD, YYYY"
    dates = re.findall(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+20\d{2}\b', text)
    print(f"Date-like strings found: {dates or '(none)'}\n")

    # First 500 chars of body
    print("Body text (first 500 chars):")
    print(text[:500])


def get_live_date(url: str) -> str | None:
    """Return ISO date from live page, None if not found, or 'ERROR: ...'."""
    # 1. Static HTTP — fast, works for plain-HTML sites
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        date = _search_date(html)
        if date:
            return date
    except Exception as exc:
        return f"ERROR: {str(exc)[:70]}"

    # 2. Playwright — for JS-rendered pages (e.g. Databricks docs / Next.js)
    if not PLAYWRIGHT_AVAILABLE:
        return None  # caller will set status NO-PLAYWRIGHT
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30_000)
            try:
                page.wait_for_selector("text=Last updated", timeout=8_000)
            except Exception:
                pass  # proceed anyway; date might still be in body text
            text = page.inner_text("body")
            browser.close()
        return _search_date(text)
    except Exception as exc:
        return f"ERROR(pw): {str(exc)[:60]}"


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
        elif live and live.startswith("ERROR"):
            status = "FETCH-ERROR"
        elif live is None and not PLAYWRIGHT_AVAILABLE:
            status = "NO-PLAYWRIGHT"
        elif live is None:
            status = "UNKNOWN"
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
    parser.add_argument("--probe",       metavar="URL", help="Debug: fetch one URL and print body context")
    args = parser.parse_args()

    if args.probe:
        probe_url(args.probe)
        sys.exit(0)

    results = scan(SOURCES_DIR, args.course, args.skip_fetch)
    if not results:
        print("No notes with Source URL metadata found.")
        sys.exit(0)

    print_table(results)
    print()

    stale   = [r for r in results if r["status"] == "STALE"]
    missing = [r for r in results if r["status"] == "MISSING-DATE"]
    errors  = [r for r in results if r["status"] == "FETCH-ERROR"]
    no_pw   = [r for r in results if r["status"] == "NO-PLAYWRIGHT"]
    unknown = [r for r in results if r["status"] == "UNKNOWN"]
    ok      = [r for r in results if r["status"] == "OK"]

    if stale:
        print(f"{RED}=== STALE ({len(stale)}) ==={RESET}")
        for r in stale:
            print(f"  {r['note']}  (captured {r['captured']} → live {r['live']})")
            print(f"  {r['url']}")
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

    if unknown:
        print(f"{DARK}=== Unknown — date not found in rendered page ({len(unknown)}) ==={RESET}")
        for r in unknown:
            print(f"  {r['note']}: {r['url']}")
        print()

    if no_pw:
        print(f"{CYAN}=== Playwright not installed ({len(no_pw)}) ==={RESET}")
        print("  These pages are JS-rendered; static HTTP cannot read their dates.")
        print("  Install Playwright to enable automatic checking:")
        print("    pip install playwright && playwright install chromium")
        print()
        for r in no_pw:
            print(f"  {r['note']} | captured {r['captured']}")
            print(f"  {r['url']}")
        print()

    if ok and not stale and not no_pw and not missing and not unknown:
        print(f"{GREEN}All {len(ok)} pages confirmed up to date.{RESET}")


if __name__ == "__main__":
    main()
