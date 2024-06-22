from fastapi import APIRouter

import app.routers.database.tools.neo4j_driver_tools as driver
import app.routers.database.tools.neo4j_session_tools as session
import app.routers.database.tools.neo4j_http_tools as http
import app.routers.database.tools.query_library as query

router = APIRouter()

@router.post("/create-database")
async def create_database(db_name: str):
    return http.send_query(query.create_database(db_name), encoded_credentials=None, params=None, method="POST", database="system", endpoint="/tx/commit")

@router.post("/reset-database")
async def reset_database(db_name: str):
    