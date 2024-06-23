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