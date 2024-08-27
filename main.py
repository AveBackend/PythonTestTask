import requests
from datetime import datetime

url = "http://127.0.0.1:5000/api/orders"

data = {
    "apartment_no": 101,
    "pet_name": "Buddyy",
    "pet_breed": "Golden Retriever",
    "start_time": datetime.now().replace(hour=15, minute=0, second=0, microsecond=0).isoformat()
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
