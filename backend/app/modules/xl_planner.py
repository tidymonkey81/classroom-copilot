import pandas as pd

def create_dataframes(excel_file, return_clean=False):
    excel_sheets = pd.read_excel(excel_file, sheet_name=None)
    return {sheet.lower() + '_df': data for sheet, data in excel_sheets.items()}

