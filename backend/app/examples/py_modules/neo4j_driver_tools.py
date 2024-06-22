print("PRINT STATEMENT: Loading neo4j_driver_tools.py...")
import sys
import os

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
    records = [record["n"] for record in result]
    logging.variables(f"Records: {records}")
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
    records = [record["n"] for record in result]
    return records