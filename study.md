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

**코드** (`main.py`)
```python
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n프로그램을 안전하게 종료합니다. (Ctrl+C 감지)")
    except EOFError:
        print("\n입력이 종료되어 프로그램을 안전하게 종료합니다.")
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

<!-- 이후 이슈(8~)는 여기에 이어서 추가 -->
