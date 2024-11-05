import os


def initialize_data_directory():
    """
    프로그램 실행에 필요한 data 디렉토리와 user.txt 파일을 초기화합니다.
    data 디렉토리가 없으면 생성하고, user.txt 파일이 없으면 새로 만듭니다.
    
    Returns:
        bool: 초기화 성공 시 True, 실패 시 False
    """
    try:
        data_dir = "./data"
        user_file = os.path.join(data_dir, "user.txt")

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print("data 디렉토리가 생성되었습니다.")

        if not os.path.exists(user_file):
            with open(user_file, "w", encoding='utf-8') as f:
                pass
            print("user.txt 파일이 생성되었습니다.")

        return True

    except PermissionError:
        print("Error: 파일 또는 디렉토리를 생성할 권한이 없습니다.")
        return False
    except OSError as e:
        print(f"Error: 파일 시스템 오류가 발생했습니다: {e}")
        return False
    except Exception as e:
        print(f"Error: 예상치 못한 오류가 발생했습니다: {e}")
        return False


if not initialize_data_directory():
    print("프로그램 초기화에 실패했습니다.")
    exit(1)


def load_user_data():
    """
    user.txt 파일에서 사용자 데이터를 로드하여 딕셔너리 형태로 반환합니다.

    Returns:
        dict: 사용자 ID를 키로, 비밀번호를 값으로 하는 딕셔너리
    """
    try:
        users = {}
        with open("./data/user.txt", "r", encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                try:
                    if not line.strip():
                        continue

                    data = line.strip().split('/')
                    if len(data) < 2:
                        print(f"Warning: 잘못된 형식의 데이터가 발견되었습니다 (라인 {line_num})")
                        continue

                    user_id = data[0].strip()
                    user_password = data[1].strip()

                    if not user_id or not user_password:
                        print(f"Warning: 빈 ID 또는 비밀번호가 발견되었습니다 (라인 {line_num})")
                        continue

                    if user_id in users:
                        print(f"Warning: 중복된 사용자 ID가 발견되었습니다: {user_id} (라인 {line_num})")
                        continue

                    users[user_id] = user_password

                except Exception as e:
                    print(f"Warning: 라인 {line_num}의 데이터를 처리하는 중 오류 발생: {e}")
                    continue

        return users

    except FileNotFoundError:
        print("파일이 존재하지 않습니다.")
        return {}
    except UnicodeDecodeError:
        print("파일 인코딩에 문제가 있습니다.")
        return {}
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return {}


def is_id_exist(user_id: str) -> bool:
    """
    사용자가 입력한 id 값이 존재하는 값인지 확인합니다.

    Args:
        user_id (str): 확인할 사용자 ID

    Returns:
        bool: ID가 존재하면 True, 존재하지 않으면 False
    """
    try:
        if not isinstance(user_id, str):
            return False

        registered_ids = list(load_user_data().keys())
        return user_id.strip() in registered_ids

    except Exception as e:
        return False


def is_password_correct(user_id: str, password: str) -> bool:
    """
    사용자가 입력한 비밀번호가 해당 아이디의 비밀번호가 맞는지 확인합니다.

    Args:
        user_id (str): 사용자 ID
        password (str): 사용자가 입력한 비밀번호

    Returns:
        bool: 비밀번호가 일치하면 True, 일치하지 않으면 False
    """
    try:
        users = load_user_data()
        return users[user_id] == password.strip()
    except Exception:
        return False


def save_user_data(user_id: str, password: str):
    """
    회원가입이 완료됐을 시 아이디와 비밀번호를 user.txt에 저장합니다.

    Args:
        user_id (str): 저장할 사용자 ID
        password (str): 저장할 비밀번호
    """
    try:
        user_data = f"{user_id.strip()}/{password.strip()}/[]/{{}}\n"
        with open("./data/user.txt", "a", encoding='utf-8') as file:
            file.write(user_data)
    except Exception as e:
        print(f"사용자 데이터 저장 중 오류가 발생했습니다: {e}")


def display_auth_menu():
    """
    인증 메뉴를 표시하고 사용자 입력을 처리합니다.
    """
    print("[회원가입·로그인 서비스] ")
    print("\n" + "=" * 30)
    print("회원가입 또는 로그인을 해주세요")
    print("=" * 30)
    print("[1] 회원가입 서비스")
    print("[2] 로그인 서비스")
    print("[0] 종료하기")
    print("=" * 30)

    while True:
        try:
            selected_number = input("메뉴를 선택하세요: ").strip()

            if not selected_number.isdigit():
                print("잘못된 입력입니다. 다시 번호를 입력해주세요. (0-2)")
                continue

            selected_number = int(selected_number)
            if selected_number == 0:
                print("\n프로그램을 종료합니다.")
                exit(0)
            elif selected_number == 1:
                return sign_up()
            elif selected_number == 2:
                return login()
            else:
                print("잘못된 입력입니다. 다시 번호를 입력해주세요. (0-2)")

        except ValueError:
            print("잘못된 입력입니다. 다시 번호를 입력해주세요. (0-2)")
        except Exception:
            print("잘못된 입력입니다. 다시 번호를 입력해주세요. (0-2)")


def login():
    """
    로그인 시 실행되는 함수, 로그인 완료 시 user_id 반환

    Returns:
        str: 로그인 성공 시 사용자 ID 반환
    """
    print("=" * 30)
    print("[로그인 서비스] ")
    print("=" * 30)
    print('로그인을 시작합니다.')

    while True:
        user_id = input('아이디를 입력하세요 : ').strip()
        if is_id_exist(user_id):
            break
        else:
            print('존재하지 않는 아이디입니다.\n')
            continue

    while True:
        password = input('비밀번호를 입력하세요 : ').strip()
        if is_password_correct(user_id, password):
            print("=" * 30)
            print('로그인 성공!')
            return user_id
        else:
            print('일치하지 않는 비밀번호입니다.')


def sign_up():
    """
    회원가입 시 실행되는 함수
    """
    print("=" * 30)
    print("[회원가입 서비스] ")
    print("=" * 30)
    print('회원가입을 시작합니다.')

    while True:
        user_id = input('아이디(영문 및 숫자)를 입력하세요: ').strip()

        if not user_id:
            print('아이디를 입력해주세요.\n')
            continue

        if not user_id.isalnum():
            print('소문자 영어와 숫자의 조합으로 이루어져야 합니다.')
            continue

        if is_id_exist(user_id):
            print('이미 존재하는 아이디입니다.\n')
            continue

        if len(user_id) > 10 or len(user_id) < 6:
            print('6자 이상 10자 이하로 입력해주세요.\n')
            continue

        break

    while True:
        password = input('비밀번호(숫자)를 입력하세요 : ').strip()

        if not password:
            print('비밀번호를 입력해주세요.\n')
            continue

        if not password.isnumeric():
            print('비밀번호는 숫자만 포함해야 합니다.')
            continue

        if len(password) != 6:
            print('비밀번호는 6자리여야 합니다.')
            continue

        break
    save_user_data(user_id, password)
    return login()
