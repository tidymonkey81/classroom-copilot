print("PRINT STATEMENT: Loading schemas.py...")
import sys
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
sys.path.append(os.getenv("PY_MODULES_PATH"))
import logger_tool as logger
logging = logger.get_logger(name='logger_tool')

import datetime
from typing import ClassVar
from neontology import BaseNode, BaseRelationship, init_neontology

# Neo4j Nodes and relatiosnhips using Neontology
## Entity layer
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
    class_id: str
    class_name: str
    class_type: str
    class_year: str
    class_subject: str
    class_teacher: str

class RoomNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Room'
    __primaryproperty__: ClassVar[str] = 'room_id'
    room_id: str
    room_name: str
    room_notes: str

## Calendar layer
class CalendarYearNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'CalendarYear'
    __primaryproperty__: ClassVar[str] = 'calendar_year_id'
    calendar_year_id: str
    calendar_year_start_date: datetime.date
    calendar_year_end_date: datetime.date
    calendar_year_notes: str

class TermNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Term'
    __primaryproperty__: ClassVar[str] = 'term_id'
    term_id: str
    term_start_date: datetime.date
    term_end_date: datetime.date
    term_notes: str

class TermBreakNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'TermBreak'
    __primaryproperty__: ClassVar[str] = 'term_break_id'
    term_break_id: str
    term_break_start_date: datetime.date
    term_break_end_date: datetime.date
    term_break_notes: str

class WeekNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Week'
    __primaryproperty__: ClassVar[str] = 'week_id'
    week_id: str
    week_start_date: datetime.date
    week_end_date: datetime.date
    week_type: str
    week_notes: str

class DateNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Date'
    __primaryproperty__: ClassVar[str] = 'date'
    date: datetime.date
    day: str
    day_type: str
    day_modifier: str
    auto_agenda: str
    agenda_heading: str
    agenda_notes: str

class PeriodNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Period'
    __primaryproperty__: ClassVar[str] = 'period_id'
    period_id: str
    period_number: str
    period_name: str
    period_start_datetime: datetime.datetime
    period_end_datetime: datetime.datetime
    period_type: str
    period_notes: str

## Curricular layer
class SubjectNode(BaseNode): # TODO: This is an example, replace with actual schema
    __primarylabel__: ClassVar[str] = 'Subject'
    __primaryproperty__: ClassVar[str] = 'subject'
    subject: str
    subject_code: str

class KeyStageNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'KeyStage'
    __primaryproperty__: ClassVar[str] = 'key_stage'
    key_stage_level: int
    key_stage: str

class TopicNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Topic'
    __primaryproperty__: ClassVar[str] = 'topic_id'
    topic_id: str
    topic_title: str
    total_number_of_lessons_for_topic: int
    topic_type: str
    topic_assessment_type: str

class TopicLessonNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'TopicLesson'
    __primaryproperty__: ClassVar[str] = 'topic_lesson_id'
    topic_lesson_id: str
    topic_lesson_title: str
    topic_lesson_type: str
    topic_lesson_length: int
    topic_lesson_suggested_activities: str
    topic_lesson_skills_learned: str
    topic_lesson_weblinks: str

class LearningStatementNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'LearningStatement'
    __primaryproperty__: ClassVar[str] = 'lesson_learning_statement_id'
    lesson_learning_statement_id: str
    lesson_learning_statement: str
    lesson_learning_statement_type: str

class ScienceLabNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'ScienceLab'
    __primaryproperty__: ClassVar[str] = 'science_lab_id'
    science_lab_id: str
    science_lab_title: str
    science_lab_summary: str
    science_lab_requirements: str
    science_lab_procedure: str
    science_lab_safety: str
    science_lab_weblinks: str

## Timetabling layer
class PlannedLessonNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Lesson'
    __primaryproperty__: ClassVar[str] = 'id'
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
    id: str
    date: datetime.date
    period_name: str
    teacher: str
    teacher_id: str
    class_name: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    notes: str

