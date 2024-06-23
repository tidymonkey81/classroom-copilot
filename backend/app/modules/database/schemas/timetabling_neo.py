import datetime
from typing import ClassVar
from neontology import BaseNode

# Neo4j Nodes and relationships using Neontology
# Timetable layer

class AcademicYearNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicYear'
    __primaryproperty__: ClassVar[str] = 'academic_year_id'
    academic_year_id: str
    academic_year_start_date: datetime.date
    academic_year_end_date: datetime.date
    academic_year_notes: str
    
class AcademicWeekNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicWeek'
    __primaryproperty__: ClassVar[str] = 'academic_week_id'
    week_id: str
    week_start_date: datetime.date
    week_end_date: datetime.date
    week_type: str
    week_notes: str
    
class AcademicDayNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicDay'
    __primaryproperty__: ClassVar[str] = 'academic_day_id'
    day_id: str
    date: datetime.date
    day: str
    day_modifier: str
    auto_agenda: str
    agenda_heading: str
    agenda_notes: str

class AcademicSessionNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicSession'
    __primaryproperty__: ClassVar[str] = 'academic_session_id'
    session_id: str
    session_name: str
    session_start_time: datetime.datetime
    session_end_time: datetime.datetime
    session_type: str
    session_mod: str
    session_notes: str

class AcademicTermNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicTerm'
    __primaryproperty__: ClassVar[str] = 'academic_term_id'
    term_id: str
    term_start_date: datetime.date
    term_end_date: datetime.date
    term_notes: str

class AcademicTermBreakNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicTermBreak'
    __primaryproperty__: ClassVar[str] = 'academic_term_break_id'
    term_break_id: str
    term_break_start_date: datetime.date
    term_break_end_date: datetime.date
    term_break_notes: str
    