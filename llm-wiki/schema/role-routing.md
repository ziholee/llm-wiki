# Role Routing

This document defines how dropped materials should move through the role-based workflow.

## Flow

```text
inbox -> collector -> synthesizer -> linker -> critic -> publisher
```

Not every source needs every role in equal depth, but this is the default order.

## Role Meanings

- `collector`: decide whether the file should enter the permanent source archive
- `synthesizer`: produce durable wiki knowledge
- `linker`: connect the result to the rest of the wiki
- `critic`: document uncertainty, conflicts, and open questions
- `publisher`: refine stable summaries and overview pages

## Current Dispatch Behavior

`make wiki-dispatch` scans `llm-wiki/inbox/` and generates markdown queue files under `llm-wiki/queues/`.

- All supported files are routed to `collector`, `synthesizer`, `linker`, and `critic`.
- Files with names like `overview`, `guide`, `faq`, `report`, or `summary` are also routed to `publisher`.

## Why This Structure

The goal is not full automation. The goal is operational clarity:

- one place to drop files,
- one command to see the next actions,
- and explicit handoffs between roles.
