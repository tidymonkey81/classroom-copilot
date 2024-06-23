import datetime
from typing import Optional
import pandas as pd
from pydantic import BaseModel, Field, validator, ValidationError

## Timetabling layer
# TODO: Verify and add schemas for timetabling entities
class PlannerSchema(BaseModel):
    planner_id: int = Field(alias='PlannerID')
    planner_id_excel: Optional[str] = Field(alias='PlannerIDExcel', default=None)
    ttver: int = Field(alias='TTVer')
    staff_code: str = Field(alias='StaffCode')
    period_date: datetime.date = Field(alias='PeriodDate')
    period_of_day: int = Field(alias='PeriodOfDay')
    period_code: str = Field(alias='PeriodCode')
    week_type: str = Field(alias='WeekType')
    period_is_lesson: Optional[int] = Field(alias='PeriodIsLesson', default=None)
    period_is_type: Optional[str] = Field(alias='PeriodIsType', default=None)
    period_mod: Optional[str] = Field(alias='PeriodMod', default=None)
    period_notes: Optional[str] = Field(alias='PeriodNotes', default=None)
    period_json: Optional[str] = Field(alias='PeriodJSON', default=None)
    period_start_time: datetime.time = Field(alias='PeriodStartTime')
    period_finish_time: datetime.time = Field(alias='PeriodFinishTime')
    room: Optional[str] = Field(alias='Room', defualt=None)
    class_key_stage: Optional[int] = Field(alias='ClassKeyStage', default=None)
    class_year: Optional[int] = Field(alias='ClassYear', default=None)
    class_code: Optional[str] = Field(alias='ClassCode', default=None)
    class_mod: Optional[str] = Field(alias='ClassMod', default=None)
    class_notes: Optional[str] = Field(alias='ClassNotes', default=None)
    class_json: Optional[str] = Field(alias='ClassJSON', default=None)
    lesson_sub_enter: Optional[str] = Field(alias='SubEnter', default=None)
    lesson_topic_enter: Optional[str] = Field(alias='TopicEnter', default=None)
    lesson_lesson_enter: Optional[str] = Field(alias='LessonEnter', default=None)
    lesson_topic_code: Optional[str] = Field(alias='TopicCode', default=None)
    lesson_code: Optional[str] = Field(alias='LessonCode', default=None)
    lesson_mod: Optional[str] = Field(alias='LessonMod', default=None)
    lesson_notes: Optional[str] = Field(alias='LessonNotes', default=None)
    lesson_json: Optional[str] = Field(alias='LessonJSON', default=None)

    class Config:
        orm_mode = True
        populate_by_name = True  # to allow field aliases
    
    # Define the validators using the new Pydantic syntax
    @validator('planner_id', 'ttver', 'period_of_day', 'class_key_stage', 'class_year', pre=True)
    def parse_int(cls, v):
        return int(v) if v is not None else None

    @validator('planner_id_excel', 'staff_code', 'period_code', 'week_type', 'period_is_type', 'period_mod', 'period_notes',
               'period_json', 'room', 'class_code', 'class_mod', 'class_notes', 'class_json',
               'lesson_sub_enter', 'lesson_topic_enter', 'lesson_lesson_enter', 'lesson_topic_code', 'lesson_code',
               'lesson_mod', 'lesson_notes', 'lesson_json', pre=True)
    def parse_str(cls, v):
        return str(v) if v is not None else None

    @validator('period_date', 'period_start_time', 'period_finish_time', pre=True)
    def parse_datetime(cls, v):
        if v is not None:
            if isinstance(v, datetime.date) or isinstance(v, datetime.time):
                return v
            elif isinstance(v, str):
                try:
                    return pd.to_datetime(v).date() if '-' in v else datetime.datetime.strptime(v, '%H:%M:%S').time()
                except ValueError:
                    return None
        return None

