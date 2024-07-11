from modules.database.tools.neontology.basenode import BaseNode
import datetime
from typing import ClassVar

# Neo4j Nodes and relationships using Neontology
# Timetable layer
class AcademicTimetableNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicTimetable'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # {school_id}_{academic_timetable_start_date.year}_{academic_timetable_end_date.year}
    name: str # {academic_timetable_start_date.year} to {academic_timetable_end_date.year} (e.g. 2023 to 2024)
    start_date: datetime.date
    end_date: datetime.date

class AcademicYearNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicYear'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # AcademicYear_{school_id}_{academic_year}
    year: str # (e.g. 2023)

class AcademicTermNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicTerm'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # AcademicTerm_{academic_timetable_id}_{term_name}
    name: str
    number: str
    start_date: datetime.date # From Excel sheet 'TermsLookup' column 'Date' and 'DateType'
    end_date: datetime.date # From Excel sheet 'TermsLookup' column 'Date' and 'DateType'

class AcademicTermBreakNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicTermBreak'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # AcademicTermBreak_{academic_timetable_id}_{term_break_name}
    name: str # From Excel sheet 'TermsLookup' column 'TermName'
    start_date: datetime.date # From Excel sheet 'TermsLookup' column 'Date' and 'DateType'
    end_date: datetime.date # From Excel sheet 'TermsLookup' column 'Date' and 'DateType'
    
class AcademicWeekNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicWeek'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # AcademicWeek_{academic_timetable_id}_{week_number}
    number: str # Iterate during timetable creation
    start_date: datetime.date # From Excel sheet 'WeeksLookup' column 'WeekStart'
    week_type: str # From Excel sheet 'WeeksLookup' column 'WeekType' (A or B, if Holiday create HolidayWeekNode)

class HolidayWeekNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'HolidayWeek'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # HolidayWeek_{academic_timetable_id}_{week_number}
    start_date: datetime.date # From Excel sheet 'WeeksLookup' column 'WeekStart'
    
class AcademicDayNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicDay'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # AcademicDay_{academic_timetable_id}_{date}
    number: str # Iterate during timetable creation
    date: datetime.date # From Excel sheet 'DaysLookup' column 'Date'
    day_of_week: str # From Excel sheet 'DaysLookup' column 'DayOfWeek'
    day_type: str  # Week type from the associated AcademicWeekNode (e.g. 'A' or 'B')

class OffTimetableDayNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'OffTimetableDay'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # OffTimetableDay_{academic_timetable_id}_{date}
    date: datetime.date # From Excel sheet 'DaysLookup' column 'Date'
    day_of_week: str # From Excel sheet 'DaysLookup' column 'DayOfWeek'

class StaffDayNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'StaffDay'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # StaffDay_{academic_timetable_id}_{date}
    date: datetime.date # From Excel sheet 'DaysLookup' column 'Date'
    day_of_week: str # From Excel sheet 'DaysLookup' column 'DayOfWeek'
    
class HolidayDayNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'HolidayDay'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # HolidayDay_{academic_timetable_id}_{date}
    date: datetime.date # From Excel sheet 'DaysLookup' column 'Date'
    day_of_week: str # From Excel sheet 'DaysLookup' column 'DayOfWeek'

class AcademicPeriodNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicPeriod'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # AcademicPeriod_{academic_timetable_id}_{period_start_time}_{period_end_time}
    name: str # From Excel sheet 'TimetableLookup' column 'PeriodName'
    day_of_week: str # The day of the wek the period falls on
    start_time: datetime.datetime # From Excel sheet 'TimetableLookup' column 'Time' and 'TimeType'
    end_time: datetime.datetime # From Excel sheet 'TimetableLookup' column 'Time' and 'TimeType'
    day_type: str # The week type the period falls on (e.g. A or B)
    
class RegistrationPeriodNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'RegistrationPeriod'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # RegistrationPeriod_{academic_timetable_id}_{registration_period_start_time}_{registration_period_end_time}
    name: str # From Excel sheet 'TimetableLookup' column 'PeriodName'
    day_of_week: str # The day of the wek the period falls on
    start_time: datetime.datetime # From Excel sheet 'TimetableLookup' column 'Time' and 'TimeType'
    end_time: datetime.datetime # From Excel sheet 'TimetableLookup' column 'Time' and 'TimeType'
    
class BreakPeriodNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'BreakPeriod'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # BreakPeriod_{academic_timetable_id}_{break_period_start_time}_{break_period_end_time}
    name: str # From Excel sheet 'TimetableLookup' column 'PeriodName'
    day_of_week: str # The day of the wek the period falls on
    start_time: datetime.datetime # From Excel sheet 'TimetableLookup' column 'Time' and 'TimeType'
    end_time: datetime.datetime # From Excel sheet 'TimetableLookup' column 'Time' and 'TimeType'
    
class OffTimetablePeriodNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'OffTimetablePeriod'
    __primaryproperty__: ClassVar[str] = 'unique_id'
    unique_id: str # OffTimetablePeriod_{academic_timetable_id}_{period_start_time}_{period_end_time}
    name: str # From Excel sheet 'TimetableLookup' column 'PeriodName'
    day_of_week: str # The day of the wek the period falls on
    start_time: datetime.datetime # From Excel sheet 'TimetableLookup' column 'Time' and 'TimeType'
    end_time: datetime.datetime # From Excel sheet 'TimetableLookup' column 'Time' and 'TimeType'