from typing import ClassVar
from neontology import BaseRelationship

class AcademicCalendarHasYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_YEAR'
    source: AcademicCalendarNode
    target: AcademicYearNode

class AcademicYearHasTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_TERM'
    source: AcademicYearNode
    target: AcademicTermNode
    
class AcademicYearHasWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_WEEK'
    source: AcademicYearNode
    target: AcademicWeekNode
        
class AcademicYearHasDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_DAY'
    source: AcademicYearAcademicYearNode
    target: AcademicDayNode

class AcademicYearHasSession(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_SESSION'
    source: AcademicYearAcademicYearNode
    target: AcademicSessionNode

class AcademicTermHasWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_WEEK'
    source: AcademicTermNode
    target: AcademicWeekNode

class AcademicTermHasDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_DAY'
    source: AcademicTermNode
    target: AcademicDayNode

class AcademicTermHasSession(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_SESSION'
    source: AcademicTermNode
    target: AcademicSessionNode
    
class AcademicWeekHasDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_DAY'
    source: AcademicWeekNode
    target: AcademicDayNode

class AcademicWeekHasSession(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_SESSION'
    source: AcademicWeekNode
    target: AcademicSessionNode

class AcademicDayHasSession(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_SESSION'
    source: AcademicDayNode
    target: AcademicSessionNode
    