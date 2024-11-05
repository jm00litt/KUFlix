from MovieDTO import MovieData
# from auth.Auth import display_auth_menu
from movie.MovieList import display_movies_list  # 영화 목록을 표시하는 함수
from movie.MovieInfo import display_movie_details  # 영화 상세 정보를 표시하는 함수
from auth.Auth import display_auth_menu


def main():
    MovieData.check_file()  # movie.txt 파일이 존재하는지 확인
    MovieData.load_movie_data()

    while True : 
        user_id = display_auth_menu()
        from home.Home import Home
        home = Home() #Home 객체 생성
        home.setUserId(user_id)
        
        while True : 
            selected_number = home.home()
            if selected_number == 0:
                print('초기화면으로 돌아갑니다.\n')
                break
            elif selected_number == 1:
                # MovieList 클래스의 인스턴스를 생성하고 display_movie_list 메서드 호출
                from movie.MovieList import display_movies_list
                from movie.MovieInfo import display_movie_details
                selected_movie_id = display_movies_list()
                if selected_movie_id is not None:
                    display_movie_details(home._userId,selected_movie_id)
            elif selected_number == 2:
                from search.Search import display_search_page
                display_search_page(home._userId)
            elif selected_number == 3:
                from mypage.MyPage import display_my_page
                display_my_page(home._userId)
            else:
                print("잘못된 입력입니다. 메뉴 번호를 입력해주세요.")

if __name__ == "__main__":
    main()