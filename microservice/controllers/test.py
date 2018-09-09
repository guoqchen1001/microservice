import requests
import json

url = 'http://127.0.0.1:5000/api/auth'

data = {'userno': '0122', "password": "0122"}
r = requests.post(url, data=data)
print(r.status_code, r.headers)
print(r.json())

