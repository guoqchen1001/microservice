import requests
import json

# url = 'http://127.0.0.1:5000/api/auth'

# data = {'user_no': '0122', "password": "0123"}
# r = requests.post(url, data=data)
# print(r.status_code, r.headers)
# print(r.content)
# response_json = r.json()
#
# print(response_json)

# token = response_json['token']
# print(token)

token = ""
url = 'http://127.0.0.1:5000/api/order'
r = requests.get(url, params={"token": token ,'sheet_type': "do"})
print(r.json())

