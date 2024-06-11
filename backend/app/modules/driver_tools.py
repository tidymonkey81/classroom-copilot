import os
import requests
import time
from neo4j import GraphDatabase as gd
import base64

# sys.path.append(os.getenv("PY_MODULES_PATH"))

# import logger_tool as logger
# log_level = os.getenv('LOG_LEVEL')
# logger_name = 'logger_tool'
# logging = logger.get_logger(name=logger_name, log_level=log_level)

# logging.prod(f"Importing Neo4j driver tools...")

# Function to send a request to the Neo4j database
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

# Function to get the Neo4j driver
def get_driver(url=None, auth=None):
    if url is None:
        host = os.getenv("NEO4J_HOST")
        port = os.getenv("NEO4J_BOLT_PORT")
        url = f"bolt://{host}:{port}"
        auth = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
    # else:
        # logging.testing(f"Using scripted Neo4j connection: {url}")
        print(f"Using scripted Neo4j connection: {url}")
    # logging.prod(f"Creating a Neo4j driver with URL and auth: {url}, {auth}")
    print(f"Creating a Neo4j driver with URL and auth: {url}, {auth}")
    driver = None
    # Try to create the driver. If it fails, retry in 10 seconds and repeat 3 times
    connection_attempts = 0
    while driver is None:
        connection_attempts += 1
        try:
            driver = gd.driver(url, auth=auth)
        except Exception as e:
            if connection_attempts >= 3:
                print(f"Failed to create Neo4j driver after {connection_attempts} attempts.")
                return None
            print(f"Retrying Neo4j driver creation in 3 seconds... (Attempt {connection_attempts})")
            time.sleep(3)
    # logging.prod(f"Neo4j driver created: {driver}")
    print(f"Neo4j driver created: {driver}")
    # Test the connection
    with driver.session() as session:
        # logging.prod(f"Testing Neo4j connection with session: {session}")
        print(f"Testing Neo4j connection with session: {session}")
        query = "RETURN 1 AS number"
        # logging.query("Running query: {query}")
        print(f"Running query: {query}")
        result = session.run(query)
        if result.single()["number"] == 1:
            # logging.prod("Neo4j connection test passed.")
            print("Neo4j connection test passed.")
        else:
            # logging.error("Neo4j connection test failed.")
            print("Neo4j connection test failed.")
    return driver

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

# Function to create a node in Neo4j via HTTP
def create_node_http(node_type: str, node_data: dict, db=None):
    query = f"CREATE (n:{node_type} $props) RETURN id(n)"
    params = {"props": node_data}
    response = send_neo4j_request(query, database=db, params=params)
    return response['results'][0]['data'][0]['meta'][0]['id']

# Function to create a node in Neo4j
def create_node(session, label, properties, returns=False):
    """
    Function to create a node in Neo4j database.
    
    Args:
        driver (neo4j.Driver): The Neo4j driver.
        session (str): The Neo4j session.
        label (str): The label of the node.
        properties (dict): A dictionary of properties for the node.
        
    Example usage:
        create_node(neo4j_driver, "Topic", {"TopicID": "AP.PAG10", "Title": "Topic 10"})
        
    Returns:
        None
    """
    transaction = session.write_transaction(_create_node, label, properties)
    if returns:
        transaction_id = transaction.id
        # logging.database(f"Created {label} node with transaction ID {transaction_id} and properties {properties}")
        print(f"Created {label} node with transaction ID {transaction_id} and properties {properties}")
        return find_node_by_transaction_id(session, transaction_id)
    else:
        # logging.warning(f"Failed to create {label} node with properties {properties}")
        print(f"Failed to create {label} node with properties {properties}")
        return None

def _create_node(tx, label, properties):
    query = f"""
    CREATE (n:{label} $properties)
    RETURN n
    """
    # logging.query(f"Running query: {query}")
    print(f"Running query: {query}")
    result = tx.run(query, properties=properties)
    return result.single()[0] if result.single() is not None else None  # Handle no record found

# Function to find a node by its element ID
def find_node_by_transaction_id(session, transaction_id):
    """
    Function to find a node in Neo4j database by its element ID.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        element_id (str): The element ID of the node to find.

    Returns:
        The matched node.
    """
    return session.read_transaction(_find_node_by_element_id, transaction_id)
    
def _find_node_by_element_id(tx, transaction_id):
    query = """
    MATCH (n)
    WHERE id(n) = $transaction_id
    RETURN n
    """
    # logging.query(f"Running query: {query}")
    result = tx.run(query, transaction_id=transaction_id)
    record = result.single()  # Get the single result record, if any
    return record[0] if record is not None else None  # Handle no record found

