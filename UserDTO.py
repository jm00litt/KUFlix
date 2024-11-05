# 유저 데이터 객체 및 메서드 생성 파일
# 추후 사용 예정

# def load_user_data(user_id):
#     # 파일 경로 업데이트
#     with open("./data/user.txt", "r") as file:
#         for line in file:
#             data = line.strip().split("/")
#             if data[0] == user_id:
#                 user_info = {
#                     "id": data[0],
#                     "password": data[1],
#                     # 각 리스트와 딕셔너리 데이터 처리 방법
#                     "favorited_movies": eval(data[2]),
#                     "rated_movies": eval(data[3])
#                 }
#                 return user_info
#     return None  # 사용자 정보가 파일에 없을 경우 None 반환