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

def create_node(node_type: str, node_data: dict, db=None):
    query = f"CREATE (n:{node_type} $props) RETURN id(n)"
    params = {"props": node_data}
    response = send_query(query, database=db, params=params)
    return response['results'][0]['data'][0]['meta'][0]['id']

def create_relationship(relationship_data: dict, db=None):
    query = """
    MATCH (a), (b) WHERE id(a) = $start_id AND id(b) = $end_id
    CREATE (a)-[r:{rel_type}]->(b)
    RETURN r
    """
    params = {"start_id": relationship_data['start_node']['id'], "end_id": relationship_data['end_node']['id'], "rel_type": relationship_data['relationship_type'], "props": relationship_data.get('properties', {})}
    return send_query("/db/neo4j/tx/commit", query, params, db=db)