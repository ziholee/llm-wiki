#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
INBOX_DIR = ROOT / "llm-wiki" / "inbox"
QUEUES_DIR = ROOT / "llm-wiki" / "queues"
REPORT_FILE = QUEUES_DIR / "dispatch-report.md"
ROLE_ORDER = ["collector", "synthesizer", "linker", "critic", "publisher"]
SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf", ".html", ".csv", ".json"}


def inbox_files() -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for path in sorted(INBOX_DIR.rglob("*")):
        if not path.is_file():
            continue
        if path.name.lower() == "readme.md":
            continue
        files.append(path)
    return files


def choose_roles(path: pathlib.Path) -> list[str]:
    roles = ["collector", "synthesizer", "linker", "critic"]
    name = path.name.lower()
    if any(token in name for token in ["overview", "guide", "faq", "report", "summary"]):
        roles.append("publisher")
    return roles


def next_action(role: str, path: pathlib.Path) -> str:
    rel = path.relative_to(ROOT)
    if role == "collector":
        return f"Review `{rel}` and decide whether to ingest it into `llm-wiki/sources/`."
    if role == "synthesizer":
        return f"Create or update durable wiki pages based on `{rel}`."
    if role == "linker":
        return f"Add links from related pages and update `llm-wiki/wiki/index.md` if needed for `{rel}`."
    if role == "critic":
        return f"Record conflicts, uncertainty, and follow-up questions introduced by `{rel}`."
    if role == "publisher":
        return f"Polish the resulting page set for readability and promote stable summaries derived from `{rel}`."
    return f"Inspect `{rel}`."


def role_header(role: str) -> str:
    titles = {
        "collector": "Collector Queue",
        "synthesizer": "Synthesizer Queue",
        "linker": "Linker Queue",
        "critic": "Critic Queue",
        "publisher": "Publisher Queue",
    }
    return titles[role]


def write_role_queue(role: str, items: list[pathlib.Path]) -> None:
    queue_file = QUEUES_DIR / f"{role}.md"
    lines = [f"# {role_header(role)}", "", f"Updated: {dt.date.today().isoformat()}", ""]
    if not items:
        lines.extend(["No pending items.", ""])
    else:
        for path in items:
            rel = path.relative_to(ROOT)
            lines.extend(
                [
                    f"## {path.name}",
                    "",
                    f"- Inbox file: `{rel}`",
                    f"- Recommended action: {next_action(role, path)}",
                    "",
                ]
            )
    queue_file.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_report(files: list[pathlib.Path], assignments: dict[str, list[pathlib.Path]]) -> None:
    lines = ["# Dispatch Report", "", f"Generated: {dt.date.today().isoformat()}", ""]
    lines.append(f"- Inbox files scanned: {len(files)}")
    for role in ROLE_ORDER:
        lines.append(f"- {role}: {len(assignments[role])} items")
    lines.append("")
    if files:
        lines.append("## Items")
        lines.append("")
        for path in files:
            rel = path.relative_to(ROOT)
            roles = ", ".join(choose_roles(path))
            lines.append(f"- `{rel}` -> {roles}")
        lines.append("")
    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    files = inbox_files()
    assignments = {role: [] for role in ROLE_ORDER}

    for path in files:
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            print(f"skip: unsupported extension for {path.relative_to(ROOT)}")
            continue
        for role in choose_roles(path):
            assignments[role].append(path)

    QUEUES_DIR.mkdir(parents=True, exist_ok=True)
    for role in ROLE_ORDER:
        write_role_queue(role, assignments[role])
    write_report(files, assignments)

    print(f"dispatch-report: {REPORT_FILE.relative_to(ROOT)}")
    for role in ROLE_ORDER:
        queue_file = QUEUES_DIR / f"{role}.md"
        print(f"{role}-queue: {queue_file.relative_to(ROOT)} ({len(assignments[role])} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
