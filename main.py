from quiz import Quiz, default_quizzes
from utils import read_int


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


def play_quizzes(quizzes):
    """퀴즈 목록을 순서대로 출제하고 채점한 뒤 최종 점수를 반환한다."""
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return 0

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
    return score


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


def list_quizzes(quizzes):
    """등록된 모든 퀴즈의 문제와 정답 번호를 목록으로 출력한다."""
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return

    print(f"\n총 {len(quizzes)}개의 퀴즈가 등록되어 있습니다.")
    for i, quiz in enumerate(quizzes, start=1):
        print(f"{i}. {quiz.question} (정답: {quiz.answer}번)")


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
        # read_int가 빈 입력, 숫자가 아닌 입력, 1~5 범위 밖 입력을
        # 전부 걸러내고 재입력을 요청하므로 여기서는 별도 검증이 필요 없다.
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n프로그램을 안전하게 종료합니다. (Ctrl+C 감지)")
    except EOFError:
        print("\n입력이 종료되어 프로그램을 안전하게 종료합니다.")
