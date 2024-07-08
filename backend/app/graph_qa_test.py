import os
import requests

def test_query_graph(prompt):
    url = f"http://{os.environ['BACKEND_URL']}:{os.environ['BACKEND_PORT']}/langchain/graph_qa/prompt"
    params = {"prompt": prompt}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        print("Response:", data)
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
    prompt = "It is Monday, 8th July 2024. What is happening today?"
    test_query_graph(prompt)
