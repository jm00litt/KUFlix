# 검색화면 프롬프트 (구현 : 김종권)
# 미완

from MovieDTO import MovieData
from movie.MovieList import get_movies

def display_search_page():

    while True:
        print("\n" + "=" * 40)
        print("[영화 검색]")
        print("('0'을 입력할 시 이전 화면으로 돌아갑니다.)")
        print("\n" + "=" * 40)
        userInput = input("찾고자 하는 영화 이름을 입력하세요: ").strip()

        if userInput == "0":
            break
        else:
            searchedList = search_movies(userInput)
            pages = (len(searchedList) - 1) // 10 + 1
            currentPage = 1

            print("\n" + "=" * 40)
            print("[찜 목록]")
            print("=" * 40)

            while True:
                print(f"({currentPage}페이지)")

                # 현재 페이지의 시작 인덱스와 끝 인덱스 계산
                start_index = (currentPage - 1) * 10
                end_index = min(start_index + 10, len(searchedList))

                # 영화 제목을 출력
                for i in range(start_index, end_index):
                    movie_id = searchedList[i]                # 수정할 예정
                    print(f"[{i - start_index + 1}] {MovieData.movies[movie_id]['title']}")

                print("=" * 40)
                print("이전 페이지: - / 다음 페이지: + / 뒤로가기: 0")

                userInput = input("상세정보를 조회할 영화 번호를 입력하세요:").strip()
                    
                # 사용자 입력에 따른 페이지 전환 또는 영화 상세 정보 조회
                if userInput == "-":
                    if currentPage == 1:
                        print("첫 번째 페이지입니다.")
                    else:
                        currentPage -= 1
                elif userInput == "+":
                    if currentPage == pages:
                        print("마지막 페이지입니다.")
                    else:
                        currentPage += 1
                elif userInput == "0":
                    print("홈 화면으로 돌아갑니다.")
                    break
                else:
                    try:
                        # 사용자가 입력한 번호가 1부터 (현재 페이지의 영화 수)까지인지 확인
                        selected_index = int(userInput) - 1  # 1부터 시작하므로 -1
                        if 0 <= selected_index < (end_index - start_index):
                            movie_id = searchedList[start_index + selected_index]  # 실제 ID 찾기
                            # 영화의 상세 정보를 출력 (예시로 title을 출력)
                            print(f"선택한 영화 제목: {MovieData.movies[movie_id]['title']}")
                            # 여기서 추가적인 상세 정보를 출력할 수 있음
                        else:
                            print("유효하지 않은 영화 번호입니다.")
                    except ValueError:
                        print("유효한 입력을 해주세요.")  # 입력이 숫자가 아닐 경우 처리

def search_movies(keyword):
    movies = get_movies
    matched_movie_ids = []  # 검색된 movie_id를 저장할 리스트

    for movie_id, movie_data in movies.items():
        # 대소문자를 구별하지 않고 부분문자열 찾기
        if keyword.lower() in movie_data["title"].lower():
            matched_movie_ids.append(movie_id)  # 검색된 movie_id 추가

    return matched_movie_ids