# Function to create a relationship between two nodes in Neo4j via HTTP
def create_relationship_http(relationship_data: dict, db=None):
    query = """
    MATCH (a), (b) WHERE id(a) = $start_id AND id(b) = $end_id
    CREATE (a)-[r:{rel_type}]->(b)
    RETURN r
    """
    params = {"start_id": relationship_data['start_node']['id'], "end_id": relationship_data['end_node']['id'], "rel_type": relationship_data['relationship_type'], "props": relationship_data.get('properties', {})}
    return send_neo4j_request("/db/neo4j/tx/commit", query, params, db=db)

# Function to create a relationship between two nodes in Neo4j
def create_relationship(session, start_node, end_node, label, properties=None, returns=False):
    """
    Function to create a relationship between two nodes in Neo4j database.
    
    Args:
        driver (neo4j.Driver): The Neo4j driver.
        session (str): The Neo4j session.
        start_node (str): The ID of the start node.
        end_node (str): The ID of the end node.
        rel_type (str): The type of the relationship.
        properties (dict): A dictionary of properties for the relationship.
        
    Example usage:
        create_relationship(neo4j_driver, "AP.PAG10", "AP.PAG11", "HAS_NEXT")
        
    Returns:
        None
    """
    relationship = session.write_transaction(_create_relationship, start_node, end_node, label, properties)
    if returns:
        relationship_id = relationship.id
        return find_relationship_by_relationship_id(session, relationship_id)
    else:
        return None
        
def _create_relationship(tx, start_node, end_node, label, properties):
    query = f"""
    MATCH (a), (b)
    WHERE ID(a) = $start_node_id AND ID(b) = $end_node_id
    CREATE (a)-[r:{label}]->(b)
    RETURN r
    """
    # logging.query(f"Running query: {query}")
    result = tx.run(query, start_node_id=start_node.id, end_node_id=end_node.id, properties=properties)
    single_result = result.single()
    return single_result[0] if single_result is not None else None

def order_list_of_nodes_by_property(session, label, property_name, order="ASC"):
    """
    Function to order a list of nodes in Neo4j database by a property.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        label (str): The label of the nodes to find.
        property_name (str): The name of the property to order by.
        order (str): The order of the sorting (ASC or DESC).

    Returns:
        List of matched nodes.
    """
    return session.read_transaction(_order_list_of_nodes_by_property, label, property_name, order)

def _order_list_of_nodes_by_property(tx, label, property_name, order):
    query = f"""
    MATCH (n:{label})
    RETURN n
    ORDER BY n.{property_name} {order}
    """
    # logging.query(f"Running query: {query}")
    result = tx.run(query)
    return [record["n"] for record in result]

def find_relationship_by_relationship_id(session, relationship_id):
    """
    Function to find a relationship in Neo4j database by its relationship ID.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        relationship_id (str): The relationship ID of the relationship to find.

    Returns:
        The matched relationship.
    """
    return session.read_transaction(_find_relationship_by_relationship_id, relationship_id)
    
def _find_relationship_by_relationship_id(tx, relationship_id):
    query = """
    MATCH ()-[r]->()
    WHERE id(r) = $relationship_id
    """
    # logging.query(f"Running query: {query}")
    print(f"Running query: {query}")
    result = tx.run(query, relationship_id=relationship_id)
    record = result.single()  # Get the single result record, if any
    return record[0] if record is not None else None  # Handle no record found

# Function to create a relationship between two nodes in two different databases
def create_relationship_between_databases(session, start_database, start_node, end_database, end_node, label, properties=None, returns=False):
    """
    BROKEN function to create a relationship between two nodes in two different databases.
    
    Args:
        driver (neo4j.Driver): The Neo4j driver.
        start_database (str): The name of the start database.
        start_node (str): The ID of the start node.
        end_database (str): The name of the end database.
        end_node (str): The ID of the end node.
        rel_type (str): The type of the relationship.
        properties (dict): A dictionary of properties for the relationship.
        
    Example usage:
        create_relationship_between_databases(neo4j_driver, "AP", "AP.PAG10", "PAG", "PAG.PAG11", "HAS_NEXT")
        
    Returns:
        None
    """
    relationship = session.write_transaction(_create_relationship_between_databases, start_database, start_node, end_database, end_node, label, properties)
    if returns:
        relationship_id = relationship.id
        return find_relationship_by_relationship_id(session, relationship_id)
    else:
        return None

