import sys
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
sys.path.append(os.getenv("PY_MODULES_PATH"))
import logger_tool as logger
logging = logger.get_logger(name='logger_tool')

import pandas as pd

# Function to output all excel sheets as pandas dataframes with specific naming
def get_excel_sheets(excel_file, return_clean=False):
    excel_sheets = pd.read_excel(excel_file, sheet_name=None)
    dataframes = {sheet.lower() + '_df': data for sheet, data in excel_sheets.items()}
    logging.debug(f"Excel sheets: {list(dataframes.keys())}")
    return dataframes