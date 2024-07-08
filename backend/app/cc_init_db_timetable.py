from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os

import modules.logger_tool as logger
os.environ['LOG_NAME'] = 'Timetable'
os.environ['LOG_DIR'] = 'logs'
os.environ['LOG_LEVEL'] = 'INFO'

logging = logger.get_logger(os.environ['LOG_NAME'], log_level=os.environ['LOG_LEVEL'], log_path=os.environ['LOG_DIR'], log_file=os.environ['LOG_NAME'])

import modules.database.schemas.calendar_neo as calendar_neo
import modules.database.schemas.timetable_neo as timetable_neo
import modules.database.schemas.relationships.calendar_rels as cal_rels
import modules.database.schemas.relationships.timetable_rels as tt_rels
import modules.database.schemas.relationships.calendar_timetable_rels as cal_tt_rels

import modules.database.tools.xl_tools as xl
import modules.database.tools.neontology_tools as neon
import modules.database.tools.neo4j_driver_tools as driver_tools

import requests
from datetime import timedelta, datetime, date
import pandas as pd
from pydantic import ValidationError

db_name = os.environ['LOG_NAME']

url = f'http://{os.environ["BACKEND_URL"]}:{os.environ["BACKEND_PORT"]}/database/admin/stop-database'
data = {'db_name': db_name}
response = requests.post(url, json=data)
logging.info(response.text)

url = f'http://{os.environ["BACKEND_URL"]}:{os.environ["BACKEND_PORT"]}/database/admin/drop-database'
data = {'db_name': db_name}
response = requests.post(url, json=data)
logging.info(response.text)

url = f'http://{os.environ["BACKEND_URL"]}:{os.environ["BACKEND_PORT"]}/database/admin/create-database'
params = {'db_name': db_name}
response = requests.post(url, params=params)
logging.info(response.text)

# Initialize driver
driver = driver_tools.get_driver(database=db_name)

# Initialize connection
neon.init_neo4j_connection()

