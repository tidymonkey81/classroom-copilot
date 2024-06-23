from typing import ClassVar
from neontology import BaseRelationship

class SchoolHasAcademicCalendar(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_ACADEMIC_CALENDAR'
    source: SchoolNode
    target: AcademicCalendarNode
    
class SchoolHasDepartment(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_DEPARTMENT'
    source: SchoolNode
    target: DepartmentNode

class SchoolHasRoom(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 
    source: SchoolNode
    target: 
    
class DepartmentProvideSubjectLevel(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'PROVIDES_SUBJECT_LEVEL'
    source: DepartmentNode
    target: SubjectLevelNode

class StaffTeachesSubjectLevel(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'TEACHES_SUBJECT_LEVEL'
    source: StaffNode
    target: SubjectLevelNode

class StaffTeachesLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'TEACHES_LESSON'
    source: StaffNode
    target: LessonNode
    
class ClassTaughtByStaff(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'TAUGHT_BY_STAFF'
    source: ClassNode
    target: StaffNode

class ClassHasStudent(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_STUDENT'
    source: ClassNode
    target: StudentNode