# 영화 상세정보 프롬프트

from movie.MovieList import get_movies

# 임의의 사용자 정보 설정
user_info = {
    "password": "password123",
    "favorited_movies": [],  # 찜한 영화 목록
    "rated_movies": {}
}
def display_movie_details():
    # movie.txt 파일에서 영화 데이터 불러오기
    movies = get_movies()  

    # 영화 ID가 "7"인 영화 세부 정보 출력
    movie_id = "1"
    movie = movies.get(movie_id)

    if movie:
        # 조회수 증가
        add_viewcount(movie_id)
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
    if movie_id in user_info["favorited_movies"]:
        user_info["favorited_movies"].remove(movie_id)
        print("\n찜이 해제되었습니다!\n")
    else:
        user_info["favorited_movies"].append(movie_id)
        print("\n찜이 설정되었습니다!\n")

def rate_movie(movie, user_info, movie_id):
    print("\n평점을 남겨주세요!")
    print("[1] ⭐️ [2] ⭐️⭐️ [3] ⭐️⭐️⭐️ [4] ⭐️⭐️⭐️⭐️ [5] ⭐️⭐️⭐️⭐️⭐️ [0] 뒤로가기")

    rating_input = input("번호를 입력하세요(0-5): ")
    if rating_input.isdigit() and 0 <= int(rating_input) <= 5:
        if int(rating_input) == 0:
            return
        # 평점 계산 및 저장
        current_rating = movie['rating']
        current_count = movie['rating_count']
        new_rating = (current_rating * current_count + int(rating_input)) / (current_count + 1)
        movie['rating'] = round(new_rating, 1)
        movie['rating_count'] += 1
        user_info["rated_movies"][movie_id] = int(rating_input)
        print(f"평점이 {rating_input}점으로 등록되었습니다!\n")

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

    
display_movie_details()
