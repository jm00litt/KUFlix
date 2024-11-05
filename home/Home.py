class Home:
    def __init__(self):
        self._userId = ""  # 현재 로그인한 사용자의 ID를 저장하는 전역 변수
    
    def setUserId(self, userId: str):
        """로그인한 사용자의 ID를 설정합니다."""
        self._userId = userId
    
    def getUserId(self) -> str:
        """현재 로그인한 사용자의 ID를 반환합니다."""
        return self._userId

    def display_menu(self):
        """홈 메뉴 화면을 출력합니다."""
        print("\n" + "=" * 30)
        print("KUFLIX 홈")
        print("=" * 30)
        print("1. 영화 리스트")
        print("2. 영화 검색")
        print("3. 마이페이지")
        print("0. 종료")
        print("=" * 30)

    def home(self):
        """
        홈 화면의 메인 로직을 처리합니다.
        사용자의 입력을 받아 해당하는 메뉴로 이동합니다.
        """
        while True:
            self.display_menu()
            
            try:
                selected_number = input("선택할 메뉴를 입력하세요(0-3): ")
                
                # 입력값 검증
                if not selected_number.isdigit():
                    raise ValueError("존재하지 않는 메뉴 번호입니다.")
                
                selected_number = int(selected_number)
                
                if selected_number == 0:
                    print("\n프로그램을 종료합니다.")
                    break
                elif selected_number == 1:
                    # MovieList 클래스의 인스턴스를 생성하고 display_movie_list 메서드 호출
                    from movie.MovieList import display_movies_list
                    from movie.MovieInfo import display_movie_details
                    selected_movie_id = display_movies_list()
                    if selected_movie_id is not None:
                        display_movie_details(self._userId,selected_movie_id)
                elif selected_number == 2:
                    from search.Search import display_search_page
                    display_search_page(self._userId)
                elif selected_number == 3:
                    from mypage.MyPage import display_my_page
                    display_my_page(self._userId)
                else:
                    raise ValueError("잘못된 입력입니다. 메뉴 번호를 입력해주세요.")
                    
            except ValueError as e:
                print(f"\n오류: {str(e)}")
                continue
            except Exception as e:
                print(f"\n오류가 발생했습니다: {str(e)}")
                continue