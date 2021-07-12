from requests import Response
import json.decoder
from datetime import datetime


class Basecase:
    def get_cookies(self, response: Response, cookies_name):
        assert cookies_name in response.cookies, f"Can't find cookie with name {cookies_name} in the response"
        return response.cookies[cookies_name]

    def get_headers(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Can't find header with name {headers_name} in the response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is '{response.text}'"
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%d%m%Y%H%M%S%f")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
