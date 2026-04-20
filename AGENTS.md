# AGENTS.md

This repository uses an `llm-wiki` workflow.

## Mission

Maintain a persistent markdown knowledge base that compounds over time.

- Raw inputs live in `llm-wiki/sources/`.
- Synthesized knowledge lives in `llm-wiki/wiki/`.
- Reusable templates and rules live in `llm-wiki/schema/`.

## Operating Model

When new information arrives:

1. Save the original material in `llm-wiki/sources/`.
2. Read the existing wiki before writing anything new.
3. Update the smallest number of pages necessary to integrate the new facts.
4. Prefer revising durable concept pages over creating one-off summaries.
5. Log the ingestion in `llm-wiki/wiki/log.md`.
6. Add uncertainty to `llm-wiki/wiki/open-questions.md` instead of hiding it.

If materials are dropped into `llm-wiki/inbox/` first:

1. Run `make wiki-dispatch`.
2. Read the generated queues in `llm-wiki/queues/`.
3. Execute work in this default order: `collector -> synthesizer -> linker -> critic -> publisher`.

## Source Handling Rules

- Treat files in `llm-wiki/sources/` as immutable.
- Never overwrite or silently rewrite raw source documents.
- Every non-trivial claim in the wiki should be traceable to one or more source files.
- If two sources conflict, record the conflict explicitly.

## Writing Rules

- Write in markdown.
- Prefer short, durable pages with stable titles.
- Link related pages whenever a connection is useful.
- Avoid duplicate pages that differ only by wording.
- When a page grows too broad, split it into focused pages and leave links behind.

## Role Model

The repository uses five default roles:

- `collector`: preserves worthy raw material and starts ingest.
- `synthesizer`: turns source material into durable wiki content.
- `linker`: connects new pages to existing navigation and related concepts.
- `critic`: records uncertainty, conflicts, and open questions.
- `publisher`: polishes stable summaries for human readability.

## Page Types

Use these page shapes by default:

- `project-overview.md` for the high-level summary of the repository knowledge state.
- Topic pages for concepts, systems, or recurring themes.
- Entity pages for named people, tools, organizations, datasets, or components.
- `open-questions.md` for unresolved ambiguity.
- `log.md` for chronological operational history.

## Update Standard

Each ingestion should aim to leave the wiki in a better state than before:

- more connected,
- less redundant,
- more explicit about uncertainty,
- and easier to navigate.

## Task Expectations

For non-trivial work:

1. Record the plan in `tasks/todo.md`.
2. Mark progress as work advances.
3. Add a short review note before finishing.
4. If the user corrects a mistake, capture the lesson in `tasks/lessons.md`.