## Neonology Relationships for Neo4j Database
## Entity layer relationships
class SchoolHasDepartment(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_DEPARTMENT'
    source: SchoolNode
    target: DepartmentNode

class DepartmentProvidesSubject(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'PROVIDES_SUBJECT'
    source: DepartmentNode
    target: SubjectNode
    
class StaffTeachesSubject(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'TEACHES_SUBJECT'
    source: StaffNode
    target: SubjectNode

class StaffTeachesClass(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'TEACHES_CLASS'
    source: StaffNode
    target: ClassNode

class ClassHasStudent(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_STUDENT'
    source: ClassNode
    target: StudentNode

## Calendar layer relationships
class SchoolHasCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_ACADEMIC_YEAR'
    source: SchoolNode
    target: CalendarYearNode

class CalendarYearBelongsToSchool(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_SCHOOL'
    source: CalendarYearNode
    target: SchoolNode

class SchoolHasTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_TERM'
    source: SchoolNode
    target: TermNode

class TermBelongsToSchool(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_SCHOOL'
    source: TermNode
    target: SchoolNode

class SchoolHasTermBreak(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_TERM_BREAK'
    source: SchoolNode
    target: TermBreakNode

class TermBreakBelongsToSchool(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_SCHOOL'
    source: TermBreakNode
    target: SchoolNode

class SchoolHasWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_WEEK'
    source: SchoolNode
    target: WeekNode

class WeekBelongsToSchool(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_SCHOOL'
    source: WeekNode
    target: SchoolNode

class SchoolHasDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_DAY'
    source: SchoolNode
    target: DateNode

class DayBelongsToSchool(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_SCHOOL'
    source: DateNode
    target: SchoolNode

class SchoolHasPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PERIOD'
    source: SchoolNode
    target: PeriodNode

class PeriodBelongsToSchool(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_SCHOOL'
    source: PeriodNode
    target: SchoolNode

class CalendarYearHasTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_TERM'
    source: CalendarYearNode
    target: TermNode

class TermBelongsToCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_CALENDAR_YEAR'
    source: TermNode
    target: CalendarYearNode

class CalendarYearHasTermBreak(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_TERM_BREAK'
    source: CalendarYearNode
    target: TermBreakNode

class TermBreakBelongsToCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_CALENDAR_YEAR'
    source: TermBreakNode
    target: CalendarYearNode

class CalendarYearHasWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_WEEK'
    source: CalendarYearNode
    target: WeekNode

class WeekBelongsToCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_CALENDAR_YEAR'
    source: WeekNode
    target: CalendarYearNode

class CalendarYearHasDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_DAY'
    source: CalendarYearNode
    target: DateNode

class DayBelongsToCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_CALENDAR_YEAR'
    source: DateNode
    target: CalendarYearNode

class CalendarYearHasPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PERIOD'
    source: CalendarYearNode
    target: PeriodNode

class PeriodBelongsToCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_CALENDAR_YEAR'
    source: PeriodNode
    target: CalendarYearNode

class TermHasWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_WEEK'
    source: TermNode
    target: WeekNode

class WeekBelongsToTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_TERM'
    source: WeekNode
    target: TermNode

class TermHasDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_DAY'
    source: TermNode
    target: DateNode

class DayBelongsToTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_TERM'
    source: DateNode
    target: TermNode

class TermHasPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PERIOD'
    source: TermNode
    target: PeriodNode

class PeriodBelongsToTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_TERM'
    source: PeriodNode
    target: TermNode

class TermBreakHasWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_WEEK'
    source: TermBreakNode
    target: WeekNode

class WeekBelongsToTermBreak(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_TERM_BREAK'
    source: WeekNode
    target: TermBreakNode

class TermBreakHasDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_DAY'
    source: TermBreakNode
    target: DateNode

class DayBelongsToTermBreak(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_TERM_BREAK'
    source: DateNode
    target: TermBreakNode

class WeekHasDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_DAY'
    source: WeekNode
    target: DateNode

class DayBelongsToWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_WEEK'
    source: DateNode
    target: WeekNode

class WeekHasPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PERIOD'
    source: WeekNode
    target: PeriodNode

class PeriodBelongsToWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_WEEK'
    source: PeriodNode
    target: WeekNode

class DayHasPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PERIOD'
    source: DateNode
    target: PeriodNode

class PeriodBelongsToDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_DAY'
    source: PeriodNode
    target: DateNode

## Curriculum layer relationships
class SubjectForKeyStage(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOR_KEY_STAGE'
    source: SubjectNode
    target: KeyStageNode

class KeyStageIncludesTopic(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES_TOPIC'
    source: KeyStageNode
    target: TopicNode

class SubjectIncludesTopic(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES_TOPIC'
    source: SubjectNode
    target: TopicNode

class TopicIncludesTopicLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES_LESSON'
    source: TopicNode
    target: TopicLessonNode

class TopicIncludesLearningStatement(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES_LEARNING_STATEMENT'
    source: TopicNode
    target: LearningStatementNode

class LearningStatementPartOfTopic(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'PART_OF_TOPIC'
    source: LearningStatementNode
    target: TopicNode

class TopicLessonIncludesLearningStatement(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES_LEARNING_STATEMENT'
    source: TopicLessonNode
    target: LearningStatementNode

class LearningStatementPartOfTopicLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'PART_OF_LESSON'
    source: LearningStatementNode
    target: TopicLessonNode

# Science-specific curriculum layer relationships
class TopicLessonIncludesScienceLab(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES_SCIENCE_LAB'
    source: TopicLessonNode
    target: ScienceLabNode

## Timetabling layer relationships
    # Entity layer relationships
class StaffTeachesPlannedLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'TEACHES_LESSON'
    source: StaffNode
    target: PlannedLessonNode

class PlannedLessonHasRoom(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_ROOM'
    source: PlannedLessonNode
    target: RoomNode

class ClassHasPlannedLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_LESSON'
    source: ClassNode
    target: PlannedLessonNode

    # Calendar layer relationships
class CalendarYearHasPlannedLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_LESSON'
    source: CalendarYearNode
    target: PlannedLessonNode

class TermHasPlannedLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_LESSON'
    source: TermNode
    target: PlannedLessonNode

class WeekHasPlannedLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_LESSON'
    source: WeekNode
    target: PlannedLessonNode

class DayHasPlannedLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_LESSON'
    source: DateNode
    target: PlannedLessonNode

class PeriodHasPlannedLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_LESSON'
    source: PeriodNode
    target: PlannedLessonNode

    # Curriculum layer relationships
class TopicLessonIsForPlannedLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_FOR_LESSON'
    source: TopicLessonNode
    target: PlannedLessonNode

class PlannedLessonIsAboutTopicLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_ABOUT_LESSON'
    source: PlannedLessonNode
    target: TopicLessonNode

class PlannedLessonIsForSubject(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_FOR_SUBJECT'
    source: PlannedLessonNode
    target: SubjectNode

class PlannedLessonIsFPartOfTopic(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_PART_OF_TOPIC'
    source: PlannedLessonNode
    target: TopicNode

# Time layer relationships
class CalendarYearHasNextCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT_CALENDAR_YEAR'
    source: CalendarYearNode
    target: CalendarYearNode

class CalendarYearHasPreviousCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS_CALENDAR_YEAR'
    source: CalendarYearNode
    target: CalendarYearNode

class TermHasNextTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT_TERM'
    source: TermNode
    target: TermNode

class TermHasPreviousTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS_TERM'
    source: TermNode
    target: TermNode

class TermBreakHasNextTermBreak(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT_TERM_BREAK'
    source: TermBreakNode
    target: TermBreakNode

class TermBreakHasPreviousTermBreak(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS_TERM_BREAK'
    source: TermBreakNode
    target: TermBreakNode

class TermHasNextTermBreak(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT_TERM_BREAK'
    source: TermNode
    target: TermBreakNode

class TermHasPreviousTermBreak(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS_TERM_BREAK'
    source: TermNode
    target: TermBreakNode

class TermBreakHasNextTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT_TERM'
    source: TermBreakNode
    target: TermNode

class TermBreakHasPreviousTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS_TERM'
    source: TermBreakNode
    target: TermNode

class WeekHasNextWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT_WEEK'
    source: WeekNode
    target: WeekNode

class WeekHasPreviousWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS_WEEK'
    source: WeekNode
    target: WeekNode

class DateHasNextDate(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT_DAY'
    source: DateNode
    target: DateNode

class DateHasPreviousDate(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS_DAY'
    source: DateNode
    target: DateNode

class PeriodHasNextPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT_PERIOD'
    source: PeriodNode
    target: PeriodNode

class PeriodHasPreviousPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS_PERIOD'
    source: PeriodNode
    target: PeriodNode

class PlannedLessonHasNextPlannedLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT_LESSON'
    source: PlannedLessonNode
    target: PlannedLessonNode

class PlannedLessonHasPreviousPlannedLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS_LESSON'
    source: PlannedLessonNode
    target: PlannedLessonNode