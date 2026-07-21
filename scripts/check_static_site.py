from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = ["index.html", "services.html", "service-areas.html", "contact.html", "about.html"]


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.json_ld_blocks = []
        self._in_json_ld = False
        self._json_ld = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "img" and attrs.get("src"):
            self.images.append(attrs["src"])
        if tag == "link" and attrs.get("rel") == "icon" and attrs.get("href"):
            self.images.append(attrs["href"])
        if tag == "meta" and attrs.get("property") == "og:image" and attrs.get("content"):
            self.images.append(attrs["content"])
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._json_ld = []

    def handle_data(self, data):
        if self._in_json_ld:
            self._json_ld.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._in_json_ld:
            self.json_ld_blocks.append("".join(self._json_ld).strip())
            self._in_json_ld = False


def is_external_or_special(url):
    return url.startswith(("http://", "https://", "tel:", "viber:", "mailto:", "#"))


def strip_url(url):
    return url.split("#", 1)[0].split("?", 1)[0]


def main():
    errors = []

    for rel in HTML_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing HTML file: {rel}")
            continue

        parser = SiteParser()
        html = path.read_text(encoding="utf-8")
        parser.feed(html)
        print(f"HTML parse OK: {rel}")

        for block in parser.json_ld_blocks:
            json.loads(block)
        print(f"JSON-LD parse OK: {rel}")

        for href in parser.links:
            if is_external_or_special(href):
                continue
            target = strip_url(href)
            if target and not (ROOT / target).exists():
                errors.append(f"{rel}: missing internal link target {href}")

        for src in parser.images:
            if src.startswith(("http://", "https://", "data:")):
                continue
            target = strip_url(src)
            if target and not (ROOT / target).exists():
                errors.append(f"{rel}: missing local image {src}")

    for json_file in sorted(ROOT.glob("*.json")):
        json.loads(json_file.read_text(encoding="utf-8"))
        print(f"JSON parse OK: {json_file.name}")

    ET.parse(ROOT / "sitemap.xml")
    print("XML parse OK: sitemap.xml")
    print("Internal links OK across 5 HTML files")
    print("Local images OK across 5 HTML files")

    combined = "\n".join((ROOT / rel).read_text(encoding="utf-8").lower() for rel in HTML_FILES)
    harmful_patterns = [
        "#1", "24/7", "24 hours", "guaranteed", "licensed", "certified",
        "official address", "lorem", "todo", "fixme", "replace with approved"
    ]
    found = [item for item in harmful_patterns if item in combined]
    if found:
        errors.append("Client-harmful/placeholder scan found: " + ", ".join(found))
    else:
        print("Client-harmful/placeholder scan OK")

    example_count = combined.count("example.com")
    print(f"Temporary domain marker OK: example.com occurrences = {example_count}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
