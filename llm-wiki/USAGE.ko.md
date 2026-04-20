# 사용 가이드

이 문서는 이 저장소의 `llm-wiki` 워크플로우를 사용하는 가장 기본적인 시작점입니다.

## 시작 전 확인

- 명령은 저장소 루트에서 실행합니다.
- `make wiki-ingest`의 `SRC=...`에는 절대 경로를 사용하는 편이 안전합니다.
- `llm-wiki/sources/`에 들어간 파일은 ingest 후 수정하지 않는 것을 기본 원칙으로 합니다.
- 어디서 시작할지 모르겠다면 바로 아래 `빠른 시작`만 따라가면 됩니다.

## 폴더 용도

- `llm-wiki/inbox/`: 새 자료를 먼저 넣는 폴더
- `llm-wiki/sources/`: 채택된 원본 자료를 변경 없이 보관하는 폴더
- `llm-wiki/wiki/`: 정리되고 유지되는 지식 문서 폴더
- `llm-wiki/queues/`: 역할별 작업 큐가 생성되는 폴더
- `llm-wiki/roles/`: 역할 정의 문서 폴더
- `llm-wiki/schema/`: 워크플로우 규칙과 템플릿 폴더

## 빠른 시작

처음 보는 사람이 하나의 추천 경로만 따라가고 싶다면 이렇게 하면 됩니다.

1. 파일 하나를 `llm-wiki/inbox/`에 넣습니다.
2. `make wiki-dispatch`를 실행합니다.
3. `llm-wiki/queues/collector.md`를 엽니다.
4. 그 파일을 `llm-wiki/sources/`에 보관할지 결정합니다.
5. 보관할 가치가 있다면 `make wiki-ingest SRC=/absolute/path/to/file.md TITLE="읽기 좋은 제목"`을 실행합니다.
6. `llm-wiki/wiki/`에 생긴 드래프트 페이지를 엽니다.
7. placeholder 요약을 실제 요약으로 바꿉니다.
8. `make wiki-lint`를 실행합니다.

자료를 폴더에 넣고 역할별로 처리하고 싶다면:

1. 파일을 `llm-wiki/inbox/`에 넣습니다.
2. `make wiki-dispatch`를 실행합니다.
3. `llm-wiki/queues/`에 생성된 큐 파일을 엽니다.
4. 아래 기본 순서대로 진행합니다.
   `collector -> synthesizer -> linker -> critic -> publisher`

이미 어떤 파일을 영구 source로 넣어야 할지 확실하다면:

1. `make wiki-ingest SRC=/absolute/path/to/file.md TITLE="읽기 좋은 제목"`을 실행합니다.
2. `llm-wiki/wiki/`에 생성된 드래프트 페이지를 엽니다.
3. placeholder 내용을 실제 요약과 정리 내용으로 바꿉니다.
4. `make wiki-lint`를 실행합니다.

## 성공한 상태는 무엇인가

직접 ingest가 잘 끝났다면 보통 다음이 보입니다.

- source 파일이 `llm-wiki/sources/` 아래에 생깁니다.
- 초안 또는 갱신된 페이지가 `llm-wiki/wiki/` 아래에 생깁니다.
- `llm-wiki/wiki/index.md`에 해당 페이지가 반영됩니다.
- `llm-wiki/wiki/log.md`에 작업 기록이 남습니다.
- `make wiki-lint` 결과가 `wiki-lint: OK`로 끝납니다.

## 일상적인 사용 흐름

### 방법 A: Inbox 먼저 사용

ingest 전에 가볍게 분류하고 싶은 경우에 적합합니다.

```bash
make wiki-dispatch
```

이 명령은 다음을 수행합니다.

- `llm-wiki/inbox/`를 스캔합니다.
- `llm-wiki/queues/dispatch-report.md`를 생성합니다.
- `collector.md`, `synthesizer.md` 같은 역할별 큐를 생성하거나 갱신합니다.

다음에 열어볼 파일:

- 전체 현황을 보려면 `llm-wiki/queues/dispatch-report.md`
- 어떤 파일을 영구 source로 둘지 결정하려면 `llm-wiki/queues/collector.md`

### 방법 B: 바로 Ingest

이미 source로 보관할 가치가 확실한 자료라면 바로 wiki 흐름으로 넣을 수 있습니다.

```bash
make wiki-ingest SRC=/absolute/path/to/source.md TITLE="예시 자료"
```