def create_calendar(start_date, end_date, attach=False):
    # Dictionary to track created nodes to avoid duplicates
    created_years = {}
    created_months = {}
    created_weeks = {}
    created_days = {}

    # Variables to store the last node of each type
    last_year_node = None
    last_month_node = None
    last_week_node = None
    last_day_node = None

    # Dictionary to store the nodes and relationships
    calendar_nodes = {
        'calendar_node': [],
        'calendar_year_nodes': [],
        'calendar_month_nodes': [],
        'calendar_week_nodes': [],
        'calendar_day_nodes': []
    }
    
    current_date = start_date

    if attach:
        calendar_node = calendar_neo.CalendarNode(
            calendar_id=f"calendar_{db_name}",
            calendar_name=db_name
        )
        neon.create_or_merge_neontology_node(calendar_node, database=db_name, operation='merge')
        calendar_nodes['calendar_node'] = calendar_node

    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        day = current_date.day
        iso_year, iso_week, iso_weekday = current_date.isocalendar()

        # Ensure year node is created for the Gregorian calendar year
        if year not in created_years:
            year_node = calendar_neo.CalendarYearNode(
                unique_id=f"calendar_year_{year}",
                year=year,
                iso_year=str(year),
                localised_year_name=f"Year {year}"
            )
            neon.create_or_merge_neontology_node(year_node, database=db_name, operation='merge')
            calendar_nodes['calendar_year_nodes'].append(year_node)
            created_years[year] = year_node
            
            if attach:
                neon.create_or_merge_neontology_relationship(
                    cal_rels.CalendarIncludesYear(source=calendar_node, target=year_node),
                    database=db_name,
                    operation='merge'
                )

            if last_year_node:
                neon.create_or_merge_neontology_relationship(
                    cal_rels.YearFollowsYear(source=last_year_node, target=year_node),
                    database=db_name,
                    operation='merge'
                )
            last_year_node = year_node

        # Ensure month node is created
        month_key = f"{year}-{month}"
        if month_key not in created_months:
            month_node = calendar_neo.CalendarMonthNode(
                unique_id=f"calendar_month_{year}_{month}",
                month=month,
                month_name=datetime(year, month, 1).strftime('%B'),
                iso_month=f"{year}-{month:02}",
                localised_month_name=f"{datetime(year, month, 1).strftime('%B')} {year}"
            )
            neon.create_or_merge_neontology_node(month_node, database=db_name, operation='merge')
            calendar_nodes['calendar_month_nodes'].append(month_node)
            created_months[month_key] = month_node

            # Check for the end of year transition for months
            if last_month_node:
                if month == 1 and last_month_node.month == 12 and int(last_month_node.unique_id.split('_')[2]) == year - 1:
                    neon.create_or_merge_neontology_relationship(
                        cal_rels.MonthFollowsMonth(source=last_month_node, target=month_node),
                        database=db_name,
                        operation='merge'
                    )
                elif month == last_month_node.month + 1:
                    neon.create_or_merge_neontology_relationship(
                        cal_rels.MonthFollowsMonth(source=last_month_node, target=month_node),
                        database=db_name,
                        operation='merge'
                    )

            last_month_node = month_node

            neon.create_or_merge_neontology_relationship(
                cal_rels.YearIncludesMonth(source=year_node, target=month_node),
                database=db_name,
                operation='merge'
            )

        # Week node management
        week_key = f"{iso_year}-W{iso_week}"
        if week_key not in created_weeks:
            # Get the date of the first monday of the week
            week_start_date = current_date - timedelta(days=current_date.weekday())
            week_node = calendar_neo.CalendarWeekNode(
                unique_id=f"calendar_week_{iso_year}_{iso_week}",
                start_date=week_start_date,
                week_number=iso_week,
                iso_week=f"{iso_year}-W{iso_week:02}",
                localised_week_name=f"Week {iso_week}, {iso_year}"
            )
            neon.create_or_merge_neontology_node(week_node, database=db_name, operation='merge')
            calendar_nodes['calendar_week_nodes'].append(week_node)
            created_weeks[week_key] = week_node

            if last_week_node and ((last_week_node.iso_week.split('-')[0] == str(iso_year) and last_week_node.week_number == iso_week - 1) or
                                (last_week_node.iso_week.split('-')[0] != str(iso_year) and last_week_node.week_number == 52 and iso_week == 1)):
                neon.create_or_merge_neontology_relationship(
                    cal_rels.WeekFollowsWeek(source=last_week_node, target=week_node),
                    database=db_name,
                    operation='merge'
                )
            last_week_node = week_node

            neon.create_or_merge_neontology_relationship(
                cal_rels.YearIncludesWeek(source=year_node, target=week_node),
                database=db_name,
                operation='merge'
            )

        # Day node management
        day_key = f"{year}-{month}-{day}"
        day_node = calendar_neo.CalendarDayNode(
            unique_id=f"calendar_day_{year}_{month}_{day}",
            date=current_date,
            day_of_week=current_date.strftime('%A'),
            iso_day=f"{year}-{month:02}-{day:02}",
            localised_day_name=f"{current_date.strftime('%A')}, {current_date.strftime('%B')} {day}, {year}",
            is_weekend=current_date.weekday() > 4
        )
        neon.create_or_merge_neontology_node(day_node, database=db_name, operation='merge')
        calendar_nodes['calendar_day_nodes'].append(day_node)
        created_days[day_key] = day_node

        if last_day_node:
            neon.create_or_merge_neontology_relationship(
                cal_rels.DayFollowsDay(source=last_day_node, target=day_node),
                database=db_name,
                operation='merge'
            )
        last_day_node = day_node

        neon.create_or_merge_neontology_relationship(
            cal_rels.MonthIncludesDay(source=month_node, target=day_node),
            database=db_name,
            operation='merge'
        )

        neon.create_or_merge_neontology_relationship(
            cal_rels.WeekIncludesDay(source=week_node, target=day_node),
            database=db_name,
            operation='merge'
        )

        current_date += timedelta(days=1)
    logging.info(f'Created calendar: {calendar_nodes["calendar_node"].calendar_id}')
    return calendar_nodes

