import os
import requests
import base64

def send_query(query, encoded_credentials=None, params=None,  method='POST', database="system", endpoint="/tx/commit"):
    if encoded_credentials is None:
        credentials = f"{os.getenv('NEO4J_USER')}:{os.getenv('NEO4J_PASSWORD')}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode('utf-8')
    url = f"http://{os.getenv('NEO4J_HOST')}:{os.getenv('NEO4J_HTTP_PORT')}/db/{database}{endpoint}"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Basic {encoded_credentials}'}
    data = {
        "statements": [{
            "statement": query,
            "parameters": params or {}
        }]
    }
    response = requests.request(method, url, json=data, headers=headers)
    return response.json()