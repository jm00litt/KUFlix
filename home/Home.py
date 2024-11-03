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
                selected_number = input("메뉴를 선택하세요: ")
                
                # 입력값 검증
                if not selected_number.isdigit():
                    raise ValueError("잘못된 입력입니다. 메뉴 번호를 입력해주세요.")
                
                selected_number = int(selected_number)
                
                if selected_number == 0:
                    print("\n프로그램을 종료합니다.")
                    break
                elif selected_number == 1:
                    # MovieList 클래스의 인스턴스를 생성하고 display_movie_list 메서드 호출
                    from movie.MovieList import MovieList
                    movie_list = MovieList()
                    movie_list.choose_genre()
                elif selected_number == 2:
                    # Search 클래스의 인스턴스를 생성하고 display_searchpage 메서드 호출
                    from search.Search import Search
                    search = Search()
                    search.display_searchpage()
                elif selected_number == 3:
                    # MyPage 클래스의 인스턴스를 생성하고 display_mypage 메서드 호출
                    from mypage.MyPage import MyPage
                    mypage = MyPage()
                    if mypage.load_user(self._userId):
                        mypage.display_mypage()
                else:
                    raise ValueError("잘못된 입력입니다. 메뉴 번호를 입력해주세요.")
                    
            except ValueError as e:
                print(f"\n오류: {str(e)}")
                continue
            except Exception as e:
                print(f"\n오류가 발생했습니다: {str(e)}")
                continue