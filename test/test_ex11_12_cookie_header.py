import requests


def test_cookie():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    print(response.cookies)
    assert response.cookies.get('HomeWork') == "hw_value"


def test_header():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")
    print(response.headers)
    assert response.headers.get('x-secret-homework-header') == "Some secret value"
