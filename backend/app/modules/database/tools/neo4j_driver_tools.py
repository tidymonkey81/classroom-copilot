from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import modules.logger_tool as logger
log_name = 'api_modules_database_tools_neo4j_driver_tools'
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
import time
from neo4j import GraphDatabase as gd

def get_driver(url=None, auth=None, database=None):
    if url is None:
        host = os.getenv("NEO4J_HOST")
        port = os.getenv("NEO4J_BOLT_PORT")
        url = f"bolt://{host}:{port}"
        auth = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
    if database is None:
        logging.warning("No database specified, using system database")
        database = 'system'
        
    driver = None
    connection_attempts = 0
    while driver is None:
        connection_attempts += 1
        try:
            driver = gd.driver(url, auth=auth)
            driver.verify_connectivity()
        except Exception as e:
            logging.error(f"Connection attempt {connection_attempts} failed: {e}")
            if connection_attempts >= 3:
                return None
            time.sleep(3)
    
    # Ensure the connection is to the specific database
    try:
        with driver.session(database=database) as session:
            # Test the connection
            result = session.run("RETURN 'Connection successful' AS message")
            message = result.single()["message"]
            logging.info(message)
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        driver.close()
        return None
    
    return driver

def close_driver(driver):
    driver.close()
