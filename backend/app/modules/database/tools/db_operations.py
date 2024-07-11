from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import modules.logger_tool as logger
log_name = 'api_routers_database_init_timetable'
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
from fastapi.testclient import TestClient

def get_client():
    from routers.main import app  # Delayed import to avoid circular dependency
    return TestClient(app)

def stop_database(db_name):
    client = get_client()
    response = client.post("/database/admin/stop-database", json={"db_name": db_name})
    logging.info(response.text)
    return response

def drop_database(db_name):
    client = get_client()
    response = client.post("/database/admin/drop-database", json={"db_name": db_name})
    logging.info(response.text)
    return response

def create_database(db_name):
    client = get_client()
    response = client.post("/database/admin/create-database", params={"db_name": db_name})
    logging.info(response.text)
    return response