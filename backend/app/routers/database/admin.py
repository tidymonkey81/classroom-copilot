import modules.logger_tool as logger

import modules.database.tools.neo4j_driver_tools as driver
import modules.database.tools.neo4j_session_tools as session
import modules.database.tools.neo4j_http_tools as http
import modules.database.tools.queries as query

import os
from fastapi import APIRouter, Depends
from dependencies import admin_dependency
from pydantic import BaseModel

router = APIRouter()

logging = logger.get_logger(os.environ['LOG_NAME'], log_level=os.environ['LOG_LEVEL'], log_path=os.environ['LOG_DIR'], log_file=os.environ['LOG_NAME'])

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
