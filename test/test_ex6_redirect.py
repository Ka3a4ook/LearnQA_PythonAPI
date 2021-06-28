import requests


def test_redirect():
    response = requests.get("https://playground.learnqa.ru/api/long_redirect")
    first_response = response.history
    print(first_response)
    print(response.url)
