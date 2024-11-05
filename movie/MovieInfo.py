from MovieDTO import MovieData

def get_movies():
    movie_data = MovieData()
    if movie_data.load_movie_data():
        return movie_data.movies
    else:
        print("영화 데이터를 불러오는 데 실패했습니다.")
        return {}


def display_movie_details(user_id, movie_id):
    # 사용자 정보 로드
    user_info = load_user_data(user_id)
    # movie.txt 파일에서 영화 데이터 불러오기
    movies = get_movies()
    movie = movies.get(movie_id)

    if movie:
        # 조회수 증가 및 movie.txt에 업데이트
        MovieData.load_movie_data()
        movie_id_int = int(movie_id)
        if movie_id_int in MovieData.movies:
            MovieData.movies[movie_id_int]['views'] += 1
            MovieData.update_movie_file()
            movie['views'] = MovieData.movies[movie_id_int]['views']
        else:
            print("해당 ID의 영화가 존재하지 않습니다.")
            return
        while True:
            user_info = load_user_data(user_id)  # 사용자 정보 갱신
            movies = get_movies()  # 영화 정보 갱신
            movie = movies.get(movie_id)  # 수정된 영화 정보 로드
            
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
            if not choose_status(user_id, movie_id):
                break
    else:
        print("해당 ID의 영화가 존재하지 않습니다.")

def choose_status(user_id, movie_id):
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
        like_movie(user_id, movie_id)
    elif user_input == 2:
        rate_movie(user_id, movie_id)
    elif user_input == 0:
        return False
    return True

def like_movie(user_id, movie_id):
    user_info = load_user_data(user_id)
    if movie_id in user_info["favorited_movies"]:
        user_info["favorited_movies"].remove(movie_id)
        print("\n찜이 해제되었습니다!\n")
    else:
        user_info["favorited_movies"].append(movie_id)
        print("\n찜이 설정되었습니다!\n")
    save_user_data(user_info)

def rate_movie(user_id, movie_id):
    user_info = load_user_data(user_id)
    movie = get_movies().get(movie_id)
    print("\n평점을 남겨주세요!")
    print("[1] ⭐️ [2] ⭐️⭐️ [3] ⭐️⭐️⭐️ [4] ⭐️⭐️⭐️⭐️ [5] ⭐️⭐️⭐️⭐️⭐️ [0] 뒤로가기")
    rating_input = input("번호를 입력하세요(0-5): ")
    if not rating_input.isdigit():
        print("숫자만 입력 가능합니다.")
        rate_movie(user_id, movie_id)
    if int(rating_input) < 0 or int(rating_input) > 5:
        print("존재하지 않는 번호 입니다.")
        rate_movie(user_id, movie_id)
    if rating_input.isdigit() and 0 <= int(rating_input) <= 5:
        if int(rating_input) == 0:
            return
        rating_input = float(rating_input)
        current_rating = movie['rating']
        current_count = movie['rating_count']
        
        if current_count == 0 and rating_input > 0:
            new_rating = rating_input
            movie['rating_count'] = 1
        elif movie_id in user_info["rated_movies"]:
            previous_rating = user_info["rated_movies"][movie_id]
            new_rating = ((current_rating * current_count) - previous_rating + rating_input) / current_count
        else:
            new_rating = ((current_rating * current_count) + rating_input) / (current_count + 1)
            movie['rating_count'] += 1

        movie['rating'] = round(new_rating, 1)
        user_info["rated_movies"][movie_id] = rating_input
        print(f"평점이 {rating_input}점으로 등록되었습니다!\n")
        save_user_data(user_info)
        save_movie_data(movie_id, movie)

def load_user_data(user_id):
    with open("./data/user.txt", "r") as file:
        for line in file:
            data = line.strip().split("/")
            if data[0] == user_id:
                user_info = {
                    "id": data[0],
                    "password": data[1],
                    "favorited_movies": eval(data[2]),
                    "rated_movies": eval(data[3])
                }
                return user_info
    return None

def save_user_data(user_info):
    users = []
    updated = False
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
    if not updated:
        favorited_str = str(user_info["favorited_movies"])
        rated_str = str(user_info["rated_movies"])
        users.append(f"{user_info['id']}/{user_info['password']}/{favorited_str}/{rated_str}\n")
    with open("./data/user.txt", "w") as file:
        file.writelines(users)

def save_movie_data(movie_id, updated_movie):
    movies = get_movies()
    movies[movie_id] = updated_movie
    with open("movie.txt", "w", encoding="utf-8") as file:
        for id, data in movies.items():
            line = f"{id}/{data['title']}/{data['year']}/{data['director']}/" \
                   f"{data['genre']}/{data['runtime']}/{data['views']}/" \
                   f"{data['rating']}/{data['rating_count']}\n"
            file.write(line)
