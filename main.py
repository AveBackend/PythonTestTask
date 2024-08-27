import requests
from datetime import datetime

url = "http://127.0.0.1:5000/api/orders"

data = {
    "apartment_no": 102,
    "pet_name": "Kirrr",
    "pet_breed": "Dog",
    "start_time": datetime.now().replace(hour=15, minute=30, second=0, microsecond=0).isoformat()
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