def _create_relationship_between_databases(tx, start_database, start_node, end_database, end_node, label, properties):
    query = f"""
    MATCH (a:{start_database}), (b:{end_database})
    WHERE a.id = $start_node_id AND b.id = $end_node_id
    CREATE (a)-[r:{label}]->(b)
    RETURN r
    """
    # logging.query(f"Running query: {query}")
    print(f"Running query: {query}")
    result = tx.run(query, start_node_id=start_node, end_node_id=end_node, properties=properties)
    single_result = result.single()
    return single_result[0] if single_result is not None else None

# Function to find nodes in Neo4j database by label
def find_nodes_by_label(session, label):
    """
    Function to find nodes in Neo4j database by label.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        label (str): The label of the nodes to find.
        
    Example usage:
        find_nodes_by_label(neo4j_driver, "Topic")

    Returns:
        List of matched nodes.
    """
    return session.read_transaction(_find_nodes_by_label, label)

def _find_nodes_by_label(tx, label):
    query = f"""
    MATCH (n:{label})
    RETURN n
    """
    # logging.query(f"Running query: {query}")
    print(f"Running query: {query}")
    result = tx.run(query)
    return [record["n"] for record in result]

# Function to find nodes in Neo4j database by label and properties
def find_nodes_by_label_and_properties(session, label, properties):
    """
    Function to find nodes in Neo4j database by label and properties.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        label (str): The label of the nodes to find.
        properties (dict): A dictionary of properties to match.

    Returns:
        List of matched nodes.
    """
    with session:
        return session.read_transaction(_find_nodes_by_label_and_properties, label, properties)

def _find_nodes_by_label_and_properties(tx, label, properties):
    query = f"""
    MATCH (n:{label})
    WHERE {' AND '.join([f'n.{key} = ${key}' for key in properties.keys()])}
    RETURN n
    """
    # logging.query(f"Running query: {query}")
    print(f"Running query: {query}")
    result = tx.run(query, **properties)
    return [record["n"] for record in result]

# Function to find relationships in Neo4j database by type
def find_relationships_by_type(session, rel_type):
    """
    Function to find relationships in Neo4j database by type.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        rel_type (str): The type of the relationships to find.

    Returns:
        List of matched relationships.
    """
    return session.read_transaction(_find_relationships_by_type, rel_type)
    
def _find_relationships_by_type(tx, rel_type):
    query = f"""
    MATCH ()-[r:{rel_type}]->()
    RETURN r
    """
    # logging.query(f"Running query: {query}")
    print(f"Running query: {query}")
    result = tx.run(query)
    return [record["r"] for record in result]

# Function to find relationships in Neo4j database by type and properties
def find_relationships_by_type_and_properties(session, label, properties):
    """
    Function to find relationships in Neo4j database by type and properties.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        rel_type (str): The type of the relationships to find.
        properties (dict): A dictionary of properties to match.

    Returns:
        List of matched relationships.
    """
    return session.read_transaction(_find_relationships_by_type_and_properties, label, properties)
    

def _find_relationships_by_type_and_properties(tx, label, properties):
    query = f"""
    MATCH (a)-[r:{label}]->(b)
    WHERE {' AND '.join([f'r.{key} = ${key}' for key in properties.keys()])}
    RETURN r
    """
    # logging.query(f"Running query: {query}")
    print(f"Running query: {query}")
    result = tx.run(query, **properties)
    return [record["r"] for record in result]

# Function to find nodes and relationships in Neo4j database by label and properties
def find_nodes_and_relationships_by_label_and_properties(session, label, properties):
    """
    Function to find nodes and relationships in Neo4j database by label and properties.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        label (str): The label of the nodes to find.
        properties (dict): A dictionary of properties to match.

    Returns:
        List of matched nodes and relationships.
    """
    return session.read_transaction(_find_nodes_and_relationships_by_label_and_properties, label, properties)
    
def _find_nodes_and_relationships_by_label_and_properties(tx, label, properties):
    query = f"""
    MATCH (n:{label})
    WHERE {' AND '.join([f'n.{key} = ${key}' for key in properties.keys()])}
    RETURN n
    """
    # logging.query(f"Running query: {query}")
    result = tx.run(query, **properties)
    return [record["n"] for record in result]

