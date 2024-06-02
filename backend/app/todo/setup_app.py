import sys
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
sys.path.append(os.getenv("PY_MODULES_PATH"))

import logger_tool as logger
logging = logger.get_logger(name='logger_tool')

def setup_tools(tools=None):
    load_dotenv(find_dotenv())
    tools = [tools] if isinstance(tools, str) else tools or ['default']
    
    for tool in tools:
        logging.pedantic(f"Setting up {tool} tools...")
        tool = tool.upper()
        logging.pedantic(f"Loading environment variables from {'.env.' + tool if tool != 'default' else '.env'}")
        tools_path_key = f"{tool}_TOOLS_PATH" if tool != 'default' else "TOOLS_PATH"
        logging.pedantic(f"Looking for {tool} tools path in environment variable: {tools_path_key}")
        tools_path = os.getenv(tools_path_key)
        logging.pedantic(f"Found {tool} tools path: {tools_path}")
        if tools_path:
            sys.path.append(r'' + tools_path)
            logging.debug(f"Added {tool} tools path: {tools_path}")
        else:
            logging.warning(f"No {tool} tools path found. Skipping...")