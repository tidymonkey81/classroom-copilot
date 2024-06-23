import datetime
from typing import ClassVar
from neontology import BaseNode

# Neo4j Nodes and relationships using Neontology
# Calendar layer

class CalendarYearNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'CalendarYear'
    __primaryproperty__: ClassVar[str] = 'calendar_year_id'
    calendar_year_id: str
    calendar_year_start_date: datetime.date
    calendar_year_end_date: datetime.date
    calendar_year_notes: str
    
class CalendarMonthNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'CalendarMonth'
    __primaryproperty__: ClassVar[str] = 'calendar_month_id'
    calendar_month_id: str
    calendar_month_start_date: datetime.date
    calendar_month_end_date: datetime.date
    calendar_month_notes: str
    
class CalendarWeekNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'CalendarWeek'
    __primaryproperty__: ClassVar[str] = 'calendar_week_id'
    week_id: str
    week_start_date: datetime.date
    week_end_date: datetime.date
    week_type: str
    week_notes: str
    
class CalendarDayNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'CalendarDay'
    __primaryproperty__: ClassVar[str] = 'calendar_day_id'
    day_id: str
    date: datetime.date
    day: str
    day_modifier: str
    auto_agenda: str
    agenda_heading: str
    agenda_notes: str