"""Validate this small static policy site without third-party dependencies."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://jackiewang1208.github.io"
PREFIX = "/app-policies/"
EMAIL = "wangjackiedev@gmail.com"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.links = []
        self.h1 = 0
        self.lang = None
        self.canonical = None
        self.has_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "title":
            self.has_title = True
        if tag == "h1":
            self.h1 += 1
        if "id" in attrs:
            assert attrs["id"] not in self.ids, (self.path, "duplicate ID")
            self.ids.add(attrs["id"])
        assert tag not in {"script", "iframe", "form"}, (self.path, tag)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if "href" in attrs:
            self.links.append(attrs["href"])


pages = {}
for path in sorted(ROOT.rglob("*.html")):
    source = path.read_text(encoding="utf-8")
    page = Page(path)
    page.feed(source)
    page.close()
    assert source.lower().startswith("<!doctype html>"), path
    assert page.lang and page.h1 == 1 and page.has_title, path
    expected_url = ORIGIN + PREFIX + path.parent.relative_to(ROOT).as_posix().strip(".")
    expected_url = expected_url.rstrip("/") + "/"
    assert page.canonical == expected_url, (path, page.canonical, expected_url)
    assert set(re.findall(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", source)) == {EMAIL}, path
    assert "Jackie Liao" in source, path
    if path != ROOT / "index.html":
        assert "Arrow Trails" in source, path
    assert not re.search(r"\bTODO\b|\bTBD\b|to be supplied|开发者填写", source), path
    pages[path] = page

assert len(pages) == 2, f"Expected neutral home + one English policy page, found {len(pages)}"
for path, page in pages.items():
    for href in page.links:
        url = urlsplit(href)
        if url.scheme == "mailto":
            assert url.path == EMAIL, (path, href)
            continue
        if url.scheme or url.netloc:
            assert url.scheme == "https", (path, href)
            if url.netloc != "jackiewang1208.github.io":
                continue
            assert url.path.startswith(PREFIX), (path, href)
            target = ROOT / unquote(url.path.removeprefix(PREFIX))
        elif url.path:
            target = path.parent / unquote(url.path)
        else:
            target = path
        target = target.resolve()
        assert target.is_relative_to(ROOT), (path, "link outside repo", href)
        if target.is_dir():
            target /= "index.html"
        assert target.is_file(), (path, "broken link", href)
        if target.suffix == ".html":
            if path == ROOT / "index.html":
                assert target == path, (path, "homepage must not list apps", href)
            else:
                app_root = ROOT / path.relative_to(ROOT).parts[0]
                assert target.is_relative_to(app_root), (path, "cross-app or directory link", href)
        if url.fragment:
            assert target in pages and unquote(url.fragment) in pages[target].ids, (path, href)
    print(f"PASS {path.relative_to(ROOT)}: language, metadata, contacts and links")

english = pages[ROOT / "arrow-trails/privacy/index.html"]
assert english.lang == "en", "Arrow Trails policy must be English"
assert not any("/zh/" in href for href in english.links), "Removed Chinese policy is still linked"
assert (ROOT / ".nojekyll").is_file(), "Missing static publishing marker"
print("PASS: 2 static pages; English-only policy; no cross-app links, scripts or forms")
