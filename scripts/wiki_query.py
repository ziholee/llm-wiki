#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import re
import sys

from wiki_common import INDEX_FILE, ROOT, append_log_entry, extract_summary, extract_title, knowledge_pages, read_text

SEARCH_DIRS = [
    ROOT / "llm-wiki" / "wiki",
    ROOT / "llm-wiki" / "sources",
    ROOT / "llm-wiki" / "schema",
    ROOT / "llm-wiki" / "roles",
    ROOT / "llm-wiki" / "queues",
    ROOT / "llm-wiki" / "inbox",
]


def load_index_catalog() -> dict[str, tuple[str, str]]:
    catalog: dict[str, tuple[str, str]] = {}
    for path in knowledge_pages():
        catalog[path.name] = (extract_title(path), extract_summary(path))
    return catalog


def score_wiki_page(query: str, path: pathlib.Path, catalog: dict[str, tuple[str, str]]) -> tuple[int, list[str]]:
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    reasons: list[str] = []
    score = 0
    title, summary = catalog.get(path.name, (extract_title(path), extract_summary(path)))
    if pattern.search(title):
        score += 6
        reasons.append("title match")
    if pattern.search(summary):
        score += 4
        reasons.append("index summary match")
    text = read_text(path)
    hits = len(pattern.findall(text))
    if hits:
        score += min(hits, 5)
        reasons.append(f"{hits} content hits")
    return score, reasons


def collect_matches(query: str):
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    matches = []
    for directory in SEARCH_DIRS:
        for path in sorted(directory.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines()
            hits = []
            for index, line in enumerate(lines, start=1):
                if pattern.search(line):
                    hits.append((index, line.strip()))
            if hits:
                matches.append((path, hits))
    return matches


def recommended_pages(query: str, matches, catalog: dict[str, tuple[str, str]]) -> list[tuple[pathlib.Path, int, list[str]]]:
    wiki_match_paths = {path.name for path, _ in matches if path.parent == ROOT / "llm-wiki" / "wiki"}
    scored: list[tuple[pathlib.Path, int, list[str]]] = []
    for path in knowledge_pages():
        score, reasons = score_wiki_page(query, path, catalog)
        if path.name in wiki_match_paths:
            score += 2
            reasons.append("direct wiki match")
        if score > 0:
            scored.append((path, score, reasons))
    scored.sort(key=lambda item: (-item[1], item[0].name))
    return scored[:5]


def main() -> int:
    parser = argparse.ArgumentParser(description="Query the llm-wiki markdown files.")
    parser.add_argument("query", help="Text to search for in wiki markdown files.")
    args = parser.parse_args()

    query = args.query.strip()
    if not query:
        print("error: query must not be empty", file=sys.stderr)
        return 1

    matches = collect_matches(query)
    catalog = load_index_catalog()
    if not matches:
        print(f"no matches for: {query}")
        append_log_entry(
            "query",
            query,
            [
                "Index used: `llm-wiki/wiki/index.md`",
                "Recommended pages: `none`",
                "Files matched: 0",
                "Outcome: No matches found.",
            ],
        )
        return 0

    recommendations = recommended_pages(query, matches, catalog)
    print(f"query: {query}")
    print(f"index: {INDEX_FILE.relative_to(ROOT)}")
    print(f"files-matched: {len(matches)}")
    if recommendations:
        print("\n## Recommended Wiki Pages")
        for path, score, reasons in recommendations:
            title, summary = catalog.get(path.name, (extract_title(path), extract_summary(path)))
            print(f"- {title} ({path.relative_to(ROOT)})")
            print(f"  score={score}; reasons={', '.join(reasons)}")
            print(f"  summary: {summary}")
    for path, hits in matches:
        print(f"\n## {path.relative_to(ROOT)}")
        for line_no, line in hits[:5]:
            print(f"{line_no}: {line}")
        if len(hits) > 5:
            print(f"... {len(hits) - 5} more matches")

    append_log_entry(
        "query",
        query,
        [
            "Index used: `llm-wiki/wiki/index.md`",
            f"Recommended pages: {', '.join(f'`{path.relative_to(ROOT)}`' for path, _, _ in recommendations) if recommendations else '`none`'}",
            f"Files matched: {len(matches)}",
            "Outcome: Printed prioritized wiki pages followed by raw text matches.",
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