class ClassTimeTableModel(BaseModel):
    timetable_id: int = Field(alias='TimetableID')
    ttver: int = Field(alias='TTVer')
    class_code: str = Field(alias='ClassCode')
    week_type: str = Field(alias='WeekType')
    day_of_week: int = Field(alias='DayOfWeek')
    period_of_day: int = Field(alias='PeriodOfDay')
    room: str = Field(alias='Room')
    staff_code: str = Field(alias='StaffCode')
    period_code: str = Field(alias='PeriodCode')

    class Config:
        populate_by_name = True

    # Define the validators using the new Pydantic syntax

    @validator('timetable_id')
    def _parse_timetable_id(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('ttver')
    def _parse_ttver(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('class_code')
    def _parse_class_code(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('week_type')
    def _parse_week_type(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('day_of_week')
    def _parse_day_of_week(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('period_of_day')
    def _parse_period_of_day(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('room')
    def _parse_room(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('staff_code')
    def _parse_staff_code(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('period_code')
    def _parse_period_code(cls, v):
        return str(v) if pd.notnull(v) else None

class StaffTimetableModel(BaseModel):
    timetable_id: int = Field(alias='TimetableID')
    ttver: int = Field(alias='TTVer')
    staff_code: str = Field(alias='StaffCode')
    week_type: str = Field(alias='WeekType')
    day_of_week: int = Field(alias='DayOfWeek')
    period_of_day: int = Field(alias='PeriodOfDay')
    room: str = Field(alias='Room')
    class_code: str = Field(alias='ClassCode')
    period_code: str = Field(alias='PeriodCode')

    class Config:
        populate_by_name = True

    # Define the validators using the new Pydantic syntax

    @validator('timetable_id')
    def _parse_timetable_id(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('ttver')
    def _parse_ttver(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('staff_code')
    def _parse_staff_code(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('week_type')
    def _parse_week_type(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('day_of_week')
    def _parse_day_of_week(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('period_of_day')
    def _parse_period_of_day(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('room')
    def _parse_room(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('class_code')
    def _parse_class_code(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('period_code')
    def _parse_period_code(cls, v):
        return str(v) if pd.notnull(v) else None

class StudentTimetableModel(BaseModel):
    timetable_id: int = Field(alias='TimetableID')
    ttver: int = Field(alias='TTVer')
    student_code: str = Field(alias='StudentCode')
    week_type: str = Field(alias='WeekType')
    day_of_week: int = Field(alias='DayOfWeek')
    period_of_day: int = Field(alias='PeriodOfDay')
    room: str = Field(alias='Room')
    class_code: str = Field(alias='ClassCode')
    period_code: str = Field(alias='PeriodCode')

    class Config:
        populate_by_name = True

    # Define the validators using the new Pydantic syntax

    @validator('timetable_id')
    def _parse_timetable_id(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('ttver')
    def _parse_ttver(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('student_code')
    def _parse_student_code(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('week_type')
    def _parse_week_type(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('day_of_week')
    def _parse_day_of_week(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('period_of_day')
    def _parse_period_of_day(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('room')
    def _parse_room(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('class_code')
    def _parse_class_code(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('period_code')
    def _parse_period_code(cls, v):
        return str(v) if pd.notnull(v) else None
    
class PeriodModel(BaseModel):

    period_code: str = Field(alias='PeriodCode')
    period_name: str = Field(alias='PeriodName')
    period_week_type: str = Field(alias='PeriodWeekType')
    period_start_time: datetime.time = Field(alias='PeriodStartTime')
    period_finish_time: datetime.time = Field(alias='PeriodFinishTime')
    period_is_lesson: int = Field(alias='PeriodIsLesson')
    period_is_type: str = Field(alias='PeriodIsType')
    period_mod: str = Field(alias='PeriodMod')
    period_notes: str = Field(alias='PeriodNotes')
    period_json: str = Field(alias='PeriodJSON')

    class Config:
        populate_by_name = True

    # Define the validators using the new Pydantic syntax

    @validator('period_code')
    def _parse_period_code(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('period_name')
    def _parse_period_name(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('period_week_type')
    def _parse_period_week_type(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('period_start_time')
    def _parse_period_start_time(cls, v):
        return pd.to_datetime(v).time() if pd.notnull(v) else None
    
    @validator('period_finish_time')
    def _parse_period_finish_time(cls, v):
        return pd.to_datetime(v).time() if pd.notnull(v) else None
    
    @validator('period_is_lesson')
    def _parse_period_is_lesson(cls, v):
        return int(v) if pd.notnull(v) else None
    
    @validator('period_is_type')
    def _parse_period_is_type(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('period_mod')
    def _parse_period_mod(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('period_notes')
    def _parse_period_notes(cls, v):
        return str(v) if pd.notnull(v) else None
    
    @validator('period_json')
    def _parse_period_json(cls, v):
        return str(v) if pd.notnull(v) else None