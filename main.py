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


def main():
    while True:
        print_menu()
        # read_int가 빈 입력, 숫자가 아닌 입력, 1~5 범위 밖 입력을
        # 전부 걸러내고 재입력을 요청하므로 여기서는 별도 검증이 필요 없다.
        choice = read_int("선택: ", 1, 5)

        if choice == 5:
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
