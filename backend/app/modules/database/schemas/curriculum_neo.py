from typing import ClassVar
from neontology import BaseNode

# Neo4j Nodes and relationships using Neontology
# Curriculum layer

class KeyStageNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'KeyStage'
    __primaryproperty__: ClassVar[str] = 'key_stage'
    key_stage_level: int
    key_stage: str

class SubjectNode(BaseNode): # TODO: This is an example, replace with actual schema
    __primarylabel__: ClassVar[str] = 'Subject'
    __primaryproperty__: ClassVar[str] = 'subject_id'
    subject_id: str
    subject_name: str
    
class TopicNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Topic'
    __primaryproperty__: ClassVar[str] = 'topic_id'
    topic_id: str
    topic_title: str
    total_number_of_lessons_for_topic: int
    topic_type: str
    topic_assessment_type: str

class TopicLessonNode(BaseNode):
    __primarylabel__: ClassVar[str] = 'Lesson'
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