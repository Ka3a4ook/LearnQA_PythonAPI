from lib.base_case import Basecase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from datetime import datetime


class TestUserRegister(Basecase):
    def setup(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%d%m%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/api/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response.content}"

    def test_create_user_without_one_param(self):
        missed_param = 'username'
        data = {
            'password': '123',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = MyRequests.post("/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missed_param}", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_very_short_name(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'l',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = MyRequests.post("/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_very_long_name(self):
        name = 'llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll' \
               'llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll' \
               'llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': name,
            'lastName': 'learnqa',
            'email': self.email
        }
        response = MyRequests.post("/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long", \
            f"Unexpected response content {response.content}"
