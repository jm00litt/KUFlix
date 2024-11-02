def load_user_data():
    """
    user.txt 파일에서 사용자 데이터를 로드하여 딕셔너리 형태로 반환합니다.
    
    Returns:
        dict: 사용자 ID를 키로, 비밀번호를 값으로 하는 딕셔너리
    """
    try:
        users = {}
        with open("./data/user.txt", "r", encoding='utf-8') as file:
            for line in file:
                data = line.strip().split('/')
                user_id = data[0]
                user_password = data[1]
                users[user_id] = user_password
        return users
    except FileNotFoundError:
        print("파일이 존재하지 않습니다.")
    except UnicodeDecodeError:
        print("파일 인코딩에 문제가 있습니다.")
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")

def is_id_exist(user_id: str) -> bool:
    """
    사용자가 입력한 id 값이 존재하는 값인지 확인합니다.
    
    Args:
        user_id (str): 확인할 사용자 ID
        
    Returns:
        bool: ID가 존재하면 True, 존재하지 않으면 False
    """
    registered_ids = list(load_user_data().keys())
    return user_id in registered_ids

def is_password_correct(password: str) -> bool:
    """
    사용자가 입력한 비밀번호가 해당 아이디의 비밀번호가 맞는지 확인합니다.
    
    Args:
        password (str): 사용자가 입력한 비밀번호
        
    Returns:
        bool: 비밀번호가 일치하면 True, 일치하지 않으면 False
    """
    users = load_user_data()
    return password in users.values()

def save_user_data(user_id: str, password: str):
    """
    회원가입이 완료됐을 시 아이디와 비밀번호를 user.txt에 저장합니다.
    
    Args:
        user_id (str): 저장할 사용자 ID
        password (str): 저장할 비밀번호
    """
    try:
        user_data = f"{user_id}/{password}/[]/{{}}\n"
        with open("./data/user.txt", "a", encoding='utf-8') as file:
            file.write(user_data)
    except Exception as e:
        print(f"사용자 데이터 저장 중 오류가 발생했습니다: {e}")

def login():
    """
    로그인 시 실행되는 함수, 로그인 완료 시 user_id 반환
    
    Returns:
        str: 로그인 성공 시 사용자 ID 반환
    """
    users = load_user_data()
    
    while True:
        user_id = input()
        if not is_id_exist(user_id):
            return None
            
        password = input()
        if not is_password_correct(password):
            return None
            
        return user_id

def sign_up():
    """
    회원가입 시 실행되는 함수
    """
    while True:
        user_id = input()
        if is_id_exist(user_id):
            return False
            
        password = input()
        save_user_data(user_id, password)
        return True