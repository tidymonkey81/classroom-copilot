import modules.database.schemas.timetable_neo as neo_timetable
from modules.database.tools.neontology.baserelationship import BaseRelationship
from typing import ClassVar

# Timetable hierarchy structure relationships
class AcademicTimetableHasAcademicYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_ACADEMIC_YEAR'
    source: neo_timetable.AcademicTimetableNode
    target: neo_timetable.AcademicYearNode

class AcademicYearHasAcademicTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_ACADEMIC_TERM'
    source: neo_timetable.AcademicYearNode
    target: neo_timetable.AcademicTermNode

class AcademicYearHasAcademicTermBreak(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_ACADEMIC_TERM_BREAK'
    source: neo_timetable.AcademicYearNode
    target: neo_timetable.AcademicTermBreakNode
    
class AcademicYearHasAcademicWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_ACADEMIC_WEEK'
    source: neo_timetable.AcademicYearNode
    target: neo_timetable.AcademicWeekNode
    
class AcademicYearHasHolidayWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_HOLIDAY_WEEK'
    source: neo_timetable.AcademicYearNode
    target: neo_timetable.HolidayWeekNode

class AcademicTermHasAcademicWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_ACADEMIC_WEEK'
    source: neo_timetable.AcademicTermNode
    target: neo_timetable.AcademicWeekNode

class AcademicTermBreakHasHolidayWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_HOLIDAY_WEEK'
    source: neo_timetable.AcademicTermBreakNode
    target: neo_timetable.HolidayWeekNode

class AcademicTermBreakHasHolidayDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_HOLIDAY_DAY'
    source: neo_timetable.AcademicTermBreakNode
    target: neo_timetable.HolidayDayNode

class AcademicTermHasAcademicDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_ACADEMIC_DAY'
    source: neo_timetable.AcademicTermNode
    target: neo_timetable.AcademicDayNode

class AcademicTermHasHolidayDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_HOLIDAY_DAY'
    source: neo_timetable.AcademicTermNode
    target: neo_timetable.HolidayDayNode
    
class AcademicTermHasOffTimetableDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_OFF_TIMETABLE_DAY'
    source: neo_timetable.AcademicTermNode
    target: neo_timetable.OffTimetableDayNode
    
class AcademicTermHasStaffDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_STAFF_DAY'
    source: neo_timetable.AcademicTermNode
    target: neo_timetable.StaffDayNode
    
class AcademicWeekHasAcademicDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_ACADEMIC_DAY'
    source: neo_timetable.AcademicWeekNode
    target: neo_timetable.AcademicDayNode

class AcademicWeekHasHolidayDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_HOLIDAY_DAY'
    source: neo_timetable.AcademicWeekNode
    target: neo_timetable.HolidayDayNode
    
class AcademicWeekHasOffTimetableDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_OFF_TIMETABLE_DAY'
    source: neo_timetable.AcademicWeekNode
    target: neo_timetable.OffTimetableDayNode
    
class AcademicWeekHasStaffDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_STAFF_DAY'
    source: neo_timetable.AcademicWeekNode
    target: neo_timetable.StaffDayNode

class HolidayWeekHasHolidayDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_HOLIDAY_DAY'
    source: neo_timetable.HolidayWeekNode
    target: neo_timetable.HolidayDayNode

class AcademicDayHasAcademicPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_ACADEMIC_PERIOD'
    source: neo_timetable.AcademicDayNode
    target: neo_timetable.AcademicPeriodNode

class AcademicDayHasRegistrationPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_REGISTRATION_PERIOD'
    source: neo_timetable.AcademicDayNode
    target: neo_timetable.RegistrationPeriodNode
    
class AcademicDayHasBreakPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_BREAK_PERIOD'
    source: neo_timetable.AcademicDayNode
    target: neo_timetable.BreakPeriodNode

class AcademicDayHasOffTimetablePeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_OFF_TIMETABLE_PERIOD'
    source: neo_timetable.AcademicDayNode
    target: neo_timetable.OffTimetablePeriodNode
    
# Timetable sequence relationships
class AcademicYearFollowsAcademicYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_ACADEMIC_YEAR'
    source: neo_timetable.AcademicYearNode
    target: neo_timetable.AcademicYearNode
    
class AcademicTermFollowsAcademicTermBreak(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_ACADEMIC_TERM_BREAK'
    source: neo_timetable.AcademicTermNode
    target: neo_timetable.AcademicTermBreakNode
    
class AcademicTermBreakFollowsAcademicTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_ACADEMIC_TERM'
    source: neo_timetable.AcademicTermBreakNode
    target: neo_timetable.AcademicTermNode
    
class AcademicWeekFollowsAcademicWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_ACADEMIC_WEEK'
    source: neo_timetable.AcademicWeekNode
    target: neo_timetable.AcademicWeekNode

class HolidayWeekFollowsHolidayWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_HOLIDAY_WEEK'
    source: neo_timetable.HolidayWeekNode
    target: neo_timetable.HolidayWeekNode
    
class AcademicWeekFollowsHolidayWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_HOLIDAY_WEEK'
    source: neo_timetable.AcademicWeekNode
    target: neo_timetable.HolidayWeekNode
    
class HolidayWeekFollowsAcademicWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_ACADEMIC_WEEK'
    source: neo_timetable.HolidayWeekNode
    target: neo_timetable.AcademicWeekNode
    
class AcademicDayFollowsAcademicDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_ACADEMIC_DAY'
    source: neo_timetable.AcademicDayNode
    target: neo_timetable.AcademicDayNode
    
class AcademicDayFollowsHolidayDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_HOLIDAY_DAY'
    source: neo_timetable.AcademicDayNode
    target: neo_timetable.HolidayDayNode
    
class AcademicDayFollowsOffTimetableDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_OFF_TIMETABLE_DAY'
    source: neo_timetable.AcademicDayNode
    target: neo_timetable.OffTimetableDayNode
    
class AcademicDayFollowsStaffDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_STAFF_DAY'
    source: neo_timetable.AcademicDayNode
    target: neo_timetable.StaffDayNode
    
class HolidayDayFollowsHolidayDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_HOLIDAY_DAY'
    source: neo_timetable.HolidayDayNode
    target: neo_timetable.HolidayDayNode

class HolidayDayFollowsAcademicDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_ACADEMIC_DAY'
    source: neo_timetable.HolidayDayNode
    target: neo_timetable.AcademicDayNode
    
class HolidayDayFollowsOffTimetableDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_OFF_TIMETABLE_DAY'
    source: neo_timetable.HolidayDayNode
    target: neo_timetable.OffTimetableDayNode
    
class HolidayDayFollowsStaffDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_STAFF_DAY'
    source: neo_timetable.HolidayDayNode
    target: neo_timetable.StaffDayNode
    
class OffTimetableDayFollowsOffTimetableDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_OFF_TIMETABLE_DAY'
    source: neo_timetable.OffTimetableDayNode
    target: neo_timetable.OffTimetableDayNode
    
class OffTimetableDayFollowsAcademicDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_ACADEMIC_DAY'
    source: neo_timetable.OffTimetableDayNode
    target: neo_timetable.AcademicDayNode
    
class OffTimetableDayFollowsHolidayDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_HOLIDAY_DAY'
    source: neo_timetable.OffTimetableDayNode
    target: neo_timetable.HolidayDayNode
    
class OffTimetableDayFollowsStaffDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_STAFF_DAY'
    source: neo_timetable.OffTimetableDayNode
    target: neo_timetable.StaffDayNode
    
class StaffDayFollowsStaffDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_STAFF_DAY'
    source: neo_timetable.StaffDayNode
    target: neo_timetable.StaffDayNode
    
class StaffDayFollowsAcademicDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_ACADEMIC_DAY'
    source: neo_timetable.StaffDayNode
    target: neo_timetable.AcademicDayNode
    
class StaffDayFollowsHolidayDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_HOLIDAY_DAY'
    source: neo_timetable.StaffDayNode
    target: neo_timetable.HolidayDayNode
    
class StaffDayFollowsOffTimetableDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_OFF_TIMETABLE_DAY'
    source: neo_timetable.StaffDayNode
    target: neo_timetable.OffTimetableDayNode
    
class AcademicPeriodFollowsAcademicPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_ACADEMIC_PERIOD'
    source: neo_timetable.AcademicPeriodNode
    target: neo_timetable.AcademicPeriodNode

class AcademicPeriodFollowsBreakPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_BREAK_PERIOD'
    source: neo_timetable.AcademicPeriodNode
    target: neo_timetable.BreakPeriodNode
    
class AcademicPeriodFollowsRegistrationPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_REGISTRATION_PERIOD'
    source: neo_timetable.AcademicPeriodNode
    target: neo_timetable.RegistrationPeriodNode
    
class BreakPeriodFollowsAcademicPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_ACADEMIC_PERIOD'
    source: neo_timetable.BreakPeriodNode
    target: neo_timetable.AcademicPeriodNode

class RegistrationPeriodFollowsAcademicPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_ACADEMIC_PERIOD'
    source: neo_timetable.RegistrationPeriodNode
    target: neo_timetable.AcademicPeriodNode
    
class RegistrationPeriodFollowsOffTimetablePeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_OFF_TIMETABLE_PERIOD'
    source: neo_timetable.RegistrationPeriodNode
    target: neo_timetable.OffTimetablePeriodNode

class OffTimetablePeriodFollowsAcademicPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_ACADEMIC_PERIOD'
    source: neo_timetable.OffTimetablePeriodNode
    target: neo_timetable.AcademicPeriodNode

class OffTimetablePeriodFollowsOffTimetablePeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOLLOWS_OFF_TIMETABLE_PERIOD'
    source: neo_timetable.OffTimetablePeriodNode
    target: neo_timetable.OffTimetablePeriodNode