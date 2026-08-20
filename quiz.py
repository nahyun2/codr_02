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
