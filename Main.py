from MovieDTO import MovieData
from movie.MovieInfo import display_movie_details

def main():
    movieData_instance = MovieData() # MovieData 클래스 인스턴스 생성 및 movie.txt 파일 확인 및 로드

    print(movieData_instance.movies.keys())
    movieData_instance.movies[1]['year'] = 2021
    movieData_instance.update_movie_file()

    display_movie_details()
if __name__ == "__main__":
    main()