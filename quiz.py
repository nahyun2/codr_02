import json
import os
from typing import Any, Dict, List

from utils import read_int


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

    def to_dict(self) -> Dict[str, Any]:
        """state.json에 저장할 수 있도록 dict 형태로 변환한다."""
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Quiz":
        """state.json에서 읽어온 dict로부터 Quiz 객체를 만든다."""
        return cls(data["question"], data["choices"], data["answer"])


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


class QuizGame:
    """퀴즈 목록/최고 점수 상태를 갖고 게임 전체 흐름을 관리하는 클래스."""

    def __init__(self, state_file: str = "state.json"):
        self.state_file = state_file
        self.quizzes: List[Quiz] = []
        self.best_score: int = 0
        self.load_state()

    def load_state(self) -> None:
        """state_file에서 퀴즈 목록과 최고 점수를 불러온다.

        파일이 없거나 JSON이 손상된 경우 기본 퀴즈 데이터로 대체한다.
        """
        if not os.path.exists(self.state_file):
            self.quizzes = default_quizzes()
            self.best_score = 0
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

    def save_state(self) -> None:
        """현재 퀴즈 목록과 최고 점수를 state_file에 JSON(UTF-8)으로 저장한다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
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
        print("5. 종료")
        print("=" * 20)

    def play(self) -> None:
        """등록된 모든 퀴즈를 순서대로 출제 및 채점하고, 최고 점수를 갱신한다."""
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

        self.quizzes.append(Quiz(question, choices, answer))
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
        """지금까지 기록된 최고 점수를 출력한다."""
        if self.best_score <= 0:
            print("아직 기록된 점수가 없습니다. 퀴즈를 풀어보세요!")
        else:
            print(f"최고 점수: {self.best_score} / {len(self.quizzes)}")
