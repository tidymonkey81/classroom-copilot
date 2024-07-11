from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import modules.logger_tool as logger
log_name = 'api_modules_database_tools_init_timetable'
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
import modules.database.schemas.timetable_neo as timetable_neo
import modules.database.schemas.relationships.timetable_rels as tt_rels
import modules.database.schemas.relationships.calendar_timetable_rels as cal_tt_rels
import modules.database.tools.neontology_tools as neon
from datetime import timedelta, datetime
import pandas as pd

def create_timetable(dataframes, db_name):
    if dataframes is None:
        raise ValueError("Data is required to create the calendar and timetable.")
    
    school_df = dataframes['school']
    terms_df = dataframes['terms']
    weeks_df = dataframes['weeks']
    days_df = dataframes['days']
    periods_df = dataframes['periods']
    
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

    calendar_nodes = init_calendar.create_calendar(db_name, start_date, end_date, attach=False)

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
                        cal_tt_rels.AcademicWeekIsCalendarWeek(source=week_node, target=calendar_node),
                        database=db_name, operation='merge'
                    )
                elif isinstance(week_node, timetable_neo.HolidayWeekNode):
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
                        cal_tt_rels.AcademicDayIsCalendarDay(source=day_node, target=calendar_node),
                        database=db_name, operation='merge'
                    )
                elif isinstance(day_node, timetable_neo.HolidayDayNode):
                    neon.create_or_merge_neontology_relationship(
                        cal_tt_rels.HolidayDayIsCalendarDay(source=day_node, target=calendar_node),
                        database=db_name, operation='merge'
                    )
                elif isinstance(day_node, timetable_neo.OffTimetableDayNode):
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