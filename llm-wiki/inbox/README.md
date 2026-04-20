# Inbox

Drop new materials here when you want the role-based workflow to pick them up.

## How To Use

1. Put raw files into this folder.
2. Run `make wiki-dispatch`.
3. Read the generated files in `llm-wiki/queues/`.
4. Execute the suggested role workflow.

If you are new:

1. Start with `llm-wiki/queues/dispatch-report.md`.
2. Then open `llm-wiki/queues/collector.md`.
3. Use `collector.md` to decide whether each file belongs in `llm-wiki/sources/`.

## Suggestions

- Use descriptive filenames.
- Keep one source per file.
- Prefer original documents over hand-edited excerpts.
- Supported draft extensions: `.md`, `.txt`, `.pdf`, `.html`, `.csv`, `.json`

## Typical Pattern

- Put a source in `llm-wiki/inbox/`.
- Let `collector` review and ingest it.
- Let `synthesizer` convert it into durable wiki knowledge.
- Let `linker` connect it to existing pages.
- Let `critic` capture uncertainty and conflicts.
- Let `publisher` refine stable summary pages when needed.

Expected result after dispatch:

- `dispatch-report.md` tells you how many files were routed to each role.
- each role file lists the next action in plain language.
