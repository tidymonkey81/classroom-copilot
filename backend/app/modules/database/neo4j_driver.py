import os
import requests
import time
from neo4j import GraphDatabase as gd
import base64

def get_driver(url=None, auth=None):
    if url is None:
        host = os.getenv("NEO4J_HOST")
        port = os.getenv("NEO4J_BOLT_PORT")
        url = f"bolt://{host}:{port}"
        auth = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
    driver = None
    connection_attempts = 0
    while driver is None:
        connection_attempts += 1
        try:
            driver = gd.driver(url, auth=auth)
        except Exception as e:
            if connection_attempts >= 3:
                return None
            time.sleep(3)
    return driver

def send_neo4j_request(query, encoded_credentials=None, database=None, endpoint=None, params=None, method='POST'):
    if database is None:
        database = "system"
    if endpoint is None:
        endpoint = "/tx/commit"
    if encoded_credentials is None:
        credentials = f"{os.getenv('NEO4J_USER')}:{os.getenv('NEO4J_PASSWORD')}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode('utf-8')
    url = f"http://{os.getenv('NEO4J_HOST')}:{os.getenv('NEO4J_HTTP_PORT')}/db/{database}{endpoint}"
    print(f"Sending request to {url}")
    headers = {'Content-Type': 'application/json', 'Authorization': f'Basic {encoded_credentials}'}
    print(f"Headers: {headers}")
    data = {
        "statements": [{
            "statement": query,
            "parameters": params or {}
        }]
    }
    print(f"Data: {data}")
    response = requests.request(method, url, json=data, headers=headers)
    print(f"Response: {response.json()}")
    return response.json()



from contextlib import suppress

def close_session(session):
    """
    Closes a Neo4j session.

    Parameters:
    - session: The Neo4j session to be closed.
    """
    if session:
        with suppress(Exception):
            # Attempt to close the session if it's not already closed
            # logging.database(f"Closing Neo4j session: {session}")
            session.close()

# Function to close the Neo4j driver
def close_driver(driver):
    # logging.prod(f"Closing Neo4j driver: {driver}")
    driver.close()