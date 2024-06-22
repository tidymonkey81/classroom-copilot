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
## Assets
class SchoolNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'School'
    __primaryproperty__: ClassVar[str] = 'name'
    name: str
    org_type: str
    address: str
    website: str

class RoomNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Room'
    __primaryproperty__: ClassVar[str] = 'name'
    name: str
    type: str
    notes: str

class DepartmentNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Department'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    name: str

class ClassNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Class'
    __primaryproperty__: ClassVar[str] = 'name'
    name: str
    notes: str

class YearGroupNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'YearGroup'
    __primaryproperty__: ClassVar[str] = 'year_group'
    year_group: str

class FormGroupNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'FormGroup'
    __primaryproperty__: ClassVar[str] = 'form_group'
    form_group: str

class TutorGroupNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'TutorGroup'
    __primaryproperty__: ClassVar[str] = 'tutor_group'
    tutor_group: str

class PersonNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Person'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    full_name: str
    email: str
    
class TeacherNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Teacher'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    full_name: str
    email: str

class StudentNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Student'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    full_name: str
    email: str

class DepartmentHeadNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'DepartmentHead'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    full_name: str
    email: str

class SubjectLeadNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'SubjectLead'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    full_name: str
    email: str

## Calendar layer
class CalendarNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Calendar'
    __primaryproperty__: ClassVar[str] = 'version'
    version: int
    notes: str

class YearNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'CalendarYear'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    start_date: datetime.date
    end_date: datetime.date
    notes: str

class MonthNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Month'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    start_date: datetime.date
    end_date: datetime.date
    notes: str

class WeekNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Week'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    start_date: datetime.date
    end_date: datetime.date
    type: str
    notes: str

class DayNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Day'
    __primaryproperty__: ClassVar[str] = 'date'
    date: datetime.date
    day: str
    type: str
    modifier: str
    notes: str

## Timetable layer
class TimetableNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Timetable'
    __primaryproperty__: ClassVar[str] = 'version'
    version: int
    notes: str
    
class AcademicYearNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicYear'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    start_date: datetime.date
    end_date: datetime.date
    notes: str

class TermNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Term'
    __primaryproperty__: ClassVar[str] = 'number'
    number: str
    start_date: datetime.date
    end_date: datetime.date
    notes: str

class AcademicWeekNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicWeek'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    start_date: datetime.date
    end_date: datetime.date
    notes: str

class AcademicDayNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AcademicDay'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    date: datetime.date
    type: str
    notes: str

class PeriodNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Period'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    number: str
    name: str
    date: datetime.date
    start_time: datetime.datetime
    end_time: datetime.datetime
    type: str
    name: str
    notes: str

## Curricular layer
class SubjectNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Subject'
    __primaryproperty__: ClassVar[str] = 'subject'
    subject: str
    subject_code: str

class KeyStageNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'KeyStage'
    __primaryproperty__: ClassVar[str] = 'level'
    level: int

class TopicNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Topic'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    title: str
    type: str
    assessment_type: str

class TopicLessonNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'TopicLesson'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    title: str
    type: str
    length: str

class LearningStatementNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'LearningStatement'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    statement: str
    type: str

class LearningResourceNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'LearningResource'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    title: str
    type: str
    summary: str

class LearningResourceFileNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'LearningResourceFile'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    directory: str
    filename: str

class ScienceLabNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'ScienceLab'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    title: str
    type: str
    summary: str

## Timetabling layer
class TimetableNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Timetable'
    __primaryproperty__: ClassVar[str] = 'version'
    version: int
    notes: str

class LessonNode(BaseNode):
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
    - TeacherNode
    - ClassNode
    - RoomNode
    TODO: other directly required nodes
    '''
    id: str
    date: datetime.date
    start_time: datetime.datetime
    end_time: datetime.datetime
    timetable_period_name: str
    period_number: str
    subject: str
    teacher_name: str
    teacher_id: str
    class_name: str
    location: str
    notes: str

# Planner layer
class PlannerNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Planner'
    __primaryproperty__: ClassVar[str] = 'version'
    version: int
    notes: str

class PlannedLessonNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'PlannedLesson'
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
    - TeacherNode
    - ClassNode
    - RoomNode
    '''
    id: str
    date: datetime.date
    start_time: datetime.datetime
    end_time: datetime.datetime
    timetable_period_name: str
    period_number: str
    subject: str
    teacher_name: str
    teacher_id: str
    class_name: str
    location: str
    notes: str

class PlannedLessonSequenceNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'PlannedLessonSequence'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    title: str
    type: str
    summary: str

class PlannedActivityNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'PlannedActivity'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    title: str
    length: str
    type: str
    summary: str

class AssignmentNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Assignment'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    title: str
    due_date: datetime.date
    type: str
    summary: str

class AssignmentSubmissionNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AssignmentSubmission'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    title: str
    due_date: datetime.date
    type: str
    summary: str

class AssignmentSubmissionFileNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'AssignmentSubmissionFile'
    __primaryproperty__: ClassVar[str] = 'id'
    id: str
    directory: str
    filename: str

