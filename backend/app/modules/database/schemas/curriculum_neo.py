from modules.database.tools.neontology.basenode import BaseNode
from typing import ClassVar, Optional

# Curriculum layer
class KeyStageNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'KeyStage'
    __primaryproperty__: ClassVar[str] = 'key_stage_id'
    key_stage_id: str
    key_stage_name: Optional[str] = None
    
class YearGroupNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'YearGroup'
    __primaryproperty__: ClassVar[str] = 'year_group_id'
    year_group_id: str
    year_group_name: Optional[str] = None

class KeyStageSyllabusNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'KeyStageSyllabus'
    __primaryproperty__: ClassVar[str] = 'ks_syllabus_id'
    ks_syllabus_id: str
    ks_syllabus_name: Optional[str] = None

class YearGroupSyllabusNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'YearGroupSyllabus'
    __primaryproperty__: ClassVar[str] = 'yr_syllabus_id'
    yr_syllabus_id: str
    yr_syllabus_name: Optional[str] = None
    
class SubjectNode(BaseNode): # TODO: This is an example, replace with actual schema
    __primarylabel__: ClassVar[str] = 'Subject'
    __primaryproperty__: ClassVar[str] = 'subject_id'
    subject_id: str
    subject_name: Optional[str] = None
    
class TopicNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Topic'
    __primaryproperty__: ClassVar[str] = 'topic_id'
    topic_id: str
    topic_title: Optional[str] = None
    total_number_of_lessons_for_topic: Optional[str] = None
    topic_type: Optional[str] = None
    topic_assessment_type: Optional[str] = None

class TopicLessonNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Lesson'
    __primaryproperty__: ClassVar[str] = 'topic_lesson_id'
    topic_lesson_id: str
    topic_lesson_title: Optional[str] = None
    topic_lesson_type: Optional[str] = None
    topic_lesson_length: Optional[str] = None
    topic_lesson_suggested_activities: Optional[str] = None
    topic_lesson_skills_learned: Optional[str] = None
    topic_lesson_weblinks: Optional[str] = None

class LearningStatementNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'LearningStatement'
    __primaryproperty__: ClassVar[str] = 'lesson_learning_statement_id'
    lesson_learning_statement_id: str
    lesson_learning_statement: Optional[str] = None
    lesson_learning_statement_type: Optional[str] = None

class ScienceLabNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'ScienceLab'
    __primaryproperty__: ClassVar[str] = 'science_lab_id'
    science_lab_id: str
    science_lab_title: Optional[str] = None
    science_lab_summary: Optional[str] = None
    science_lab_requirements: Optional[str] = None
    science_lab_procedure: Optional[str] = None
    science_lab_safety: Optional[str] = None
    science_lab_weblinks: Optional[str] = None