# 검색화면 프롬프트 (구현 : 김종권)
# 미완

from ..MovieDTO import MovieData

class SearchPage:
    def display_searchPage(self):

        print("\n" + "=" * 40)
        print("[영화 검색]")
        print("('0'을 입력할 시 이전 화면으로 돌아갑니다.)")
        print("\n" + "=" * 40)
        userInput = input("찾고자 하는 영화 이름을 입력하세요: ")
