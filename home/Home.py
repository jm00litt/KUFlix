def home():
    """
    홈 화면의 메인 로직을 처리합니다.
    사용자의 입력을 받아 해당하는 메뉴로 이동합니다.
    
    Returns:
        int: 선택된 메뉴 번호 (0-3)
    """
    # 메뉴는 처음 한 번만 표시
    print("\n" + "=" * 50)
    print("KUFLIX 홈")
    print("=" * 50)
    print("1. 영화 리스트")
    print("2. 영화 검색")
    print("3. 마이페이지")
    print("0. 종료")
    print("=" * 50)
    
    while True:
        selected_number = input("선택할 메뉴 번호를 입력하세요(0-3): ").strip()

        if selected_number != selected_number.lstrip('0') and selected_number != '0':
            print("존재하지 않는 메뉴 번호입니다.")
            continue
    
        # 숫자가 아닌 입력 처리
        if not selected_number.isdigit():
            print("숫자만 입력하세요.")
            continue
            
        # 숫자로 변환
        number = int(selected_number)
        
        # 범위 검사
        if number not in range(0, 4):
            print("존재하지 않는 메뉴 번호입니다.")
            continue
            
        # 유효한 입력인 경우 반환
        return number