# llm-wiki

This repository is a markdown-first knowledge base built around an `llm-wiki` workflow.

- `llm-wiki/sources/` stores immutable raw source material.
- `llm-wiki/wiki/` stores synthesized knowledge pages.
- `llm-wiki/schema/` stores workflow rules and page templates.
- `llm-wiki/inbox/` and `llm-wiki/queues/` support role-based intake and dispatch.
- `scripts/` contains the helper commands behind ingest, query, lint, and dispatch.

If you are new to the repo, start with [llm-wiki/README.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/README.md) and then [llm-wiki/USAGE.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/USAGE.md).

## English Doc Map

Read the internal docs in this order when you want the clearest path through the repository:

1. [llm-wiki/README.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/README.md): high-level layout and command entrypoints.
2. [llm-wiki/USAGE.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/USAGE.md): the main operational guide.
3. Pick one workflow:
   [llm-wiki/schema/workflow.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/schema/workflow.md) for direct ingest/query/lint, or
   [llm-wiki/schema/role-routing.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/schema/role-routing.md) for inbox-to-role routing.
4. Open the supporting folder guides:
   [llm-wiki/inbox/README.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/inbox/README.md),
   [llm-wiki/queues/README.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/queues/README.md),
   [llm-wiki/sources/README.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/sources/README.md).
5. Read the role definitions in order:
   [collector.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/roles/collector.md),
   [synthesizer.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/roles/synthesizer.md),
   [linker.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/roles/linker.md),
   [critic.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/roles/critic.md),
   [publisher.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/roles/publisher.md).
6. Use the maintained wiki pages as the live knowledge layer:
   [index.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/wiki/index.md),
   [project-overview.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/wiki/project-overview.md),
   [log.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/wiki/log.md),
   [open-questions.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/wiki/open-questions.md).
7. Use [llm-wiki/schema/page-template.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/schema/page-template.md) when creating or reshaping wiki pages.

## 한국어 안내

이 저장소는 `llm-wiki` 워크플로우를 기반으로 한 마크다운 중심 지식베이스입니다.

- `llm-wiki/sources/`에는 변경하지 않는 원본 자료를 보관합니다.
- `llm-wiki/wiki/`에는 정리되고 합성된 지식 문서를 저장합니다.
- `llm-wiki/schema/`에는 워크플로우 규칙과 페이지 템플릿을 둡니다.
- `llm-wiki/inbox/`와 `llm-wiki/queues/`는 역할 기반 분류와 작업 큐를 지원합니다.
- `scripts/`에는 ingest, query, lint, dispatch 명령의 실행 로직이 들어 있습니다.

처음 보는 경우 영어 기준 개요 문서인 [llm-wiki/README.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/README.md)부터 읽고, 이어서 한국어 사용 가이드 [llm-wiki/USAGE.ko.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/USAGE.ko.md)를 보면 됩니다.

## 한국어 문서 매핑

영문 문서를 기준으로 내부 설명 파일을 다음 순서로 따라가면 됩니다.

1. [llm-wiki/README.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/README.md): 저장소 전체 구조와 핵심 명령 개요
2. [llm-wiki/USAGE.ko.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/USAGE.ko.md): 한국어 기준 실제 사용 흐름
3. 작업 방식 선택:
   [llm-wiki/schema/workflow.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/schema/workflow.md) 는 직접 ingest/query/lint 흐름,
   [llm-wiki/schema/role-routing.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/schema/role-routing.md) 는 inbox 기반 역할 라우팅 흐름입니다.
4. 보조 설명 문서:
   [llm-wiki/inbox/README.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/inbox/README.md),
   [llm-wiki/queues/README.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/queues/README.md),
   [llm-wiki/sources/README.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/sources/README.md).
5. 역할 정의는 한국어 문서를 순서대로 읽으면 됩니다:
   [collector.ko.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/roles/collector.ko.md),
   [synthesizer.ko.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/roles/synthesizer.ko.md),
   [linker.ko.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/roles/linker.ko.md),
   [critic.ko.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/roles/critic.ko.md),
   [publisher.ko.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/roles/publisher.ko.md).
6. 실제 지식 레이어는 공통으로 다음 파일을 보면 됩니다:
   [index.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/wiki/index.md),
   [project-overview.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/wiki/project-overview.md),
   [log.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/wiki/log.md),
   [open-questions.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/wiki/open-questions.md).
7. 페이지를 새로 만들거나 구조를 맞출 때는 [llm-wiki/schema/page-template.md](/Users/leejiho/Desktop/llm-wiki/llm-wiki/schema/page-template.md)를 참고하면 됩니다.
