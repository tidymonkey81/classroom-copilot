import sys
import os
import pandas as pd
from datetime import datetime, time, timedelta

# Function to output all excel sheets as pandas dataframes with specific naming
def get_excel_sheets(excel_file, return_clean=False):
    excel_sheets = pd.read_excel(excel_file, sheet_name=None)
    return {sheet.lower() + '_df': data for sheet, data in excel_sheets.items()}

def extract_academic_year_info(calendar_df, info_type):
    # logging.debug(f"Extracting academic year info for {info_type}...")
    # logging.pedantic(f"calendar_df: {calendar_df}")
    academic_year_info = {}
    for index, row in calendar_df.iterrows():
        identifier = str(row['Identifier'])  # Convert identifier to string
        if info_type == 'staff':
            if 'StaffYear' in identifier:
                if 'Start' in identifier:
                    academic_year_info['start_date'] = row['Data']
                elif 'End' in identifier:
                    academic_year_info['end_date'] = row['Data']
        elif info_type == 'student':
            if 'AcademicYear' in identifier:
                if 'Start' in identifier:
                    academic_year_info['start_date'] = row['Data']
                elif 'End' in identifier:
                    academic_year_info['end_date'] = row['Data']
        else:
            raise ValueError("Invalid info_type. Choose 'staff' or 'student'.")
    return academic_year_info

def extract_academic_terms_or_breaks(calendar_df, info_type='term'):
    academic_periods = []
    identifiers = calendar_df['Identifier'].unique()
    if info_type == 'term':
        term_identifiers = [id for id in identifiers if 'Term' in str(id) and 'Start' in str(id)]
        for identifier in term_identifiers:
            term_name = identifier.split('Term')[0] + 'Term'  # Adjusted to include 'Term' in the term name
            start_date = calendar_df[calendar_df['Identifier'] == identifier]['Data'].iloc[0]
            end_date_identifier = identifier.replace('Start', 'End')
            end_date = calendar_df[calendar_df['Identifier'] == end_date_identifier]['Data'].iloc[0]
            academic_periods.append({'name': term_name, 'start_date': start_date, 'end_date': end_date})
            
    elif info_type == 'break':
        break_identifiers = [id for id in identifiers if 'Break' in str(id) and 'Start' in str(id) and not 'Period' in str(id)]  # Exclude 'Period' from 'Break' identifiers
        for identifier in break_identifiers:
            break_name = identifier.split('Break')[0]  # Extract the full break name before 'Break'
            break_name = break_name.replace(' ', '')  # Remove any spaces from the break name
            start_date = calendar_df[calendar_df['Identifier'] == identifier]['Data'].iloc[0]
            end_date_identifier = identifier.replace('Start', 'End')
            end_date = calendar_df[calendar_df['Identifier'] == end_date_identifier]['Data'].iloc[0]
            academic_periods.append({'name': break_name + 'Break', 'start_date': start_date, 'end_date': end_date})
    else:
        raise ValueError("Invalid info_type. Choose 'term' or 'break'.")
    return academic_periods

def populate_weeks_array(weekslookup_df):
    excel_weeks_list_of_dicts = []
    for _, row in weekslookup_df.iterrows():
        week_type = f"academic_week_{row['WeekType']}" if row['WeekType'] in ['A', 'B'] else \
                'holiday' if row['WeekType'] == 'H' else \
                'staff_only' if row['WeekType'] =='S' else ValueError(f"WeekType {row['WeekType']} not recognized")
        week_info = {
            'week_number': row['AcademicWeek'],
            'start_date': row['WeekStartDate'],
            'end_date': row['WeekStartDate'] + timedelta(days=6),
            'type': week_type,
            'calendar_agenda': row['WeekCalendarAgenda'],
            'agenda_heading': row['WeekAgendaHeading'],
            'agenda_notes': row['WeekAgendaNotes']
        }
        if week_type == 'academic_week':
            week_info['academic_week_type'] = 'A' if row['WeekType'] == 'A' else 'B'
        excel_weeks_list_of_dicts.append(week_info)
    return excel_weeks_list_of_dicts

def populate_days_array(dayslookup_df):
    excel_days_list_of_dicts = []
    for _, row in dayslookup_df.iterrows():
        day_type = 'academic_day' if row['DayModifier'] == 'A' else \
                'partial' if row['DayModifier'] == 'P' else \
                'holiday' if row['DayModifier'] == 'H' else \
                'staff_day' if row['DayModifier'] == 'S' else \
                'off_timetable' if row['DayModifier'] == 'O' else ValueError(f"DayModifier {row['DayModifier']} not recognized")
        day_info = {
            'date': row['Date'],
            'type': day_type,
            'calendar_agenda': row['DayCalendarAgenda'],
            'agenda_heading': row['DayAgendaHeading'],
            'agenda_notes': row['DayAgendaNotes']
        }
        excel_days_list_of_dicts.append(day_info)
    return excel_days_list_of_dicts

def extract_period_times(calendar_df):
    period_times = {}
    for row in calendar_df.itertuples():
        identifier = str(row.Identifier)
        if '.PeriodStartTime' in identifier or '.PeriodEndTime' in identifier:
            parts = identifier.split('.')
            period_class = parts[0]  # e.g., A=auto, F=manual_work, M=meeting, R=registration, P=period
            period_name = parts[1]  # e.g., Registration, [1, 2, 3, 4, 5, 6], Break, Lunch, Meeting, day_autostart, day_autostop, day_begin, day_end
            time_type = 'start' if 'StartTime' in identifier else 'end'
            time_data = row.Data
            if isinstance(time_data, time):
                time_obj = time_data
            else:
                time_obj = datetime.strptime(time_data, '%H:%M').time() # Convert the time to a datetime.time object, assuming the time is in HH:MM format
            if period_name not in period_times:
                period_times[period_name] = {}
            if not period_times[period_name].get('class'):
                period_times[period_name]['class'] = period_class
            period_times[period_name][time_type] = time_obj
    return period_times

# Function to convert a date string to a date object
def convert_excel_date(excel_date):
    if pd.isna(excel_date) or excel_date == 'Null':
        # logging.debug(f"Doing nothing. Excel date is NaN or Null: {excel_date}")
        return None
    if isinstance(excel_date, datetime):
        # logging.debug(f"Sending it back. Excel date is already a datetime: {excel_date}")
        return excel_date.date()
    else:
        # Assuming excel_date is a fraction of the day
        # logging.debug(f"Making assumption. Excel date is a fraction of the day: {excel_date}")
        return (datetime(1899, 12, 30) + timedelta(days=excel_date)).date()

# Function to convert a time string to a time object
def convert_to_date(date_str):
    try:
        # logging.debug(f"Converting {date_str} to date object...")
        return pd.to_datetime(date_str, dayfirst=True).date()  # Assuming day comes first in your date format
    except ValueError:
        # logging.error(f"Error converting {date_str} to date object.")
        return None

