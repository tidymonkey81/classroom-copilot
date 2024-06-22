from sqlalchemy import create_engine, Column, Integer, String, Date, Time
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel, Field, validator, ValidationError
import datetime
import os
import pandas as pd
from typing import Optional

Base = declarative_base()

# Define the SQLAlchemy ORM model
class PlannerModel(Base):
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
    lesson_title = Column(String)
    lesson_mod = Column(String)
    lesson_notes = Column(String)
    lesson_json = Column(String)

# Define the Pydantic Schema
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
    lesson_title: Optional[str] = Field(alias='LessonTitle', default=None)
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
               'lesson_sub_enter', 'lesson_topic_enter', 'lesson_lesson_enter', 'lesson_topic_code', 'lesson_code', 'lesson_title',
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

# Function to convert from Pydantic Schema to SQLAlchemy Model
def schema_to_orm(schema: PlannerSchema) -> PlannerModel:
    return PlannerModel(
        planner_id=schema.planner_id,
        planner_id_excel=schema.planner_id_excel,
        ttver=schema.ttver,
        staff_code=schema.staff_code,
        period_date=schema.period_date,
        period_of_day=schema.period_of_day,
        period_code=schema.period_code,
        week_type=schema.week_type,
        period_is_lesson=schema.period_is_lesson,
        period_is_type=schema.period_is_type,
        period_mod=schema.period_mod,
        period_notes=schema.period_notes,
        period_json=schema.period_json,
        period_start_time=schema.period_start_time,
        period_finish_time=schema.period_finish_time,
        room=schema.room,
        class_key_stage=schema.class_key_stage,
        class_year=schema.class_year,
        class_code=schema.class_code,
        class_mod=schema.class_mod,
        class_notes=schema.class_notes,
        class_json=schema.class_json,
        lesson_sub_enter=schema.lesson_sub_enter,
        lesson_topic_enter=schema.lesson_topic_enter,
        lesson_lesson_enter=schema.lesson_lesson_enter,
        lesson_code=schema.lesson_code,
        lesson_title=schema.lesson_title,
        lesson_mod=schema.lesson_mod,
        lesson_notes=schema.lesson_notes,
        lesson_json=schema.lesson_json
    )

# Function to convert to time object
def convert_to_time(time_input):
    if pd.notnull(time_input):
        if isinstance(time_input, datetime.time):
            return time_input
        elif isinstance(time_input, str):
            print("The old time input is: ",time_input)
            new_time_input = datetime.datetime.strptime(time_input, '%H:%M:%S').time()
            print("The new time input is: ",new_time_input)
            return new_time_input
    return None

def create_database():
    print("Creating database...")
    # If the file exists, don't delete it, just connect to it
    # SQLAlchemy engine and session creation to create the tables in the database
    engine = create_engine('sqlite:///tmp/kevlar_ai.db')  # Adjust the path as necessary
    Base.metadata.create_all(engine)  # This will create tables if they don't exist yet
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def create_session(file_path=None):
    print("Creating session")
    # Specify the absolute path to the database file
    db_file_path = os.path.join(os.getcwd(), 'tmp', 'kevlar_ai.db')

    # Check if the directory exists and create it if it does not
    db_dir = os.path.dirname(db_file_path)
    if not os.path.exists(db_dir):
        print("Creating directory...")
        os.makedirs(db_dir)
        # There is no database file yet, so create it
        engine = create_engine('sqlite:///tmp/kevlar_ai.db')  # Adjust the path as necessary
        print("Doing the base thing...")
        Base.metadata.create_all(engine)  # This will create tables if they don't exist yet
        Session = sessionmaker(bind=engine)
        session = Session()
        # Enter the data into the database
        print("Inserting data...")
        insert_data(session, file_path)
        return session
    else:
        print("Directory already exists. Using existing database...")
        engine = create_engine('sqlite:///tmp/kevlar_ai.db')  # Adjust the path as necessary
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

# Function to insert the data into the database
def insert_data(session, file_path):
    # Read the Excel file
    planner_df = pd.read_excel(file_path, sheet_name='Planner')

    # Insert the data into the database
    i = 0
    for _, row in planner_df.iterrows():
        # If row['PeriodMod'] == 'H', skip the row
        if row['PeriodMod'] == 'H':
            continue
        try:
            planner_schema = PlannerSchema(
                planner_id=i,
                planner_id_excel=str(row['StaffWeekPeriodCode']) if pd.notnull(row['StaffWeekPeriodCode']) else None,
                ttver=row['TTVer'],
                staff_code=row['StaffCode'],
                week_type=row['WeekAOrBOfTimetable'],
                period_of_day=row['PeriodOfDay'],
                period_code=row['PeriodCode'],
                period_date=pd.to_datetime(row['LessonDate']) if pd.notnull(row['LessonDate']) else None,
                period_mod=str(row['PeriodMod']) if pd.notnull(row['PeriodMod']) else None,
                period_start_time=convert_to_time(row.get('LessonStartTime')),
                period_finish_time=convert_to_time(row.get('LessonFinishTime')),
                period_is_lesson=None,
                period_is_type=None,
                period_notes=None,
                period_json=None,
                room=str(row['Room']) if pd.notnull(row['Room']) else None,
                class_key_stage=row['KeyStage'] if pd.notnull(row['KeyStage']) else None,
                class_year=row['YearGroup'] if pd.notnull(row['YearGroup']) else None,
                class_code=str(row['ClassCode']) if pd.notnull(row['ClassCode']) else None,
                class_mod=None,
                class_notes=None,
                class_json=None,
                lesson_sub_enter=str(row['SubEnter']) if pd.notnull(row['SubEnter']) else None,
                lesson_topic_enter=str(row['TopicEnter']) if pd.notnull(row['TopicEnter']) else None,
                lesson_lesson_enter=str(row['LessonEnter']) if pd.notnull(row['LessonEnter']) else None,
                lesson_topic_code=str(row['TopicCode']) if pd.notnull(row['TopicCode']) else None,
                lesson_code=str(row['TopicLessonCode']) if pd.notnull(row['TopicLessonCode']) else None,
                lesson_title=str(row['LessonTitle']) if pd.notnull(row['LessonTitle']) else None,
                lesson_mod=None,
                lesson_notes=str(row['LessonNotesEnter']) if pd.notnull(row['LessonNotesEnter']) else None,
                lesson_json=str(row['LessonJSON']) if pd.notnull(row['LessonJSON']) else None,
            )
            # Convert schema to ORM
            planner_orm = schema_to_orm(planner_schema)
            session.add(planner_orm)
            i += 1
        except ValidationError as exc:
            print(repr(exc.errors()[0]))

    # Commit the transaction
    session.commit()