def create_calendar_and_timetable(data=None):
    # Check if data is None
    if data is None:
        raise ValueError("Data is required to create the calendar and timetable.")
    
    # Extract worksheets into dataframes
    school_df = data['schoollookup_df']
    terms_df = data['termslookup_df']
    weeks_df = data['weekslookup_df']
    days_df = data['dayslookup_df']
    periods_df = data['periodslookup_df']
    
    # Parse start and end dates for the timetable
    start_date_value = school_df[school_df['Identifier'] == 'AcademicYearStart']['Data'].iloc[0]
    end_date_value = school_df[school_df['Identifier'] == 'AcademicYearEnd']['Data'].iloc[0]

    if isinstance(start_date_value, str):
        start_date = datetime.strptime(start_date_value, '%Y-%m-%d')
    else:
        start_date = start_date_value

    if isinstance(end_date_value, str):
        end_date = datetime.strptime(end_date_value, '%Y-%m-%d')
    else:
        end_date = end_date_value

    school_id = school_df[school_df['Identifier'] == 'SchoolID']['Data'].iloc[0]

    # Create the calendar and retrieve nodes
    calendar_nodes = create_calendar(start_date, end_date, attach=True)

    # Create a dictionary to store the timetable nodes
    timetable_nodes = {
        'timetable_node': None,
        'academic_year_nodes': [],
        'academic_term_nodes': [],
        'academic_week_nodes': [],
        'academic_day_nodes': [],
        'academic_period_nodes': []
    }
    
    # Create AcademicTimetable Node
    academic_timetable_node = timetable_neo.AcademicTimetableNode(
        unique_id=f"{school_id}_{start_date.year}_{end_date.year}",
        name=f"{start_date.year} to {end_date.year}",
        start_date=start_date,
        end_date=end_date
    )
    neon.create_or_merge_neontology_node(academic_timetable_node, database=db_name, operation='merge')
    timetable_nodes['timetable_node'] = academic_timetable_node
    logging.debug(f'Created timetable node: {academic_timetable_node.unique_id}')

    # Create AcademicYear nodes for each year within the range
    for year in range(start_date.year, end_date.year + 1):
        academic_year_node = timetable_neo.AcademicYearNode(
            unique_id=f"AcademicYear_{school_id}_{year}",
            year=str(year)
        )
        neon.create_or_merge_neontology_node(academic_year_node, database=db_name, operation='merge')
        timetable_nodes['academic_year_nodes'].append(academic_year_node)
        logging.debug(f'Created academic year node: {academic_year_node.unique_id}')
        neon.create_or_merge_neontology_relationship(
            tt_rels.AcademicTimetableHasAcademicYear(source=academic_timetable_node, target=academic_year_node),
            database=db_name, operation='merge'
        )

        # Link the academic year with the corresponding calendar year node
        for year_node in calendar_nodes['calendar_year_nodes']:
            if year_node.year == year:
                neon.create_or_merge_neontology_relationship(
                    cal_tt_rels.CalendarYearIsAcademicYear(source=year_node, target=academic_year_node),
                    database=db_name, operation='merge'
                )
                neon.create_or_merge_neontology_relationship(
                    cal_tt_rels.AcademicYearIsCalendarYear(source=academic_year_node, target=year_node),
                    database=db_name, operation='merge'
                )
                break

    # Create Term and TermBreak nodes linked to AcademicYear
    for _, term_row in terms_df.iterrows():
        term_node_class = timetable_neo.AcademicTermNode if term_row['TermType'] == 'Term' else timetable_neo.AcademicTermBreakNode
        
        term_start_date = term_row['StartDate']
        if isinstance(term_start_date, pd.Timestamp):
            term_start_date = term_start_date.strftime('%Y-%m-%d')
        
        term_end_date = term_row['EndDate']
        if isinstance(term_end_date, pd.Timestamp):
            term_end_date = term_end_date.strftime('%Y-%m-%d')

        if term_row['TermType'] == 'Term':
            term_number = str(len(timetable_nodes['academic_term_nodes']) + 1)
            term_node = term_node_class(
                unique_id=f"{term_row['TermType']}_{term_row['TermName'].replace(' ', '')}",
                name=term_row['TermName'],
                number=term_number,
                start_date=datetime.strptime(term_start_date, '%Y-%m-%d') if term_start_date else None,
                end_date=datetime.strptime(term_end_date, '%Y-%m-%d') if term_end_date else None
            )
        else:
            term_node = term_node_class(
                unique_id=f"{term_row['TermType']}_{term_row['TermName'].replace(' ', '')}",
                name=term_row['TermName'],
                start_date=datetime.strptime(term_start_date, '%Y-%m-%d') if term_start_date else None,
                end_date=datetime.strptime(term_end_date, '%Y-%m-%d') if term_end_date else None
            )
        neon.create_or_merge_neontology_node(term_node, database=db_name, operation='merge')
        timetable_nodes['academic_term_nodes'].append(term_node)
        logging.debug(f'Created academic term node: {term_node.unique_id}')

        # Link term node to the correct academic year
        term_years = set()
        term_years.update([term_node.start_date.year, term_node.end_date.year])

        for academic_year_node in timetable_nodes['academic_year_nodes']:
            if int(academic_year_node.year) in term_years:
                relationship_class = tt_rels.AcademicYearHasAcademicTerm if term_row['TermType'] == 'Term' else tt_rels.AcademicYearHasAcademicTermBreak
                neon.create_or_merge_neontology_relationship(
                    relationship_class(source=academic_year_node, target=term_node),
                    database=db_name, operation='merge'
                )

    # Create Week nodes
    for _, week_row in weeks_df.iterrows():
        week_number = str(len(timetable_nodes['academic_week_nodes']) + 1)
        week_node_class = timetable_neo.HolidayWeekNode if week_row['WeekType'] == 'Holiday' else timetable_neo.AcademicWeekNode
        week_start_date = week_row['WeekStart']
        if isinstance(week_start_date, pd.Timestamp):
            week_start_date = week_start_date.strftime('%Y-%m-%d')
        
        if week_row['WeekType'] == 'Holiday':
            week_node = week_node_class(
                unique_id=f"{week_row['WeekType']}_{week_row['WeekNumber']}",
                start_date=datetime.strptime(week_start_date, '%Y-%m-%d')
            )
        else:
            week_node = week_node_class(
                unique_id=f"{week_row['WeekType']}_{week_row['WeekNumber']}",
                number=week_number,
                start_date=datetime.strptime(week_start_date, '%Y-%m-%d'),
                week_type=week_row['WeekType']
            )
        
        neon.create_or_merge_neontology_node(week_node, database=db_name, operation='merge')
        timetable_nodes['academic_week_nodes'].append(week_node)
        for calendar_node in calendar_nodes['calendar_week_nodes']:
            if calendar_node.start_date == week_node.start_date:
                if isinstance(week_node, timetable_neo.AcademicWeekNode):
                    neon.create_or_merge_neontology_relationship(
                        cal_tt_rels.CalendarWeekIsAcademicWeek(source=calendar_node, target=week_node),
                        database=db_name, operation='merge'
                    )
                    neon.create_or_merge_neontology_relationship(
                        cal_tt_rels.AcademicWeekIsCalendarWeek(source=week_node, target=calendar_node),
                        database=db_name, operation='merge'
                    )
                elif isinstance(week_node, timetable_neo.HolidayWeekNode):
                    neon.create_or_merge_neontology_relationship(
                        cal_tt_rels.CalendarWeekIsHolidayWeek(source=calendar_node, target=week_node),
                        database=db_name, operation='merge'
                    )
                    neon.create_or_merge_neontology_relationship(
                        cal_tt_rels.HolidayWeekIsCalendarWeek(source=week_node, target=calendar_node),
                        database=db_name, operation='merge'
                    )
                break
        logging.debug(f'Created academic week node: {week_node.unique_id}')

        # Link week node to the correct academic term
        for term_node in timetable_nodes['academic_term_nodes']:
            if term_node.start_date <= week_node.start_date <= term_node.end_date:
                relationship_class = tt_rels.AcademicTermHasAcademicWeek if week_row['WeekType'] != 'Holiday' else tt_rels.AcademicTermBreakHasHolidayWeek
                neon.create_or_merge_neontology_relationship(
                    relationship_class(source=term_node, target=week_node),
                    database=db_name, operation='merge'
                )
                break

        # Link week node to the correct academic year
        for academic_year_node in timetable_nodes['academic_year_nodes']:
            if int(academic_year_node.year) == week_node.start_date.year:
                relationship_class = tt_rels.AcademicYearHasAcademicWeek if week_row['WeekType'] != 'Holiday' else tt_rels.AcademicYearHasHolidayWeek
                neon.create_or_merge_neontology_relationship(
                    relationship_class(source=academic_year_node, target=week_node),
                    database=db_name, operation='merge'
                )
                break

    # Create Day nodes
    for _, day_row in days_df.iterrows():
        academic_day_number = str(len(timetable_nodes['academic_day_nodes']) + 1)
        
        date_str = day_row['Date']
        if isinstance(date_str, pd.Timestamp):
            date_str = date_str.strftime('%Y-%m-%d')

        day_node_class = {
            'Academic': timetable_neo.AcademicDayNode,
            'Holiday': timetable_neo.HolidayDayNode,
            'OffTimetable': timetable_neo.OffTimetableDayNode,
            'StaffDay': timetable_neo.StaffDayNode
        }[day_row['DayType']]

        day_node_data = {
            'unique_id': f"{day_row['DayType']}_{date_str}",
            'date': datetime.strptime(date_str, '%Y-%m-%d'),
            'day_of_week': day_row['DayOfWeek']
        }

        if day_row['DayType'] == 'Academic':
            day_node_data['number'] = academic_day_number
            day_node_data['day_type'] = day_row['WeekType']

        day_node = day_node_class(**day_node_data)
        neon.create_or_merge_neontology_node(day_node, database=db_name, operation='merge')
        for calendar_node in calendar_nodes['calendar_day_nodes']:
            if calendar_node.date == day_node.date:
                if isinstance(day_node, timetable_neo.AcademicDayNode):
                    neon.create_or_merge_neontology_relationship(
                        cal_tt_rels.CalendarDayIsAcademicDay(source=calendar_node, target=day_node),
                        database=db_name, operation='merge'
                    )
                    neon.create_or_merge_neontology_relationship(
                        cal_tt_rels.AcademicDayIsCalendarDay(source=day_node, target=calendar_node),
                        database=db_name, operation='merge'
                    )
                elif isinstance(day_node, timetable_neo.HolidayDayNode):
                    neon.create_or_merge_neontology_relationship(
                        cal_tt_rels.CalendarDayIsHolidayDay(source=calendar_node, target=day_node),
                        database=db_name, operation='merge'
                    )
                    neon.create_or_merge_neontology_relationship(
                        cal_tt_rels.HolidayDayIsCalendarDay(source=day_node, target=calendar_node),
                        database=db_name, operation='merge'
                    )
                elif isinstance(day_node, timetable_neo.OffTimetableDayNode):
                    neon.create_or_merge_neontology_relationship(
                        cal_tt_rels.CalendarDayIsOffTimetableDay(source=calendar_node, target=day_node),
                        database=db_name, operation='merge'
                    )
                    neon.create_or_merge_neontology_relationship(
                        cal_tt_rels.OffTimetableDayIsCalendarDay(source=day_node, target=calendar_node),
                        database=db_name, operation='merge'
                    )
                break
        timetable_nodes['academic_day_nodes'].append(day_node)
        logging.debug(f'Created academic day node: {day_node.unique_id}')

        # Link day node to the correct academic week
        for academic_week_node in timetable_nodes['academic_week_nodes']:
            if academic_week_node.start_date <= day_node.date <= (academic_week_node.start_date + timedelta(days=6)):
                if day_row['DayType'] == 'Academic':
                    relationship_class = tt_rels.AcademicWeekHasAcademicDay
                elif day_row['DayType'] == 'Holiday':
                    if hasattr(academic_week_node, 'week_type') and academic_week_node.week_type in ['A', 'B']:
                        relationship_class = tt_rels.AcademicWeekHasHolidayDay
                    else:
                        relationship_class = tt_rels.HolidayWeekHasHolidayDay
                elif day_row['DayType'] == 'OffTimetable':
                    relationship_class = tt_rels.AcademicWeekHasOffTimetableDay
                elif day_row['DayType'] == 'Staff':
                    relationship_class = tt_rels.AcademicWeekHasStaffDay
                else:
                    continue  # Skip linking for other day types
                neon.create_or_merge_neontology_relationship(
                    relationship_class(source=academic_week_node, target=day_node),
                    database=db_name, operation='merge'
                )
                break

        # Link day node to the correct academic term
        for term_node in timetable_nodes['academic_term_nodes']:
            if term_node.start_date <= day_node.date <= term_node.end_date:
                if day_row['DayType'] == 'Academic':
                    relationship_class = tt_rels.AcademicTermHasAcademicDay
                elif day_row['DayType'] == 'Holiday':
                    if isinstance(term_node, timetable_neo.AcademicTermNode):
                        relationship_class = tt_rels.AcademicTermHasHolidayDay
                    else:
                        relationship_class = tt_rels.AcademicTermBreakHasHolidayDay
                elif day_row['DayType'] == 'OffTimetable':
                    relationship_class = tt_rels.AcademicTermHasOffTimetableDay
                elif day_row['DayType'] == 'Staff':
                    relationship_class = tt_rels.AcademicTermHasStaffDay
                else:
                    continue  # Skip linking for other day types
                neon.create_or_merge_neontology_relationship(
                    relationship_class(source=term_node, target=day_node),
                    database=db_name, operation='merge'
                )
                break

        # Create Period nodes for each academic day
        if day_row['DayType'] == 'Academic' and day_node.day_type in ['A', 'B']:
            for _, period_row in periods_df.iterrows():
                period_node_class = {
                    'Academic': timetable_neo.AcademicPeriodNode,
                    'Registration': timetable_neo.RegistrationPeriodNode,
                    'Break': timetable_neo.BreakPeriodNode,
                    'OffTimetable': timetable_neo.OffTimetablePeriodNode
                }[period_row['PeriodType']]
                
                period_node_data = {
                    'unique_id': f"{period_row['PeriodType']}_{day_node.unique_id}_{str(period_row['StartTime']).replace(':', '')}_{str(period_row['EndTime']).replace(':', '')}",
                    'name': period_row['PeriodName'],
                    'day_of_week': day_node.day_of_week,
                    'start_time': datetime.combine(day_node.date, period_row['StartTime']),
                    'end_time': datetime.combine(day_node.date, period_row['EndTime'])
                }
                
                if period_row['PeriodType'] == 'Academic':
                    period_node_data['day_type'] = day_node.day_type

                period_node = period_node_class(**period_node_data)
                neon.create_or_merge_neontology_node(period_node, database=db_name, operation='merge')
                timetable_nodes['academic_period_nodes'].append(period_node)
                logging.debug(f'Created academic period node: {period_node.unique_id}')
                
                relationship_class = {
                    'Academic': tt_rels.AcademicDayHasAcademicPeriod,
                    'Registration': tt_rels.AcademicDayHasRegistrationPeriod,
                    'Break': tt_rels.AcademicDayHasBreakPeriod,
                    'OffTimetable': tt_rels.AcademicDayHasOffTimetablePeriod
                }[period_row['PeriodType']]
                
                neon.create_or_merge_neontology_relationship(
                    relationship_class(source=day_node, target=period_node),
                    database=db_name, operation='merge'
                )

    def create_timetable_node_sequence_rels(timetable_nodes):
        # Sort and create relationships for Academic Years
        academic_year_nodes = sorted(timetable_nodes['academic_year_nodes'], key=lambda x: int(x.year))
        for i in range(len(academic_year_nodes) - 1):
            neon.create_or_merge_neontology_relationship(
                tt_rels.AcademicYearFollowsAcademicYear(
                    source=academic_year_nodes[i],
                    target=academic_year_nodes[i + 1]
                ),
                database=db_name, operation='merge'
            )
        
        # Sort and create relationships for Academic Terms and Term Breaks
        academic_term_nodes = sorted(timetable_nodes['academic_term_nodes'], key=lambda x: x.start_date)
        for i in range(len(academic_term_nodes) - 1):
            if isinstance(academic_term_nodes[i], timetable_neo.AcademicTermNode) and isinstance(academic_term_nodes[i + 1], timetable_neo.AcademicTermBreakNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.AcademicTermFollowsAcademicTermBreak(
                        source=academic_term_nodes[i],
                        target=academic_term_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_term_nodes[i], timetable_neo.AcademicTermBreakNode) and isinstance(academic_term_nodes[i + 1], timetable_neo.AcademicTermNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.AcademicTermBreakFollowsAcademicTerm(
                        source=academic_term_nodes[i],
                        target=academic_term_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
        
        # Sort and create relationships for Academic Weeks
        academic_week_nodes = sorted(timetable_nodes['academic_week_nodes'], key=lambda x: x.start_date)
        for i in range(len(academic_week_nodes) - 1):
            if isinstance(academic_week_nodes[i], timetable_neo.AcademicWeekNode) and isinstance(academic_week_nodes[i + 1], timetable_neo.AcademicWeekNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.AcademicWeekFollowsAcademicWeek(
                        source=academic_week_nodes[i],
                        target=academic_week_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_week_nodes[i], timetable_neo.HolidayWeekNode) and isinstance(academic_week_nodes[i + 1], timetable_neo.HolidayWeekNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.HolidayWeekFollowsHolidayWeek(
                        source=academic_week_nodes[i],
                        target=academic_week_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_week_nodes[i], timetable_neo.AcademicWeekNode) and isinstance(academic_week_nodes[i + 1], timetable_neo.HolidayWeekNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.AcademicWeekFollowsHolidayWeek(
                        source=academic_week_nodes[i],
                        target=academic_week_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_week_nodes[i], timetable_neo.HolidayWeekNode) and isinstance(academic_week_nodes[i + 1], timetable_neo.AcademicWeekNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.HolidayWeekFollowsAcademicWeek(
                        source=academic_week_nodes[i],
                        target=academic_week_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
        
        # Sort and create relationships for Academic Days
        academic_day_nodes = sorted(timetable_nodes['academic_day_nodes'], key=lambda x: x.date)
        for i in range(len(academic_day_nodes) - 1):
            if isinstance(academic_day_nodes[i], timetable_neo.AcademicDayNode) and isinstance(academic_day_nodes[i + 1], timetable_neo.AcademicDayNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.AcademicDayFollowsAcademicDay(
                        source=academic_day_nodes[i],
                        target=academic_day_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_day_nodes[i], timetable_neo.HolidayDayNode) and isinstance(academic_day_nodes[i + 1], timetable_neo.HolidayDayNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.HolidayDayFollowsHolidayDay(
                        source=academic_day_nodes[i],
                        target=academic_day_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_day_nodes[i], timetable_neo.AcademicDayNode) and isinstance(academic_day_nodes[i + 1], timetable_neo.HolidayDayNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.AcademicDayFollowsHolidayDay(
                        source=academic_day_nodes[i],
                        target=academic_day_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_day_nodes[i], timetable_neo.OffTimetableDayNode) and isinstance(academic_day_nodes[i + 1], timetable_neo.OffTimetableDayNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.OffTimetableDayFollowsOffTimetableDay(
                        source=academic_day_nodes[i],
                        target=academic_day_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_day_nodes[i], timetable_neo.OffTimetableDayNode) and isinstance(academic_day_nodes[i + 1], timetable_neo.AcademicDayNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.OffTimetableDayFollowsAcademicDay(
                        source=academic_day_nodes[i],
                        target=academic_day_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_day_nodes[i], timetable_neo.OffTimetableDayNode) and isinstance(academic_day_nodes[i + 1], timetable_neo.HolidayDayNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.OffTimetableDayFollowsHolidayDay(
                        source=academic_day_nodes[i],
                        target=academic_day_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_day_nodes[i], timetable_neo.StaffDayNode) and isinstance(academic_day_nodes[i + 1], timetable_neo.StaffDayNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.StaffDayFollowsStaffDay(
                        source=academic_day_nodes[i],
                        target=academic_day_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_day_nodes[i], timetable_neo.StaffDayNode) and isinstance(academic_day_nodes[i + 1], timetable_neo.AcademicDayNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.StaffDayFollowsAcademicDay(
                        source=academic_day_nodes[i],
                        target=academic_day_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_day_nodes[i], timetable_neo.StaffDayNode) and isinstance(academic_day_nodes[i + 1], timetable_neo.HolidayDayNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.StaffDayFollowsHolidayDay(
                        source=academic_day_nodes[i],
                        target=academic_day_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
        # Sort and create relationships for Academic Periods
        academic_period_nodes = sorted(timetable_nodes['academic_period_nodes'], key=lambda x: (x.start_time, x.end_time))
        for i in range(len(academic_period_nodes) - 1):
            if isinstance(academic_period_nodes[i], timetable_neo.AcademicPeriodNode) and isinstance(academic_period_nodes[i + 1], timetable_neo.AcademicPeriodNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.AcademicPeriodFollowsAcademicPeriod(
                        source=academic_period_nodes[i],
                        target=academic_period_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_period_nodes[i], timetable_neo.AcademicPeriodNode) and isinstance(academic_period_nodes[i + 1], timetable_neo.BreakPeriodNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.AcademicPeriodFollowsBreakPeriod(
                        source=academic_period_nodes[i],
                        target=academic_period_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_period_nodes[i], timetable_neo.AcademicPeriodNode) and isinstance(academic_period_nodes[i + 1], timetable_neo.RegistrationPeriodNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.AcademicPeriodFollowsRegistrationPeriod(
                        source=academic_period_nodes[i],
                        target=academic_period_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_period_nodes[i], timetable_neo.BreakPeriodNode) and isinstance(academic_period_nodes[i + 1], timetable_neo.AcademicPeriodNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.BreakPeriodFollowsAcademicPeriod(
                        source=academic_period_nodes[i],
                        target=academic_period_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_period_nodes[i], timetable_neo.RegistrationPeriodNode) and isinstance(academic_period_nodes[i + 1], timetable_neo.AcademicPeriodNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.RegistrationPeriodFollowsAcademicPeriod(
                        source=academic_period_nodes[i],
                        target=academic_period_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_period_nodes[i], timetable_neo.RegistrationPeriodNode) and isinstance(academic_period_nodes[i + 1], timetable_neo.OffTimetablePeriodNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.RegistrationPeriodFollowsOffTimetablePeriod(
                        source=academic_period_nodes[i],
                        target=academic_period_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_period_nodes[i], timetable_neo.OffTimetablePeriodNode) and isinstance(academic_period_nodes[i + 1], timetable_neo.OffTimetablePeriodNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.OffTimetablePeriodFollowsOffTimetablePeriod(
                        source=academic_period_nodes[i],
                        target=academic_period_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            elif isinstance(academic_period_nodes[i], timetable_neo.OffTimetablePeriodNode) and isinstance(academic_period_nodes[i + 1], timetable_neo.AcademicPeriodNode):
                neon.create_or_merge_neontology_relationship(
                    tt_rels.OffTimetablePeriodFollowsAcademicPeriod(
                        source=academic_period_nodes[i],
                        target=academic_period_nodes[i + 1]
                    ),
                    database=db_name, operation='merge'
                )
            
        logging.info("Created all timetable node sequence relationships")

    logging.info(f'Created timetable: {timetable_nodes["timetable_node"].unique_id}')
    
    # Call the function with the created timetable nodes
    create_timetable_node_sequence_rels(timetable_nodes)

    return {
        'calendar_nodes': calendar_nodes,
        'timetable_nodes': timetable_nodes
    }

nodes = create_calendar_and_timetable(data=xl.create_dataframes(os.getenv("EXCEL_TIMETABLE_FILE")))
