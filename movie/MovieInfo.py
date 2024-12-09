from MovieDTO import MovieData
from auth.Auth import load_user_data as load

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
            genres_str = ','.join(movie['genre'])
            
            favorited_status = "♥︎" if movie_id in user_info["favorited_movies"] else "♡"
            print(f"============================================")
            print(f"[영화 세부 정보]")
            print(f"============================================")
            print(f"<{movie['title']}>")
            print(f"개봉년도: {movie['year']}년")
            print(f"영화 감독: {movie['directors']}")
            print(f"장르: {genres_str}")
            print(f"러닝타임: {movie['runtime']}분")
            print(f"조회수: {movie['views']}")
            print(f"평균 평점: {'-' if movie['rating_count'] == 0 else movie['average_rating']}")
            print(f"평가 인원수 : {'-' if movie['rating_count'] == 0 else movie['rating_count']}")
            print(f"찜: {favorited_status}")
            print("============================================")
            print("찜하기/해제하기: 1 / 평점 남기기: 2 / 평가 인원 확인하기: 3 / 뒤로가기: 0")

            if not choose_status(user_id, movie_id):
                break
    else:
        print("해당 ID의 영화가 존재하지 않습니다.")

def choose_status(user_id, movie_id):
    valid_input = False
    while not valid_input:
        choice = input("번호를 입력하세요(0-3): ").strip()
        if choice.isdigit() and int(choice) in [0, 1, 2, 3]:
            valid_input = True
        elif not choice.isdigit():
            print("숫자만 입력하세요.")
        else:
            print("존재하지 않는 메뉴 번호입니다.")

    choice = int(choice)
    if choice == 1:
        like_movie(user_id, movie_id)
    elif choice == 2:
        rate_movie(user_id, movie_id)
    elif choice == 3:
        view_movie_ratings(movie_id)
    elif choice == 0:
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
    while True:
        try:
            print("[1] ⭐️ [2] ⭐️⭐️ [3] ⭐️⭐️⭐️ [4] ⭐️⭐️⭐️⭐️ [5] ⭐️⭐️⭐️⭐️⭐️ [6] 0점 [0] 뒤로가기")
            rating_input = input("번호를 입력하세요(0-6): ").strip()
            
            # 입력값이 비어있는 경우
            if not rating_input:
                print("입력값이 비어있습니다. 다시 입력해주세요.")
                continue
                
            # 숫자가 아닌 경우
            if not rating_input.isdigit():
                print("숫자만 입력 가능합니다.")
                continue
                
            # 숫자로 변환
            rating_input = int(rating_input)
            
            # 범위 체크
            if rating_input < 0 or rating_input > 6:
                print("0부터 6까지의 숫자만 입력 가능합니다.")
                continue
                
            # 뒤로가기
            if rating_input == 0:
                print("평점 입력을 취소합니다.")
                return
                
            # 0점 선택
            if rating_input == 6:
                rating_input = 0
                
            break
            
        except ValueError:
            print("올바르지 않은 입력입니다. 다시 입력해주세요.")
            continue
        except KeyboardInterrupt:
            print("\n평점 입력을 취소합니다.")
            return
        except:
            print("예상치 못한 오류가 발생했습니다. 다시 입력해주세요.")
            continue

    # 평점 계산 로직
    rating_input = float(rating_input)
    current_rating = movie['average_rating']
    current_count = movie['rating_count']

    # 새 평점 계산
    new_rating = ((current_rating * current_count) + rating_input) / (current_count + 1)
    movie['average_rating'] = round(new_rating, 1)
    movie['rating_count'] += 1

    # 사용자 평점 업데이트
    user_rating_entry = f"{user_id}:{rating_input}"
    movie['user_ratings'].append(user_rating_entry)  # 항상 새 평점을 추가

    # 사용자 데이터 저장
    if movie_id in user_info["rated_movies"].keys():
        tmp = user_info["rated_movies"][movie_id]
        tmp.extend([rating_input])
        user_info["rated_movies"][movie_id] = tmp
    else :
        user_info["rated_movies"][movie_id] = [rating_input]
    save_user_data(user_info)

    # 영화 데이터 저장 (MovieData.update_movie_file 사용)
    movie_id_int = int(movie_id)
    MovieData.movies[movie_id_int] = movie
    MovieData.update_movie_file()

    print(f"평점이 {rating_input}점으로 등록되었습니다!")


    
def show_users_rate(user_id):
    print(f"============================================")
    print(f'유저 아이디 : {user_id}')
    rate_total_average = 0
    rate_total_count = 0
    rate_genre_average = {
        "액션" : 0,
        "코미디" : 0,
        "로맨스" : 0,
        "호러" : 0,
        "SF" : 0}
    rate_genre_count = {
        "액션" : 0,
        "코미디" : 0,
        "로맨스" : 0,
        "호러" : 0,
        "SF" : 0
        }
    user_data = load_user_data(user_id)
    for key in user_data['rated_movies'].keys():
        movies = get_movies()
        movie = movies.get(key)
        genres_str = ','.join(movie['genre'])
        print(f'<{movie["title"]}> : {user_data["rated_movies"][key]}')
        print(f"개봉년도: {movie['year']}년")
        print(f"장르: {genres_str}")
        print(f"영화 감독: {movie['directors']}")
        print(f'영화 아이디 : {key}\n')
        for g in movie['genre'] :
            score = 0.0
            cnt = 0
            for rate in user_data['rated_movies'][key] :
                score+=float(rate)
                cnt+=1
            rate_genre_average[g] +=(score/cnt)
            rate_genre_count[g]+=1

        score = 0.0
        cnt = 0
        for rate in user_data['rated_movies'][key] :
            score+=float(rate)
            cnt+=1
        rate_total_average+=(score/cnt)
        rate_total_count+=1
    if(rate_total_count == 0):
        print(f'전체 평점 평균 : -')
    else : 
        print(f'전체 평점 평균 : {round(rate_total_average/rate_total_count,1)}')
    print(f'장르별 평점 평균 :')
    for genre in rate_genre_count.keys():
        if(rate_genre_count[genre] == 0):
            print(f'>{genre} : -')
        else :
            print(f'>{genre} : {round(rate_genre_average[genre]/rate_genre_count[genre],1)}')
    print(f"============================================")
    while True :
        print('뒤로가기 : 0')
        zero = input('번호를 입력하세요 : ').strip()
        if zero == '0':
            return
        else :
            print('잘못된 입력입니다.')

def view_movie_ratings(movie_id):
    while(True):
        movies = get_movies()
        movie = movies.get(movie_id)

        user_ratings = movie.get("user_ratings", [])
        
        if(len(user_ratings) == 1):
            print('평가한 유저가 없습니다.\n')
            return

        print("\n평가한 사용자 목록")
        print(f"============================================")

        # 평점 데이터를 순서대로 출력
        users = load()
        user_ids = users.keys()
        for i in user_ids :
            user_data = load_user_data(i)
            user_movies = user_data['rated_movies'].keys()
            if movie_id in user_movies:
                print(f'{user_data["rated_movies"][movie_id]} : {i}')
                
        print("============================================")
        print('유저 아이디 입력 시 해당 유저의 <평점,영화> 리스트를 출력합니다.(뒤로 가기는 0)\n')

        users = load()
        user_ids = users.keys()
        while True:
            choice = input("아이디 또는 번호를 입력하세요(0): ").strip()
            if choice.isdigit() and int(choice) == 0:
                return
            elif choice in user_ids:
                show_users_rate(choice)
                break
            else:
                print("해당 아이디가 없거나 잘못된 번호입니다.")

    
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
