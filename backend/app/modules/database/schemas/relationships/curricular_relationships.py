from typing import ClassVar
from neontology import BaseRelationship

## Curriculum layer relationships
class SubjectForKeyStage(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'SUBJECT_FOR_KEY_STAGE'
    source: SubjectNode
    target: KeyStageNode

class KeyStageIncludesTopic(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'KEY_STAGE_INCLUDES_TOPIC'
    source: KeyStageNode
    target: TopicNode

class SubjectIncludesTopic(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'SUBJECT_INCLUDES_TOPIC'
    source: SubjectNode
    target: TopicNode

class TopicIncludesTopicLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'TOPIC_INCLUDES_LESSON'
    source: TopicNode
    target: TopicLessonNode

class TopicIncludesLearningStatement(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'TOPIC_INCLUDES_LEARNING_STATEMENT'
    source: TopicNode
    target: LearningStatementNode

class LearningStatementPartOfTopicLesson(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'LEARNING_STATEMENT_PART_OF_LESSON'
    source: LearningStatementNode
    target: TopicLessonNode

# Science-specific curriculum layer relationships
class TopicLessonIncludesScienceLab(BaseRelationship):
    __relationshiptype__: ClassVar[str] = 'LESSON_INCLUDES_SCIENCE_LAB'
    source: TopicLessonNode
    target: ScienceLabNode