from typing import ClassVar
from neontology import BaseRelationship

class CalendarYearHasTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'CALENDAR_YEAR_HAS_TERM'
    source: CalendarYearNode
    target: TermNode

class CalendarYearHasTermBreak(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'CALENDAR_YEAR_HAS_TERM_BREAK'
    source: CalendarYearNode
    target: TermBreakNode

class CalendarYearHasWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'CALENDAR_YEAR_HAS_WEEK'
    source: CalendarYearNode
    target: WeekNode

class CalendarYearHasDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'CALENDAR_YEAR_HAS_DAY'
    source: CalendarYearNode
    target: DayNode

class CalendarYearHasPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'CALENDAR_YEAR_HAS_PERIOD'
    source: CalendarYearNode
    target: PeriodNode