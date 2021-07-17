from lib.base_case import Basecase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("LearnQA PythonAPI")
@allure.feature("User deletion cases")
class TestUserDelete(Basecase):
    @allure.description("Trying to delete second user")
    def test_delete_second_user(self):
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step("Login as second user"):
            response1 = MyRequests.post("/api/user/login", data=login_data)
        auth_sid = self.get_cookies(response1, "auth_sid")
        token = self.get_headers(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")
        with allure.step("Trying to delete second user after logging"):
            response2 = MyRequests.delete(f"/api/user/{user_id_from_auth_method}", headers={"x-csrf-token": token},
                                          cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response2.content}"

    @allure.description("Trying to delete just created user")
    def test_delete_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        with allure.step("Create new user"):
            response1 = MyRequests.post("/api/user/", data=register_data)
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
        with allure.step("Login as new user"):
            response2 = MyRequests.post("/api/user/login", data=login_data)
        auth_sid = self.get_cookies(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        # Delete
        with allure.step("Deleting new user after logging"):
            response3 = MyRequests.delete(f"/api/user/{user_id}", headers={"x-csrf-token": token},
                                          cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response3, 200)

        # Check that user was deleted
        with allure.step("Check that new user was successfully deleted"):
            response4 = MyRequests.get(f"/api/user/{user_id}")
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == "User not found", f"Unexpected response content {response4.content}"

    @allure.description("Trying to delete just created user without authorization")
    def test_delete_just_created_user_auth_as_another_user(self):
        # Register first user
        register_data1 = self.prepare_registration_data()
        with allure.step("Create first user"):
            response1 = MyRequests.post("/api/user/", data=register_data1)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email = register_data1['email']
        password = register_data1['password']

        # Register second user
        register_data2 = self.prepare_registration_data()
        with allure.step("Create second user"):
            response2 = MyRequests.post("/api/user/", data=register_data2)
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")
        user_id = self.get_json_value(response2, "id")

        # Login as first user
        login_data1 = {
            'email': email,
            'password': password
        }
        with allure.step("Login as first user"):
            response3 = MyRequests.post("/api/user/login", data=login_data1)
        auth_sid = self.get_cookies(response3, "auth_sid")
        token = self.get_headers(response3, "x-csrf-token")

        # Try to delete second user
        with allure.step("Trying to delete second user"):
            response4 = MyRequests.delete(f"/api/user/{user_id}", headers={"x-csrf-token": token},
                                          cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 200)

        # Check that second user wasn't deleted
        with allure.step("Check that second user wasn't deleted"):
            response5 = MyRequests.get(f"/api/user/{user_id}")
        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_has_key(response5, "username")
