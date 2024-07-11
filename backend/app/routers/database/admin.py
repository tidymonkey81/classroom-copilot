from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import modules.logger_tool as logger
log_name = 'api_routers_database_admin'
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
import modules.database.tools.neo4j_http_tools as http
import modules.database.tools.queries as query
from fastapi import APIRouter, Depends
from dependencies import admin_dependency
from pydantic import BaseModel

router = APIRouter()

class DatabaseRequest(BaseModel):
    db_name: str

@router.post("/create-database")
async def create_database(db_name: str):
    logging.info(f"Creating database: {db_name}")
    generated_query = query.create_database(db_name)
    logging.info(f"Generated query: {generated_query}")
    return http.send_query(generated_query, encoded_credentials=None, params=None, method="POST", database="system", endpoint="/tx/commit")

@router.post("/stop-database")
async def stop_database(request: DatabaseRequest):
    db_name = request.db_name
    logging.info(f"Stopping database: {db_name}")
    generated_query = query.stop_database(db_name)
    return http.send_query(generated_query, encoded_credentials=None, params=None, method="POST", database="system", endpoint="/tx/commit")

@router.post("/drop-database")
async def drop_database(request: DatabaseRequest):
    db_name = request.db_name
    logging.info(f"Dropping database: {db_name}")
    generated_query = query.drop_database(db_name)
    return http.send_query(generated_query, encoded_credentials=None, params=None, method="POST", database="system", endpoint="/tx/commit")

@router.post("/reset-database")
async def reset_database(db_name: str):
    pass

@router.post("/backup-database")
async def backup_database(admin: bool = Depends(admin_dependency)):
    # Placeholder for database backup logic
    return {"status": "success", "message": "Database backup initiated"}

@router.get("/view-logs")
async def view_logs(admin: bool = Depends(admin_dependency)):
    # Placeholder for log viewing logic
    return {"status": "success", "message": "Logs displayed"}

@router.post("/execute-query")
async def execute_query(query: str, admin: bool = Depends(admin_dependency)):
    # Placeholder for query execution logic
    return {"status": "success", "message": "Query executed"}