## Neonology Relationships for Neo4j Database
## Entity layer relationships
class SchoolHasDepartment(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_DEPARTMENT'
    source: SchoolNode
    target: DepartmentNode

class DepartmentManagedByHeadOfDepartment(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'MANAGED_BY'
    source: DepartmentNode
    target: DepartmentHeadNode

class DepartmentProvidesSubject(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'PROVIDES_SUBJECT'
    source: DepartmentNode
    target: SubjectNode

class SubjectHasSubjectLead(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_SUBJECT_LEAD'
    source: SubjectNode
    target: SubjectLeadNode

class DepartmentHasTeacher(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_TEACHER'
    source: DepartmentNode
    target: TeacherNode

class TeacherBelongsToDepartment(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_IN'
    source: TeacherNode
    target: DepartmentNode
    
class TeacherTeachesSubject(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'TEACHES'
    source: TeacherNode
    target: SubjectNode

class TeacherToClass(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'RESPONSIBLE_FOR'
    source: TeacherNode
    target: ClassNode

class ClassHasTeacher(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_TEACHER'
    source: ClassNode
    target: TeacherNode

class ClassHasStudent(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_STUDENT'
    source: ClassNode
    target: StudentNode

class StudentBelongsToClass(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_IN'
    source: StudentNode
    target: ClassNode

class StudentBelongsToYearGroup(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_IN'
    source: StudentNode
    target: YearGroupNode

class StudentBelongsToFormGroup(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_IN'
    source: StudentNode
    target: FormGroupNode

class StudentBelongsToTutorGroup(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_IN'
    source: StudentNode
    target: TutorGroupNode

class YearGroupHasClass(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS'
    source: YearGroupNode
    target: ClassNode

class ClassBelongsToYearGroup(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_IN'
    source: ClassNode
    target: YearGroupNode

class FormGroupHasStudent(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS'
    source: FormGroupNode
    target: StudentNode

class TutorGroupHasStudent(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS'
    source: TutorGroupNode
    target: StudentNode

class YearGroupHasStudent(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS'
    source: YearGroupNode
    target: StudentNode

class StudentBelongsToYearGroup(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_IN'
    source: StudentNode
    target: YearGroupNode

## Calendar layer relationships
class SchoolHasCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_ACADEMIC_YEAR'
    source: SchoolNode
    target: YearNode

class CalendarYearBelongsToSchool(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_SCHOOL'
    source: YearNode
    target: SchoolNode

class SchoolHasTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_TERM'
    source: SchoolNode
    target: TermNode

class TermBelongsToSchool(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_SCHOOL'
    source: TermNode
    target: SchoolNode

class SchoolHasWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS'
    source: SchoolNode
    target: WeekNode

class WeekBelongsToSchool(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_SCHOOL'
    source: WeekNode
    target: SchoolNode

class SchoolHasDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS'
    source: SchoolNode
    target: DayNode

class DayBelongsToSchool(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BELONGS_TO_SCHOOL'
    source: DayNode
    target: SchoolNode

class SchoolHasPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_TIMETABLED_PERIOD'
    source: SchoolNode
    target: PeriodNode

class PeriodBelongsToSchool(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'AT'
    source: PeriodNode
    target: SchoolNode

class CalendarYearHasTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: YearNode
    target: TermNode

class TermBelongsToCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: TermNode
    target: YearNode

class CalendarYearHasWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: YearNode
    target: WeekNode

class WeekBelongsToCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: WeekNode
    target: YearNode

class CalendarYearHasDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: YearNode
    target: DayNode

class DayBelongsToCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: DayNode
    target: YearNode

class CalendarYearHasPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: YearNode
    target: PeriodNode

class PeriodBelongsToCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: PeriodNode
    target: YearNode

class TermHasWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: TermNode
    target: WeekNode

class WeekBelongsToTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: WeekNode
    target: TermNode

class TermHasDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: TermNode
    target: DayNode

class DayBelongsToTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: DayNode
    target: TermNode

class TermHasPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: TermNode
    target: PeriodNode

class PeriodBelongsToTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: PeriodNode
    target: TermNode

class WeekHasDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: WeekNode
    target: DayNode

class DayBelongsToWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: DayNode
    target: WeekNode

class WeekHasPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: WeekNode
    target: PeriodNode

class PeriodBelongsToWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: PeriodNode
    target: WeekNode

class DayHasPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: DayNode
    target: PeriodNode

class PeriodBelongsToDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'ON'
    source: PeriodNode
    target: DayNode

## Curriculum layer relationships
    # commented out in code
class SubjectForKeyStage(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'FOR_KEY_STAGE'
    source: SubjectNode
    target: KeyStageNode

class KeyStageIncludesTopic(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'MUST_INCLUDE'
    source: KeyStageNode
    target: TopicNode

class SubjectIncludesTopic(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: SubjectNode
    target: TopicNode

class TopicIncludesTopicLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: TopicNode
    target: TopicLessonNode

class TopicIncludesLearningStatement(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BY_THE_END_OF_THE_TOPIC_THE_STUDENT_SHOULD_BE_ABLE_TO'
    source: TopicNode
    target: LearningStatementNode

class LearningStatementPartOfTopic(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'PART_OF'
    source: LearningStatementNode
    target: TopicNode

class TopicLessonIncludesLearningStatement(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'BY_THE_END_OF_THE_LESSON_THE_STUDENT_SHOULD_BE_ABLE_TO'
    source: TopicLessonNode
    target: LearningStatementNode

class LearningStatementPartOfTopicLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'PART_OF'
    source: LearningStatementNode
    target: TopicLessonNode

# Science-specific curriculum layer relationships
class TopicLessonIncludesScienceLab(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'COULD_INCLUDE'
    source: TopicLessonNode
    target: ScienceLabNode

## Timetabling layer relationships
    # Entity layer relationships
class SchoolHasTimetable(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'MANAGES'
    source: SchoolNode
    target: TimetableNode

class TimetableBelongsToSchool(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'CREATED_BY'
    source: TimetableNode
    target: SchoolNode

class TimetableHasPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: TimetableNode
    target: PeriodNode

class PeriodBelongsToTimetable(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: PeriodNode
    target: TimetableNode

class TeacherTeachesLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_RESPONSIBLE_FOR'
    source: TeacherNode
    target: LessonNode

class LessonHasRoom(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'LOCATED_IN'
    source: LessonNode
    target: RoomNode

class ClassToSubject(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_TAUGHT'
    source: ClassNode
    target: SubjectNode

class SubjectToClass(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_THE_SUBJECT_DOMAIN_FOR'
    source: SubjectNode
    target: ClassNode

class ClassHasLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'ATTENDS'
    source: ClassNode
    target: LessonNode

class ClassToYearGroup(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_IN'
    source: ClassNode
    target: YearGroupNode

class YearGroupToClass(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS'
    source: YearGroupNode
    target: ClassNode

    # Calendar layer relationships
class CalendarYearHasLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: YearNode
    target: LessonNode

class LessonInCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: LessonNode
    target: YearNode

class TermHasLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: TermNode
    target: LessonNode

class LessonInTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: LessonNode
    target: TermNode

class WeekHasLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: WeekNode
    target: LessonNode

class LessonInWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: LessonNode
    target: WeekNode

class DayHasLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: DayNode
    target: LessonNode

class LessonInDay(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: LessonNode
    target: DayNode

class PeriodHasLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'INCLUDES'
    source: PeriodNode
    target: LessonNode

class LessonInPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IN'
    source: LessonNode
    target: PeriodNode

    # Curriculum layer relationships
class LessonIsForSubject(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_FOR'
    source: LessonNode
    target: SubjectNode

class SubjectTeachesLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_THE_SUBJECT_DOMAIN_FOR'
    source: SubjectNode
    target: LessonNode

class LessonIsFPartOfTopic(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'COVERS_PART_OF'
    source: LessonNode
    target: TopicNode

class TopicIncludesLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_THE_TOPIC_DOMAIN_FOR'
    source: TopicNode
    target: LessonNode    

class TopicLessonIsForLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_TAUGHT_DURING'
    source: TopicLessonNode
    target: LessonNode

class LessonIsAboutTopicLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'TEACHES'
    source: LessonNode
    target: TopicLessonNode

class LearningStatementIsForLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'IS_COVERED_DURING'
    source: LearningStatementNode
    target: LessonNode

class LessonIsAboutLearningStatement(BaseRelationship):
    __relationshiptype__: ClassVar[str] = "BY_THE_END_OF_THE_LESSON_THE_STUDENT_SHOULD_BE_ABLE_TO"
    source: LessonNode
    target: LearningStatementNode

# Planner layer relationships
    

# Time layer relationships
class CalendarYearHasNextCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = "HAS_NEXT"
    source: YearNode
    target: YearNode

class CalendarYearHasPreviousCalendarYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS'
    source: YearNode
    target: YearNode

class MonthHasNextMonth(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT'
    source: MonthNode
    target: MonthNode

class MonthHasPreviousMonth(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS'
    source: MonthNode
    target: MonthNode

class WeekHasNextWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT'
    source: WeekNode
    target: WeekNode

class WeekHasPreviousWeek(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS'
    source: WeekNode
    target: WeekNode

class DateHasNextDate(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT'
    source: DayNode
    target: DayNode

class DateHasPreviousDate(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS'
    source: DayNode
    target: DayNode

class AcademicYearHasNextAcademicYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT'
    source: AcademicYearNode
    target: AcademicYearNode

class AcademicYearHasPreviousAcademicYear(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS'
    source: AcademicYearNode
    target: AcademicYearNode

class TermHasNextTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT'
    source: TermNode
    target: TermNode

class TermHasPreviousTerm(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS'
    source: TermNode
    target: TermNode

class PeriodHasNextPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT'
    source: PeriodNode
    target: PeriodNode

class PeriodHasPreviousPeriod(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS'
    source: PeriodNode
    target: PeriodNode

    # Timetabling layer relationships
class LessonHasNextLessonInSubjectSequence(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_NEXT'
    source: LessonNode
    target: LessonNode

class LessonHasPreviousLessonInSubjectSequence(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'HAS_PREVIOUS'
    source: LessonNode
    target: LessonNode