from MovieDTO import MovieData
from home.Home import home
from movie.MovieList import display_movies_list  # 영화 목록을 표시하는 함수
from auth.Auth import display_auth_menu
from search.Search import display_search_page
from mypage.MyPage import display_my_page


def main():
    MovieData.check_file()  # director.txt 및 movie.txt 파일이 존재하는지 확인하고 없으면 생성
    result = MovieData.load_director_data()
    if not result:
        return
    result = MovieData.load_movie_data()
    if not result:
        return
    print("감독 및 영화 데이터가 성공적으로 로드됨")

    while True:
        user_id = display_auth_menu()

        while True:
            selected_number = home()


            if selected_number == 0:
                print('서비스를 종료합니다.')
                exit(0)
            elif selected_number == 1:
                # MovieList 클래스의 인스턴스를 생성하고 display_movie_list 메서드 호출
                display_movies_list(user_id)
            elif selected_number == 2:
                display_search_page(user_id)
            elif selected_number == 3:
                display_my_page(user_id)
            else:
                print("잘못된 입력입니다. 메뉴 번호를 입력해주세요.")


if __name__ == "__main__":
    main()