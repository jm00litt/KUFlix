from MovieDTO import MovieData
# from auth.Auth import display_auth_menu
from movie.MovieList import display_movies_list  # 영화 목록을 표시하는 함수
from movie.MovieInfo import display_movie_details  # 영화 상세 정보를 표시하는 함수
from auth.Auth import display_auth_menu


def main():
    MovieData.check_file()  # movie.txt 파일이 존재하는지 확인

    display_auth_menu()



if __name__ == "__main__":
    main()
