from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import modules.logger_tool as logger
log_name = 'api_modules_database_init_curriculum'
user_profile = os.environ.get("USERPROFILE", "")
app_dir = os.environ.get("APP_DIR", "")
log_dir = os.path.join(user_profile, app_dir, "logs")
logging = logger.get_logger(
    name=log_name,
    log_level='DEBUG',
    log_path=log_dir,
    log_file=log_name,
    runtime=True,
    log_format='default'
)
from modules.database.tools.db_operations import stop_database, drop_database, create_database
import modules.database.schemas.curriculum_neo as neo_curriculum
import modules.database.schemas.relationships.curricular_relationships as neo_relationships
import modules.database.tools.neontology_tools as neon
import pandas as pd

def create_curriculum(dataframes, db_name):
    stop_database(db_name)
    drop_database(db_name)
    create_database(db_name)
    
    keystagesyllabus_df = dataframes['keystagesyllabuses']
    yeargroupsyllabus_df = dataframes['yeargroupsyllabuses']
    topic_df = dataframes['topics']
    lesson_df = dataframes['lessons']
    statement_df = dataframes['statements']
    resource_df = dataframes['resources']
    
    default_topic_values = {
        'topic_assessment_type': 'Null',
        'topic_type': 'Null',
        'total_number_of_lessons_for_topic': '1',
        'topic_title': 'Null'
    }

    default_topic_lesson_values = {
        'topic_lesson_title': 'Null',
        'topic_lesson_type': 'Null',
        'topic_lesson_length': '1',
        'topic_lesson_suggested_activities': 'Null',
        'topic_lesson_skills_learned': 'Null',
        'topic_lesson_weblinks': 'Null',
    }

    default_learning_statement_values = {
        'lesson_learning_statement': 'Null',
        'lesson_learning_statement_type': 'Student learning outcome'
    }

    node_library = {}
    key_stage_nodes_created = {}
    year_group_nodes_created = {}
    last_year_group_node = {}
    last_key_stage_node = None

    # Function to sort year groups numerically where possible
    def sort_year_groups(df):
        df = df.copy()
        df['YearGroupNumeric'] = pd.to_numeric(df['YearGroup'], errors='coerce')
        return df.sort_values(by='YearGroupNumeric')
    
    for index, ks_row in keystagesyllabus_df.sort_values('KeyStage').iterrows():
        key_stage = str(ks_row['KeyStage'])
        if key_stage not in key_stage_nodes_created:
            key_stage_node = neo_curriculum.KeyStageNode(
                key_stage_id=f'KS{key_stage}',
                key_stage_name=f"Key Stage {key_stage}"
            )
            neon.create_or_merge_neontology_node(key_stage_node, database=db_name, operation='merge')
            key_stage_nodes_created[key_stage] = key_stage_node
            node_library[key_stage] = key_stage_node

            if last_key_stage_node:
                neon.create_or_merge_neontology_relationship(
                    neo_relationships.KeyStageFollowsKeyStage(source=last_key_stage_node, target=key_stage_node),
                    database=db_name, operation='merge'
                )
            last_key_stage_node = key_stage_node

        key_stage_syllabus_node = neo_curriculum.KeyStageSyllabusNode(
            ks_syllabus_id=ks_row['ID'],
            ks_syllabus_name=ks_row['Title'],
            ks_syllabus_key_stage=str(ks_row['KeyStage']),
            ks_syllabus_subject=ks_row['Subject']
        )
        neon.create_or_merge_neontology_node(key_stage_syllabus_node, database=db_name, operation='merge')
        node_library[ks_row['ID']] = key_stage_syllabus_node

        neon.create_or_merge_neontology_relationship(
            neo_relationships.KeyStageIncludesKeyStageSyllabus(source=key_stage_node, target=key_stage_syllabus_node),
            database=db_name,
            operation='merge'
        )

        related_yeargroups = sort_year_groups(yeargroupsyllabus_df[yeargroupsyllabus_df['KeyStage'] == ks_row['KeyStage']])
        
        for yg_index, yg_row in related_yeargroups.iterrows():
            year_group = yg_row['YearGroup']
            numeric_year_group = pd.to_numeric(year_group, errors='coerce')

            if pd.notna(numeric_year_group):
                numeric_year_group = int(numeric_year_group)
                if numeric_year_group not in year_group_nodes_created:
                    year_group_node = neo_curriculum.YearGroupNode(
                        year_group_id=f'Y{numeric_year_group}',
                        year_group=numeric_year_group,
                        year_group_name=f"Year {numeric_year_group}"
                    )
                    neon.create_or_merge_neontology_node(year_group_node, database=db_name, operation='merge')
                    year_group_nodes_created[numeric_year_group] = year_group_node
                    node_library[str(numeric_year_group)] = year_group_node

                    # Create sequential relationships correctly
                    if numeric_year_group - 1 in last_year_group_node:
                        neon.create_or_merge_neontology_relationship(
                            neo_relationships.YearGroupFollowsYearGroup(source=last_year_group_node[numeric_year_group - 1], target=year_group_node),
                            database=db_name, operation='merge'
                        )
                    last_year_group_node[numeric_year_group] = year_group_node

            # Always create year group syllabus nodes
            year_group_syllabus_node = neo_curriculum.YearGroupSyllabusNode(
                yr_syllabus_id=yg_row['ID'],
                yr_syllabus_name=yg_row['Title'],
                yr_syllabus_year_group=str(yg_row['YearGroup']),
                yr_syllabus_subject=yg_row['Subject']
            )
            neon.create_or_merge_neontology_node(year_group_syllabus_node, database=db_name, operation='merge')
            node_library[yg_row['ID']] = year_group_syllabus_node

            if yg_row['Subject'] == ks_row['Subject']:
                neon.create_or_merge_neontology_relationship(
                    neo_relationships.KeyStageSyllabusIncludesYearGroupSyllabus(source=key_stage_syllabus_node, target=year_group_syllabus_node),
                    database=db_name, operation='merge'
                )

            if pd.notna(numeric_year_group) and str(numeric_year_group) == str(year_group_node.year_group):
                neon.create_or_merge_neontology_relationship(
                    neo_relationships.YearGroupHasYearGroupSyllabus(source=year_group_node, target=year_group_syllabus_node),
                    database=db_name, operation='merge'
                )

    # Process topics, lessons, and statements
    for index, topic_row in topic_df.iterrows():
        yr_syllabus_node = node_library.get(topic_row['SyllabusYearID'])
        if yr_syllabus_node:
            topic_node = neo_curriculum.TopicNode(
                topic_id=topic_row['TopicID'],
                topic_title=topic_row.get('TopicTitle', default_topic_values['topic_title']),
                total_number_of_lessons_for_topic=str(topic_row.get('TotalNumberOfLessonsForTopic', default_topic_values['total_number_of_lessons_for_topic'])),
                topic_type=topic_row.get('TopicType', default_topic_values['topic_type']),
                topic_assessment_type=topic_row.get('TopicAssessmentType', default_topic_values['topic_assessment_type'])
            )
            neon.create_or_merge_neontology_node(topic_node, database=db_name, operation='merge')
            node_library[topic_row['TopicID']] = topic_node
            neon.create_or_merge_neontology_relationship(
                neo_relationships.TopicPartOfYearGroupSyllabus(source=yr_syllabus_node, target=topic_node),
                database=db_name, operation='merge'
            )

            lessons_df = lesson_df[lesson_df['TopicID'] == topic_row['TopicID']].copy()
            lessons_df.loc[:, 'Lesson'] = lessons_df['Lesson'].astype(str)
            lessons_df = lessons_df.sort_values('Lesson')

            previous_lesson_node = None
            for lesson_index, lesson_row in lessons_df.iterrows():
                lesson_data = {
                    'topic_lesson_id': lesson_row['LessonID'],
                    'topic_lesson_title': lesson_row.get('LessonTitle', default_topic_lesson_values['topic_lesson_title']),
                    'topic_lesson_type': lesson_row.get('LessonType', default_topic_lesson_values['topic_lesson_type']),
                    'topic_lesson_length': str(lesson_row.get('SuggestedNumberOfPeriodsForLesson', default_topic_lesson_values['topic_lesson_length'])),
                    'topic_lesson_suggested_activities': lesson_row.get('SuggestedActivities', default_topic_lesson_values['topic_lesson_suggested_activities']),
                    'topic_lesson_skills_learned': lesson_row.get('SkillsLearned', default_topic_lesson_values['topic_lesson_skills_learned']),
                    'topic_lesson_weblinks': lesson_row.get('WebLinks', default_topic_lesson_values['topic_lesson_weblinks'])
                }
                for key, value in lesson_data.items():
                    if pd.isna(value):
                        lesson_data[key] = default_topic_lesson_values[key]

                lesson_node = neo_curriculum.TopicLessonNode(**lesson_data)
                neon.create_or_merge_neontology_node(lesson_node, database=db_name, operation='merge')
                node_library[lesson_row['LessonID']] = lesson_node
                neon.create_or_merge_neontology_relationship(
                    neo_relationships.TopicIncludesTopicLesson(source=topic_node, target=lesson_node),
                    database=db_name, operation='merge'
                )

                # Create sequential relationships if the lesson number is a digit
                if lesson_row['Lesson'].isdigit() and previous_lesson_node:
                    neon.create_or_merge_neontology_relationship(
                        neo_relationships.TopicLessonFollowsTopicLesson(source=previous_lesson_node, target=lesson_node),
                        database=db_name, operation='merge'
                    )

                previous_lesson_node = lesson_node  # Update the previous lesson node for the next iteration

                # Process each learning statement related to the lesson
                for statement_index, statement_row in statement_df[statement_df['LessonID'] == lesson_row['LessonID']].iterrows():
                    statement_data = {
                        'lesson_learning_statement_id': statement_row['StatementID'],
                        'lesson_learning_statement': statement_row.get('LearningStatement', default_learning_statement_values['lesson_learning_statement']),
                        'lesson_learning_statement_type': statement_row.get('StatementType', default_learning_statement_values['lesson_learning_statement_type'])
                    }
                    for key in statement_data:
                        if pd.isna(statement_data[key]):
                            statement_data[key] = default_learning_statement_values[key]

                    statement_node = neo_curriculum.LearningStatementNode(**statement_data)
                    neon.create_or_merge_neontology_node(statement_node, database=db_name, operation='merge')
                    node_library[statement_row['StatementID']] = statement_node
                    neon.create_or_merge_neontology_relationship(
                        neo_relationships.LessonIncludesLearningStatement(source=lesson_node, target=statement_node),
                        database=db_name, operation='merge'
                    )

    return node_library