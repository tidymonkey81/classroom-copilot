from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import modules.logger_tool as logger
log_name = 'api_modules_database_tools_init_calendar'
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
from modules.database.tools.db_operations import stop_database, drop_database, create_database
import modules.database.schemas.calendar_neo as calendar_neo
import modules.database.schemas.relationships.calendar_rels as cal_rels
import modules.database.tools.neontology_tools as neon
import modules.database.tools.neo4j_driver_tools as driver_tools
import requests
from datetime import timedelta, datetime

def create_calendar(db_name, start_date, end_date, attach=False):
    stop_database(db_name)
    drop_database(db_name)
    create_database(db_name)

    db_name = db_name

    db_name=db_name

    created_years = {}
    created_months = {}
    created_weeks = {}
    created_days = {}

    last_year_node = None
    last_month_node = None
    last_week_node = None
    last_day_node = None

    calendar_nodes = {
        'calendar_node': None,
        'calendar_year_nodes': [],
        'calendar_month_nodes': [],
        'calendar_week_nodes': [],
        'calendar_day_nodes': []
    }
    
    current_date = start_date

    if attach:
        calendar_node = calendar_neo.CalendarNode(
            unique_id=f"calendar_{db_name}",
            name=db_name
        )
        neon.create_or_merge_neontology_node(calendar_node, database=db_name, operation='merge')
        calendar_nodes['calendar_node'] = calendar_node

    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        day = current_date.day
        iso_year, iso_week, iso_weekday = current_date.isocalendar()

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
    
    if attach:
        log_message_name = calendar_nodes["calendar_node"].unique_id
    else:
        log_message_name = f"calendar_{db_name}"
    logging.info(f'Created calendar: {log_message_name}')
    return calendar_nodes