# 영화 리스트 프롬프트

def get_movies(file_name="movie.txt"):
    # 영화 정보를 저장할 딕셔너리 초기화
    movies = {}  # 영화 ID를 키로, 영화 정보를 값으로 저장할 딕셔너리

    try:
        # 파일 열기 및 읽기
        with open(file_name, "r", encoding="utf-8") as file:  # movie.txt 파일을 읽기 모드로 열기
            for line in file:
                # 각 줄을 읽어와 슬래시(/)를 기준으로 문자열 분리하여 리스트로 저장
                data = line.strip().split('/')  

                # 데이터가 예상하는 필드 수(9개)와 일치하는지 확인
                if len(data) != 9:
                    print("Warning: 데이터 필드 수가 일치하지 않습니다.", line)
                    continue  # 필드 수가 맞지 않으면 무시하고 다음 줄로

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

def choose_genre():
    genre_map = {
        "1": "액션",
        "2": "코미디",
        "3": "로맨스",
        "4": "호러",
        "5": "SF",
        "6": "조회수",
        "0": "뒤로가기"
    }

    while True:
        print("="*44)
        print("[리스트]")
        print("="*44)
        for key, genre in genre_map.items():
            print(f"[{key}] {genre}")
        print("="*44)

        choice = input("정렬 옵션을 선택하세요(0-6): ").strip()

        if choice in genre_map:
            if choice == "0":
                return None
            return genre_map[choice]
        elif not choice.isdigit():
            print("숫자만 입력하세요.")
        else:
            print("존재하지 않는 메뉴 번호입니다.")

def paginative_movies(movies, page, page_size=10):
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return movies[start_index:end_index]


def display_movies_list():
    while True:
        # 사용자에게 장르 선택을 요청
        selected_genre = choose_genre()
        if selected_genre is None: # 뒤로 가기 선택한 경우
            # TO_DO : 홈화면으로 이동 (현재는 종료)
            return 
        
        # 전체 영화 데이터를 불러온 후, 선택한 장르로 필터링
        movies = get_movies()
        filtered_movies = [movie for movie in movies.values() if movie["genre"] == selected_genre]

        if not filtered_movies:
            print(f"선택한 장르 '{selected_genre}'에 영화가 없습니다. 다른 장르를 선택해 주세요.")
            continue

        page = 1
        while True:
            current_page_movies = paginative_movies(filtered_movies, page)

            print("="*44)
            print(f"[리스트] ({selected_genre})")
            print("="*44)
            print(f"({page}페이지)")

            for i, movie in enumerate(current_page_movies, start=1):
                print(f"[{i}] {movie['title']}")

            print("="*44)
            action = input("이전 페이지: - / 다음 페이지: + / 뒤로가기: 0\n상세정보를 조회할 영화 번호를 입력하세요: ").strip()

            if action == "0":
                break  # 뒤로 가기
            elif action == "+":
                if (page * 10) < len(filtered_movies):
                    page += 1
                else:
                    print("마지막 페이지입니다.")
            elif action == "-":
                if page > 1:
                    page -= 1
                else:
                    print("첫 번째 페이지입니다.")
            elif action.isdigit() and 1 <= int(action) <= len(current_page_movies):
                movie_index = int(action) - 1
                print(f"선택한 영화: {current_page_movies[movie_index]['title']}")  # 상세 정보 보기 등 추가 가능
            else:
                print("존재하지 않는 영화 번호입니다." if action.isdigit() else "숫자만 입력하세요.")


display_movies_list()