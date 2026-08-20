from quiz import default_quizzes
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
        # read_int가 빈 입력, 숫자가 아닌 입력, 1~5 범위 밖 입력을
        # 전부 걸러내고 재입력을 요청하므로 여기서는 별도 검증이 필요 없다.
        choice = read_int("선택: ", 1, 5)

        if choice == 1:
            play_quizzes(quizzes)
        elif choice == 5:
            print("종료합니다.")
            break
        else:
            print(f"{choice}번은 아직 준비 중입니다")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n프로그램을 안전하게 종료합니다. (Ctrl+C 감지)")
    except EOFError:
        print("\n입력이 종료되어 프로그램을 안전하게 종료합니다.")
