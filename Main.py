from MovieDTO import MovieData
# from auth.Auth import display_auth_menu
from movie.MovieList import display_movies_list  # 영화 목록을 표시하는 함수
from movie.MovieInfo import display_movie_details  # 영화 상세 정보를 표시하는 함수
from mypage.MyPage import display_myPage


def main():
    MovieData.check_file()  # movie.txt 파일이 존재하는지 확인

    selected_movie_id = display_movies_list()

    if selected_movie_id is not None:
        display_movie_details(selected_movie_id)
1
    # display_auth_menu()


if __name__ == "__main__":
    main()
