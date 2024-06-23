from typing import ClassVar
from neontology import BaseNode

# Neo4j Nodes and relationships using Neontology
# Entity layer

class SchoolNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'School'
    __primaryproperty__: ClassVar[str] = 'school_id'
    school_id: str
    school_name: str
    school_org_type: str
    school_address: str
    school_website: str

class DepartmentNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Department'
    __primaryproperty__: ClassVar[str] = 'department_id'
    department_id: str
    department_name: str
    
class StaffNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Staff'
    __primaryproperty__: ClassVar[str] = 'staff_id'
    staff_id: str
    staff_name: str
    staff_type: str
    staff_nickname: str
    staff_email: str

class StudentNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Student'
    __primaryproperty__: ClassVar[str] = 'student_id'
    student_id: str
    student_name: str
    student_year: str
    student_nickname: str
    student_email: str

class ClassNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Class'
    __primaryproperty__: ClassVar[str] = 'class_id'
    class_id: int
    class_code: str
    class_name: str
    class_type: str
    class_year: str
    class_students: str
    class_json: str

class RoomNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Room'
    __primaryproperty__: ClassVar[str] = 'room_id'
    room_id: str
    room_name: str
    room_notes: str