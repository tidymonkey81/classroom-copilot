from fastapi import APIRouter, Depends, File, UploadFile
from ..dependencies import admin_dependency
from ..modules.driver_tools import get_driver, create_node, create_relationship
from ..modules.get_planner import get_excel_sheets

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
        dataframes = get_excel_sheets(await file.read())
        # Process the dataframes to create the graph
        result = process_curriculum_data(dataframes)
        return {"status": "Success", "data": result}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

def process_curriculum_data(dataframes):
    driver = get_driver()
    with driver.session() as session:
        # Example: Create nodes and relationships
        for label, df in dataframes.items():
            for _, row in df.iterrows():
                node_properties = prepare_local_curriculum_node(label, row)
                node = create_node(session, label, node_properties)
                # Assume relationships are to be created here
                # create_relationship(session, start_node, end_node, rel_type, properties)
        return "Graph created successfully"