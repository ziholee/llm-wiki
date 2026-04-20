# LLM Wiki

This repository uses an `llm-wiki` layout inspired by Karpathy's gist:

- `sources/` stores immutable raw inputs.
- `wiki/` stores synthesized markdown knowledge that agents maintain over time.
- `schema/` stores the rules and templates that control wiki maintenance.
- `inbox/` is where new materials are dropped before routing.
- `queues/` is where role-based work queues are generated.
- `roles/` defines what each role is responsible for.

The goal is to accumulate high-signal knowledge instead of rebuilding context from scratch for every question.

## Start Here

- English guide: `llm-wiki/USAGE.md`
- 한국어 가이드: `llm-wiki/USAGE.ko.md`

If you are new to this repo, read the usage guide first and follow one path only:

- Use `inbox -> dispatch` if you want the role-based workflow.
- Use `wiki-ingest` if you already trust the file and want to add it directly.

## Draft Commands

```bash
make wiki-ingest SRC=/absolute/path/to/source.md TITLE="Example Source"
make wiki-query Q="example"
make wiki-lint
make wiki-dispatch
```

Expected outcomes:

- `make wiki-dispatch` updates files in `llm-wiki/queues/`
- `make wiki-ingest` adds a file under `llm-wiki/sources/` and may create a draft page under `llm-wiki/wiki/`
- `make wiki-query` prints likely wiki pages and matching lines
- `make wiki-lint` reports whether the wiki structure is healthy

See `llm-wiki/USAGE.md` for the practical workflow in English.
See `llm-wiki/USAGE.ko.md` for the practical workflow in Korean.
See `llm-wiki/schema/workflow.md` for the current ingest/query/lint draft.
See `llm-wiki/schema/role-routing.md` for the role-based inbox workflow.
