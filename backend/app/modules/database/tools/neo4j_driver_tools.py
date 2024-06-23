import os
import time
from neo4j import GraphDatabase as gd

def get_driver(url=None, auth=None):
    if url is None:
        host = os.getenv("NEO4J_HOST")
        port = os.getenv("NEO4J_BOLT_PORT")
        url = f"bolt://{host}:{port}"
        auth = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
    driver = None
    connection_attempts = 0
    while driver is None:
        connection_attempts += 1
        try:
            driver = gd.driver(url, auth=auth)
        except Exception as e:
            if connection_attempts >= 3:
                return None
            time.sleep(3)
    return driver

def close_driver(driver):
    driver.close()
