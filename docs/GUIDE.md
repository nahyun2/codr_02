# 프로젝트 가이드 (나만의 퀴즈 게임)

> 이 문서는 여러 컴퓨터를 오가며 작업할 때 Claude가 프로젝트 맥락을 빠르게 파악하기 위한 참고 문서입니다.
> Git으로 커밋되므로 어느 컴퓨터에서든 `git pull` 하면 최신 내용을 볼 수 있습니다.
> 제출 요건과 무관한 작업 메모이니, 진행하면서 자유롭게 갱신하세요.

## 0. Claude 작업 방식 (필독)

- 사용자는 **Python을 배우면서** 이 프로젝트를 진행 중.
- 새 기능을 시작할 때: **개념 설명 → Claude가 직접 완성 코드 작성** 순서로 진행한다 (2026-08-20부터: 스켈레톤/TODO 방식 대신 완성 코드로 변경, 사용자 요청).
- 기능 하나가 끝나면 아래 3번의 "Git 체크포인트"를 상기시키고 커밋을 제안한다.
- 아래 6번 체크리스트의 캡쳐/기록 시점에 도달하면 **먼저 알려줄 것** (사용자가 잊기 쉬움).

## 1. 미션 한 줄 요약

터미널 기반 퀴즈 게임을 Python + Git으로 처음부터 끝까지 만들며 기초 문법, 클래스(OOP), 파일 입출력(JSON 영속성), Git 워크플로우(커밋/브랜치/merge/clone/pull)를 익히는 학습 미션.

## 2. 최종 결과물 요구사항 (요약 체크리스트)

**기능**
- [ ] 메뉴에서 번호 선택 → 퀴즈풀기 / 퀴즈추가 / 퀴즈목록 / 점수확인 / 종료
- [ ] 선택한 주제(현재: 넌센스 퀴즈)의 퀴즈 5개 이상
- [ ] 종료 후 재실행해도 퀴즈/최고점수 유지 (`state.json`)

**코드 구조**
- [ ] 클래스 2개 이상 (`Quiz`, `QuizGame`)
- [ ] 기능별 메서드 분리 (입력 처리 / 게임 진행 / 저장 로직 등)
- [ ] `state.json`을 프로젝트 루트에 UTF-8로 저장/불러오기

**공통 입력/예외 처리 (최소 요구)**
- [ ] 숫자 입력: 공백 제거, 변환 실패(abc), 범위 밖, 빈 입력 → 안내 후 재입력
- [ ] `KeyboardInterrupt` / `EOFError` → 비정상 종료 없이 안내 후 저장·안전 종료
- [ ] `state.json` 없음/손상 시에도 실행 가능 (기본 데이터로 대체)

**GitHub**
- [ ] 커밋 10개 이상 (의미있는 메시지: `Feat:`/`Fix:`/`Docs:`/`Refactor:`)
- [ ] 브랜치 생성 + 병합(merge) 최소 1회 (퀴즈 풀기 기능에서 사용)
- [ ] `clone`, `pull` 각 1회 이상 사용 기록 (전용 실습 단계 있음, 3-13번)
- [ ] Git 명령어 7종(`init/add/commit/push/pull/checkout/clone`) 각 1load_data회 이상
- [ ] README.md에 필수 항목 6개 (개요/주제선정이유/실행방법/기능목록/파일구조/데이터파일설명)

## 3. 기능별 구현 순서 + Git 체크포인트

