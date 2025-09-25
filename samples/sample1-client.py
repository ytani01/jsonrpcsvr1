import requests
import json


url = "http://localhost:8000/api"  # サーバーのURL

payload1 = {
    "jsonrpc": "2.0",
    "method": "echo",
    "params": {"s": [42, 23]},
    "id": 1
}
response = requests.post(url, data=json.dumps(payload1))
result = response.json()
print(result)

payload2 = {
    "jsonrpc": "2.0",
    "method": "sub",
    "params": {"a": 2, "b": 3},
    "id": 2
}
response = requests.post(url, data=json.dumps(payload2))
result = response.json()
print(result)
