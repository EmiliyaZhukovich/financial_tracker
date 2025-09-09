import requests
import json

# Тест PUT запроса
url = "http://localhost:5050/revenues/1"
data = {
    "amount": 1000,
    "description": "Updated revenue"
}

try:
    response = requests.put(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

