# 옇화 상세정보 프롬프트
def display_movie_details():
    # 임의의 영화 데이터
    movies = {
        "001": {
            "title": "인사이드 아웃",
            "year": 2015,
            "director": "피트 닥터",
            "genre": "애니메이션",
            "runtime": 94,
            "views": 50000,
            "rating": 4.8,
            "rating_count": 1200,
        }
    }

    # 임의의 사용자 정보
    user_info = {
        "password": "password123",
        "favorited_movies": ["001"],  # 찜한 영화 목록
        "rated_movies": {}
    }

    movie_id = "001"
    movie = movies.get(movie_id)
    
    while True:
        if movie:
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
            
            # digit 화 되는 것만 유효한 숫자
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
                toggle_favorite(user_info, movie_id)
            elif user_input == 2:
                rate_movie(movie, user_info, movie_id)
            elif user_input == 0:
                break
        else:
            print("해당 ID의 영화가 존재하지 않습니다.")
            break


def toggle_favorite(user_info, movie_id):
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
        user_info["rated_movies"][movie_id] = rating_input
        print(f"평점이 {rating_input}점으로 등록되었습니다!\n")