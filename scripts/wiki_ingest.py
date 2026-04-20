#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import shutil
import sys

from wiki_common import ROOT, SOURCES_DIR, WIKI_DIR, append_log_entry, extract_title, rebuild_index, slugify, suggest_related_pages


def scaffold_page(page_file: pathlib.Path, title: str, source_file: pathlib.Path) -> bool:
    if page_file.exists():
        return False

    related_pages = suggest_related_pages(title)
    relationship_lines = ["- Review and replace these starter links with durable cross-references."]
    if related_pages:
        for related_path in related_pages:
            relationship_lines.append(f"- [{extract_title(related_path)}](./{related_path.name})")
    relationship_lines.append("- [Project Overview](./project-overview.md)")
    relationship_lines.append("- [Open Questions](./open-questions.md)")
    relationships_block = "\n".join(relationship_lines)

    content = f"""# {title}

## Summary

Draft page created by `wiki_ingest.py`. Replace this section with a real synthesis.

## Key Facts

- Source ingested and ready for review.

## Relationships

{relationships_block}

## Source Basis

- `../sources/{source_file.name}`

## Open Issues

- The source has not been summarized yet.
"""
    page_file.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest a raw source into llm-wiki.")
    parser.add_argument("source", help="Path to the raw source file to ingest.")
    parser.add_argument("--title", help="Human-readable title for the wiki page.")
    parser.add_argument("--slug", help="Optional slug override for the wiki page.")
    args = parser.parse_args()

    source_path = pathlib.Path(args.source).expanduser().resolve()
    if not source_path.exists() or not source_path.is_file():
        print(f"error: source file not found: {source_path}", file=sys.stderr)
        return 1

    title = args.title.strip() if args.title else source_path.stem.replace("-", " ").replace("_", " ").title()
    slug = args.slug.strip() if args.slug else slugify(title)
    today = dt.date.today().isoformat()

    source_name = f"{today}-{slug}{source_path.suffix.lower()}"
    dest_source = SOURCES_DIR / source_name
    if dest_source.exists():
        print(f"error: destination source already exists: {dest_source}", file=sys.stderr)
        return 1

    shutil.copy2(source_path, dest_source)

    page_file = WIKI_DIR / f"{slug}.md"
    created_page = scaffold_page(page_file, title, dest_source)
    rebuild_index()
    updated_pages = ["`llm-wiki/wiki/index.md`", f"`{page_file.relative_to(ROOT)}`"]
    follow_up = "Summarize the source, add cross-links, and record any uncertainty in `open-questions.md`."
    append_log_entry(
        "ingest",
        title,
        [
            f"Source file: `{dest_source.relative_to(ROOT)}`",
            f"Pages updated: {', '.join(updated_pages)}",
            f"New pages created: `{page_file.name}`" if created_page else "New pages created: `none`",
            "Key additions: Created or refreshed the target wiki page and rebuilt the wiki catalog.",
            f"Open follow-ups: {follow_up}",
        ],
    )

    print(f"ingested: {dest_source.relative_to(ROOT)}")
    if created_page:
        print(f"draft-page: {page_file.relative_to(ROOT)}")
    else:
        print(f"draft-page-exists: {page_file.relative_to(ROOT)}")
    print("next-step: summarize the source and update related wiki pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
