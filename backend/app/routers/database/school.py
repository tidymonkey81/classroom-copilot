from fastapi import APIRouter, Depends, File, UploadFile
from ..dependencies import admin_dependency

router = APIRouter()

@router.post("/create-school")
async def add_school_to_global(file: UploadFile = File(...)):
    if file is None:
        return {"status": "Error", "message": "No file received"}

    try:
        import pandas as pd
        from io import BytesIO
        data = pd.read_excel(BytesIO(await file.read()), usecols=[0], nrows=5).squeeze()
        print("Data read from file:", data)
        if len(data) < 5:
            return {"status": "Error", "message": "Insufficient data in file"}
        school_data = {
            "name": data[0],
            "address": data[1],
            "ofsted_number": data[2],
            "website": data[3],
            "geo_location": data[4]
        }
        from app.modules.driver_tools import create_node_http
        response = create_node_http("globalschools", "School", school_data)
        return {"status": "School added to global school db via HTTP", "school_data": school_data, "response": response}
    except Exception as e:
        print("Failed to process file:", e)
        return {"status": "Error", "message": "Failed to process file"}

@router.post("/create-school-db")
async def create_school_db(file: UploadFile = File(...)):
    import pandas as pd
    import subprocess
    from io import BytesIO
    data = pd.read_excel(BytesIO(await file.read()), usecols=[0], skiprows=1, nrows=1).squeeze()
    school_name = data[0].replace(" ", "_").lower()  # Format the school name to be suitable for a database name
    command = f"docker exec neo4j_container neo4j-admin dbms create --database={school_name}"
    process = subprocess.run(command, shell=True, capture_output=True)
    if process.returncode == 0:
        return {"status": "School DB Created", "database_name": school_name}
    else:
        return {"status": "Failed to create database", "error": process.stderr}

