from modules.database.tools.neontology.basenode import BaseNode
import datetime
from typing import ClassVar

# Neo4j Nodes and relationships using Neontology
# Calendar layer
class CalendarNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Calendar'
    __primaryproperty__: ClassVar[str] = 'calendar_id'
    calendar_id: str
    calendar_name: str

class CalendarYearNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'CalendarYear'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str
    year: int
    iso_year: str  # ISO 8601 year
    localised_year_name: str

class CalendarMonthNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'CalendarMonth'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str
    month: int
    month_name: str
    iso_month: str  # ISO 8601 month
    localised_month_name: str

class CalendarWeekNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'CalendarWeek'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str
    start_date: datetime.date
    week_number: int
    iso_week: str  # ISO 8601 week
    localised_week_name: str

class CalendarDayNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'CalendarDay'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str
    date: datetime.date
    day_of_week: str
    iso_day: str  # ISO 8601 day
    localised_day_name: str
    is_weekend: bool
