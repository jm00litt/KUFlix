# 마이페이지 프롬프트 (구현 : 김종권)
# 미완
# userId를 통해 찜 목록을 불러올 수 있으면 구현 (현재 _userId로부터 찜 목록에 접근할 수 없음, user.txt 파일 읽고 딕셔너리로 저장하는 기능이 구현되어야 함)

from MovieDTO import MovieData
from movie.MovieInfo import display_movie_details
from movie.MovieInfo import load_user_data


def display_my_page(user_id):
    while True:
        print("\n" + "=" * 40)
        print("[마이페이지]")
        print("=" * 40)
        print("[1] 개인정보 조회")
        print("[2] 찜한 영화 목록")
        print("[0] 뒤로가기")
        print("=" * 40)
        user_selection = input("선택할 메뉴 번호를 입력하세요(0-2): ").strip()

        if not user_selection.isdigit():
            print("숫자만 입력하세요.")
            continue

        if user_selection != user_selection.lstrip('0') and user_selection != '0':
            print("존재하지 않는 메뉴 번호입니다.")
            continue

        user_selection = int(user_selection)

        if user_selection == 0:
            print("\n이전 화면으로 돌아갑니다.")  # 수정할 예정
            return
        elif user_selection == 1:
            display_my_info(user_id)
        elif user_selection == 2:
            display_my_favorite(user_id)
        else:
            print("존재하지 않는 메뉴 번호입니다.")
            continue


def display_my_info(user_id):
    print("\n" + "=" * 40)
    print("[개인정보]")
    print("=" * 40)
    print(f"아이디: {user_id}")


def display_my_favorite(user_id):

    print("\n" + "=" * 40)
    print("[찜 목록]")
    current_page = 1

    while True:

        fravorite_list = load_user_data(user_id)["favorited_movies"]

        if len(fravorite_list) == 0:
            print("찜한 영화가 없습니다!")
            return

        # 총 페이지 수 계산
        pages = (len(fravorite_list) - 1) // 10 + 1
        print("=" * 40)
        print(f"({current_page}페이지)")

        # 현재 페이지의 시작 인덱스와 끝 인덱스 계산
        start_index = (current_page - 1) * 10
        end_index = min(start_index + 10, len(fravorite_list))

        rated_movies = load_user_data(user_id)["rated_movies"]
        # 영화 제목을 출력
        for i in range(start_index, end_index):
            movie_id = fravorite_list[i]
            rated_indicator = "✅" if movie_id in rated_movies else "☑️"
            title = MovieData.movies[movie_id]["title"]
            directors = MovieData.movies[movie_id]["directors"]
            average_rating = MovieData.movies[movie_id]["average_rating"]
            rating_count = MovieData.movies[movie_id]["rating_count"]
            print(f"[{i - start_index + 1}] {title} (감독명: {directors} / 평점: {average_rating} / 평가 인원 수: {rating_count}) {rated_indicator}")

        print("=" * 40)
        print("이전 페이지: - / 다음 페이지: + / 뒤로가기: 0")

        while True:

            user_input = input("상세정보를 조회할 영화 번호를 입력하세요: ").strip()

            # 사용자 입력에 따른 페이지 전환 또는 영화 상세 정보 조회
            if user_input == "-":
                if current_page == 1:
                    print("첫 페이지입니다.")
                    print("=" * 40)
                else:
                    current_page -= 1
                    break
            elif user_input == "+":
                if current_page == pages:
                    print("마지막 페이지입니다.")
                    print("=" * 40)
                else:
                    current_page += 1
                    break
            elif user_input == "0":
                return
            else:
                try:
                    # 사용자가 입력한 번호가 1부터 (현재 페이지의 영화 수)까지인지 확인
                    selected_index = int(user_input) - 1  # 1부터 시작하므로 -1
                    if 0 <= selected_index < (end_index - start_index):
                        movie_id = fravorite_list[start_index + selected_index]  # 실제 ID 찾기
                        display_movie_details(user_id, movie_id)
                        break
                    else:
                        print("유효하지 않은 영화 번호입니다.")
                except ValueError:
                    print("유효한 입력을 해주세요.")  # 입력이 숫자가 아닐 경우 처리
