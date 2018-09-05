import requests
import json

url = 'http://127.0.0.1:5000/api/order'

url = url + '/' + '18090500DO0128'
r = requests.put(url)
print(r.status_code, r.headers)
print(r.json())

