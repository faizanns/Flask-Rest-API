import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 78, "name": "Tim", "views": 100},
        {"likes": 100, "name": "How to make REST API", "views": 1000},
        {"likes": 35, "name": "Tim", "views": 1000}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
# Test 'GET' and 'PUT'request
response = requests.get(BASE + "video/2")
print(response.json())

input()
# Test 'PATCH' request
response = requests.patch(BASE + "video/2", {"views": 900, "likes": 19})
print(response.json())

input()
# Test 'DELETE' request
response = requests.delete(BASE + "video/0")
print(response)
input()
response = requests.get(BASE + "video/2")
print(response.json())