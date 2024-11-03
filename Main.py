from MovieDTO import MovieData
from movie.MovieList import display_movies_list  # 영화 목록을 표시하는 함수
from movie.MovieInfo import display_movie_details  # 영화 상세 정보를 표시하는 함수


def main():
    selected_movie_id = display_movies_list()

    if selected_movie_id is not None:
        display_movie_details(selected_movie_id)


if __name__ == "__main__":
    main()
