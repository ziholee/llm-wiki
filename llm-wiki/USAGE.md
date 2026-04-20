# Usage Guide

This is the single starting point for using the `llm-wiki` workflow in this repository.

## Before You Start

- Run commands from the repository root.
- Use absolute paths for `SRC=...` when running `make wiki-ingest`.
- Treat `llm-wiki/sources/` as immutable after ingest.
- If you are unsure where to begin, start with the `Fast Start` section below.

## What Goes Where

- `llm-wiki/inbox/`: drop new materials here first
- `llm-wiki/sources/`: immutable raw sources that have been accepted
- `llm-wiki/wiki/`: maintained knowledge pages
- `llm-wiki/queues/`: generated role-based task queues
- `llm-wiki/roles/`: role definitions
- `llm-wiki/schema/`: workflow rules and templates

## Fast Start

If you only want one recommended beginner path, use this:

1. Put one file into `llm-wiki/inbox/`.
2. Run `make wiki-dispatch`.
3. Open `llm-wiki/queues/collector.md`.
4. Decide whether the file belongs in `llm-wiki/sources/`.
5. If yes, run `make wiki-ingest SRC=/absolute/path/to/file.md TITLE="Readable Title"`.
6. Open the created draft page in `llm-wiki/wiki/`.
7. Replace the placeholder summary with actual synthesis.
8. Run `make wiki-lint`.

If you want to put files in a folder and process them by role:

1. Put files into `llm-wiki/inbox/`.
2. Run `make wiki-dispatch`.
3. Open the generated queue files in `llm-wiki/queues/`.
4. Work through the default order:
   `collector -> synthesizer -> linker -> critic -> publisher`

If you already know a file should become a permanent source:

1. Run `make wiki-ingest SRC=/absolute/path/to/file.md TITLE="Readable Title"`.
2. Open the created draft page in `llm-wiki/wiki/`.
3. Replace the placeholder text with actual synthesis.
4. Run `make wiki-lint`.

## What Success Looks Like

After a healthy direct ingest:

- the source file exists under `llm-wiki/sources/`
- a draft or updated page exists under `llm-wiki/wiki/`
- `llm-wiki/wiki/index.md` includes the page
- `llm-wiki/wiki/log.md` records the operation
- `make wiki-lint` ends with `wiki-lint: OK`

## Daily Workflow

### Option A: Inbox First

Use this when you want a lightweight triage step before ingesting.

```bash
make wiki-dispatch
```

What it does:

- scans `llm-wiki/inbox/`
- creates `llm-wiki/queues/dispatch-report.md`
- creates or refreshes role queues such as `collector.md` and `synthesizer.md`

What you should open next:

- `llm-wiki/queues/dispatch-report.md` for the big picture
- `llm-wiki/queues/collector.md` if you are deciding whether files should become permanent sources

### Option B: Direct Ingest

Use this when the source is already vetted and you want to move straight into the wiki.

```bash
make wiki-ingest SRC=/absolute/path/to/source.md TITLE="Example Source"
```

What it does:

- copies the file into `llm-wiki/sources/`
- creates a draft page in `llm-wiki/wiki/` if needed
- seeds starter relationship links for follow-up synthesis
- refreshes `llm-wiki/wiki/index.md`
- appends an entry to `llm-wiki/wiki/log.md`

What you should open next:

- the new page in `llm-wiki/wiki/`
- `llm-wiki/wiki/index.md` to confirm the page was cataloged
- `llm-wiki/wiki/log.md` to confirm the ingest was recorded

## Query The Knowledge Base

```bash
make wiki-query Q="keyword"
```

This searches markdown content in:

- `llm-wiki/wiki/index.md` first, to prioritize maintained wiki pages
- `llm-wiki/wiki/`
- `llm-wiki/sources/`
- `llm-wiki/schema/`
- `llm-wiki/roles/`
- `llm-wiki/queues/`
- `llm-wiki/inbox/`

How to read the output:

- the `Recommended Wiki Pages` section is the best place to start
- the file-by-file match list is raw evidence that supports or expands the recommendation

## Validate The Structure

```bash
make wiki-lint
```

This checks:

- required files exist
- core wiki pages exist
- key wiki pages contain required sections
- source references resolve
- relative markdown links are not broken
- the wiki catalog includes every maintained page
- the wiki log heading format stays parse-friendly
- orphan pages and empty relationship sections are reported as warnings
- potentially stale summary language is reported when it relies on thin source support
- `[[Concept]]` mentions without a matching page are suggested as missing concept pages
- similar summary claims with opposing signals are flagged as possible contradictions

How to interpret the result:

- `wiki-lint: OK` means the structure is valid
- `wiki-lint: WARNINGS` means the wiki is usable but probably wants human review
- `wiki-lint: FAIL` means the structure is broken and should be fixed before trusting the wiki

## Role Meanings

- `collector`: decides whether an inbox file should become a permanent source
- `synthesizer`: turns sources into durable wiki knowledge
- `linker`: connects new pages to related pages and indexes
- `critic`: records uncertainty, conflicts, and open questions
- `publisher`: polishes stable summaries for readability

## Common Usage Patterns

### I just dropped a bunch of files into the folder

1. Run `make wiki-dispatch`.
2. Start with `llm-wiki/queues/collector.md`.
3. Ingest the files that should become permanent sources.
4. Move to `synthesizer`, `linker`, and `critic`.

### I only want quick text search

Run:

```bash
make wiki-query Q="your term"
```

### I changed several wiki pages and want to sanity-check them

Run:

```bash
make wiki-lint
```

### I do not know which markdown file to open first

Open them in this order:

1. `llm-wiki/USAGE.md`
2. `llm-wiki/wiki/index.md`
3. `llm-wiki/wiki/log.md`
4. `llm-wiki/queues/dispatch-report.md` if you are using the inbox workflow

## Related Docs

- Workflow details: `llm-wiki/schema/workflow.md`
- Role routing: `llm-wiki/schema/role-routing.md`
- Inbox notes: `llm-wiki/inbox/README.md`
- Queue notes: `llm-wiki/queues/README.md`
- Role definitions: `llm-wiki/roles/*.md`
