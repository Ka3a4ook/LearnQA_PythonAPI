import requests
from lib.base_case import Basecase
from lib.assertions import Assertions


class TestUserEdit(Basecase):
    def test_edit_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookies(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        # Edit
        new_name = "Changed name"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}, data={"firstName": new_name})
        Assertions.assert_code_status(response3, 200)

        # Get
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")

    def test_edit_just_created_user_not_auth(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user_id = self.get_json_value(response1, "id")

        # Edit
        new_name = "Changed name"
        response2 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", data={"firstName": new_name})
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content {response2.content}"

    def test_edit_just_created_user_auth_as_another_user(self):
        # Register first user
        register_data1 = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data1)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email1 = register_data1['email']
        password1 = register_data1['password']

        # Register second user
        register_data2 = self.prepare_registration_data()
        response2 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data2)
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")
        email2 = register_data2['email']
        password2 = register_data2['password']
        first_name2 = register_data2['firstName']
        user_id2 = self.get_json_value(response2, "id")

        # Login as first user
        login_data1 = {
            'email': email1,
            'password': password1
        }
        response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data1)
        auth_sid1 = self.get_cookies(response3, "auth_sid")
        token1 = self.get_headers(response3, "x-csrf-token")

        # Try to edit second user
        new_name = "Changed name"
        response4 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id2}", headers={"x-csrf-token": token1},
                                 cookies={"auth_sid": auth_sid1}, data={"firstName": new_name})
        Assertions.assert_code_status(response4, 200)

        # Login as second user
        login_data2 = {
            'email': email2,
            'password': password2
        }
        response5 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data2)
        auth_sid2 = self.get_cookies(response5, "auth_sid")
        token2 = self.get_headers(response5, "x-csrf-token")

        # Check that second user's firstName wasn't changed
        response6 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id2}", headers={"x-csrf-token": token2},
                                 cookies={"auth_sid": auth_sid2})
        Assertions.assert_json_value_by_name(response6, "firstName", first_name2, "The name was wrongly changed.")

    def test_edit_just_created_user_with_wrong_email_auth(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookies(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        # Edit
        new_email = "learnqaexample.com"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}, data={"email": new_email})
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response3.content}"

    def test_edit_just_created_user_with_very_short_firstname_auth(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookies(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        # Edit
        new_name = "l"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}, data={"firstName": new_name})
        Assertions.assert_code_status(response3, 200)

        # Get
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")