# Function to delete nodes in Neo4j based on given criteria
def delete_nodes(session, criteria, delete_related=False):
    """
    Function to delete nodes in Neo4j based on given criteria.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        criteria (dict): A dictionary containing the properties to match for deletion.
        delete_related (bool): If True, deletes related nodes and relationships; otherwise, deletes only the matched nodes.

    Example usage:
        # Delete only the nodes matching the criteria
        delete_nodes(neo4j_driver, {'TopicID': 'AP.PAG10'})

        # Delete the nodes and their related relationships
        delete_nodes(neo4j_driver, {'TopicID': 'AP.PAG10'}, delete_related=True)
    """
    session.write_transaction(_delete_nodes, criteria, delete_related)

def _delete_nodes(tx, criteria, delete_related=False):
    """
    Internal function to execute a Cypher query to delete nodes based on criteria.

    Args:
        tx (neo4j.Transaction): The Neo4j transaction.
        criteria (dict): A dictionary containing the properties to match for deletion.
        delete_related (bool): Specifies whether to delete related nodes and relationships.
    """
    condition_str = " AND ".join([f"n.{key} = ${key}" for key in criteria])
    if delete_related:
        query = f"""
        MATCH (n)-[r]-()
        WHERE {condition_str}
        DELETE n, r
        """
    else:
        query = f"""
        MATCH (n)
        WHERE {condition_str}
        DELETE n
        """
    # logging.query(f"Running query: {query}")
    tx.run(query, **criteria)

# Function to delete all nodes and relationships in the Neo4j database in batches
def delete_lots_of_nodes_and_relationships(session):
    """
    Function to delete all nodes and relationships in the Neo4j database in batches.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        session (str): The Neo4j session.
    """
    total_deleted = 0
    while True:
        deleted_count = session.write_transaction(_delete_batch)
        total_deleted += deleted_count
        if deleted_count == 0:
            break  # Exit the loop if no more nodes are deleted
    # logging.prod(f"All nodes and relationships have been deleted. Total deleted: {total_deleted}")
    print(f"All nodes and relationships have been deleted. Total deleted: {total_deleted}")

def _delete_batch(tx):
    """
    Function to execute a Cypher query to delete a batch of nodes and relationships.

    Args:
        tx (neo4j.Transaction): The Neo4j transaction.
    """
    batch_size = 10000  # Adjust the batch size according to your needs
    query = """
    MATCH (n)
    WITH n LIMIT $batch_size
    DETACH DELETE n
    RETURN count(*)
    """
    # logging.query(f"Running query: {query}")
    result = tx.run(query, batch_size=batch_size)
    result_data = result.single()
    
    if result_data is None:
        return 0
    deleted_count = result_data[0]
    if deleted_count is None:  # This check might be redundant, but kept for clarity
        return 0
    if deleted_count > 0:
        # logging.database(f"Deleted {deleted_count} nodes.")
        print(f"Deleted {deleted_count} nodes.")
    return deleted_count

def delete_all_constraints(session):
    # Correct command to fetch all constraints for Neo4j 4.x and later
    constraints_query = "SHOW CONSTRAINTS"
    # logging.query(f"Running query: {constraints_query}")
    if constraints_query_result := session.run(constraints_query).data():
        for constraint in constraints_query_result:
            # Ensure correct key is used to extract constraint name
            constraint_name = constraint['name']  # Adjust this if necessary
            drop_query = f"DROP CONSTRAINT {constraint_name}"
            # logging.query(f"Running query: {drop_query}")
            session.run(drop_query)
            # logging.database(f"Dropped constraint: {constraint_name}")
            print(f"Dropped constraint: {constraint_name}")
    else:
        # logging.warning("No constraints found to delete.")
        print("No constraints found to delete.")
        
def reset_all_indexes(session):
    indexes = session.run("SHOW INDEXES").data()
    for index in indexes:
        index_name = index['name']
        session.run(f"DROP INDEX {index_name}")
        # logging.info(f"Deleted index: {index_name}")
        print(f"Deleted index: {index_name}")

def reset_database(session):
    delete_lots_of_nodes_and_relationships(session)
    delete_all_constraints(session)
    reset_all_indexes(session)

def create_database(session, db_name):
    """
    Creates a new database in Neo4j if it does not already exist.

    Args:
        session (neo4j.Session): The Neo4j session.
        db_name (str): The name of the database to create.
    """
    query = f"CREATE DATABASE `{db_name}` IF NOT EXISTS"
    try:
        session.run(query)
        print(f"Database {db_name} created successfully.")
    except Exception as e:
        print(f"Failed to create database {db_name}: {str(e)}")