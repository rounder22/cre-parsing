import requests

try:
    response = requests.get('http://127.0.0.1:5000/')
    print(f'Status: {response.status_code}')
    print(f'Content (first 300 chars): {response.text[:300]}')
except Exception as e:
    print(f'Error: {e}')
