from fastapi import APIRouter, Depends, File, UploadFile
from ..dependencies import admin_dependency
from app.modules.driver_tools import send_neo4j_request

router = APIRouter()

@router.post("/create-global-school-db")
async def create_global_school_db():
    query = "CREATE DATABASE `GlobalSchools` IF NOT EXISTS"
    return send_neo4j_request(query) 

