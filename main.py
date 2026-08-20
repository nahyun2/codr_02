from quiz import QuizGame
from utils import read_int


def main():
    game = QuizGame()

    try:
        while True:
            game.show_menu()
            # read_int가 빈 입력, 숫자가 아닌 입력, 1~5 범위 밖 입력을
            # 전부 걸러내고 재입력을 요청하므로 여기서는 별도 검증이 필요 없다.
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
    except KeyboardInterrupt:
        game.save_state()
        print("\n프로그램을 안전하게 종료합니다. (Ctrl+C 감지)")
    except EOFError:
        game.save_state()
        print("\n입력이 종료되어 프로그램을 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
