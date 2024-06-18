from pydantic import BaseModel, Field, validator, ValidationError

class SchoolSchema(BaseModel):
    school_id: str = Field(alias='SchoolID')
    school_name: str = Field(alias='SchoolName')
    school_short_name: str = Field(alias='SchoolShortName')
    school_abbreviation: str = Field(alias='SchoolAbbreviation')

    class Config:
        orm_mode = True
        populate_by_name = True

class StaffModel(BaseModel):
    staff_id: int = Field(alias='StaffID')
    staff_type: str = Field(alias='StaffType')
    staff_code: str = Field(alias='StaffCode')
    staff_name: str = Field(alias='StaffName')
    staff_nickname: str = Field(alias='StaffNickname')
    staff_email: str = Field(alias='StaffEmail')
    staff_onenote: str = Field(alias='StaffOneNote')
    staff_json: str = Field(alias='StaffJSON')

    class Config:
        populate_by_name = True

    # Define the validators using the new Pydantic syntax

    @validator('staff_id')
    def _parse_staff_id(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('staff_type')
    def _parse_staff_type(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('staff_code')
    def _parse_staff_code(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('staff_name')
    def _parse_staff_name(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('staff_nickname')
    def _parse_staff_nickname(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('staff_email')
    def _parse_staff_email(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('staff_onenote')
    def _parse_staff_onenote(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('staff_json')
    def _parse_staff_json(cls, v):
        return str(v) if pd.notnull(v) else None

class StudentModel(BaseModel):
    student_id: int = Field(alias='StudentID')
    student_code: str = Field(alias='StudentCode')
    student_year: str = Field(alias='StudentYear')
    student_name: str = Field(alias='StudentName')
    student_nickname: str = Field(alias='StudentNickname')
    student_email: str = Field(alias='StudentEmail')

    class Config:
        populate_by_name = True

    # Define the validators using the new Pydantic syntax

    @validator('student_id')
    def _parse_student_id(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('student_code')
    def _parse_student_code(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('student_year')
    def _parse_student_year(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('student_name')
    def _parse_student_name(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('student_nickname')
    def _parse_student_nickname(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('student_email')
    def _parse_student_email(cls, v):
        return str(v) if pd.notnull(v) else None
    
class ClassModel(BaseModel):
    class_id: int = Field(alias='ClassID')
    class_code: str = Field(alias='ClassCode')
    class_name: str = Field(alias='ClassName')
    class_type: str = Field(alias='ClassType')
    class_year: str = Field(alias='ClassYear')
    class_students: str = Field(alias='ClassStudents')
    class_json: str = Field(alias='ClassJSON')

    class Config:
        populate_by_name = True

    # Define the validators using the new Pydantic syntax

    @validator('class_id')
    def _parse_class_id(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('class_code')
    def _parse_class_code(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('class_name')
    def _parse_class_name(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('class_type')
    def _parse_class_type(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('class_year')
    def _parse_class_year(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('class_students')
    def _parse_class_students(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('class_json')
    def _parse_class_json(cls, v):
        return str(v) if pd.notnull(v) else None
            
class RoomModel(BaseModel):
            
    room_code: str = Field(alias='RoomCode')
    room_name: str = Field(alias='RoomName')
    room_notes: str = Field(alias='RoomNotes')
    room_json: str = Field(alias='RoomJSON')

    class Config:
        populate_by_name = True

    # Define the validators using the new Pydantic syntax

    @validator('room_code')
    def _parse_room_code(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('room_name')
    def _parse_room_name(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('room_notes')
    def _parse_room_notes(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('room_json')
    def _parse_room_json(cls, v):
        return str(v) if pd.notnull(v) else None