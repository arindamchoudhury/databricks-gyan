"""
embed_images.py — Download images from cache files and embed them in source notes.

For each slug, reads the === Images === section from the cache file, downloads
images to docs/sources/databricks-docs/assets/{slug}/, then appends an Images
section to the corresponding source note (if one isn't already present).
"""

import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).parent.parent
CACHE_DIR = REPO / "cache" / "web"
NOTES_DIR = REPO / "docs" / "sources" / "databricks-docs"
ASSETS_DIR = NOTES_DIR / "assets"

SLUGS_WITH_IMAGES = [
    "notebook-debugger",
    "serverless-notebooks",
    "serverless-jobs",
    "classic-compute-configure",
    "compute-pools",
    "lakeguard",
    "notebooks-overview",
    "notebook-dashboards",
    "notebook-widgets",
    "notebook-workflows",
    "notebook-share-code",
    "spark-ui-guide",
    "optimize-data-workloads-guide",
    "failing-spark-jobs",
    "long-spark-stage",
    "long-spark-stage-page",
    "long-spark-stage-io",
    "slow-spark-stage-low-io",
    "spark-rewriting-data",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    ),
    "Referer": "https://docs.databricks.com/",
}


def parse_images_from_cache(cache_file: Path) -> list[dict]:
    """Extract image entries from the === Images === section of a cache file."""
    text = cache_file.read_text(encoding="utf-8")
    idx = text.find("\n=== Images ===")
    if idx == -1:
        return []
    section = text[idx:]
    results = []
    for line in section.splitlines():
        m = re.match(r"^!\[\]\((.+?)\)$", line)
        if m:
            url = m.group(1)
            results.append({"url": url, "alt": "", "caption": ""})
        elif line.startswith("*") and results:
            # Caption line: *alt (WxH)*
            cap = line.strip("* \n")
            results[-1]["caption"] = cap
            m2 = re.match(r"^(.+?)\s+\(\d+×\d+\)$", cap)
            results[-1]["alt"] = m2.group(1) if m2 else cap
    return results


def download_image(url: str, dest: Path) -> bool:
    if dest.exists():
        print(f"  skip (exists): {dest.name}")
        return True
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            dest.write_bytes(resp.read())
        print(f"  downloaded: {dest.name}")
        return True
    except Exception as e:
        print(f"  FAIL {url}: {e}", file=sys.stderr)
        return False


def note_has_images_section(note_text: str) -> bool:
    return "## Images" in note_text or "=== Images ===" in note_text


def process_slug(slug: str) -> None:
    cache_file = CACHE_DIR / f"{slug}.txt"
    note_file = NOTES_DIR / f"{slug}.md"

    if not cache_file.exists():
        print(f"[{slug}] no cache file — skip")
        return
    if not note_file.exists():
        print(f"[{slug}] no note file — skip")
        return

    images = parse_images_from_cache(cache_file)
    if not images:
        print(f"[{slug}] no images in cache")
        return

    note_text = note_file.read_text(encoding="utf-8")
    if note_has_images_section(note_text):
        print(f"[{slug}] images section already present — skip")
        return

    print(f"[{slug}] {len(images)} image(s) to embed")

    asset_dir = ASSETS_DIR / slug
    asset_dir.mkdir(parents=True, exist_ok=True)

    lines = ["\n\n## Images\n"]
    for i, img in enumerate(images, 1):
        # Derive a local filename from URL
        url_path = img["url"].split("?")[0]
        ext = Path(url_path).suffix or ".png"
        local_name = f"{i:02d}{ext}"
        local_path = asset_dir / local_name
        rel_path = f"assets/{slug}/{local_name}"

        ok = download_image(img["url"], local_path)
        if not ok:
            continue

        alt = img["alt"] or f"diagram {i}"
        cap = img["caption"]
        lines.append(f"[![{alt}]({rel_path})]({rel_path})")
        if cap:
            lines.append(f"*{cap}*\n")

    if len(lines) <= 1:
        print(f"[{slug}] all downloads failed — note not updated")
        return

    note_file.write_text(note_text.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print(f"[{slug}] note updated")


def main():
    slugs = sys.argv[1:] if len(sys.argv) > 1 else SLUGS_WITH_IMAGES
    for slug in slugs:
        process_slug(slug)


if __name__ == "__main__":
    main()
