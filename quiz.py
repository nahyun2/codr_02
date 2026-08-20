import json
import os
import random
from datetime import datetime
from typing import Any, Dict, List

from utils import read_int


class Quiz:
    """퀴즈 문제 하나(질문/선택지/정답)를 표현하는 클래스."""

    def __init__(self, question: str, choices: List[str], answer: int, hint: str = ""):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("question은 비어있지 않은 문자열이어야 합니다.")
        if not isinstance(choices, list) or len(choices) < 2:
            raise ValueError("choices는 최소 2개 이상의 리스트여야 합니다.")
        if not isinstance(answer, int) or not (1 <= answer <= len(choices)):
            raise ValueError(f"answer는 1~{len(choices)} 사이의 정수여야 합니다.")

        self.question = question
        self.choices = choices
        self.answer = answer  # choices의 1-based 인덱스
        self.hint = hint

    def display(self) -> None:
        """문제와 선택지를 번호와 함께 출력한다."""
        print(f"\nQ. {self.question}")
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_choice: int) -> bool:
        """user_choice가 정답 번호와 같은지 반환한다."""
        return user_choice == self.answer

    def to_dict(self) -> Dict[str, Any]:
        """state.json에 저장할 수 있도록 dict 형태로 변환한다."""
        return {"question": self.question, "choices": self.choices, "answer": self.answer, "hint": self.hint}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Quiz":
        """state.json에서 읽어온 dict로부터 Quiz 객체를 만든다."""
        return cls(data["question"], data["choices"], data["answer"], data.get("hint", ""))


def default_quizzes() -> List[Quiz]:
    """기본 넌센스 퀴즈 5개를 생성해 반환한다."""
    raw = [
        ("백가지 과일이 죽기 직전을 다른 말로?",
         ["백과사전", "백조", "과실사고", "과일농장"], 1,
         "한 글자씩 보세요."),
        ("A젖소와 B젖소가 싸움을 했는데 B젖소가 이겼다. 이유는?",
         ["삐졌소", "비겼소", "에이졌소", "에이비졌소"], 3,
         "A젖소와 B젖소가 어떻게 됐는지 상상해보세요."),
        ("깨뜨리고 칭찬 받는 것은?",
         ["계란", "유리", "신기록", "수박"], 3,
         "넷 중에 어떤 걸 깨야 칭찬받을까요."),
        ("청바지를 돋보이게하는 걸음 걸이는?",
         ["에메랄드 반지", "다이아목걸이", "루비귀걸이", "진주목걸이"], 4,
         "청바지는 영어로 뭘까요"),
        ("무가 자기소개할 때 하는 말은?",
         ["무슨 일이에요?", "나무", "무엇이든 물어보세요", "무한도전"], 2,
         "힌트없음"),
    ]
    return [Quiz(q, c, a, h) for q, c, a, h in raw]


class QuizGame:
    """퀴즈 목록/최고 점수 상태를 갖고 게임 전체 흐름을 관리하는 클래스."""

    def __init__(self, state_file: str = "state.json"):
        self.state_file = state_file
        self.quizzes: List[Quiz] = []
        self.best_score: int = 0
        self.history: List[Dict[str, Any]] = []
        self.load_state()

    def load_state(self) -> None:
        """state_file에서 퀴즈 목록과 최고 점수를 불러온다.

        파일이 없거나 JSON이 손상된 경우 기본 퀴즈 데이터로 대체하고,
        그 기본 데이터를 곧바로 state_file에 저장해 처음 실행한 순간부터
        state.json이 계속 유지되도록 한다.
        """
        if not os.path.exists(self.state_file):
            self.quizzes = default_quizzes()
            self.best_score = 0
            self.history = []
            self.save_state()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            raw_quizzes = data.get("quizzes", [])
            self.quizzes = [Quiz.from_dict(q) for q in raw_quizzes] if raw_quizzes else default_quizzes()
            self.best_score = data.get("best_score", 0)
            self.history = data.get("history", [])
        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            print("state.json 파일이 손상되어 기본 데이터로 시작합니다.")
            self.quizzes = default_quizzes()
            self.best_score = 0
            self.history = []
            self.save_state()

    def save_state(self) -> None:
        """현재 퀴즈 목록/최고 점수/풀이 기록을 state_file에 JSON(UTF-8)으로 저장한다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
        }
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def show_menu(self) -> None:
        """메뉴 화면을 출력한다."""
        print("=" * 20)
        print("🎯 넌센스 퀴즈 게임 🎯")
        print("=" * 20)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")
        print("=" * 20)

    def play(self) -> None:
        """사용자가 고른 개수만큼 퀴즈를 무작위 순서로 출제 및 채점한다.

        전체 퀴즈를 다 풀었을 때만 최고 점수를 갱신한다(적은 개수만 풀면
        "N개 중 최고 점수"라는 의미가 흐려지므로).
        """
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

    def add_quiz(self) -> None:
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
        hint = input("힌트를 입력하세요 (없으면 그냥 엔터): ").strip()

        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.save_state()
        print("퀴즈가 추가되었습니다!")

    def list_quizzes(self) -> None:
        """등록된 모든 퀴즈의 문제와 정답 번호를 목록으로 출력한다."""
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n총 {len(self.quizzes)}개의 퀴즈가 등록되어 있습니다.")
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"{i}. {quiz.question} (정답: {quiz.answer}번)")

    def show_score(self) -> None:
        """최고 점수와 지금까지의 풀이 기록을 최신순으로 출력한다."""
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
        """번호를 입력받아 해당 퀴즈를 목록에서 삭제한다."""
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
