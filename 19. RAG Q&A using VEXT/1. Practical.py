import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("VEXT_API_KEY")

### Headers for the API request
headers = {
    'Content-Type': 'application/json',
    'Apikey': f'Api-Key {api_key}'
}

query = "What is machine learning?"

data = {
    "payload": query,
}

url = "https://payload.vextapp.com/hook/95B57FFZAO/catch/$(adityakumar504703)"

response = requests.post(url, headers=headers, json=data)

print(response.text)