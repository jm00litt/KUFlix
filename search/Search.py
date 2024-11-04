# 검색화면 프롬프트 (구현 : 김종권)
# 미완

from MovieDTO import MovieData
from movie.MovieInfo import display_movie_details
from movie.MovieInfo import load_user_data

def display_search_page(user_id):

    while True:
        print("\n" + "=" * 40)
        print("[영화 검색]")
        print("('0'을 입력할 시 이전 화면으로 돌아갑니다.)")
        print("\n" + "=" * 40)
        user_input = input("찾고자 하는 영화 제목을 입력하세요: ").strip()

        if user_input == "0":
            break
        else:
            searched_list = search_movies(user_input)
            if len(searched_list) == 0:
                print("검색 결과가 없습니다.")
                continue
            pages = (len(searched_list) - 1) // 10 + 1
            current_page = 1

            print("\n" + "=" * 40)
            print("[찜 목록]")
            print("=" * 40)

            while True:
                print(f"({current_page}페이지)")

                # 현재 페이지의 시작 인덱스와 끝 인덱스 계산
                start_index = (current_page - 1) * 10
                end_index = min(start_index + 10, len(searched_list))

                # 영화 제목을 출력
                for i in range(start_index, end_index):
                    movie_id = searched_list[i]                # 수정할 예정
                    print(f"[{i - start_index + 1}] {MovieData.movies[movie_id]['title']}")

                print("=" * 40)
                print("이전 페이지: - / 다음 페이지: + / 뒤로가기: 0")

                user_input = input("상세정보를 조회할 영화 번호를 입력하세요: ").strip()
                    
                # 사용자 입력에 따른 페이지 전환 또는 영화 상세 정보 조회
                if user_input == "-":
                    if current_page == 1:
                        print("\n첫 페이지입니다.")
                        print("=" * 40)
                    else:
                        current_page -= 1
                elif user_input == "+":
                    if current_page == pages:
                        print("\n마지막 페이지입니다.")
                        print("=" * 40)
                    else:
                        current_page += 1
                elif user_input == "0":
                    print("\n홈 화면으로 돌아갑니다.")
                    print("=" * 40)
                    break
                else:
                    try:
                        # 사용자가 입력한 번호가 1부터 (현재 페이지의 영화 수)까지인지 확인
                        selected_index = int(user_input) - 1  # 1부터 시작하므로 -1
                        if 0 <= selected_index < (end_index - start_index):
                            movie_id = searched_list[start_index + selected_index]  # 실제 ID 찾기
                            display_movie_details(user_id, movie_id)
                        else:
                            print("유효하지 않은 영화 번호입니다.")
                    except ValueError:
                        print("유효한 입력을 해주세요.")  # 입력이 숫자가 아닐 경우 처리

def search_movies(keyword):
    matched_movie_ids = []  # 검색된 movie_id를 저장할 리스트

    # keyword의 공백 제거 및 소문자 처리
    processed_keyword = keyword.replace(" ", "").lower()

    for movie_id, movie_data in MovieData.movies.items():
        # title의 공백 제거 및 소문자 처리
        processed_title = movie_data["title"].replace(" ", "").lower()

        # 부분 문자열 찾기
        if processed_keyword in processed_title:
            matched_movie_ids.append(movie_id)  # 검색된 movie_id 추가

    return matched_movie_ids
