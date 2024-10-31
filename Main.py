from MovieDTO import MovieData
from logIn.LogIn import LogIn

def main():
    print("여기서 부터 시작")

    movieData_instance = MovieData() # MovieData 클래스 인스턴스 생성 및 movie.txt 파일 확인 및 로드
    login_instance = LogIn() # LogIn 클래스 인스턴스 생성

    print(movieData_instance.movies.keys())
    movieData_instance.movies[1]['year'] = 2021
    movieData_instance.update_movieFile()

    # LogIn 클래스 내 메서드 호출
    # login_instance.authenticate("조하상", "조하상123")
    # login_instance.authenticate("송재현Test", "송재현Test")
    
if __name__ == "__main__":
    main()