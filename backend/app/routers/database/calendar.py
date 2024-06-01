from fastapi import APIRouter, Depends, File, UploadFile
from ..dependencies import admin_dependency

router = APIRouter()

@router.post("/create-global-calendar")
async def create_global_calendar(file: UploadFile = File(...), admin: bool = Depends(admin_dependency)):
    # Logic to process file and create global calendar
    return {"status": "Global Calendar Created"}

@router.post("/upload-school-calendar")
async def upload_school_calendar(file: UploadFile = File(...)):
    # Logic to process file and create school calendar
    return {"status": "School Calendar Uploaded"}


