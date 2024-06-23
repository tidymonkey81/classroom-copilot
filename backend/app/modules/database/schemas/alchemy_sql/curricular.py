from pydantic import BaseModel, Field, validator, ValidationError

class SubjectSchema(BaseModel):
    subject: str = Field(alias='Subject')
    subject_code: str = Field(alias='SubjectCode')

    class Config:
        orm_mode = True
        populate_by_name = True

class KeyStageSchema(BaseModel):
    key_stage_level: int = Field(alias='KeyStageLevel')
    key_stage: str = Field(alias='KeyStage')

    class Config:
        orm_mode = True
        populate_by_name = True

class TopicSchema(BaseModel):
    topic_id: str = Field(alias='TopicID')
    topic_title: str = Field(alias='TopicTitle')
    total_number_of_lessons_for_topic: int = Field(alias='TotalNumberOfLessonsForTopic')
    topic_type: str = Field(alias='TopicType')
    topic_assessment_type: str = Field(alias='TopicAssessmentType')

    class Config:
        orm_mode = True
        populate_by_name = True

class TopicLessonSchema(BaseModel):
    topic_lesson_id: str = Field(alias='TopicLessonID')
    topic_lesson_title: str = Field(alias='TopicLessonTitle')
    topic_lesson_type: str = Field(alias='TopicLessonType')
    topic_lesson_length: int = Field(alias='TopicLessonLength')
    topic_lesson_suggested_activities: str = Field(alias='TopicLessonSuggestedActivities')
    topic_lesson_weblinks: str = Field(alias='TopicLessonWeblinks')
    
    class Config:
        orm_mode = True
        populate_by_name = True

class LearningStatementSchema(BaseModel):
    learning_statement_id: str = Field(alias='LearningStatementID')
    learning_statement: str = Field(alias='LearningStatementTitle')
    learning_statement_type: str = Field(alias='LearningStatementType')

    class Config:
        orm_mode = True
        populate_by_name = True

class ScienceLabSchema(BaseModel):
    science_lab_id: str = Field(alias='ScienceLabID')
    science_lab_title: str = Field(alias='ScienceLabTitle')
    science_lab_summary: str = Field(alias='ScienceLabSummary')
    science_lab_requirements: str = Field(alias='ScienceLabRequirements')
    science_lab_procedure: str = Field(alias='ScienceLabProcedure')
    science_lab_safety: str = Field(alias='ScienceLabSafety')
    science_lab_weblinks: str = Field(alias='ScienceLabLinks')

    class Config:
        orm_mode = True
        populate_by_name = True