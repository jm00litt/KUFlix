from MovieDTO import MovieData
# from auth.Auth import display_auth_menu
from movie.MovieList import display_movies_list  # 영화 목록을 표시하는 함수
from movie.MovieInfo import display_movie_details  # 영화 상세 정보를 표시하는 함수
from auth.Auth import display_auth_menu


def main():
    MovieData.check_file()  # movie.txt 파일이 존재하는지 확인
    MovieData.load_movie_data()

    user_id = display_auth_menu()
    
    from home import Home
    home = Home.Home(user_id) #Home 객체 생성
    home.home()

if __name__ == "__main__":
    main()
