import requests


def test_cookie():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    print(response.cookies)
    assert response.cookies.get('HomeWork') == "hw_value"
