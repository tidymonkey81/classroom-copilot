from typing import ClassVar
from neontology import BaseRelationship
    
class PlannedLessonHasRoom(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_ROOM'
    source: PlannedLessonNode
    target: RoomNode
    
class PlannedLessonIsForSession(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'PLANNED_FOR'
    source: PlannedLessonNode
    target: AcademicSessionNode

class PlannedLessonIsForDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'PLANNED_FOR'
    source: AcademicDayNode
    target: PlannedLessonNode


# OLD CALENDAR RELATIONSHIPS COPIED HERE FROM CALENDAR r'^(?P<import modules.database.schemas.curriculum_neo as neo_curriculum
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