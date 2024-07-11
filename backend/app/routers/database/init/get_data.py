from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import modules.logger_tool as logger
log_name = 'api_routers_database_init_get_data'
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
from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/get-dataframes-from-xl")
async def get_dataframes_from_xl(file: UploadFile = File(...)):
    if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        return {"status": "Error", "message": "Invalid file format"}
    try:
        logging.info(f"Getting dataframes from {file.filename}")
        return xl.create_dataframes(await file.read())
    except Exception as e:
        return {"status": "Error", "message": str(e)}