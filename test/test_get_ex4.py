import requests


def test_get_ex4():
    response = requests.get("https://playground.learnqa.ru/api/get_text")
    print(response.text)
