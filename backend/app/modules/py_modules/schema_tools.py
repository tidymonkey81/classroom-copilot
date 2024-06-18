print("PRINT STATEMENT: Loading schema_tools.py...")
import sys
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
sys.path.append(os.getenv("PY_MODULES_PATH"))
import logger_tool as logger
logging = logger.get_logger(name='logger_tool')

def convert_pydantic_to_neontology(pydantic_instance, neontology_node_class):
    """
    Convert a Pydantic model instance to a Neontology node instance.

    Args:
        pydantic_instance (BaseModel): An instance of a Pydantic model.
        neontology_node_class (BaseNode): The Neontology node class to convert to.

    Returns:
        An instance of the specified Neontology node class.
    """
    logging.debug(f"Converting Pydantic instance to Neontology node instance: {pydantic_instance}...")
    node_data = pydantic_instance.dict()
    logging.variables(f"Node data: {node_data}")
    return neontology_node_class(**node_data)

def convert_neontology_to_pydantic(neontology_node_instance, pydantic_model_class):
    """
    Convert a Neontology node instance to a Pydantic model instance.

    Args:
        neontology_node_instance (BaseNode): An instance of a Neontology node.
        pydantic_model_class (BaseModel): The Pydantic model class to convert to.

    Returns:
        An instance of the specified Pydantic model class.
    """
    logging.debug(f"Converting Neontology node instance to Pydantic instance: {neontology_node_instance}...")
    model_data = neontology_node_instance.__dict__
    logging.variables(f"Model data: {model_data}")
    return pydantic_model_class(**model_data)