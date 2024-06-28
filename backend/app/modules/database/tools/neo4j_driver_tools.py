import modules.logger_tool as logger
import os
import time
from neo4j import GraphDatabase as gd

logging = logger.get_logger(os.environ['LOG_NAME'], log_level=os.environ['LOG_LEVEL'], log_path=os.environ['LOG_DIR'], log_file=os.environ['LOG_NAME'])

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
