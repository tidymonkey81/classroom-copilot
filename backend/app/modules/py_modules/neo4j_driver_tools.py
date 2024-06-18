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

def delete_lots_of_nodes_and_relationships(driver):
    """
    Function to delete all nodes and relationships in the Neo4j database in batches.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
    """
    total_deleted = 0
    while True:
        with driver.session() as session:
            deleted_count = session.write_transaction(_delete_batch)
            total_deleted += deleted_count
            if deleted_count == 0:
                break  # Exit the loop if no more nodes are deleted

    logging.info(f"All nodes and relationships have been deleted. Total deleted: {total_deleted}")

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
    result = tx.run(query, batch_size=batch_size)
    return result.single()[0]  # Returns the count of deleted nodes in this batch
