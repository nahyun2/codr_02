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
        choice = input("선택: ")

        if choice == "5":
            print("종료합니다.")
            break
        else:
            print(f"{choice}번은 아직 준비 중입니다")


if __name__ == "__main__":
    main()