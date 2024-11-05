def display_menu():
    """홈 메뉴 화면을 출력합니다."""
    print("\n" + "=" * 30)
    print("KUFLIX 홈")
    print("=" * 30)
    print("1. 영화 리스트")
    print("2. 영화 검색")
    print("3. 마이페이지")
    print("0. 종료")
    print("=" * 30)


def home():
    """
    홈 화면의 메인 로직을 처리합니다.
    사용자의 입력을 받아 해당하는 메뉴로 이동합니다.
    """
    while True:
        display_menu()

        try:
            selected_number = input("선택할 메뉴 번호를 입력하세요(0-3): ")

            # 입력값 검증
            if not selected_number.isdigit():
                print("숫자만 입력하세요.")
                continue

            selected_number = int(selected_number)

            if selected_number not in range(0, 4):
                print("존재하지 않는 메뉴 번호입니다.")
                continue
            else:
                return selected_number

        except ValueError as e:
            print(f"\n오류: {str(e)}")
            continue
        except Exception as e:
            print(f"\n오류가 발생했습니다: {str(e)}")
            continue
