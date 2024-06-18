from sqlalchemy import create_engine, Column, Integer, String, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine.reflection import Inspector

Base = declarative_base()

class YourNewORM(Base):
    __tablename__ = 'your_table_name'
    id = Column(Integer, primary_key=True)
    # Define other fields here
    # Example: new_field = Column(String)

## Curricular layer
# TODO: Verify and add ORM models for curricular entities
class SubjectORM(Base):
    __tablename__ = 'subjects'
    subject_id = Column(String, primary_key=True)
    subject = Column(String)

class KeyStageORM(Base):
    __tablename__ = 'key_stages'
    key_stage_id = Column(Integer, primary_key=True)

class TopicORM(Base):
    __tablename__ = 'topics'
    topic_id = Column(Integer, primary_key=True)
    topic_title = Column(String)
    total_number_of_lessons_for_topic = Column(Integer)
    topic_type = Column(String)
    topic_assessment_type = Column(String)

class TopicLessonORM(Base):
    __tablename__ = 'topic_lessons'
    topic_lesson_id = Column(Integer, primary_key=True)
    topic_lesson_title = Column(String)

class LearningStatementORM(Base):
    __tablename__ = 'learning_statements'
    learning_statement_id = Column(Integer, primary_key=True)
    learning_statement = Column(String)
    learning_statement_type = Column(String)

class ScienceLabORM(Base):
    __tablename__ = 'science_labs'
    science_lab_id = Column(Integer, primary_key=True)
    science_lab_title = Column(String)
    science_lab_summary = Column(String)
    science_lab_requirements = Column(String)
    science_lab_procedure = Column(String)
    science_lab_safety = Column(String)
    science_lab_weblinks = Column(String)

## Calendar layer


## Timetabling layer
# TODO: Verify and add ORM models for timetabling entities
class PlannerORM(Base):
    __tablename__ = 'planner'
    planner_id = Column(Integer, primary_key=True)
    planner_id_excel = Column(String, unique=True)
    ttver = Column(Integer)
    staff_code = Column(String)
    period_date = Column(Date)
    period_of_day = Column(Integer)
    period_code = Column(String)
    week_type = Column(String)
    period_is_lesson = Column(Integer)
    period_is_type = Column(String)
    period_mod = Column(String)
    period_notes = Column(String)
    period_json = Column(String)
    period_start_time = Column(Time)
    period_finish_time = Column(Time)
    room = Column(String)
    class_key_stage = Column(Integer)
    class_year = Column(Integer)
    class_code = Column(String)
    class_mod = Column(String)
    class_notes = Column(String)
    class_json = Column(String)
    lesson_sub_enter = Column(String)
    lesson_topic_enter = Column(String)
    lesson_lesson_enter = Column(String)
    lesson_topic_code = Column(String)
    lesson_code = Column(String)
    lesson_mod = Column(String)
    lesson_notes = Column(String)
    lesson_json = Column(String)

class ClassTimetableORM(Base):
    __tablename__ = 'class_timetable'
    id = Column(Integer, primary_key=True)
    # Verify and add fields and relationships

class StaffTimetableORM(Base):
    __tablename__ = 'staff_timetable'
    id = Column(Integer, primary_key=True)
    # Verify and add fields and relationships

class StudentTimetableORM(Base):
    __tablename__ = 'student_timetable'
    id = Column(Integer, primary_key=True)
    # Verify and add fields and relationships

class PeriodORM(Base):
    __tablename__ = 'period'
    id = Column(Integer, primary_key=True)
    # Verify and add fields and relationships

## Entity layer
# TODO: Verify and add ORM models for entities
class StaffORM(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    # Verify and add fields and relationships

class StudentORM(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    # Verify and add fields and relationships

class ClassORM(Base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True)
    # Verify and add fields and relationships

class RoomORM(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    # Verify and add fields and relationships