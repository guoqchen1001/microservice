import requests
import json

url = 'http://127.0.0.1:5000/api/auth'

data = {'user_no': '0122', "password": "0122"}
r = requests.post(url, data=data)
print(r.text)
print(r.status_code, r.headers)

response_json = r.json()

token = response_json['Token']
print(token)

url = 'http://127.0.0.1:5000/api/order'
headers = {"token":  "eyJhbGciOiJIUzI1NiIsImlhdCI6MTUzNzMyMDgwNCwiZXhwIjoxNTM3MzIxNDA0fQ.eyJ1c2VyX25vIjoiMDEyMiJ9.0RZtYjNjBzV-KmVapbZRZbkwTC0e28oIvVQOJ54TX2I"}
r = requests.get(url, headers=headers)
print(r.headers)
print(r.text)


# url = 'http://127.0.0.1:5000/api/order/do/18091700DO0130'
# data = {"token": token}
# r = requests.put(url, data=data)
# print(r.text)

