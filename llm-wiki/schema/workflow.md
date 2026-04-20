# Workflow Draft

This document defines a lightweight markdown-first workflow for `ingest`, `query`, and `lint`.

## Goal

Keep the workflow simple enough to run locally while still enforcing the core `llm-wiki` rules:

- raw sources are preserved,
- synthesized knowledge lives in markdown pages,
- uncertainty is explicit,
- and broken wiki structure is caught early.

## Ingest

Purpose: move a raw source into the repository and create the smallest useful draft artifact.

### Inputs

- A local source file.
- An optional human-readable title.

### Command

```bash
make wiki-ingest SRC=/absolute/path/to/source.md TITLE="Example Source"
```

### Current Behavior

- Copies the source into `llm-wiki/sources/` with a date-prefixed filename.
- Creates a draft wiki page if one does not already exist.
- Seeds the draft page with starter relationship links.
- Refreshes `llm-wiki/wiki/index.md` so the catalog stays current.
- Appends an entry to `llm-wiki/wiki/log.md`.

### Human Follow-up

- Replace the draft summary with an actual synthesis.
- Update related pages instead of leaving the new page isolated.
- Add unresolved ambiguity to `llm-wiki/wiki/open-questions.md`.

## Query

Purpose: search the markdown knowledge base without requiring a vector database.

### Command

```bash
make wiki-query Q="keyword"
```

### Current Behavior

- Uses `llm-wiki/wiki/index.md` as the first navigation layer.
- Prioritizes likely wiki pages before printing raw text matches.
- Searches markdown files in `llm-wiki/wiki/`, `llm-wiki/sources/`, and supporting folders.
- Appends an entry to `llm-wiki/wiki/log.md`.

## Lint

Purpose: check that the wiki remains structurally healthy.

### Command

```bash
make wiki-lint
```

### Current Checks

- Required repository files exist.
- Core wiki pages exist.
- Non-exempt wiki pages include `Summary` and `Source Basis` sections.
- Referenced source files exist.
- Relative markdown links resolve.
- The wiki catalog includes every maintained page.
- The wiki log uses parse-friendly headings.
- Orphan pages and empty relationship sections are surfaced as warnings.
- Potentially stale summary language is surfaced when it leans on only one cited source.
- `[[Concept]]` mentions without a matching page are surfaced as missing concept-page suggestions.
- Similar summary claims with opposing signals are surfaced as potential contradictions.

## Intended Evolution

This is a draft workflow, not a final system. Good next upgrades would be:

- frontmatter for page metadata,
- source-to-page relationship manifests,
- richer query ranking,
- semantic duplicate detection,
- and stricter lint rules for evidence quality.

## Role-Based Intake

If you want to drop materials into a folder first and process them by role later:

```bash
make wiki-dispatch
```

This scans `llm-wiki/inbox/` and generates role queues in `llm-wiki/queues/`.
