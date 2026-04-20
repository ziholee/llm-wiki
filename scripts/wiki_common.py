#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
LLM_WIKI_DIR = ROOT / "llm-wiki"
SOURCES_DIR = LLM_WIKI_DIR / "sources"
WIKI_DIR = LLM_WIKI_DIR / "wiki"
INDEX_FILE = WIKI_DIR / "index.md"
LOG_FILE = WIKI_DIR / "log.md"
CORE_PAGE_ORDER = ["project-overview.md", "log.md", "open-questions.md"]
PAGE_EXCEPTIONS = {"index.md", "log.md", "open-questions.md"}
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "source"


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_section(path: pathlib.Path, heading: str) -> str:
    lines = read_text(path).splitlines()
    collected: list[str] = []
    in_section = False
    for line in lines:
        if line.startswith("## "):
            if in_section:
                break
            in_section = line.strip() == heading
            continue
        if in_section:
            collected.append(line)
    return "\n".join(collected).strip()


def extract_title(path: pathlib.Path) -> str:
    lines = read_text(path).splitlines()
    if lines and lines[0].startswith("# "):
        return lines[0][2:].strip()
    return path.stem.replace("-", " ").title()


def extract_summary(path: pathlib.Path) -> str:
    summary = "Summary not available yet."
    lines = read_text(path).splitlines()
    in_summary = False
    summary_lines: list[str] = []
    for line in lines[1:]:
        if line.startswith("## "):
            if in_summary:
                break
            in_summary = line.strip() == "## Summary"
            continue
        if not in_summary:
            continue
        stripped = line.strip()
        if stripped:
            summary_lines.append(stripped.lstrip("- ").strip())
        elif summary_lines:
            break
    if summary_lines:
        summary = " ".join(summary_lines)
    return summary


def iter_wiki_pages() -> list[pathlib.Path]:
    return sorted(path for path in WIKI_DIR.glob("*.md"))


def knowledge_pages() -> list[pathlib.Path]:
    return [path for path in iter_wiki_pages() if path.name not in PAGE_EXCEPTIONS and path.name not in CORE_PAGE_ORDER]


def wiki_links_from(path: pathlib.Path) -> set[str]:
    text = read_text(path)
    links: set[str] = set()
    for _, target in LINK_RE.findall(text):
        if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
            continue
        clean = target.split("#", 1)[0]
        target_path = (path.parent / clean).resolve()
        if target_path.is_file() and target_path.parent == WIKI_DIR.resolve():
            links.add(target_path.name)
    return links


def rebuild_index() -> None:
    pages = [path for path in iter_wiki_pages() if path.name != "index.md"]
    core_pages = [WIKI_DIR / name for name in CORE_PAGE_ORDER if (WIKI_DIR / name).exists()]
    topic_pages = [path for path in pages if path.name not in CORE_PAGE_ORDER and path.name not in PAGE_EXCEPTIONS]

    lines = [
        "# Wiki Index",
        "",
        "## Purpose",
        "",
        "This catalog is the first place to look when navigating the maintained knowledge layer.",
        "",
        "## Core Pages",
        "",
    ]
    for path in core_pages:
        lines.append(f"- [{extract_title(path)}](./{path.name}): {extract_summary(path)}")

    lines.extend(["", "## Knowledge Pages", ""])
    if topic_pages:
        for path in topic_pages:
            lines.append(f"- [{extract_title(path)}](./{path.name}): {extract_summary(path)}")
    else:
        lines.append("- No synthesized topic or entity pages have been filed yet.")

    lines.extend(
        [
            "",
            "## Conventions",
            "",
            "- List each maintained page with a short summary.",
            "- Prefer updating an existing page over creating duplicates.",
            "- Add links between related concepts as the wiki grows.",
            "- Keep claims traceable back to files in `../sources/`.",
            "",
        ]
    )
    INDEX_FILE.write_text("\n".join(lines), encoding="utf-8")


def append_log_entry(action: str, subject: str, bullets: list[str]) -> None:
    today = dt.date.today().isoformat()
    entry_lines = [f"## [{today}] {action} | {subject}", ""]
    entry_lines.extend([f"- {bullet}" for bullet in bullets])
    entry_lines.append("")
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(entry_lines))


def title_to_filename_map() -> dict[str, pathlib.Path]:
    mapping: dict[str, pathlib.Path] = {}
    for path in knowledge_pages():
        mapping[extract_title(path).lower()] = path
    return mapping


def suggest_related_pages(title: str, limit: int = 3) -> list[pathlib.Path]:
    title_tokens = {token for token in slugify(title).split("-") if len(token) > 2}
    scored: list[tuple[int, pathlib.Path]] = []
    for path in knowledge_pages():
        candidate_tokens = {token for token in slugify(extract_title(path)).split("-") if len(token) > 2}
        overlap = title_tokens & candidate_tokens
        if overlap:
            scored.append((len(overlap), path))
    scored.sort(key=lambda item: (-item[0], item[1].name))
    return [path for _, path in scored[:limit]]
