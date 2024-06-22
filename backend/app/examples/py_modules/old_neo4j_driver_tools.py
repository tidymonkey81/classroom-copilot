print("PRINT STATEMENT: Loading neo4j_driver_tools.py...")
import sys
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
sys.path.append(os.getenv("PY_MODULES_PATH"))
import logger_tool as logger
logging = logger.get_logger(name='logger_tool')

logging.pedantic(f"Loading tools created by KevlarAI...")
import setup_dev as dev
dev.setup_tools('kevlarai')
import schemas
logging.pedantic(f"Tools created by KevlarAI loaded")

import neo4j
from pydantic import ValidationError

# Setup tools
def get_neo4j_driver(url=None, auth=None):
    logging.info(f"Getting Neo4j driver...")
    logging.warning(f"Connecting to Neo4j with hard-coded details. This should be changed to use environment variables.")
    url = "bolt://192.168.0.20:7687"
    auth = ("neo4j", "c0mput3r")
    return neo4j.GraphDatabase.driver(url, auth=auth)

def find_nodes_by_label(driver, label):
    """
    Function to find nodes in Neo4j database by label.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        label (str): The label of the nodes to find.

    Returns:
        List of matched nodes.
    """
    with driver.session() as session:
        logging.debug(f"Finding nodes by label: {label}")
        return session.read_transaction(_find_nodes_by_label, label)

def _find_nodes_by_label(tx, label):
    query = f"""
    MATCH (n:{label})
    RETURN n
    """
    logging.pedantic(f"Query: {query}")
    result = tx.run(query)
    logging.variables(f"Result: {result}")
    records = [record["n"] for record in result]

    # Log details about the result
    logging.debug(f"Keys: {result.keys()}")
    logging.debug(f"Data: {result.data()}")
    # Note: single() can only be called once and before iterating over records
    # logging.debug(f"Single Record: {result.single()}")
    logging.debug(f"Values: {result.values()}")
    return records

def find_nodes_by_label_and_properties(driver, label, properties):
    """
    Function to find nodes in Neo4j database by label and properties.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        label (str): The label of the nodes to find.
        properties (dict): A dictionary of properties to match.

    Returns:
        List of matched nodes.
    """
    with driver.session() as session:
        logging.debug(f"Finding nodes by label and properties: {label}, {properties}")
        return session.read_transaction(_find_nodes_by_label_and_properties, label, properties)

def _find_nodes_by_label_and_properties(tx, label, properties):
    query = f"""
    MATCH (n:{label})
    WHERE {' AND '.join([f'n.{key} = ${key}' for key in properties.keys()])}
    RETURN n
    """
    logging.pedantic(f"Query: {query}")
    result = tx.run(query, **properties)
    logging.pedantic(f"Result: {result}")
    return [record["n"] for record in result]

def create_nodes(driver, nodes, operation_type='merge'):
    """
    Function to create or merge nodes in Neo4j using Cypher, based on their properties.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        nodes (list): A list of dictionaries, each containing the properties of a node.
        operation_type (str): Type of operation ('create' or 'merge').

    """
    with driver.session() as session:
        for node in nodes:
            if operation_type.lower() == 'create':
                session.write_transaction(_create_node, node, create=True)
            else:  # Defaults to 'merge'
                session.write_transaction(_create_node, node, create=False)
            logging.debug(f"Node processed: {node}")

def _create_node(tx, node, create=False):
    """
    Internal function to create or merge a node in Neo4j using Cypher, based on its properties.

    Args:
        tx (neo4j.Transaction): The Neo4j transaction.
        node (dict): A dictionary containing the node properties.
        create (bool): If True, creates a new node; otherwise, merges based on a unique property.

    Returns:
        The result of the query execution.
    """
    unique_prop_key = next(iter(node))  # Get the first property key as an example
    unique_prop_value = node[unique_prop_key]

    if create:
        query = f"""
        CREATE (n {{', '.join(f'{key}: ${key}' for key in node.keys())}})
        RETURN n
        """
    else:
        query = f"""
        MERGE (n {{{unique_prop_key}: $unique_prop_value}})
        SET {', '.join(f'n.{key} = ${key}' for key in node.keys())}
        RETURN n
        """
    logging.pedantic(f"Query: {query}")
    return tx.run(query, unique_prop_value=unique_prop_value, **node).single()

def create_relationship(driver, node1_props, node2_props, relationship_type, node1_label, node2_label):
    """
    Function to create a relationship of a specified type between two nodes in the Neo4j database.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        node1_props (dict): Properties to identify the first node.
        node2_props (dict): Properties to identify the second node.
        relationship_type (str): The type of the relationship to be created.
        node1_label (str): Label of the first node.
        node2_label (str): Label of the second node.

    Example usage:
        node1_props = {'name': 'Alice'}
        node2_props = {'name': 'Bob'}
        create_relationship(neo4j_driver, node1_props, node2_props, 'KNOWS', 'Person', 'Person')
    """
    with driver.session() as session:
        session.write_transaction(_create_relationship, node1_props, node2_props, relationship_type, node1_label, node2_label)
        logging.info(f"Relationship {relationship_type} created between nodes.")

def _create_relationship(tx, node1_props, node2_props, relationship_type, node1_label, node2_label):
    """
    Internal function to execute a Cypher query to create a relationship.

    Args:
        tx (neo4j.Transaction): The Neo4j transaction.
        node1_props, node2_props (dict): Properties to identify the nodes.
        relationship_type (str): Type of the relationship.
        node1_label, node2_label (str): Labels of the nodes.
    """
    query = f"""
    MATCH (a:{node1_label}), (b:{node2_label})
    WHERE { ' AND '.join([f'a.{k} = ${k}' for k in node1_props.keys()]) }
      AND { ' AND '.join([f'b.{k} = $b_{k}' for k in node2_props.keys()]) }
    MERGE (a)-[r:{relationship_type}]->(b)
    RETURN r
    """

    # Prepare parameters, prefixing the second node's properties
    params = {**node1_props, **{f'b_{k}': v for k, v in node2_props.items()}}
    result = tx.run(query, **params)
    logging.pedantic("Executed query to create relationship.")

    return result.single()

def create_relationship_by_label(driver, relationship_type, node1_label, node2_label):
    with driver.session() as session:
        session.write_transaction(_create_relationship_by_label, relationship_type, node1_label, node2_label)
        logging.info(f"Relationship {relationship_type} created between {node1_label} and {node2_label} nodes.")

def _create_relationship_by_label(tx, relationship_type, node1_label, node2_label):
    query = f"""
    MATCH (a:{node1_label}), (b:{node2_label})
    MERGE (a)-[r:{relationship_type}]->(b)
    RETURN r
    """
    return tx.run(query).single()

def delete_nodes(driver, criteria, delete_related=False):
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
    with driver.session() as session:
        session.write_transaction(_delete_nodes, criteria, delete_related)
        logging.info(f"Nodes deleted based on criteria: {criteria}")

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
    
    logging.pedantic(f"Query: {query}")
    tx.run(query, **criteria)

def delete_all_nodes_and_relationships(driver):
    """
    Function to delete all nodes and relationships in the Neo4j database.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
    """
    with driver.session() as session:
        session.write_transaction(_delete_all)
        logging.info("All nodes and relationships have been deleted.")

def _delete_all(tx):
    """
    Function to execute a Cypher query to delete all nodes and relationships.

    Args:
        tx (neo4j.Transaction): The Neo4j transaction.
    """
    query = """
    MATCH (n)
    DETACH DELETE n
    """
    tx.run(query)
    logging.pedantic("Executed query to delete all nodes and relationships.")