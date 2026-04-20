# Collector

## Purpose

Decide whether a dropped file should become an immutable source in `llm-wiki/sources/`.

## Responsibilities

- Verify the inbox file is worth preserving.
- Keep the original file unchanged.
- Ingest it into `llm-wiki/sources/`.
- Start or update the wiki log.

## Exit Criteria

- The source exists in `llm-wiki/sources/`.
- The wiki log mentions it.
- The next role has enough context to continue.
