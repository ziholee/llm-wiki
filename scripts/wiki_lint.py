#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys

from wiki_common import (
    LOG_FILE,
    PAGE_EXCEPTIONS,
    ROOT,
    WIKI_DIR,
    append_log_entry,
    extract_section,
    extract_title,
    iter_wiki_pages,
    knowledge_pages,
    read_text,
    slugify,
    wiki_links_from,
)

REQUIRED_FILES = [
    ROOT / "AGENTS.md",
    ROOT / "llm-wiki" / "README.md",
    ROOT / "llm-wiki" / "inbox" / "README.md",
    ROOT / "llm-wiki" / "queues" / "README.md",
    ROOT / "llm-wiki" / "schema" / "workflow.md",
    ROOT / "llm-wiki" / "schema" / "role-routing.md",
    ROOT / "llm-wiki" / "roles" / "collector.md",
    ROOT / "llm-wiki" / "roles" / "synthesizer.md",
    ROOT / "llm-wiki" / "roles" / "linker.md",
    ROOT / "llm-wiki" / "roles" / "critic.md",
    ROOT / "llm-wiki" / "roles" / "publisher.md",
    WIKI_DIR / "index.md",
    WIKI_DIR / "project-overview.md",
    WIKI_DIR / "log.md",
    WIKI_DIR / "open-questions.md",
]
REQUIRED_SECTIONS = ["## Summary", "## Source Basis"]
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
SOURCE_RE = re.compile(r"`(\.\./sources/[^`]+)`")
LOG_HEADER_RE = re.compile(r"^## \[(\d{4}-\d{2}-\d{2}|YYYY-MM-DD)\] (ingest|query|lint) \| .+")
ASSERTION_RE = re.compile(
    r"\b(is|are|was|were|supports|supported|enables|enabled|requires|required|always|never|best|better|worse|deprecated|current|latest)\b",
    re.IGNORECASE,
)
STALE_RE = re.compile(
    r"\b(currently|today|now|latest|recent|recently|at present|state of the art)\b",
    re.IGNORECASE,
)
CONTRADICTION_SIGNAL_RE = re.compile(
    r"\b(always|never|all|none|required|deprecated|supported|unsupported|enabled|disabled)\b",
    re.IGNORECASE,
)
OPEN_QUESTIONS_HINT_RE = re.compile(r"^\s*-\s*Question:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
STOPWORD_RE = re.compile(r"\b(this|that|these|those|system|feature|page|currently|today|now)\b", re.IGNORECASE)


def lint_required_files(errors: list[str]) -> None:
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")


def lint_page_structure(errors: list[str]) -> None:
    for path in iter_wiki_pages():
        if path.name in PAGE_EXCEPTIONS:
            continue
        text = read_text(path)
        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{path.relative_to(ROOT)} missing section: {section}")
        for match in SOURCE_RE.findall(text):
            target = (path.parent / match).resolve()
            if not target.exists():
                errors.append(f"{path.relative_to(ROOT)} references missing source: {match}")


def lint_links(errors: list[str]) -> None:
    for path in sorted((ROOT / "llm-wiki").rglob("*.md")):
        text = read_text(path)
        for _, target in LINK_RE.findall(text):
            if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
                continue
            clean = target.split("#", 1)[0]
            target_path = (path.parent / clean).resolve()
            if not target_path.exists():
                errors.append(f"{path.relative_to(ROOT)} has broken link: {target}")


def lint_index_catalog(errors: list[str]) -> None:
    index_text = read_text(WIKI_DIR / "index.md")
    for path in iter_wiki_pages():
        if path.name in PAGE_EXCEPTIONS:
            continue
        expected = f"](./{path.name})"
        if expected not in index_text:
            errors.append(f"llm-wiki/wiki/index.md is missing catalog entry for: {path.name}")


def lint_log_format(errors: list[str]) -> None:
    lines = read_text(LOG_FILE).splitlines()
    seen_entry = False
    for line in lines:
        if line.startswith("## ["):
            seen_entry = True
            if not LOG_HEADER_RE.match(line):
                errors.append(f"{LOG_FILE.relative_to(ROOT)} has non-standard entry header: {line}")
    if not seen_entry:
        errors.append(f"{LOG_FILE.relative_to(ROOT)} is missing a parse-friendly entry template")


def lint_orphan_pages(warnings: list[str]) -> None:
    inbound: dict[str, set[str]] = {path.name: set() for path in knowledge_pages()}
    for path in knowledge_pages():
        for target_name in wiki_links_from(path):
            if target_name in inbound:
                inbound[target_name].add(path.name)
    for page_name, referrers in sorted(inbound.items()):
        if not referrers:
            warnings.append(
                f"llm-wiki/wiki/{page_name} has no inbound links from other knowledge pages; only the catalog can currently find it"
            )


def lint_missing_relationships(warnings: list[str]) -> None:
    for path in knowledge_pages():
        text = read_text(path)
        if "## Relationships" not in text:
            warnings.append(f"{path.relative_to(ROOT)} is missing a Relationships section")
            continue
        rel_block = text.split("## Relationships", 1)[1]
        if "## " in rel_block:
            rel_block = rel_block.split("## ", 1)[0]
        if "](" not in rel_block:
            warnings.append(f"{path.relative_to(ROOT)} has an empty Relationships section")


def lint_stale_claims(warnings: list[str]) -> None:
    for path in knowledge_pages():
        summary = extract_section(path, "## Summary")
        source_basis = extract_section(path, "## Source Basis")
        has_single_source = len(SOURCE_RE.findall(source_basis)) <= 1
        for line in summary.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if STALE_RE.search(stripped) and ASSERTION_RE.search(stripped) and has_single_source:
                warnings.append(
                    f"{path.relative_to(ROOT)} contains potentially stale language in Summary with only one cited source: {stripped}"
                )


def lint_missing_concept_pages(warnings: list[str]) -> None:
    known_titles = {extract_title(path).lower() for path in knowledge_pages()}
    open_questions_text = read_text(WIKI_DIR / "open-questions.md")
    tracked_terms = {match.group(1).strip().lower() for match in OPEN_QUESTIONS_HINT_RE.finditer(open_questions_text)}

    candidates: dict[str, set[str]] = {}
    for path in knowledge_pages():
        summary = extract_section(path, "## Summary")
        for raw_match in re.findall(r"\[\[([^\]]+)\]\]", summary):
            concept = raw_match.strip()
            concept_key = concept.lower()
            if concept_key in known_titles or concept_key in tracked_terms:
                continue
            candidates.setdefault(concept, set()).add(path.name)

    for concept, pages in sorted(candidates.items()):
        warnings.append(
            f"Concept page may be missing for '{concept}' mentioned in {', '.join(f'llm-wiki/wiki/{page}' for page in sorted(pages))}"
        )


def lint_possible_contradictions(warnings: list[str]) -> None:
    claim_index: dict[str, list[tuple[str, str]]] = {}
    for path in knowledge_pages():
        summary = extract_section(path, "## Summary")
        sentences = re.split(r"(?<=[.!?])\s+", summary)
        for sentence in sentences:
            stripped = sentence.strip().lstrip("- ").strip()
            if not stripped or not CONTRADICTION_SIGNAL_RE.search(stripped):
                continue
            normalized = re.sub(r"\[\[([^\]]+)\]\]", r"\1", stripped.lower())
            normalized = CONTRADICTION_SIGNAL_RE.sub(" ", normalized)
            normalized = STOPWORD_RE.sub(" ", normalized)
            key = slugify(normalized)
            if len(key) < 12:
                continue
            claim_index.setdefault(key, []).append((path.name, stripped))

    for claim_key, claims in sorted(claim_index.items()):
        unique_lines = {line.lower() for _, line in claims}
        if len(claims) < 2 or len(unique_lines) < 2:
            continue
        positive = any(re.search(r"\b(always|all|required|supported|enabled)\b", line, re.IGNORECASE) for _, line in claims)
        negative = any(re.search(r"\b(never|none|deprecated|unsupported|disabled)\b", line, re.IGNORECASE) for _, line in claims)
        if positive and negative:
            formatted = "; ".join(f"llm-wiki/wiki/{page}: {line}" for page, line in claims[:4])
            warnings.append(f"Potential contradiction across summaries for similar claim '{claim_key}': {formatted}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    lint_required_files(errors)
    lint_page_structure(errors)
    lint_links(errors)
    lint_index_catalog(errors)
    lint_log_format(errors)
    lint_orphan_pages(warnings)
    lint_missing_relationships(warnings)
    lint_stale_claims(warnings)
    lint_missing_concept_pages(warnings)
    lint_possible_contradictions(warnings)

    if errors:
        print("wiki-lint: FAIL")
        for error in errors:
            print(f"- {error}")
        if warnings:
            print("wiki-lint: WARNINGS")
            for warning in warnings:
                print(f"- {warning}")
        append_log_entry(
            "lint",
            "structural check",
            [
                f"Errors: {len(errors)}",
                f"Warnings: {len(warnings)}",
                "Outcome: Lint failed.",
            ],
        )
        return 1

    print("wiki-lint: OK")
    if warnings:
        print("wiki-lint: WARNINGS")
        for warning in warnings:
            print(f"- {warning}")
    append_log_entry(
        "lint",
        "structural check",
        [
            "Errors: 0",
            f"Warnings: {len(warnings)}",
            "Outcome: Lint completed and reported wiki health warnings where relevant.",
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