GitHub 이슈(#1~#18)가 이 순서와 거의 1:1로 대응합니다.

| # | 단계 | Git 체크포인트 | 상태 |
|---|------|----------------|------|
| 1 | Git/GitHub 초기 설정 | 최초 commit + push | ✅ 완료 |
| 2 | README/​.gitignore 뼈대 | commit | ✅ 완료 |
| 3 | main.py 진입점 + 메뉴 출력 | commit | ✅ 완료 |
| 4 | 메뉴 선택 루프 + 종료 처리 | commit | ✅ 완료 |
| 5 | 공통 숫자 입력 검증 함수 | commit | ⬜ |
| 6 | KeyboardInterrupt/EOFError 안전 종료 | commit | ⬜ |
| 7 | Quiz 클래스 정의 | commit | ⬜ |
| 8 | 기본 퀴즈 데이터 5개 이상 | commit | ⬜ |
| 9 | 퀴즈 풀기 (★`feature/play` 브랜치에서 작업 후 main에 merge) | commit + merge | ⬜ |
| 10 | 퀴즈 추가 기능 | commit | ⬜ |
| 11 | 퀴즈 목록 기능 | commit | ⬜ |
| 12 | 점수 확인 기능 | commit | ⬜ |
| 13 | QuizGame 클래스로 책임 분리 (리팩터링) | commit | ⬜ |
| 14 | state.json 저장/불러오기 구현 | commit | ⬜ |
| 15 | 퀴즈 추가/점수 갱신 시 자동 저장 연결 | commit | ⬜ |
| 16 | README 최종 작성 | commit + push | ⬜ |
| 17 | 저장소 clone/pull 실습 (별도 디렉토리) | clone, commit, push, pull | ⬜ |
| 18 | 보너스 (선택) | - | ⬜ |

## 4. 현재 진행 상황 (스냅샷: 2026-08-12)

- 커밋 4개: `Initial commit` → `Docs: 초기 설정` → `Feat: main.py 진입점 및 메뉴 화면 출력` → `Feat: 메뉴 선택 루프 및 종료 처리`
- `main.py`: `print_menu()`와 메뉴 루프만 존재. 1~4번 선택지는 "아직 준비 중" placeholder. 잘못된 입력(문자/범위밖/빈입력) 처리 없음.
- `Quiz` / `QuizGame` 클래스: 아직 없음
- `state.json`: 아직 없음
- 브랜치: `main`만 존재 (feature 브랜치 아직 없음)
- GitHub 이슈 #1~#18 등록됨, #1~#4는 closed, #5~#18은 open

**주의**: 이 섹션은 특정 시점의 스냅샷입니다. 실제 최신 상태는 `git log --oneline --graph`, `git branch -a` 로 항상 다시 확인할 것 — 특히 다른 컴퓨터에서 pull 받은 직후.

## 5. 캡쳐/기록해야 하는 시점 체크리스트 (제출물용)

Claude는 아래 시점에 도달하면 사용자에게 먼저 캡쳐/기록을 알려줄 것.

- [ ] 개발 환경 설정 스크린샷 (VSCode, `python --version`, `git config --list` 등)
- [ ] 퀴즈 추가 실행 화면 → `docs/screenshots/add_quiz.png`
- [ ] 퀴즈 목록 실행 화면 → `docs/screenshots/menu.png`
- [ ] 퀴즈 풀기 실행 화면 → `docs/screenshots/play.png`
- [ ] 점수 확인 실행 화면 → `docs/screenshots/score.png`
- [ ] 브랜치 merge 완료 후, merge 커밋이 보이는 `git log --oneline --graph` 스크린샷
- [ ] 커밋 10개 이상 채워진 뒤 최종 `git log --oneline --graph` 스크린샷
- [ ] clone 실습: 별도 디렉토리에 clone → README 한 줄 추가 → commit → push (터미널 출력 캡쳐)
- [ ] 기존 디렉토리에서 pull → 반영 확인 (터미널 출력 캡쳐)
- [ ] 최종 GitHub 저장소 URL 기록

## 6. 참고

- 저장소: https://github.com/nahyun2/codr_02
- 요구사항 원문(전체 스펙)은 이슈 #1~#18과 이 문서 2~3번에 요약되어 있음. 세부 문구가 더 필요하면 사용자에게 원문을 다시 요청할 것.

## 7. 추가할 내용 및 체크리스트 (이번 단계에서 문서에 추가함)

- **0번(필독) 재강조**: `0. Claude 작업 방식 (필독)` 섹션을 반드시 숙지하세요. 새로운 기능을 구현할 때는 "개념 설명 → TODO 스켈레톤 코드" 순서로 제공하도록 유의합니다.
- **실행/설치 명령 예시**: 프로젝트 루트에서 Python 3.10+가 설치되어 있음을 전제로 아래 명령으로 실행합니다.

```bash
python --version
python main.py
```

- **`state.json` 스키마(권장)**:

```json
{
	"quizzes": [
		{
			"question": "질문 문자열",
			"choices": ["선택1","선택2","선택3","선택4"],
			"answer": 1
		}
	],
	"best_score": 0
}
```

- **파일/디렉토리 권장 구조**:
	- `main.py` — 진입점 및 메뉴 루프
	- `quiz.py` — `Quiz`, `QuizGame` 클래스 정의(혹은 `models.py`로 분리)
	- `state.json` — 데이터 저장소
	- `README.md` — 제출용 설명
	- `docs/screenshots/` — 실행화면 캡쳐

- **권장 Git 커밋 흐름(예시)**:
	- `Feat: Quiz 클래스 추가`
	- `Feat: 기본 퀴즈 데이터 5개 추가`
	- `Feat: 퀴즈 풀기 기능 구현 (feature/play 브랜치)`
	- `Merge feature/play into main`

- **문서에 추가할 항목 (이슈로 분리 권장)**:
	- 보너스 기능 중 어느 것을 우선 적용할지(랜덤/힌트/삭제 등) 우선순위 결정
	- 스크린샷 찍는 정확한 위치와 파일명 규칙

---

위 항목들을 문서에 반영해두었으니, 다음으로는 실제 코드(`main.py`, `quiz.py`) 골격과 TODO 주석을 생성할까요? 원하시면 언어는 `Python`으로 진행하겠습니다.
