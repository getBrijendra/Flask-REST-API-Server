import requests

URL = "http://127.0.0.1:5000/"

assets = [
    {"name": "Ramayan", "views": 3000000, "likes": 20000000},
    {"name": "Hare Krishna", "views": 3560000, "likes": 74360000},
    {"name": "Jai Hanuman", "views": 3566700, "likes": 50343000},
    {"name": "Mahakal", "views": 97534500, "likes": 83467000},
]

# for i in range(len(assets)):
#     response = requests.put(URL + f"asset/{i}", assets[i])
#     print(response.json())

response = requests.patch(URL + "asset/2", {})
print(response.json())

# response = requests.get(URL + "asset/2")
# print(response.json())
