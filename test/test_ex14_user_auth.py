import pytest
from lib.base_case import Basecase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("LearnQA PythonAPI")
@allure.feature("User authentication cases")
class TestUserAuth(Basecase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step("Login as second user"):
            response1 = MyRequests.post("/api/user/login", data=data)
        self.auth_sid = self.get_cookies(response1, "auth_sid")
        self.token = self.get_headers(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.description("Successful authentication test")
    def test_auth_user(self):
        with allure.step("Second user authentication"):
            response1 = MyRequests.get("/api/user/auth", headers={"x-csrf-token": self.token},
                                       cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_value_by_name(response1, "user_id", self.user_id_from_auth_method,
                                             "User id from auth method is not equal to user id from check method")

    @allure.title(f"Parameterized test_negative_auth_check")
    @allure.description("Unsuccessful authentication test")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            with allure.step("Trying to authenticate as second user"):
                response1 = MyRequests.get("/api/user/auth", headers={"x-csrf-token": self.token})
        else:
            with allure.step("Trying to authenticate as second user"):
                response1 = MyRequests.get("/api/user/auth", cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_value_by_name(response1, "user_id", 0, f"User is authorized with condition {condition}")
