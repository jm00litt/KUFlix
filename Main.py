from logIn.LogIn import LogIn

def main():
    print("여기서 부터 시작")
    
    # LogIn 클래스 인스턴스 생성
    login_instance = LogIn()
    
    # LogIn 클래스 내 메서드 호출
    login_instance.authenticate("조하상", "조하상123")
    
if __name__ == "__main__":
    main()