from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import modules.logger_tool as logger
log_name = 'api_routers_database_init_calendar'
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
import modules.database.init.init_calendar as init_calendar
from fastapi import APIRouter
from datetime import date

router = APIRouter()

@router.post("/create-calendar")
async def create_calendar(db_name: str, start_date: date, end_date: date, attach: bool = False):
    logging.info(f"Creating calendar for {db_name} from {start_date} to {end_date}")
    return init_calendar.create_calendar(db_name, start_date, end_date, attach)
