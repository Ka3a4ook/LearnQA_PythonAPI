import requests
from lib.base_case import Basecase
from lib.assertions import Assertions


class TestUserGet(Basecase):
    def test_get_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/1")
        expected_values = ["email", "firstName", "firstName"]
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, expected_values)

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        auth_sid = self.get_cookies(response1, "auth_sid")
        token = self.get_headers(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")
        response2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
                                  headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        expected_values = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_values)

    def test_get_user_details_auth_as_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        auth_sid = self.get_cookies(response1, "auth_sid")
        token = self.get_headers(response1, "x-csrf-token")
        response2 = requests.get(f"https://playground.learnqa.ru/api/user/1",
                                  headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        expected_values = ["email", "firstName", "firstName"]
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_keys(response2, expected_values)
