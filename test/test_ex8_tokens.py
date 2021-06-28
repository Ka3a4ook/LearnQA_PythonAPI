import requests
import json
import time


def test_tokens():
    response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
    response_parsed = json.loads(response.text)
    response_1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job",
                              params={"token": f"{response_parsed['token']}"})
    response_parsed_1 = json.loads(response_1.text)
    assert response_parsed_1['status'] == 'Job is NOT ready'
    time.sleep(response_parsed['seconds'] + 1)
    response_2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job",
                              params={"token": f"{response_parsed['token']}"})
    response_parsed_2 = json.loads(response_2.text)
    assert response_parsed_2['result'] is not None and response_parsed_2['status'] == 'Job is ready'
