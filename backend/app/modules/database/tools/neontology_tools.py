from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import modules.logger_tool as logger
log_name = 'api_modules_database_tools_neontology_tools'
user_profile = os.environ.get("USERPROFILE", "")
app_dir = os.environ.get("APP_DIR", "")
log_dir = os.path.join(user_profile, app_dir, "logs")
logging = logger.get_logger(
    name=log_name,
    log_level='DEBUG',
    log_path=log_dir,
    log_file=log_name,
    runtime=True,
    log_format='default'
)
from modules.database.tools.neontology.graphconnection import init_neontology
from modules.database.tools.neontology.basenode import BaseNode
from modules.database.tools.neontology.baserelationship import BaseRelationship
from pydantic import ValidationError
import os
import neo4j

# Initialize Neontology with the Neo4j database details
def init_neo4j_connection(host=None, port=None, user=None, password=None):
    host = host or os.getenv("NEO4J_HOST")
    port = port or os.getenv("NEO4J_BOLT_PORT")
    user = user or os.getenv("NEO4J_USER")
    password = password or os.getenv("NEO4J_PASSWORD")

    init_neontology(
        neo4j_uri=f"bolt://{host}:{port}",
        neo4j_username=user,
        neo4j_password=password
    )
    logging.info(f"Neontology connection initialized with host: {host}, port: {port}, user: {user}")

# Terminates the Neo4j connection
def terminate_neo4j_connection():
    neo4j.close()

# Create a Neontology node in the Neo4j database
def create_or_merge_neontology_node(node: BaseNode, database: str = 'neo4j', operation: str = "merge"):
    """
    Create or merge a Neontology node in the Neo4j database.

    Args:
        node (BaseNode): A Neontology node object.
        operation (str): The operation to perform ('create' or 'merge'). Defaults to 'merge'.
    """
    try:
        if operation == "create":
            node.create(database=database)
        elif operation == "merge":
            node.merge(database=database)
        else:
            logging.error(f"Invalid operation: {operation}")
    except Exception as e:
        logging.error(f"Error in processing node: {e}")

# Create or merge a Neontology node in the Neo4j database. If a ValidationError occurs
# due to a NaN value, replace it with a default value and retry.
def create_or_merge_neontology_node_with_default(driver, node: BaseNode, database: str = 'neo4j', operation: str = "merge", default_values: dict = {}):
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
            node.create(database=database)
        else:  # "merge" by default
            logging.pedantic(f"Merging node: {node}")
            node.merge(database=database)
        logging.debug(f"Node processed: {node}")
    except ValidationError as e:
        # Handle ValidationError due to NaN value
        for field, error in e.errors():
            if field in default_values and 'type' in error and error['type'] == 'value_error.nan':
                setattr(node, field, default_values[field])
                logging.warning(f"Warning: Replacing NaN in {field} with default value '{default_values[field]}' and retrying.")
                create_or_merge_neontology_node_with_default(driver, node, database, operation, default_values)
                break
        else:
            # If the error is not due to a NaN value or field not in default_values, re-raise the error
            logging.error(f"Error in processing node: {e}")
            raise
    except Exception as e:
        logging.error(f"Error in processing node: {e}")

def create_or_merge_neontology_relationship(relationship: BaseRelationship, database: str = 'neo4j', operation: str = "merge"):
    """
    Create or merge a Neontology relationship in the Neo4j database.

    Args:
        relationship (BaseRelationship): A Neontology relationship object.
        operation (str): The operation to perform ('create' or 'merge'). Defaults to 'merge'.
    """
    try:
        if operation == "create":
            relationship.create(database=database)
        elif operation == "merge":
            relationship.merge(database=database)
        else:
            logging.error(f"Invalid operation: {operation}")
    except Exception as e:
        logging.error(f"Error in processing relationship: {e}")
