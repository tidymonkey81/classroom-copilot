from typing import ClassVar
from neontology import BaseNode

# Neo4j Nodes and relationships using Neontology
# Planning layer
class PlannedLessonNode(BaseNode):
    '''
    This timetable node connects to:
    Curriculum:
    - SubjectNode
    - KeyStageNode
    - TopicNode
    - TopicLessonNode
    - LearningStatementNode
    Calendar:
    - PeriodNode
    Entities:
    - StaffNode
    - ClassNode
    - RoomNode
    TODO: other directly required nodes
    '''
    planned_lesson_id: int
    timetable_version: int
    notes: str