from fastapi import APIRouter, Depends, File, UploadFile
from dependencies import admin_dependency
from modules.database.tools.neo4j_driver_tools import get_driver
from modules.database.tools.neo4j_http_tools import create_node, create_relationship
import modules.database.tools.xl_tools as xl

router = APIRouter()

@router.post("/upload-subject-curriculum")
async def upload_subject_curriculum(file: UploadFile = File(...)):
    # Logic to process curriculum data
    return {"status": "Subject Curriculum Uploaded"}

router = APIRouter()

@router.post("/upload-curriculum")
async def upload_curriculum(file: UploadFile = File(...)):
    if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        return {"status": "Error", "message": "Invalid file format"}

    try:
        # Read the Excel file into dataframes
        dataframes = xl.create_dataframes(await file.read())
        # Process the dataframes to create the graph
        result = process_curriculum_data(dataframes)
        return {"status": "Success", "data": result}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

def process_curriculum_data(dataframes):
    driver = get_driver()
    with driver.session() as session:
        # Example: Create nodes and relationships
        return "Graph created successfully"