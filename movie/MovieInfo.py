from movie.MovieList import get_movies
from MovieDTO import MovieData


def load_user_data(user_id):
    # 파일 경로 업데이트
    with open("./data/user.txt", "r") as file:
        for line in file:
            data = line.strip().split("/")
            if data[0] == user_id:
                user_info = {
                    "id": data[0],
                    "password": data[1],
                    # 각 리스트와 딕셔너리 데이터 처리 방법
                    "favorited_movies": eval(data[2]),
                    "rated_movies": eval(data[3])
                }
                return user_info
    return None  # 사용자 정보가 파일에 없을 경우 None 반환


def display_movie_details(id,movie_id):
    # 사용자 정보 로드
    user_id = id
    user_info = load_user_data(user_id)
    # movie.txt 파일에서 영화 데이터 불러오기
    movies = get_movies()
    movie = movies.get(movie_id)

    if movie:
        # 조회수 증가
        add_viewcount(movie_id)
        movie['views'] += 1  # 증가된 조회수를 movie 객체에 반영
        while True:
            favorited_status = "♥︎" if movie_id in user_info["favorited_movies"] else "♡"
            print(f"============================================")
            print(f"[영화 세부 정보]")
            print(f"============================================")
            print(f"<{movie['title']}>")
            print(f"개봉년도: {movie['year']}년")
            print(f"영화 감독: {movie['director']}")
            print(f"장르: {movie['genre']}")
            print(f"러닝타임: {movie['runtime']}분")
            print(f"평점: {movie['rating']}")
            print(f"조회수: {movie['views']}")
            print(f"찜: {favorited_status}")
            print("============================================")
            print("찜하기/해제하기: 1 / 평점 남기기: 2 / 뒤로가기: 0")
            if not choose_status(user_info, movie, movie_id):
                break
    else:
        print("해당 ID의 영화가 존재하지 않습니다.")


def choose_status(user_info, movie, movie_id):
    valid_input = False
    while not valid_input:
        user_input = input("번호를 입력하세요(0-2): ")
        if user_input.isdigit() and int(user_input) in [0, 1, 2]:
            valid_input = True
        elif not user_input.isdigit():
            print("숫자만 입력하세요.")
        else:
            print("존재하지 않는 메뉴 번호입니다.")

    user_input = int(user_input)
    if user_input == 1:
        like_movie(user_info, movie_id)
    elif user_input == 2:
        rate_movie(movie, user_info, movie_id)
    elif user_input == 0:
        return False
    return True


def like_movie(user_info, movie_id):
    # 찜 목록에 영화가 있는지 확인하고, 상태를 변경
    if movie_id in user_info["favorited_movies"]:
        user_info["favorited_movies"].remove(movie_id)
        print("\n찜이 해제되었습니다!\n")
    else:
        user_info["favorited_movies"].append(movie_id)
        print("\n찜이 설정되었습니다!\n")

    # 변경된 사용자 데이터를 user.txt에 저장
    save_user_data(user_info)


def rate_movie(movie, user_info, movie_id):
    print("\n평점을 남겨주세요!")
    print("[1] ⭐️ [2] ⭐️⭐️ [3] ⭐️⭐️⭐️ [4] ⭐️⭐️⭐️⭐️ [5] ⭐️⭐️⭐️⭐️⭐️ [0] 뒤로가기")

    rating_input = input("번호를 입력하세요(0-5): ")
    if rating_input.isdigit() and 0 <= int(rating_input) <= 5:
        if int(rating_input) == 0:
            return
        rating_input = float(rating_input)  # 입력받은 평점을 float 형으로 변환


        # 평점 계산 및 저장
        current_rating = movie['rating']
        current_count = movie['rating_count']

        if movie_id in user_info["rated_movies"]:
            # 이미 평가한 영화인 경우 평가 인원 수를 변경하지 않고 평점만 업데이트
            new_rating = (current_rating * current_count - user_info["rated_movies"][
                movie_id] + rating_input) / current_count
        else:
            # 새로 평가하는 경우 평가 인원 수를 증가시키고 새 평점을 계산
            new_rating = (current_rating * current_count + rating_input) / (current_count + 1)
            movie['rating_count'] += 1

        movie['rating'] = round(new_rating, 1)
        user_info["rated_movies"][movie_id] = rating_input  # 사용자 정보 업데이트

        print(f"평점이 {rating_input}점으로 등록되었습니다!\n")

        # 변경된 사용자 데이터와 영화 데이터를 저장
        save_user_data(user_info)
        save_movie_data(movie_id, movie)


def add_viewcount(movie_id):
    # movie.txt에서 전체 영화 데이터를 불러오기
    movies = get_movies()

    # 해당 movie_id가 movies에 있는지 확인 후 조회수 증가
    if movie_id in movies:
        movies[movie_id]['views'] += 1

        # 변경된 데이터를 movie.txt에 반영
        with open("movie.txt", "w", encoding="utf-8") as file:
            for id, data in movies.items():
                # 영화 정보를 슬래시로 구분하여 저장
                line = f"{id}/{data['title']}/{data['year']}/{data['director']}/" \
                       f"{data['genre']}/{data['runtime']}/{data['views']}/" \
                       f"{data['rating']}/{data['rating_count']}\n"
                file.write(line)


def save_user_data(user_info):
    users = []
    updated = False
    # 파일 경로 업데이트
    with open("./data/user.txt", "r") as file:
        for line in file:
            data = line.strip().split("/")
            if data[0] == user_info['id']:
                favorited_str = str(user_info["favorited_movies"])
                rated_str = str(user_info["rated_movies"])
                new_line = f"{user_info['id']}/{user_info['password']}/{favorited_str}/{rated_str}\n"
                users.append(new_line)
                updated = True
            else:
                users.append(line)

    if not updated:  # 새 사용자라면 추가
        favorited_str = str(user_info["favorited_movies"])
        rated_str = str(user_info["rated_movies"])
        users.append(f"{user_info['id']}/{user_info['password']}/{favorited_str}/{rated_str}\n")

    # 변경된 내용을 파일에 다시 쓰기
    with open("./data/user.txt", "w") as file:
        file.writelines(users)


def save_movie_data(movie_id, updated_movie):
    movies = get_movies()  # 기존 영화 목록을 불러옴
    movies[movie_id] = updated_movie  # 특정 영화 데이터를 업데이트

    with open("movie.txt", "w", encoding="utf-8") as file:
        for id, data in movies.items():
            # 영화 정보를 슬래시로 구분하여 저장
            line = f"{id}/{data['title']}/{data['year']}/{data['director']}/" \
                   f"{data['genre']}/{data['runtime']}/{data['views']}/" \
                   f"{data['rating']}/{data['rating_count']}\n"
            file.write(line)
