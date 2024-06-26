print("PRINT STATEMENT: Loading neontology_tools.py...")
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
from neontology import BaseNode, BaseRelationship, init_neontology
from pydantic import ValidationError

# Initialize Neontology with the Neo4j database details
def init_neo4j_connection():
    logging.info(f"Initializing Neontology connection...")
    logging.warning(f"Connecting to Neontology with hard-coded details. This should be changed to use environment variables.")
    init_neontology(
        neo4j_uri=os.getenv("bolt://192.168.0.20:7687"),
        neo4j_username=os.getenv("neo4j"),
        neo4j_password=os.getenv("c0mput3r")
    )

# Terminates the Neo4j connection
def terminate_neo4j_connection():
    logging.info(f"Terminating Neontology connection...")
    neo4j.close()

# Create a Neontology node in the Neo4j database
def create_or_merge_neontology_node(node: BaseNode, operation: str = "merge"):
    """
    Create or merge a Neontology node in the Neo4j database.

    Args:
        node (BaseNode): A Neontology node object.
        operation (str): The operation to perform ('create' or 'merge'). Defaults to 'merge'.
    """
    try:
        if operation == "create":
            node.create()
            logging.debug(f"Node created: {node}")
        elif operation == "merge":
            node.merge()
            logging.debug(f"Node merged: {node}")
        else:
            logging.error(f"Invalid operation: {operation}")
    except Exception as e:
        logging.error(f"Error in processing node: {e}")

# Create or merge a Neontology node in the Neo4j database. If a ValidationError occurs
# due to a NaN value, replace it with a default value and retry.
def create_or_merge_neontology_node_with_default(driver, node: BaseNode, operation: str = "merge", default_values: dict = {}):
    """
    Create or merge a Neontology node in the Neo4j database. If a ValidationError occurs
    due to a NaN value, replace it with a default value and retry.

    Args:
        node (BaseNode): A Neontology node object.
        operation (str): The operation to perform ('create' or 'merge'). Defaults to 'merge'.
        default_values (dict): A dictionary of default values for fields that might contain NaN.
    """
    try:
        # Attempt to create or merge the node
        if operation == "create":
            logging.pedantic(f"Creating node: {node}")
            node.create()
        else:  # "merge" by default
            logging.pedantic(f"Merging node: {node}")
            node.merge()
        logging.debug(f"Node processed: {node}")
    except ValidationError as e:
        # Handle ValidationError due to NaN value
        for field, error in e.errors():
            if field in default_values and 'type' in error and error['type'] == 'value_error.nan':
                setattr(node, field, default_values[field])
                logging.warning(f"Warning: Replacing NaN in {field} with default value '{default_values[field]}' and retrying.")
                create_or_merge_neontology_node_with_default(driver, node, operation, default_values)
                break
        else:
            # If the error is not due to a NaN value or field not in default_values, re-raise the error
            logging.error(f"Error in processing node: {e}")
            raise
    except Exception as e:
        logging.error(f"Error in processing node: {e}")

def create_or_merge_neontology_relationship(relationship: BaseRelationship, operation: str = "merge"):
    """
    Create or merge a Neontology relationship in the Neo4j database.

    Args:
        relationship (BaseRelationship): A Neontology relationship object.
        operation (str): The operation to perform ('create' or 'merge'). Defaults to 'merge'.
    """
    try:
        if operation == "create":
            relationship.create()
            logging.debug(f"Relationship created: {relationship}")
        elif operation == "merge":
            relationship.merge()
            logging.debug(f"Relationship merged: {relationship}")
        else:
            logging.error(f"Invalid operation: {operation}")
    except Exception as e:
        logging.error(f"Error in processing relationship: {e}")
