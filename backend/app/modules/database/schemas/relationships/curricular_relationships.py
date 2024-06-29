import modules.database.schemas.curriculum_neo as neo_curriculum
from modules.database.tools.neontology.baserelationship import BaseRelationship
from typing import ClassVar

## Curriculum layer relationships
class SubjectForKeyStage(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'SUBJECT_FOR_KEY_STAGE'
    source: neo_curriculum.SubjectNode
    target: neo_curriculum.KeyStageNode

class KeyStageIncludesTopic(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'KEY_STAGE_INCLUDES_TOPIC'
    source: neo_curriculum.KeyStageNode
    target: neo_curriculum.TopicNode

class SubjectIncludesTopic(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'SUBJECT_INCLUDES_TOPIC'
    source: neo_curriculum.SubjectNode
    target: neo_curriculum.TopicNode

class TopicIncludesTopicLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'TOPIC_INCLUDES_LESSON'
    source: neo_curriculum.TopicNode
    target: neo_curriculum.TopicLessonNode

class TopicIncludesLearningStatement(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'TOPIC_INCLUDES_LEARNING_STATEMENT'
    source: neo_curriculum.TopicNode
    target: neo_curriculum.LearningStatementNode

class LearningStatementPartOfTopicLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'LEARNING_STATEMENT_PART_OF_LESSON'
    source: neo_curriculum.LearningStatementNode
    target: neo_curriculum.TopicLessonNode

# Science-specific curriculum layer relationships
class TopicLessonIncludesScienceLab(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'LESSON_INCLUDES_SCIENCE_LAB'
    source: neo_curriculum.TopicLessonNode
    target: neo_curriculum.ScienceLabNode