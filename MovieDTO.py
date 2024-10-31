import os

class MovieData:
    def __init__(self):
        self.movies = {}  # 영화 정보를 저장할 딕셔너리
        self.check_file()  # 파일 존재 여부 체크
        if not self.load_movieData():  # 영화 데이터 로드
            print("영화 데이터를 로드하는 데 실패했습니다.")

    def check_file(self):
        file_path = os.path.join(os.path.dirname(__file__), "movie.txt")
        print(os.getcwd())
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write("")  # 빈 파일로 생성
            print("movie.txt 파일이 존재하지 않아 생성합니다.")
        else:
            print("movie.txt 파일이 존재합니다.")

    def load_movieData(self):
        file_path = os.path.join(os.path.dirname(__file__), "movie.txt")

        seen_ids = set()  # 영화 아이디를 저장할 집합 (중복 검사)

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # 줄 끝의 공백 제거 및 슬래시로 분리
                line = line.strip()
                elements = [element.strip() for element in line.split('/')]

                if len(elements) != 9:
                    print(f"잘못된 형식: {line}")
                    return False

                # movie_id를 정수형으로 변환
                movie_id_str, title, year, director, genre, runtime, views, rating, rating_count = elements
                movie_id = int(movie_id_str)  # movie_id를 정수형으로 변환

                # 중복 아이디 검증
                if movie_id in seen_ids:
                    print(f"중복된 영화 아이디: {movie_id}")
                    return False
                seen_ids.add(movie_id)  # 아이디를 집합에 추가

                # 규칙에 따른 검증
                if not self.validate_movie_data(movie_id_str, title, year, director, genre, runtime, views, rating, rating_count):
                    return False

                # 딕셔너리에 영화 데이터 추가
                self.movies[movie_id] = {
                    "title": title,
                    "year": year,  # release_year를 year로 변경
                    "director": director,
                    "genre": genre,
                    "runtime": runtime,
                    "views": views,
                    "rating": rating,
                    "rating_count": rating_count  # review_count를 rating_count로 변경
                }

        return True

    def validate_movie_data(self, movie_id, title, year, director, genre, runtime, views, rating, rating_count):
        # 영화 아이디: 중복되지 않으며 0 이상의 정수
        if not (movie_id.isdigit() and int(movie_id) >= 0):
            print(f"영화 아이디 형식 오류: {movie_id}")
            return False

        # 영화 제목: 길이 1~50
        if not (1 <= len(title) <= 50):
            print(f"영화 제목 형식 오류: {title}")
            return False

        # 개봉년도: 4자리 숫자
        if not (year.isdigit() and len(year) == 4):
            print(f"개봉년도 형식 오류: {year}")
            return False

        # 감독명: 길이 1~20, 한글/영문
        if not (1 <= len(director) <= 20 and all(c.isalpha() or c.isspace() for c in director)):
            print(f"감독명 형식 오류: {director}")
            return False

        # 장르: 허용된 장르 중 하나
        valid_genres = ['액션', '코미디', '로맨스', '공포', 'SF']
        if genre.strip() not in valid_genres:
            print(f"장르 형식 오류: {genre}")
            return False

        # 러닝타임: 1 이상의 숫자
        if not (runtime.isdigit() and int(runtime) > 0):
            print(f"러닝타임 형식 오류: {runtime}")
            return False

        # 조회수: 0 이상의 정수
        if not (views.isdigit() and int(views) >= 0):
            print(f"조회수 형식 오류: {views}")
            return False

        # 평점: 0.0에서 5.0 사이의 실수
        try:
            rating_float = float(rating)
            if len(rating) != 3:
                print(f"평점 길이 오류: {rating} (길이는 3이어야 합니다.)")
                return False
            if not (0.0 <= rating_float <= 5.0):
                print(f"평점 형식 오류: {rating}")
                return False
        except ValueError:
            print(f"평점 변환 오류: {rating}")
            return False

        # 평가 인원 수: 0 이상의 정수
        if not (rating_count.isdigit() and int(rating_count) >= 0):
            print(f"평가 인원 수 형식 오류: {rating_count}")
            return False

        return True
