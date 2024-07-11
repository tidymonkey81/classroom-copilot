from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import modules.logger_tool as logger
log_name = 'api_modules_database_tools_xl_tools'
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
import pandas as pd
from fastapi import UploadFile

def create_dataframes(excel_file, return_clean=False):
    excel_sheets = pd.read_excel(excel_file, sheet_name=None)
    return {sheet.lower() + '_df': data for sheet, data in excel_sheets.items()}

def create_dataframes_from_fastapiuploadfile(upload_file: UploadFile):
    from io import BytesIO
    file_content = upload_file.file.read()
    file_content_io = BytesIO(file_content)
    return pd.read_excel(file_content_io, sheet_name=None, engine='openpyxl')

def replace_nan_with_default(data, default_values):
    for key in default_values:
        if pd.isna(data.get(key, None)):
            # logging.debug(f"Replacing NaN in {key} with default value '{default_values[key]}'")
            data[key] = default_values[key]
    return data
