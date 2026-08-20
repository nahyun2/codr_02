# 학습 정리 (이슈별 개념 + 코드)

> `docs/GUIDE.md` 3번 표의 이슈 순서(#1~#18)에 맞춰 정리합니다.
> 실제 코드 파일에는 간단한 주석만 남기고, 자세한 개념 설명과 코드는 여기에 기록합니다.

## 이슈 1. Git/GitHub 초기 설정

**개념**
- `git init`: 현재 폴더를 Git 저장소로 초기화 (`.git` 폴더 생성).
- `git remote add origin <URL>`: 로컬 저장소와 GitHub 원격 저장소를 연결.
- `git add` → `git commit` → `git push`: 변경사항을 스테이징 → 로컬에 기록 → 원격에 반영하는 기본 3단계.

**코드/작업**
- 별도 소스 코드 없음. `README.md` 한 줄만 있는 상태로 최초 커밋.
```bash
git init
git remote add origin https://github.com/nahyun2/codr_02.git
git add README.md
git commit -m "Initial commit"
git push -u origin main
```

---

## 이슈 2. README / .gitignore 뼈대

**개념**
- `.gitignore`: Git이 추적하지 않을 파일/폴더 패턴을 지정. 캐시 파일(`__pycache__/`), 가상환경(`.venv/`), 에디터 설정(`.vscode/`) 등 커밋할 필요 없는 파일을 제외해 저장소를 깔끔하게 유지.
- `README.md`: 프로젝트 소개 문서. 처음엔 항목 제목과 `TODO` 주석만 있는 뼈대로 시작해서 나중에 채워 넣음.

**코드**
```gitignore
# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/
env/

# OS
.DS_Store

# Editor
.vscode/
.idea/
```
README.md는 `## 프로젝트 개요`, `## 퀴즈 주제 및 선정 이유`, `## 실행 방법`, `## 기능 목록`, `## 파일 구조`, `## 데이터 파일 설명` 6개 섹션 제목만 먼저 만들고 내용은 `<!-- TODO -->`로 남겨둠 (이슈 16에서 최종 작성 예정).

---

## 이슈 3. main.py 진입점 + 메뉴 출력

**개념**
- `if __name__ == "__main__":` : 이 파일이 `python main.py`처럼 직접 실행될 때만 안의 코드를 실행하게 하는 관용구. 다른 모듈에서 `import main`으로 불러올 땐 실행되지 않음.
- 함수로 분리(`print_menu`)해두면 나중에 메뉴 출력이 필요한 다른 곳에서도 재사용 가능.
- f-string 없이 고정 문자열을 `print()`로 나열해 화면 레이아웃 구성.

**코드**
```python
def print_menu():
    """메뉴 화면을 출력한다."""
    print("="*20)
    print("🎯 넌센스 퀴즈 게임 🎯")
    print("="*20)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("="*20)


def main():
    print_menu()


if __name__ == "__main__":
    main()
```

---

## 이슈 4. 메뉴 선택 루프 + 종료 처리

**개념**
- `while True:` 무한 루프 + `break`: 사용자가 종료를 선택하기 전까지 메뉴를 계속 다시 보여주는 패턴.
- 이 시점에는 아직 입력 검증이 없어서, 숫자가 아닌 값이나 범위 밖 값을 넣어도 그냥 "아직 준비 중입니다"로 처리됨 (검증은 이슈 5에서 추가).
- `input()`은 항상 문자열을 반환하므로 `choice == "5"`처럼 문자열끼리 비교.

**코드**
```python
def main():
    while True:
        print_menu()
        choice = input("선택: ")

        if choice == "5":
            print("종료합니다.")
            break
        else:
            print(f"{choice}번은 아직 준비 중입니다")
```

---

## 이슈 5. 공통 숫자 입력 검증 함수 (`read_int`)

**개념**
- 여러 곳(메뉴 선택, 정답 번호 입력 등)에서 "숫자 입력받고 검증하는" 로직이 반복될 걸 예상해서, `utils.py`에 재사용 함수로 미리 분리.
- 검증해야 할 케이스 4가지: ① 빈 입력 ② 공백만 있는 입력 ③ 숫자로 변환 불가능한 입력 ④ 지정한 범위(`min_val`~`max_val`) 밖의 입력. 넷 다 안내 메시지를 출력하고 `continue`로 다시 물어봄.
- `int(s)` 변환 실패는 `ValueError`로 잡아서 처리.
- `KeyboardInterrupt`/`EOFError`는 여기서 처리하지 않고 `raise`로 그대로 위로 전달 — "입력 검증"과 "프로그램 종료 처리"는 책임을 분리해서, 종료 처리는 호출자(`main.py`, 이슈 6)가 담당하게 함.

**코드** (`utils.py`)
```python
def read_int(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    while True:
        try:
            raw = input(prompt)
        except (KeyboardInterrupt, EOFError):
            raise  # 종료 처리는 호출자에게 위임

        s = raw.strip()
        if s == "":
            print("입력이 비었습니다. 값을 입력하세요.")
            continue

        try:
            val = int(s)
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력하세요.")
            continue

        if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
            print(f"허용 범위를 벗어났습니다. {min_val}~{max_val} 사이의 숫자를 입력하세요.")
            continue

        return val
```

**적용** (`main.py`) — 메뉴 선택에 바로 사용
```python
choice = read_int("선택: ", 1, 5)

if choice == 5:   # 이제 int라서 5로 비교 (이슈4의 "5"와 다름)
    print("종료합니다.")
    break
```

---

## 이슈 6. `KeyboardInterrupt` / `EOFError` 안전 종료

**개념**
- `KeyboardInterrupt`: `Ctrl+C` 입력 시 발생.
- `EOFError`: `input()`이 더 읽을 입력이 없을 때(예: 파이프 입력 종료) 발생.
- 처리 안 하면 지저분한 트레이스백과 함께 프로그램이 죽음. `main()` 호출부(`if __name__ == "__main__":`)에서 한 번에 감싸서, 어디서 발생하든(지금은 `read_int` 안에서 `raise`되어 여기까지 전달됨) 깔끔한 안내 메시지 후 정상 종료로 바꿈.
- 예외 처리 위치를 `main()` 내부가 아니라 최상단 진입점에 둔 이유: 로직 코드(`main()`)와 "프로그램 레벨 안전장치"를 분리하기 위함.

**코드** (`main.py`, 최초 작성 당시)
```python
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n프로그램을 안전하게 종료합니다. (Ctrl+C 감지)")
    except EOFError:
        print("\n입력이 종료되어 프로그램을 안전하게 종료합니다.")
```

**보완 (이슈 16 정리 중 발견)**: GUIDE 체크리스트에는 "안내 후 **저장**·안전 종료"가 명시돼 있는데, `try/except`가 `main()` 바깥(`__main__`)에 있으면 `QuizGame` 객체(`game`)에 접근할 수 없어 종료 시 저장을 못 함. 그래서 `try/except`를 `main()` 안쪽, `game = QuizGame()` 다음으로 옮기고 각 `except`에서 `game.save_state()`를 먼저 호출하도록 수정함.
```python
def main():
    game = QuizGame()

    try:
        while True:
            ...
    except KeyboardInterrupt:
        game.save_state()
        print("\n프로그램을 안전하게 종료합니다. (Ctrl+C 감지)")
    except EOFError:
        game.save_state()
        print("\n입력이 종료되어 프로그램을 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
```

---

## 이슈 7. `Quiz` 클래스 정의

**개념**
- 클래스(class): "문제 하나"라는 개념을 데이터(속성)와 동작(메서드)으로 묶어서 표현. 지금까지처럼 문제/선택지/정답을 각각 변수나 딕셔너리로 흩어서 다루는 대신, `Quiz` 객체 하나가 문제 하나를 온전히 표현하게 됨.
- `__init__(self, ...)`: 생성자. `Quiz("질문", ["선택지1", ...], 정답번호)`처럼 객체를 만들 때 호출되어 속성을 초기화. 여기서 잘못된 값(빈 질문, 선택지 2개 미만, 범위 밖 정답)이 들어오면 `ValueError`를 즉시 발생시켜서 "잘못된 퀴즈 객체"가 애초에 만들어지지 않도록 방어.
- 인스턴스 메서드(`display`, `check_answer`): 첫 인자로 항상 `self`(자기 자신 객체)를 받아서, 그 객체가 가진 속성(`self.question` 등)에 접근.
  - `display()`: 문제/선택지를 화면에 출력하는 역할만 담당 (단일 책임).
  - `check_answer(user_choice)`: 사용자가 고른 번호와 정답 번호를 비교해 `bool` 반환. 채점 로직을 `Quiz` 스스로 알고 있게 해서, 호출하는 쪽(나중에 `QuizGame.play()`)은 비교 로직을 몰라도 됨.
- `answer`는 `choices` 리스트의 **1-based 인덱스**(1번부터 시작)로 정함 — 사람이 보는 "1번, 2번" 번호와 그대로 맞아떨어지게 하기 위함 (0-based로 하면 화면 표시할 때마다 +1/-1 변환이 필요해짐).

**코드** (`quiz.py`)
```python
from typing import List


class Quiz:
    """퀴즈 문제 하나(질문/선택지/정답)를 표현하는 클래스."""

    def __init__(self, question: str, choices: List[str], answer: int):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("question은 비어있지 않은 문자열이어야 합니다.")
        if not isinstance(choices, list) or len(choices) < 2:
            raise ValueError("choices는 최소 2개 이상의 리스트여야 합니다.")
        if not isinstance(answer, int) or not (1 <= answer <= len(choices)):
            raise ValueError(f"answer는 1~{len(choices)} 사이의 정수여야 합니다.")

        self.question = question
        self.choices = choices
        self.answer = answer  # choices의 1-based 인덱스

    def display(self) -> None:
        """문제와 선택지를 번호와 함께 출력한다."""
        print(f"\nQ. {self.question}")
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_choice: int) -> bool:
        """user_choice가 정답 번호와 같은지 반환한다."""
        return user_choice == self.answer
```

**사용 예시**
```python
>>> q = Quiz("하늘은 왜 파랗게 보일까?", ["원래 파란색", "빛의 산란", "바다가 비쳐서"], 2)
>>> q.display()

Q. 하늘은 왜 파랗게 보일까?
  1. 원래 파란색
  2. 빛의 산란
  3. 바다가 비쳐서
>>> q.check_answer(2)
True
```

---

## 이슈 8. 기본 퀴즈 데이터 5개 이상

**개념**
- 아직 `state.json` 저장/불러오기(이슈 14)가 없기 때문에, 프로그램이 참조할 "시작용 퀴즈 데이터"가 코드 안에 있어야 함. `default_quizzes()` 함수가 그 역할.
- 함수로 만든 이유: 모듈 최상단에 `DEFAULT_QUIZZES = [...]`처럼 리스트를 바로 두면, 그 리스트 객체를 여러 곳에서 공유하게 되어 한쪽에서 `.append()`하면 다른 곳에도 영향이 감(리스트는 mutable). 함수로 감싸서 호출할 때마다 새 리스트 + 새 `Quiz` 객체들을 만들어 반환하면 이런 부작용을 피할 수 있음.
- `raw`에 `(질문, 선택지리스트, 정답번호)` 튜플들을 먼저 나열하고, 리스트 컴프리헨션 `[Quiz(q, c, a) for q, c, a in raw]`으로 한 번에 `Quiz` 객체 리스트로 변환 — 각 튜플을 `q, c, a`로 언패킹(unpacking)해서 `Quiz` 생성자에 그대로 넘겨줌.

**코드** (`quiz.py`에 추가)
```python
def default_quizzes() -> List[Quiz]:
    """기본 넌센스 퀴즈 5개를 생성해 반환한다."""
    raw = [
        ("하늘은 왜 파랗게 보일까?",
         ["그냥 원래 파란색", "빛의 산란 때문", "바다가 비쳐서", "우주가 파래서"], 2),
        ("물은 몇 도(℃)에서 끓을까? (1기압 기준)",
         ["0도", "50도", "100도", "1000도"], 3),
        ("대한민국의 수도는 어디일까?",
         ["부산", "인천", "서울", "대전"], 3),
        ("1년은 몇 개월일까?",
         ["10개월", "11개월", "12개월", "13개월"], 3),
        ("프로그램 코드의 오류를 부르는 말은?",
         ["버그", "피처", "패치", "커밋"], 1),
    ]
    return [Quiz(q, c, a) for q, c, a in raw]
```

**보완 (`state.json`을 직접 수정한 뒤)**: 사용자가 `state.json`의 문제 5개를 새 넌센스 퀴즈로 직접 교체하면서 "이게 이제 기본 문제"라고 정함. 그런데 `default_quizzes()`는 `state.json`을 읽는 게 아니라 코드에 하드코딩된 별도의 데이터라서, 그대로 두면 `state.json`이 사라지거나 손상됐을 때(→ `load_state()`의 폴백 경로) 예전 문제로 되돌아가는 불일치가 생김. `default_quizzes()`의 `raw` 리스트를 `state.json`에 있는 새 문제 5개(+ 힌트)로 그대로 교체해서, "파일이 있든 없든 항상 같은 기본 문제"가 되도록 맞춤. `rm state.json` 후 재실행 / 파일을 깨뜨린 후 재실행 두 경우 모두 새 `state.json`이 사용자가 만든 버전과 완전히 동일하게 복구되는 것을 확인함.

---

## 이슈 9. 퀴즈 풀기 (`feature/play` 브랜치)

**개념**
- 아직 `QuizGame` 클래스가 없는 단계라, `play_quizzes(quizzes)`라는 일반 함수로 구현. 나중에 이슈 13에서 `QuizGame` 클래스로 리팩터링될 때 이 로직이 메서드 하나로 옮겨갈 예정.
- `main()`이 시작할 때 `quizzes = default_quizzes()`로 퀴즈 목록을 한 번 만들어서, 메뉴 루프 내내 같은 리스트를 재사용 (매번 다시 만들면 이전 라운드의 상태를 유지할 수 없음).
- `for quiz in quizzes:`로 각 문제를 순서대로 출제 → `quiz.display()`로 화면에 보여주고 → `read_int(...)`로 답을 입력받되, `max_val`을 `len(quiz.choices)`로 줘서 그 문제의 선택지 개수에 맞게 범위를 동적으로 검증.
- `quiz.check_answer(choice)`가 `True`/`False`를 돌려주므로, 그 값으로 `score`를 누적하고 정답/오답 메시지를 분기.
- 함수 인자로 `quizzes`를 받는 구조라, 나중에 사용자가 추가한 퀴즈까지 포함된 리스트를 넘겨도 그대로 재사용 가능 (이슈 10과 자연스럽게 연결됨).

**코드** (`main.py`)
```python
from quiz import default_quizzes


def play_quizzes(quizzes):
    """퀴즈 목록을 순서대로 출제하고 채점한 뒤 최종 점수를 출력한다."""
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return

    score = 0
    for quiz in quizzes:
        quiz.display()
        choice = read_int("정답 번호를 입력하세요: ", 1, len(quiz.choices))
        if quiz.check_answer(choice):
            print("정답입니다!")
            score += 1
        else:
            print(f"오답입니다. 정답은 {quiz.answer}번 이었습니다.")

    print(f"\n최종 점수: {score} / {len(quizzes)}")


def main():
    quizzes = default_quizzes()

    while True:
        print_menu()
        choice = read_int("선택: ", 1, 5)

        if choice == 1:
            play_quizzes(quizzes)
        elif choice == 5:
            print("종료합니다.")
            break
        else:
            print(f"{choice}번은 아직 준비 중입니다")
```

---

## 이슈 10. 퀴즈 추가 기능 (`feature/quiz-management`)

**개념**
- `add_quiz(quizzes)`: 사용자에게 문제 1개 + 선택지 4개 + 정답 번호를 순서대로 입력받아 `Quiz` 객체를 만들고, 인자로 받은 `quizzes` 리스트에 `append`.
- 각 입력마다 `while not 값:` 패턴으로 빈 문자열을 막음 — `read_int`는 숫자 검증용이라 문자열(문제/선택지) 입력에는 못 쓰므로 직접 검증 루프를 작성.
- 리스트는 mutable(참조로 전달)이라, 함수 안에서 `quizzes.append(...)`하면 `main()`이 갖고 있는 원본 리스트에도 그대로 반영됨 — 별도로 반환값을 돌려줄 필요 없음.

**코드** (`main.py`)
```python
def add_quiz(quizzes):
    """문제/선택지4개/정답을 입력받아 퀴즈를 추가한다."""
    question = input("문제를 입력하세요: ").strip()
    while not question:
        print("문제는 비어있을 수 없습니다.")
        question = input("문제를 입력하세요: ").strip()

    choices = []
    for i in range(1, 5):
        choice = input(f"선택지 {i}를 입력하세요: ").strip()
        while not choice:
            print("선택지는 비어있을 수 없습니다.")
            choice = input(f"선택지 {i}를 입력하세요: ").strip()
        choices.append(choice)

    answer = read_int("정답 번호(1~4)를 입력하세요: ", 1, 4)

    quizzes.append(Quiz(question, choices, answer))
    print("퀴즈가 추가되었습니다!")
```

---

## 이슈 11. 퀴즈 목록 기능

**개념**
- `list_quizzes(quizzes)`: 등록된 퀴즈들의 질문과 정답 번호만 간단히 나열. 채점용이 아니라 "확인용"이라 선택지까지는 안 보여줌.
- `enumerate(quizzes, start=1)`로 1번부터 번호를 매겨서 사람이 읽기 좋은 목록 형태로 출력.

**코드** (`main.py`)
```python
def list_quizzes(quizzes):
    """등록된 모든 퀴즈의 문제와 정답 번호를 목록으로 출력한다."""
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return

    print(f"\n총 {len(quizzes)}개의 퀴즈가 등록되어 있습니다.")
    for i, quiz in enumerate(quizzes, start=1):
        print(f"{i}. {quiz.question} (정답: {quiz.answer}번)")
```

---

## 이슈 12. 점수 확인 기능

**개념**
- "최고 점수"는 한 번의 `play_quizzes` 호출로 끝나는 값이 아니라 여러 번 플레이해도 유지돼야 하는 상태 → `main()`에 `best_score = 0`을 두고 메뉴 루프가 도는 동안 계속 들고 있음 (아직 클래스가 없어서 지역 변수로 관리, 이슈 13에서 `QuizGame` 속성으로 옮겨감).
- 이를 위해 `play_quizzes`가 이제 점수를 `print`만 하지 않고 `return score`로 값을 돌려주도록 바뀜 → `main()`이 그 값을 받아 `best_score`와 비교/갱신.
- `show_score(best_score, total)`: 아직 한 번도 플레이 안 했으면(`best_score <= 0`) 안내 메시지, 아니면 "최고점수 / 전체문제수" 형태로 출력.

**코드** (`main.py`)
```python
def show_score(best_score, total):
    """지금까지 기록된 최고 점수를 출력한다."""
    if best_score <= 0:
        print("아직 기록된 점수가 없습니다. 퀴즈를 풀어보세요!")
    else:
        print(f"최고 점수: {best_score} / {total}")


def main():
    quizzes = default_quizzes()
    best_score = 0

    while True:
        print_menu()
        choice = read_int("선택: ", 1, 5)

        if choice == 1:
            score = play_quizzes(quizzes)
            if score > best_score:
                best_score = score
                print("최고 점수를 갱신했습니다!")
        elif choice == 2:
            add_quiz(quizzes)
        elif choice == 3:
            list_quizzes(quizzes)
        elif choice == 4:
            show_score(best_score, len(quizzes))
        elif choice == 5:
            print("종료합니다.")
            break
```

---

## 이슈 13. `QuizGame` 클래스로 책임 분리 (리팩터링)

**개념**
- 리팩터링(refactoring): 동작은 그대로 유지하면서 코드 구조만 개선하는 작업. 여태까지 `main.py`에 흩어져 있던 `quizzes`(리스트), `best_score`(변수), `play_quizzes`/`add_quiz`/`list_quizzes`/`show_score`(함수)를 `QuizGame`이라는 클래스 하나로 묶음.
- 왜 묶나: "퀴즈 게임의 상태(퀴즈 목록, 최고 점수)"와 "그 상태를 다루는 동작(풀기/추가/목록/점수)"이 항상 같이 다녀야 하는데, 지금까지는 함수마다 `quizzes`, `best_score`를 일일이 인자로 넘기고 반환값을 다시 받아야 했음. 클래스로 묶으면 `self.quizzes`, `self.best_score`로 공유되어 인자 전달이 사라짐.
- `__init__(self)`: 객체 생성 시점에 `self.quizzes = default_quizzes()`, `self.best_score = 0`으로 초기 상태를 세팅. 함수형 코드의 `quizzes = default_quizzes()` 한 줄이 생성자 안으로 들어간 것.
- 각 메서드는 예전 함수와 로직이 거의 동일하고, `quizzes`/`best_score` 매개변수 대신 `self.quizzes`/`self.best_score`를 사용하도록만 바뀜. `play()`는 이제 점수를 `return`하지 않고 `self.best_score`를 직접 갱신(호출한 쪽에서 비교할 필요가 없어짐).
- `main.py`는 이제 "메뉴 선택값 읽기 → 어떤 메서드를 부를지 분기"만 담당하는 아주 얇은 진입점이 됨. `game = QuizGame()` 객체 하나만 만들면 이후 모든 상태/로직은 그 객체가 책임짐.

**코드** (`quiz.py`)
```python
class QuizGame:
    """퀴즈 목록/최고 점수 상태를 갖고 게임 전체 흐름을 관리하는 클래스."""

    def __init__(self):
        self.quizzes: List[Quiz] = default_quizzes()
        self.best_score: int = 0

    def show_menu(self) -> None:
        ...

    def play(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0
        for quiz in self.quizzes:
            quiz.display()
            choice = read_int("정답 번호를 입력하세요: ", 1, len(quiz.choices))
            if quiz.check_answer(choice):
                print("정답입니다!")
                score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번 이었습니다.")

        print(f"\n최종 점수: {score} / {len(self.quizzes)}")
        if score > self.best_score:
            self.best_score = score
            print("최고 점수를 갱신했습니다!")

    def add_quiz(self) -> None: ...
    def list_quizzes(self) -> None: ...
    def show_score(self) -> None: ...
```

**코드** (`main.py`, 리팩터링 후)
```python
from quiz import QuizGame
from utils import read_int


def main():
    game = QuizGame()

    while True:
        game.show_menu()
        choice = read_int("선택: ", 1, 5)

        if choice == 1:
            game.play()
        elif choice == 2:
            game.add_quiz()
        elif choice == 3:
            game.list_quizzes()
        elif choice == 4:
            game.show_score()
        elif choice == 5:
            print("종료합니다.")
            break
```

---

## 이슈 14. `state.json` 저장/불러오기 구현 (`feature/persistence`)

**개념**
- 지금까지는 프로그램을 끄면 추가한 퀴즈나 최고 점수가 모두 사라졌음. `state.json` 파일에 직렬화(serialize)해서 남겨두고, 다음 실행 때 역직렬화(deserialize)해서 복원하는 게 목표.
- `Quiz.to_dict()` / `Quiz.from_dict()`: `Quiz` 객체 ↔ `dict` 상호 변환. JSON은 파이썬 객체를 직접 저장할 수 없고 `dict`/`list`/기본 타입만 저장 가능하므로, 저장 직전엔 `dict`로, 불러온 직후엔 다시 `Quiz`로 변환하는 다리 역할.
  - `from_dict`는 `@classmethod`로 선언 — 인스턴스가 없는 상태에서 `Quiz.from_dict(data)`처럼 클래스 자체를 통해 새 객체를 만들어야 하기 때문(일반 메서드는 이미 만들어진 `self`가 있어야 호출 가능).
- `QuizGame.__init__(self, state_file="state.json")`: 이제 생성자가 곧바로 `default_quizzes()`를 쓰지 않고 `load_state()`를 호출. `state_file` 경로를 인자로 받게 해서, 나중에 테스트할 때 임시 파일 경로를 넣는 식으로도 재사용 가능.
- `load_state()`의 방어적 처리 (요구사항 "공통 예외 처리"의 `state.json` 부분):
  - 파일이 아예 없으면(`os.path.exists`가 `False`) → 기본 데이터로 시작.
  - 파일은 있지만 JSON 파싱 실패(`json.JSONDecodeError`)나 예상과 다른 구조(`KeyError`/`ValueError`/`TypeError` — 예: `Quiz.from_dict`에서 `Quiz.__init__`의 검증 실패)면 → `except`로 잡아서 기본 데이터로 대체. 어떤 경우에도 프로그램이 죽지 않음.
- `save_state()`: `quizzes`/`best_score`를 `dict`로 만들어 `json.dump`. `ensure_ascii=False`를 꼭 줘야 한글이 `\uXXXX` 이스케이프가 아니라 사람이 읽을 수 있는 문자 그대로 저장됨.

**코드** (`quiz.py`)
```python
class Quiz:
    ...
    def to_dict(self) -> Dict[str, Any]:
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Quiz":
        return cls(data["question"], data["choices"], data["answer"])


class QuizGame:
    def __init__(self, state_file: str = "state.json"):
        self.state_file = state_file
        self.quizzes: List[Quiz] = []
        self.best_score: int = 0
        self.load_state()

    def load_state(self) -> None:
        if not os.path.exists(self.state_file):
            self.quizzes = default_quizzes()
            self.best_score = 0
            self.save_state()   # 처음 실행한 순간부터 state.json이 존재하도록 즉시 저장
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            raw_quizzes = data.get("quizzes", [])
            self.quizzes = [Quiz.from_dict(q) for q in raw_quizzes] if raw_quizzes else default_quizzes()
            self.best_score = data.get("best_score", 0)
        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            print("state.json 파일이 손상되어 기본 데이터로 시작합니다.")
            self.quizzes = default_quizzes()
            self.best_score = 0
            self.save_state()   # 손상된 파일을 정상 기본값으로 즉시 덮어써 복구

    def save_state(self) -> None:
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
        }
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
```

**주의 (헷갈리기 쉬운 부분 → 수정됨)**: 처음엔 `load_state()`가 파일이 없을 때 기본 데이터를 메모리에만 올려놓고 끝났었는데, 그러면 사용자가 퀴즈를 추가하거나 점수를 갱신하기 전까지는 `state.json`이 아예 생기지 않는 문제가 있었음. "초기 문제 데이터부터 계속 `state.json`이 유지돼야 한다"는 요구에 맞춰, 파일이 없거나 손상된 두 경우 모두 기본값을 세팅한 직후 `self.save_state()`를 바로 호출하도록 수정 — `QuizGame()` 객체를 만드는 순간(=프로그램을 처음 실행하는 순간) `state.json`이 곧바로 생성/복구됨.

---

## 이슈 15. 퀴즈 추가/점수 갱신 시 자동 저장 연결

**개념**
- `save_state()`는 이슈 14에서 "저장하는 방법"만 만든 것이고, 언제 호출할지는 정하지 않았음. 이슈 15는 그 호출 시점 두 곳을 연결하는 작업.
- ① `add_quiz()` 끝에서 새 퀴즈를 `append`한 직후 `save_state()` 호출 → 추가 직후 프로그램이 예기치 않게 꺼져도(정전, 강제종료 등) 방금 추가한 퀴즈가 유실되지 않음.
- ② `play()`에서 `self.best_score`를 갱신하는 조건문(`if score > self.best_score:`) 안에서 `save_state()` 호출 → 매번 풀 때마다 저장하는 게 아니라 **기록을 갱신했을 때만** 저장해서 불필요한 파일 쓰기를 줄임.
- 종료 시점(`main.py`의 선택지 5)에는 이미 위 두 지점에서 저장이 끝난 상태라 별도 저장 호출이 필수는 아니지만, "혹시 모를 유실"을 더 확실히 막고 싶다면 종료 직전에 한 번 더 저장하는 방어적 습관도 고려할 수 있음(현재 구현에는 미포함).

**코드** (`quiz.py`, 두 군데만 한 줄씩 추가)
```python
    def play(self) -> None:
        ...
        if score > self.best_score:
            self.best_score = score
            print("최고 점수를 갱신했습니다!")
            self.save_state()          # ← 추가

    def add_quiz(self) -> None:
        ...
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()              # ← 추가
        print("퀴즈가 추가되었습니다!")
```

---

## 이슈 16. README 최종 작성 (`develop`)

**개념**
- 제출용 문서라 브랜치를 따로 안 파고 `develop`에서 바로 작업 (문서/설정 변경은 GUIDE 3번 기준에 따라 feature 브랜치 없이 진행).
- README 필수 6항목(개요/주제선정이유/실행방법/기능목록/파일구조/데이터파일설명)의 `TODO` 주석을 실제 구현 내용에 맞춰 채움. 특히 "파일 구조"와 "데이터 파일 설명"은 이슈 7~15를 거치며 실제로 생긴 `quiz.py`, `utils.py`, `state.json` 스키마를 반영.
- 문서 작업 중 GUIDE 2번 체크리스트를 다시 훑다가, `KeyboardInterrupt`/`EOFError` 요건에 "저장"이 포함되어 있는데 실제 코드는 저장 없이 종료만 하고 있는 걸 발견 → 이슈 6에서 만든 구조를 보완(위 이슈 6 섹션의 "보완" 항목 참고). 이렇게 문서화 단계에서 요구사항을 다시 대조해보는 것도 코드 품질을 점검하는 한 방법.

**결과** (`README.md`) — 실행 방법, 파일 구조, `state.json` 스키마 설명을 실제 코드에 맞춰 채워 넣음. 자세한 내용은 `README.md` 참고.

---

## 이슈 18. 보너스 기능 (`feature/bonus`)

**개념**
- 세 가지를 한 번에 추가: **퀴즈 삭제**, **힌트**, **랜덤 출제**. GUIDE에서 언급된 후보 중 사용자가 이 세 개를 모두 선택.

**① 퀴즈 삭제**
- 메뉴가 5개(풀기/추가/목록/점수/종료)에서 6개로 늘어남 — "삭제"가 5번으로 들어가고 "종료"가 6번으로 밀림. `main.py`의 `read_int` 범위도 `1~5` → `1~6`으로 변경.
- `delete_quiz()`: 먼저 `list_quizzes()`로 번호와 함께 목록을 보여준 뒤, `read_int`로 삭제할 번호(1~len(quizzes))를 받아서 `self.quizzes.pop(index - 1)` (1-based 번호를 0-based 리스트 인덱스로 변환). 삭제 후 `save_state()`로 즉시 반영.

**② 힌트**
- `Quiz`에 `hint` 속성 추가 (기본값 `""`, 없어도 되는 선택 필드). `to_dict`/`from_dict`도 `hint`를 포함하도록 갱신 — `from_dict`는 `data.get("hint", "")`로 읽어서, 이 필드가 추가되기 전에 저장된 기존 `state.json`을 불러와도 `KeyError` 없이 동작(하위 호환).
- `play()`에서 정답 입력을 받는 부분을 `while True:` 루프로 감싸서, `read_int`의 최소값을 `0`으로 낮추고 "0을 입력하면 힌트"로 안내. `0`이 들어오면 힌트를 출력하고 `continue`로 다시 물어보고, 그 외 값이면 `break`해서 정상 채점 로직으로 진행.
- `add_quiz()`에 힌트 입력을 추가하되, 문제/선택지처럼 빈 값을 막지 않음 — 힌트는 선택 사항이라 그냥 엔터로 건너뛸 수 있게 함.

**③ 랜덤 출제**
- `play()` 시작 시 `self.quizzes.copy()`로 얕은 복사본을 만들고 `random.shuffle()`로 그 복사본만 섞음. `self.quizzes` 원본 순서는 그대로 유지 — `list_quizzes()`/`delete_quiz()`의 번호가 매번 바뀌면 사용자가 혼란스러우므로, "출제 순서"와 "목록/삭제용 순서"를 분리.

**코드** (`quiz.py`, 핵심 부분)
```python
class Quiz:
    def __init__(self, question, choices, answer, hint: str = ""):
        ...
        self.hint = hint

    def to_dict(self):
        return {"question": self.question, "choices": self.choices,
                 "answer": self.answer, "hint": self.hint}

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["choices"], data["answer"], data.get("hint", ""))


class QuizGame:
    def play(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        shuffled = self.quizzes.copy()
        random.shuffle(shuffled)

        score = 0
        for quiz in shuffled:
            quiz.display()
            while True:
                choice = read_int("정답 번호를 입력하세요 (힌트를 보려면 0): ", 0, len(quiz.choices))
                if choice == 0:
                    print(f"힌트: {quiz.hint}" if quiz.hint else "이 문제에는 힌트가 없습니다.")
                    continue
                break
            ...

    def delete_quiz(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        self.list_quizzes()
        index = read_int("삭제할 퀴즈 번호를 입력하세요: ", 1, len(self.quizzes))
        removed = self.quizzes.pop(index - 1)
        self.save_state()
        print(f"'{removed.question}' 퀴즈를 삭제했습니다.")
```

---

## 추가 기능. 풀 문제 개수 선택 (`feature/play-count`, 이슈 번호 없음)

**개념**
- GUIDE의 이슈 1~18과 별개로 사용자가 요청한 추가 기능. `play()` 시작 시 전체 퀴즈 개수를 먼저 안내하고, 몇 문제를 풀지 직접 입력받음. `read_int(prompt, 1, total)`을 그대로 재사용하기 때문에, 범위 밖 숫자를 입력하면 (이슈 5에서 만든 검증 로직이 그대로) 다시 물어봄 — 새로 검증 코드를 짤 필요가 없었음.
- 랜덤으로 섞은 전체 목록(`shuffled`)에서 앞의 `count`개만 슬라이싱(`shuffled[:count]`)해서 `selected`로 사용. "랜덤 순서"(이슈 18)와 "개수 선택"이 자연스럽게 합쳐짐 — 섞은 뒤 앞부분만 자르면 무작위로 고른 것과 같은 효과.
- **최고 점수 갱신 조건 변경**: 기존엔 "점수가 `best_score`보다 크면 무조건 갱신"이었는데, 이제 일부만 풀 수 있게 되면서 "5문제 중 최고 점수"라는 의미가 흔들릴 수 있음(예: 2문제만 풀어서 2/2를 받으면 그게 5문제 기준 최고 점수라 부르기 애매함). 그래서 `count == total`(전체 문제를 다 풀었을 때)일 때만 최고 점수 비교/저장을 하도록 제한. 일부만 풀었을 땐 그날의 점수만 보여주고 안내 문구로 이유를 설명.
- 기존 코드에 있던 사소한 버그도 같이 발견해서 고침: "최종 점수" 출력에서 분모를 `len(shuffled)`(항상 전체 개수)로 쓰고 있었는데, 실제로 푼 건 `selected`이므로 `len(selected)`로 고쳐야 정확함 (개수 선택 기능이 없던 이전까지는 `shuffled == selected`라 드러나지 않았던 버그).

**코드** (`quiz.py`, `play()`)
```python
def play(self) -> None:
    if not self.quizzes:
        print("등록된 퀴즈가 없습니다.")
        return

    total = len(self.quizzes)
    print(f"현재 등록된 퀴즈는 총 {total}개입니다.")
    count = read_int(f"몇 문제를 푸시겠습니까? (1~{total}): ", 1, total)

    shuffled = self.quizzes.copy()
    random.shuffle(shuffled)
    selected = shuffled[:count]

    score = 0
    for quiz in selected:
        quiz.display()
        while True:
            choice = read_int("정답 번호를 입력하세요 (힌트를 보려면 0): ", 0, len(quiz.choices))
            if choice == 0:
                print(f"힌트: {quiz.hint}" if quiz.hint else "이 문제에는 힌트가 없습니다.")
                continue
            break

        if quiz.check_answer(choice):
            print("정답입니다!")
            score += 1
        else:
            print(f"오답입니다. 정답은 {quiz.answer}번 이었습니다.")

    print(f"\n최종 점수: {score} / {len(selected)}")

    if count < total:
        print(f"(전체 {total}문제 중 {count}문제만 풀어서 최고 점수에는 반영되지 않습니다.)")
        return

    if score > self.best_score:
        self.best_score = score
        print("최고 점수를 갱신했습니다!")
        self.save_state()
```

---

## 추가 기능. 퀴즈 삭제 취소 + 풀이 기록 최신순 조회

**개념 ① 삭제 취소**
- `delete_quiz()`의 `read_int` 최소값을 `1`에서 `0`으로 낮추고, "취소하려면 0"이라고 안내. `0`이 들어오면 `pop` 없이 그냥 메시지 출력 후 `return` — 별도의 "정말 삭제하시겠습니까?" 확인 단계 없이, 번호 입력 자체를 취소 가능한 선택지로 만든 것.

**개념 ② 풀이 기록**
- 지금까지는 `best_score` 하나만 저장해서 "역대 최고 몇 점"만 알 수 있었음. 이제 `self.history`라는 리스트에 **매번 플레이할 때마다** 기록 하나(`{"date":..., "score":..., "total":...}`)를 추가해서, 언제 몇 문제 중 몇 개를 맞혔는지 전부 남김. (전체를 안 풀어도 기록되지만, `best_score` 갱신에는 전체를 풀었을 때만 반영 — 이 둘의 조건이 다름에 주의.)
- `datetime.now().strftime("%Y-%m-%d %H:%M")`로 기록 시각을 사람이 읽기 쉬운 문자열로 저장. JSON은 날짜 타입을 직접 저장 못 하므로 문자열로 변환해서 저장(직렬화)한 것 — 이슈 14에서 `Quiz.to_dict()`가 했던 것과 같은 이유.
- `show_score()`에서 `reversed(self.history)`로 순회 — 리스트에는 오래된 기록이 앞, 최신 기록이 뒤에 쌓이므로(항상 `append`), 화면에는 최신순으로 보여주려면 뒤집어서 순회하면 됨. 원본 리스트 자체를 뒤집는 게 아니라 순회 순서만 뒤집는 것이라 `self.history`의 저장 순서(오래된 것부터)는 그대로 유지됨.
- `play()`의 저장 로직도 같이 정리: 원래는 "최고 점수 갱신할 때만" `save_state()`를 호출했는데, 이제 매 플레이마다 기록을 남겨야 하므로 함수 끝에서 한 번만 `save_state()`를 호출하도록 단순화(조건 분기 3개가 있던 걸 `if/elif`로 정리하고 저장은 마지막에 공통으로).
- `state.json` 스키마에 `"history"` 필드가 새로 추가됨. `load_state()`는 `data.get("history", [])`로 읽어서, 이 필드가 없던 예전 `state.json`을 불러와도 에러 없이 빈 기록으로 시작(하위 호환 — 이슈 18의 `hint` 필드 추가 때와 같은 패턴).

**코드** (`quiz.py`, 핵심 변경 부분)
```python
def __init__(self, state_file: str = "state.json"):
    self.state_file = state_file
    self.quizzes: List[Quiz] = []
    self.best_score: int = 0
    self.history: List[Dict[str, Any]] = []
    self.load_state()

# play() 끝부분
print(f"\n최종 점수: {score} / {len(selected)}")

self.history.append({
    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "score": score,
    "total": len(selected),
})

if count < total:
    print(f"(전체 {total}문제 중 {count}문제만 풀어서 최고 점수에는 반영되지 않습니다.)")
elif score > self.best_score:
    self.best_score = score
    print("최고 점수를 갱신했습니다!")

self.save_state()

def show_score(self) -> None:
    if not self.history:
        print("아직 기록된 점수가 없습니다. 퀴즈를 풀어보세요!")
        return

    if self.best_score > 0:
        print(f"최고 점수: {self.best_score} / {len(self.quizzes)}")
    else:
        print("최고 점수: 아직 없음 (전체 문제를 다 풀면 기록됩니다)")

    print("\n[풀이 기록] (최신순)")
    for record in reversed(self.history):
        print(f"- {record['date']}  {record['score']} / {record['total']}")

def delete_quiz(self) -> None:
    if not self.quizzes:
        print("등록된 퀴즈가 없습니다.")
        return

    self.list_quizzes()
    index = read_int("삭제할 퀴즈 번호를 입력하세요 (취소하려면 0): ", 0, len(self.quizzes))
    if index == 0:
        print("삭제를 취소했습니다.")
        return

    removed = self.quizzes.pop(index - 1)
    self.save_state()
    print(f"'{removed.question}' 퀴즈를 삭제했습니다.")
```

---
