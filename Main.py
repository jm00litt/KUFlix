from MovieDTO import MovieData
from movie.MovieInfo import display_movie_details

def main():
    MovieData.check_file()     # movie.txt 파일이 존재하는지 확인
    if not MovieData.load_movieData():
        print("프로그램을 종료합니다.")

    print(MovieData.movies.keys())
    MovieData.movies[1]['year'] = 2021
    MovieData.update_movieFile()
    # display_auth_menu()
    
    #display_movie_details()

if __name__ == "__main__":
    main()
