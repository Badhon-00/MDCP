#!/usr/bin/env python3
"""Static smoke checks for the generated MDCP GitHub Pages site."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if attrs.get("href"):
            self.hrefs.append(attrs["href"])


def main():
    html_path = SITE / "index.html"
    catalog_path = SITE / "catalog.json"
    favicon_path = SITE / "favicon.svg"
    for path in (html_path, catalog_path, favicon_path):
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"missing or empty site asset: {path.relative_to(ROOT)}")

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    skills = catalog.get("skills")
    if not isinstance(skills, list) or not skills:
        raise SystemExit("catalog.skills must be a non-empty list")
    if catalog.get("count") != len(skills):
        raise SystemExit("catalog count does not match the skills array")

    html = html_path.read_text(encoding="utf-8")
    parser = SiteParser()
    parser.feed(html)
    required_ids = {"home", "explorer", "features", "about", "search", "grid", "chips", "count", "results", "menuToggle", "mobileMenu"}
    missing = required_ids - parser.ids
    if missing:
        raise SystemExit("missing required page elements: " + ", ".join(sorted(missing)))

    for href in parser.hrefs:
        if href.startswith("#") and href[1:] not in parser.ids:
            raise SystemExit(f"broken in-page anchor: {href}")

    if 'href="./favicon.svg"' not in html:
        raise SystemExit("custom SVG favicon is not linked")
    if "three.module.js" not in html:
        raise SystemExit("Three.js module is not loaded")
    if "prefers-reduced-motion: reduce" not in html:
        raise SystemExit("reduced-motion preference is not respected")
    if not re.search(r"@media\s*\(max-width", html):
        raise SystemExit("responsive media queries are missing")
    if re.search(r"[\U0001F300-\U0001FAFF]", html):
        raise SystemExit("emoji found in site source; use SVG iconography instead")

    print(f"Site smoke test passed: {len(skills)} skills, {len(parser.ids)} element IDs, favicon and Three.js assets present.")


if __name__ == "__main__":
    main()
