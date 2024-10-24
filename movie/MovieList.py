# 영화 카테고리 리스트 프롬프트


def get_movies(file_name="movie.txt"):
    # 영화 정보를 저장할 딕셔너리 초기화
    movies = {}  # 영화 ID를 키로, 영화 정보를 값으로 저장할 딕셔너리

    try:
        # 파일 열기 및 읽기
        with open(file_name, "r", encoding="utf-8") as file:  # movie.txt 파일을 읽기 모드로 열기
            for line in file:
                # 각 줄을 읽어와 슬래시(/)를 기준으로 문자열 분리하여 리스트로 저장
                data = line.strip().split('/')  

                # 각 요소를 변수로 할당
                movie_id = data[0]          # 영화 ID
                title = data[1]             # 영화 제목
                year = int(data[2])         # 개봉 연도
                director = data[3]          # 감독명
                genre = data[4]             # 장르
                runtime = int(data[5])      # 러닝타임
                views = int(data[6])        # 조회수
                rating = float(data[7])     # 평점
                rating_count = int(data[8]) # 평가 인원 수

                # 영화 정보를 딕셔너리 형태로 저장
                movies[movie_id] = {
                    "title": title,
                    "year": year,
                    "director": director,
                    "genre": genre,
                    "runtime": runtime,
                    "views": views,
                    "rating": rating,
                    "rating_count": rating_count
                }

    # 파일이 존재하지 않을 때의 예외 처리
    except FileNotFoundError:
        print(f"Error: 파일 '{file_name}'을 찾을 수 없습니다.")
    # 파일 인코딩 오류 처리
    except UnicodeDecodeError:
        print(f"Error: 파일 '{file_name}'을 읽는 중 인코딩 오류가 발생했습니다.")
    # 기타 예외 처리
    except Exception as e:
        print(f"Error: 파일을 읽는 중 오류가 발생했습니다 - {e}")

    # 최종적으로 영화 ID를 키로, 영화 정보를 값으로 하는 딕셔너리 반환
    return movies