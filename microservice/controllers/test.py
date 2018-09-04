import requests
import json

url = 'http://127.0.0.1:5000/api/order'
r = requests.get(url)
print(r.headers)
print(r.json())

