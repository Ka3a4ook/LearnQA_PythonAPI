import requests
import json

method_1 = {"method": "GET"}
method_2 = {"method": "POST"}
method_3 = {"method": "PUT"}
method_4 = {"method": "DELETE"}
method_5 = {"method": "HEAD"}
method_6 = '{"methods": [{"method": "GET"}, {"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}]}'


# 1. Wrong method provided
def test_methods_1():
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
    print(response.text)


# 2. Wrong method provided
def test_methods_2():
    response_5 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=method_5)
    print(response_5.text)


# 3_1. {"success":"!"} {"success":"!"} {"success":"!"} {"success":"!"}
def test_methods_3_1():
    response_1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=method_1)
    response_2 = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", params=method_2)
    response_3 = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", params=method_3)
    response_4 = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", params=method_4)
    print(response_1.text, response_2.text, response_3.text, response_4.text)


# 3_2. Wrong method provided {"success":"!"} {"success":"!"} Wrong method provided
def test_methods_3_2():
    response_1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", data=method_1)
    response_2 = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=method_2)
    response_3 = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=method_3)
    response_4 = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=method_4)
    print(response_1.text, response_2.text, response_3.text, response_4.text)


# 4.
def test_methods_4():
    all_methods = json.loads(method_6)
    for i in range(len(all_methods['methods'])):
        if all_methods['methods'][i]['method'] == 'GET':
            for range_1 in range(len(all_methods['methods'])):
                response = requests.request(method=all_methods['methods'][i]['method'],
                                            url="https://playground.learnqa.ru/ajax/api/compare_query_type",
                                            params=all_methods['methods'][range_1])
                print(all_methods['methods'][i]['method'], all_methods['methods'][range_1], response.text)
        else:
            for range_2 in range(len(all_methods['methods'])):
                response = requests.request(method=all_methods['methods'][i]['method'],
                                            url="https://playground.learnqa.ru/ajax/api/compare_query_type",
                                            data=all_methods['methods'][range_2])
                print(all_methods['methods'][i]['method'], all_methods['methods'][range_2], response.text)
