import os

class MovieData:

    # director.txt와 movie.txt의 경로
    DATA_FILE = os.path.join(os.path.dirname(__file__), "data")
    DIRECTOR_TXT = os.path.join(DATA_FILE, "director.txt")
    MOVIE_TXT = os.path.join(DATA_FILE, "movie.txt")

    # 클래스 변수로 movies 정의
    directors = {}  # ***!!! 외부에서 사용하지 마세요 !!!***
    movies = {}  # 영화 정보를 (프롬프트의 출력 형태로) 저장할 딕셔너리

    @classmethod
    def check_file(cls):
        if not os.path.exists(cls.DIRECTOR_TXT):
            with open(cls.DIRECTOR_TXT, 'w', newline='') as file:
                file.write("")  # 빈 파일로 생성
            print("director.txt 파일이 존재하지 않아 생성합니다.")

        if not os.path.exists(cls.MOVIE_TXT):
            with open(cls.MOVIE_TXT, 'w', newline='') as file:
                file.write("")  # 빈 파일로 생성
            print("movie.txt 파일이 존재하지 않아 생성합니다.")

    @classmethod
    def load_director_data(cls):
        # 파일 읽기
        if os.path.exists(cls.DIRECTOR_TXT):
            used_ids = set()  # 이미 사용된 감독 아이디를 추적하기 위한 세트
            
            with open(cls.DIRECTOR_TXT, 'r', encoding='utf-8', newline='') as file:
                for line in file:
                    # 양끝 공백 제거 및 필드 분리
                    elements = [element.strip() for element in line.split('/')]
                    
                    # 필드 개수 검사
                    if len(elements) != 2:
                        print(f"필드 개수 형식 오류: {line}")
                        return False

                    # 필드 변수 할당
                    ids_part, name = elements
                    ids = [id.strip() for id in ids_part.split(',')]  # 감독 아이디 분리

                    # 중복된 감독 아이디가 있는지 확인
                    for director_id in ids:
                        if director_id in used_ids:
                            print(f"중복된 감독 아이디 오류: {director_id}")
                            return False  # 중복된 감독 아이디가 있을 경우 False 반환
                        
                        used_ids.add(director_id)  # 사용된 아이디 세트에 추가

                    # 감독 아이디 중복 여부 설정
                    is_duplicate = len(ids) > 1
                    for director_id in ids:
                        cls.directors[(int(director_id), "name")] = name
                        cls.directors[(int(director_id), "is_dup")] = is_duplicate
                    
        return True

    @classmethod
    def load_movie_data(cls):
        seen_ids = set()  # 영화 아이디를 저장할 집합 (중복 검사)

        with open(cls.MOVIE_TXT, 'r', encoding='utf-8', newline='') as file:
            for line in file:
                # 양끝 공백 제거 및 필드 분리
                line = line.strip()
                elements = [element.strip() for element in line.split('/')]

                # 필드 개수 검사
                if len(elements) != 10:
                    print(f"필드 개수 형식 오류: {line}")
                    return False

                # 필드 변수 할당
                movie_id_str, title, year, director_ids, genres, runtime, views, average_rating, rating_count, user_ratings = elements
                movie_id = int(movie_id_str)  # movie_id를 정수형으로 변환

                # 중복된 영화 아이디가 있는지 확인
                if movie_id in seen_ids:
                    print(f"중복된 영화 아이디: {movie_id}")
                    return False
                seen_ids.add(movie_id)  # 아이디를 집합에 추가

                # 장르를 쉼표로 구분된 문자열에서 리스트로 변환
                genre_list = [genre.strip() for genre in genres.split(',')]

                # 문법 형식 검사
                if not cls.validate_movie_data(movie_id_str, title, year, director_ids, genre_list, runtime, views, average_rating, rating_count, user_ratings):
                    return False
                
                # director_ids에 따라 대응되는 감독명을 문자열로 저장
                director_id_list = [int(element.strip()) for element in director_ids.split(',')]

                # 감독명 문자열 생성
                director_names = []
                for director_id in director_id_list:
                    # 감독명 추출
                    name = cls.directors.get((director_id, "name"))
                    is_dup = cls.directors.get((director_id, "is_dup"))

                    # 중복 여부에 따라 이름 저장 방식 결정
                    if is_dup:
                        director_names.append(f"{name} #{director_id}")
                    else:
                        director_names.append(name)

                # 10번째 필드(마지막 필드)를 ','를 기준으로 나누고 list로 저장
                user_ratings_list = user_ratings.split(',')

                # movies 딕셔너리에 출력 형태 저장
                cls.movies[movie_id] = {
                    "title": title,
                    "year": int(year),  # release_year를 year로 변경
                    "directors": ', '.join(director_names),   # 출력 방식대로 문자열을 저장 - 예) "봉준호 #2, 크리스토퍼 놀란"
                    "genre": genre_list, # 장르를 리스트로 저장
                    "runtime": int(runtime),
                    "views": int(views),
                    "average_rating": float(average_rating),
                    "rating_count": int(rating_count),  # review_count를 rating_count로 변경
                    "user_ratings": user_ratings_list,  # 예) ["test123:4.0", "test456,2.5"]
                    "director_ids": director_id_list   # ***!!! 외부에서 사용하지 마세요 !!!***
                }
        return True

    # 문법 형식 검사
    @classmethod
    def validate_movie_data(cls, movie_id, title, year, director_ids, genre_list, runtime, views, rating, rating_count, user_rating):
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

        # 감독명: 길이 1~20, 한글/영문 -> 길이 상관없이 숫자만 반점으로 구분
        if not (all(c.isdigit() or c == ',' for c in director_ids)  # 숫자와 반점만 포함
                and ',,' not in director_ids                        # 반점이 연속으로 나오지 않음
                and not director_ids.startswith(',')               # 시작이 반점이 아님
                and not director_ids.endswith(',')):               # 끝이 반점이 아님
            print(f"감독명 형식 오류: {director_ids}")
            return False

        # 장르: 리스트여야 하며, 허용된 장르만 포함
        valid_genres = ['액션', '코미디', '로맨스', '호러', 'SF']
        if not isinstance(genre_list, list) or not all (genre in valid_genres for genre in genre_list):
            print(f"장르 형식 오류: {genre_list}")
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
        
        # user_rating 문법 형식 체크(현재 검사 안함)

        return True

    @classmethod
    def update_movie_file(cls):
        file_path = os.path.join(os.path.dirname(__file__), "data/movie.txt")

        with open(file_path, 'w', encoding='utf-8', newline='') as file:
            for movie_id, data in cls.movies.items():
                # 장르 및 사용자 평가를 리스트를 쉼표로 연결
                genres_str = ','.join(data['genre'])
                director_ids = ','.join(map(str, data['director_ids']))

                # user_ratings 처리: 처음 추가된 데이터는 쉼표 없이, 이후는 쉼표로 구분
                if data['user_ratings']:
                    user_ratings = ','.join(data['user_ratings'])  # 쉼표로 구분
                else:
                    user_ratings = ""  # 빈 경우

                line = f"{movie_id}/{data['title']}/{data['year']}/{director_ids}/" \
                   f"{genres_str}/{data['runtime']}/{data['views']}/" \
                   f"{data['average_rating']}/{data['rating_count']}/" \
                   f"{user_ratings}\n"

                file.write(line)
