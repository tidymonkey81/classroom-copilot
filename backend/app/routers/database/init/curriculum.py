from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import modules.logger_tool as logger
log_name = 'api_routers_database_init_curriculum'
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
import modules.database.init.xl_tools as xl
import modules.database.init.init_curriculum as init_curriculum
from fastapi import APIRouter, File, UploadFile, Form

router = APIRouter()

@router.post("/upload-curriculum")
async def upload_curriculum(file: UploadFile = File(...), db_name: str = Form(...)):
    if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        return {"status": "Error", "message": "Invalid file format"}
    logging.info(f"Uploading curriculum for {db_name}")
    dataframes = xl.create_dataframes_from_fastapiuploadfile(file)
    return init_curriculum.create_curriculum(dataframes, db_name)