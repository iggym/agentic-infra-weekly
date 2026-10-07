#!/usr/bin/env python3
"""Validate metadata.json against the articles/ directory.

Errors fail the run; warnings are printed but don't. Run from the repo root:
    python3 scripts/validate.py
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ("week", "date", "filename", "title", "topic", "bold_reframe", "research_window")
TOPICS = {
    "AI Platform Architecture",
    "AI Systems Engineering",
    "Observability",
    "Security & Governance",
    "Kubernetes & DevOps",
    "Platform Standardization",
    "Developer Enablement",
}
MIN_DATE, MAX_DATE = date(2026, 1, 1), date(2027, 12, 31)

errors, warnings = [], []


def check_metadata():
    try:
        entries = json.loads((ROOT / "metadata.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"metadata.json: cannot parse ({exc})")
        return []
    if not isinstance(entries, list):
        errors.append("metadata.json: top level must be an array")
        return []

    seen_files, seen_titles = set(), set()
    for i, e in enumerate(entries):
        where = f"metadata.json[{i}]"
        if not isinstance(e, dict):
            errors.append(f"{where}: entry must be an object")
            continue
        where += f" ({e.get('filename', '?')})"
        for key in REQUIRED:
            if key not in e or e[key] in ("", None):
                errors.append(f"{where}: missing '{key}'")
        if not isinstance(e.get("week"), int) or isinstance(e.get("week"), bool):
            errors.append(f"{where}: 'week' must be an integer, got {e.get('week')!r}")
        try:
            d = date.fromisoformat(str(e.get("date")))
            if not MIN_DATE <= d <= MAX_DATE:
                errors.append(f"{where}: date {d} outside {MIN_DATE}..{MAX_DATE}")
        except ValueError:
            errors.append(f"{where}: date {e.get('date')!r} is not YYYY-MM-DD")
        if e.get("topic") not in TOPICS:
            errors.append(f"{where}: topic {e.get('topic')!r} is not canonical")
        fn = e.get("filename", "")
        if not re.fullmatch(r"articles/[a-z0-9][a-z0-9-]*\.html", fn):
            errors.append(f"{where}: filename must look like articles/<slug>.html")
        elif not (ROOT / fn).is_file():
            errors.append(f"{where}: file does not exist")
        if fn in seen_files:
            errors.append(f"{where}: duplicate filename")
        seen_files.add(fn)
        title = (e.get("title") or "").strip().lower()
        if title in seen_titles:
            errors.append(f"{where}: duplicate title {e.get('title')!r}")
        seen_titles.add(title)

    for path in sorted((ROOT / "articles").glob("*.html")):
        rel = f"articles/{path.name}"
        if rel not in seen_files:
            errors.append(f"{rel}: orphan article (not listed in metadata.json)")
    return entries


def check_articles(entries):
    for e in entries:
        path = ROOT / str(e.get("filename", ""))
        if not path.is_file():
            continue
        html = path.read_text(encoding="utf-8")
        rel = e["filename"]
        if not re.search(r"<title>\s*\S", html):
            errors.append(f"{rel}: missing <title>")
        if re.search(r'href="/"', html):
            errors.append(f'{rel}: uses href="/" (breaks on GitHub Pages; use ../index.html)')
        if 'name="description"' not in html:
            warnings.append(f"{rel}: no <meta name=\"description\">")
        if 'rel="canonical"' not in html:
            warnings.append(f"{rel}: no canonical link")


def main():
    check_articles(check_metadata())
    for w in warnings:
        print(f"warning: {w}")
    for err in errors:
        print(f"error: {err}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