이 명령은 다음을 수행합니다.

- 파일을 `llm-wiki/sources/`로 복사합니다.
- 필요하면 `llm-wiki/wiki/`에 드래프트 페이지를 만듭니다.
- 후속 정리를 위한 starter 관계 링크를 넣습니다.
- `llm-wiki/wiki/index.md`를 갱신합니다.
- `llm-wiki/wiki/log.md`에 기록을 추가합니다.

다음에 열어볼 파일:

- 새로 생긴 `llm-wiki/wiki/` 페이지
- 카탈로그 반영 여부를 볼 `llm-wiki/wiki/index.md`
- 기록 여부를 볼 `llm-wiki/wiki/log.md`

## 지식 베이스 검색

```bash
make wiki-query Q="keyword"
```

이 명령은 다음 위치의 마크다운을 검색합니다.

- 먼저 `llm-wiki/wiki/index.md`를 읽어 유지되는 wiki 페이지를 우선 추천합니다.
- `llm-wiki/wiki/`
- `llm-wiki/sources/`
- `llm-wiki/schema/`
- `llm-wiki/roles/`
- `llm-wiki/queues/`
- `llm-wiki/inbox/`

출력 읽는 법:

- `Recommended Wiki Pages`가 있으면 거기부터 읽는 것이 가장 좋습니다.
- 그 아래 파일별 매치는 근거 줄을 보여주는 보조 정보입니다.

## 구조 검증

```bash
make wiki-lint
```

이 명령은 다음을 확인합니다.

- 필수 파일이 존재하는지
- 핵심 wiki 페이지가 존재하는지
- 주요 wiki 페이지에 필요한 섹션이 들어 있는지
- source reference가 실제로 존재하는지
- 상대 경로 마크다운 링크가 깨지지 않았는지
- wiki catalog에 모든 유지 페이지가 반영되어 있는지
- wiki log 제목 형식이 단순 파싱에 적합한지
- orphan page와 비어 있는 Relationships 섹션을 경고로 표시하는지
- 근거가 얇은 상태에서 stale해 보이는 요약 문구가 있는지
- `[[Concept]]` 표기가 있는데 대응하는 페이지가 없는지
- 비슷한 요약 주장에 상반된 신호가 있는지

결과 해석:

- `wiki-lint: OK`면 구조상 정상입니다.
- `wiki-lint: WARNINGS`면 사용은 가능하지만 사람 검토가 권장됩니다.
- `wiki-lint: FAIL`이면 구조가 깨진 상태라 먼저 수정해야 합니다.

## 역할 의미

- `collector`: inbox 파일을 영구 source로 채택할지 결정합니다.
- `synthesizer`: source를 지속 가능한 wiki 지식으로 바꿉니다.
- `linker`: 새 페이지를 기존 페이지와 인덱스에 연결합니다.
- `critic`: 불확실성, 충돌, 열린 질문을 기록합니다.
- `publisher`: 안정된 요약 페이지를 읽기 좋게 다듬습니다.

## 자주 쓰는 패턴

### 폴더에 자료를 여러 개 넣었다

1. `make wiki-dispatch`를 실행합니다.
2. `llm-wiki/queues/collector.md`부터 봅니다.
3. 영구 source로 둘 자료를 ingest 합니다.
4. 이후 `synthesizer`, `linker`, `critic` 순으로 진행합니다.

### 빠르게 텍스트 검색만 하고 싶다

다음을 실행합니다.

```bash
make wiki-query Q="검색어"
```

### 여러 wiki 페이지를 수정한 뒤 점검하고 싶다

다음을 실행합니다.

```bash
make wiki-lint
```

### 어떤 문서부터 열어야 할지 모르겠다

이 순서로 여는 것이 가장 쉽습니다.

1. `llm-wiki/USAGE.ko.md`
2. `llm-wiki/wiki/index.md`
3. `llm-wiki/wiki/log.md`
4. inbox 흐름을 쓴다면 `llm-wiki/queues/dispatch-report.md`

## 관련 문서

- 워크플로우 상세: `llm-wiki/schema/workflow.md`
- 역할 라우팅 규칙: `llm-wiki/schema/role-routing.md`
- inbox 설명: `llm-wiki/inbox/README.md`
- queue 설명: `llm-wiki/queues/README.md`
- 역할 정의(영문): `llm-wiki/roles/*.md`
- 역할 정의(국문): `llm-wiki/roles/*.ko.md`
