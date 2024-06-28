

planner = planner.get_excel_sheets('planner.xlsx ')

topic_df = planner['topiclookup_df']
lesson_df = planner['lessonlookup_df']
statement_df = planner['statementlookup_df']

topic_excel_node_list = []
topic_excel_helper_list = []
default_values = {
    'topic_assessment_type': 'Null'
    }

for index, row in topic_df.iterrows():
    # Filter and map the row to TopicNode fields
    topic_node_data = {
        'topic_id': row.get('TopicID'),
        'topic_title': row.get('TopicTitle'),
        'total_number_of_lessons_for_topic': row.get('TotalNumberOfLessonsForTopic'),
        'topic_type': row.get('TopicType'),
        'topic_assessment_type': row.get('TopicAssessmentType')
    }
    topic_excel_helper_data = {
        'topic_source': row.get('TopicSource'),
        'topic_department': row.get('TopicDepartment'),
        'topic_key_stage': row.get('TopicKeyStage'),
        'topic_year': row.get('TopicYear'),
        'topic_subject': row.get('TopicSubject'),
        'topic_sequence': row.get('TopicSequence')
    }
    # Replace NaN values with defaults
    topic_excel_node_data_processed = replace_nan_with_default(topic_node_data, default_values)
    topic_excel_helper_data_processed = replace_nan_with_default(topic_excel_helper_data, default_values)

    # Create a TopicNode instance for each row
    try:
        topic_node = TopicNode(**topic_excel_node_data_processed)
        combined_data = {
            'node': topic_node,
            'helper': topic_excel_helper_data
        }
        topic_excel_node_list.append(combined_data)
    except ValidationError as e:
        logging.error(f"Validation error for row {index}: {e}")


# Then, use the create_or_merge_neontology_node function to add these nodes to your Neo4j database
for node_data in topic_excel_node_list:
    try:
        neon.create_or_merge_neontology_node(node_data['node'], operation='merge')
    except Exception as e:
        logging.error(f"Error in processing node: {e}")


learning_statement_excel_node_list = []
learning_statement_excel_helper_list = []
default_values = {
    # Add default values for fields that might contain NaN
    'lesson_learning_statement': 'Null',
    'lesson_learning_statement_type': 'Student learning outcome'
}

for index, row in statement_df.iterrows():
    # Filter and map the row to LearningStatementNode fields
    learning_statement_node_data = {
        'lesson_learning_statement_id': row.get('LearningOutcomeID'),
        'lesson_learning_statement': row.get('LearningOutcomeStatement', default_values['lesson_learning_statement']),
        'lesson_learning_statement_type': row.get('LearningStatementType', default_values['lesson_learning_statement_type']),
    }
    logging.pedantic(f"learning_statement_node_data: {learning_statement_node_data}")
    learning_statement_excel_helper_data = {
        'lesson_learning_statement_source': row.get('TopicSource'),
        'lesson_learning_statement_department': row.get('TopicDepartment'),
        'lesson_learning_statement_key_stage': row.get('TopicKeyStage'),
        'lesson_learning_statement_topic_id': row.get('TopicID'),
        'lesson_learning_statement_lesson_id': row.get('LessonID'),
        'lesson_learning_statement_topic_year': row.get('TopicYear'),
        'lesson_learning_statement_topic_subject': row.get('TopicSubject'),
        'lesson_learning_statement_topic_sequence': row.get('TopicSequence'),
        'lesson_learning_statement_lesson_sequence': row.get('LessonSequence'),
        'lesson_learning_statement_sequence': row.get('LearningOutcomeSequence')            
    }
    logging.pedantic(f"learning_statement_excel_helper_list: {learning_statement_excel_helper_list}")

    # Replace NaN values with defaults
    learning_statement_excel_node_data_processed = replace_nan_with_default(learning_statement_node_data, default_values)
    logging.pedantic(f"processed_data: {learning_statement_excel_node_data_processed}")
    learning_statement_excel_helper_data_processed = replace_nan_with_default(learning_statement_excel_helper_data, default_values)
    logging.pedantic(f"processed_data: {learning_statement_excel_helper_data_processed}")

    # Create a LearningStatementNode instance for each row
    try:
        learning_statement_node = LearningStatementNode(**learning_statement_excel_node_data_processed)
        logging.pedantic(f"learning_statement_node: {learning_statement_node}")
        combined_data = {
            'node': learning_statement_node,
            'helper': learning_statement_excel_helper_data
        }
        logging.pedantic(f"combined_data: {combined_data}")
        learning_statement_excel_node_list.append(combined_data)
        logging.pedantic(f"Appended new combined data to learning_statement_excel_node_list, current length: {len(learning_statement_excel_node_list)}")
    except ValidationError as e:
        logging.error(f"Validation error for row {index}: {e}")

# Then, use the create_or_merge_neontology_node function to add these nodes to your Neo4j database
for node_data in learning_statement_excel_node_list:
    try:
        logging.pedantic(f"Creating or merging node: {node_data}")
        neon.create_or_merge_neontology_node(node_data['node'], operation='create')
    except Exception as e:
        logging.error(f"Error in processing node: {e}")
        
        
# Create relationships between TopicNode and TopicLessonNode
relationship_list = []
for topic_lesson_node in topic_lesson_excel_node_list:
    logging.debug(f"Processing topic lesson node: {topic_lesson_node}")
    topic_lesson_node_id = topic_lesson_node['node'].topic_lesson_id
    logging.pedantic(f"Processing topic lesson node ID: {topic_lesson_node_id}")
    lesson_nodes = neo4j.find_nodes_by_label_and_properties(neo4j_driver, 'Lesson', {'topic_lesson_id': topic_lesson_node_id})
    logging.pedantic(f"Lesson nodes found: {lesson_nodes}")
    if not lesson_nodes:  # Check if the list is empty
        logging.error(f"No lesson node found for ID {topic_lesson_node_id}")

    topic_node_id = topic_lesson_node['helper']['topic_lesson_topic_id']
    logging.pedantic(f"Processing topic node ID: {topic_node_id}")
    topic_nodes = neo4j.find_nodes_by_label_and_properties(neo4j_driver, 'Topic', {'topic_id': topic_node_id})
    logging.pedantic(f"Topic nodes found: {topic_nodes}")
    if not topic_nodes:  # Check if the list is empty
        logging.error(f"No topic node found for ID {topic_node_id}")
    
    # Assuming only one node is expected for each query
    lesson_node_properties = dict(lesson_nodes[0])  # Extract properties from the Neo4j Node
    logging.pedantic(f"Lesson node properties: {lesson_node_properties}")
    topic_node_properties = dict(topic_nodes[0])    # Extract properties from the Neo4j Node
    logging.pedantic(f"Topic node properties: {topic_node_properties}")

    # Create instances of TopicNode and TopicLessonNode using the extracted properties
    logging.pedantic(f"Creating instances of TopicNode and TopicLessonNode")
    neontology_lesson_node = TopicLessonNode(**lesson_node_properties)
    logging.pedantic(f"Neontology lesson node: {neontology_lesson_node}")
    neontology_topic_node = TopicNode(**topic_node_properties)
    logging.pedantic(f"Neontology topic node: {neontology_topic_node}")

    # Create the relationship
    logging.pedantic(f"Creating relationship between {neontology_topic_node} and {neontology_lesson_node}")
    topic_has_lesson_relationship = TopicIncludesTopicLesson(source=neontology_topic_node, target=neontology_lesson_node)
    logging.pedantic(f"Relationship created: {topic_has_lesson_relationship}")

    # Merge or create relationship in the database
    logging.pedantic(f"Merging or creating relationship: {topic_has_lesson_relationship}")
    neon.create_or_merge_neontology_relationship(topic_has_lesson_relationship, operation='merge')
    logging.pedantic(f"Relationship merged or created: {topic_has_lesson_relationship}")
    
    
topic_lesson_excel_node_list = []
topic_lesson_excel_helper_list = []
default_values = {
    'topic_lesson_title': 'Null',  # Corrected default value key
    'topic_lesson_type': 'Null',  # Corrected default value key
    'topic_lesson_length': 1,             # Corrected default value key
    'topic_lesson_suggested_activities': 'Null',  # Corrected default value key
    'topic_lesson_skills_learned': 'Null',  # Corrected default value key
    'topic_lesson_weblinks': 'Null',   # Corrected default value key
}

for index, row in lesson_df.iterrows():
    # Filter and map the row to TopicLessonNode fields
    topic_lesson_node_data = {
        'topic_lesson_id': row.get('LessonID'),
        'topic_lesson_title': row.get('LessonTitle', default_values['topic_lesson_title']),
        'topic_lesson_type': row.get('TopicLessonType', default_values['topic_lesson_type']),
        'topic_lesson_length': row.get('SuggestedNumberOfPeriodsForLesson', default_values['topic_lesson_length']),
        'topic_lesson_suggested_activities': row.get('SuggestedActivities', default_values['topic_lesson_suggested_activities']),
        'topic_lesson_skills_learned': row.get('SkillsLearned', default_values['topic_lesson_skills_learned']),
        'topic_lesson_weblinks': row.get('TopicLessonWeblinks', default_values['topic_lesson_weblinks'])
        }
    logging.pedantic(f"topic_lesson_node_data: {topic_lesson_node_data}")
    topic_lesson_excel_helper_data = {
        'topic_lesson_source': row.get('TopicSource'),
        'topic_lesson_department': row.get('TopicDepartment'),
        'topic_lesson_key_stage': row.get('TopicKeyStage'),
        'topic_lesson_topic_id': row.get('TopicID'),
        'topic_lesson_topic_year': row.get('TopicYear'),
        'topic_lesson_topic_subject': row.get('TopicSubject'),
        'topic_lesson_topic_sequence': row.get('TopicSequence'),
        'topic_lesson_lesson_sequence': row.get('LessonSequence'),
        'topic_lesson_learning_objective': row.get('LessonLearningObjective'),
        }
    logging.pedantic(f"topic_lesson_excel_helper_list: {topic_lesson_excel_helper_list}")

    # Replace NaN values with defaults
    topic_lesson_excel_node_data_processed = replace_nan_with_default(topic_lesson_node_data, default_values)
    logging.pedantic(f"topic_lesson_excel_node_list_processed_data: {topic_lesson_excel_node_data_processed}")
    topic_lesson_excel_helper_data_processed = replace_nan_with_default(topic_lesson_excel_helper_data, default_values)
    logging.pedantic(f"topic_lesson_excel_helper_list_processed_data: {topic_lesson_excel_helper_data_processed}")

    # Create a TopicLessonNode instance for each row
    try:
        topic_lesson_node = TopicLessonNode(**topic_lesson_excel_node_data_processed)
        logging.pedantic(f"topic_lesson_node: {topic_lesson_node}")
        combined_data = {
            'node': topic_lesson_node,
            'helper': topic_lesson_excel_helper_data
        }
        logging.pedantic(f"combined_data: {combined_data}")
        topic_lesson_excel_node_list.append(combined_data)
        logging.pedantic(f"Appended new combined data to topic_lesson_excel_node_list, current length: {len(topic_lesson_excel_node_list)}")
    except ValidationError as e:
        logging.error(f"Validation error for row {index}: {e}")
        
for node_data in topic_lesson_excel_node_list:
    try:
        neon.create_or_merge_neontology_node(node_data['node'], operation='create')
        logging.pedantic(f"TopicLessonNode instance created for row {index}: {topic_lesson_node}")
    except Exception as e:
        logging.error(f"Error in processing node: {e}")


    
# Create relationships between TopicNode and LearningStatementNode and LessonNode and LearningStatementNode
# Assuming only one node is expected for each query
for learning_statement_node in learning_statement_excel_node_list:
    logging.info(f"Processing learning statement node: {learning_statement_node}")
    learning_statement_node_id = learning_statement_node['node'].lesson_learning_statement_id

    logging.pedantic(f"Processing learning statement node ID: {learning_statement_node_id}")
    learning_statement_nodes = neo4j.find_nodes_by_label_and_properties(neo4j_driver, 'LearningStatement', {'lesson_learning_statement_id': learning_statement_node_id})
    if not learning_statement_nodes:  # Check if the list is empty
        logging.error(f"No learning statement node found for ID {learning_statement_node_id}")
        continue
    logging.pedantic(f"Learning statement nodes found: {learning_statement_nodes}")
    learning_statement_node_properties = dict(learning_statement_nodes[0])  # Extract properties from the Neo4j Node
    logging.pedantic(f"Learning statement node properties: {learning_statement_node_properties}")
    
    topic_node_id = learning_statement_node['helper']['lesson_learning_statement_topic_id']
    logging.pedantic(f"Processing topic node ID: {topic_node_id}")
    topic_nodes = neo4j.find_nodes_by_label_and_properties(neo4j_driver, 'Topic', {'topic_id': topic_node_id})
    if not topic_nodes:  # Check if the list is empty
        logging.error(f"No topic node found for ID {topic_node_id}")
        continue
    logging.pedantic(f"Topic nodes found: {topic_nodes}")
    topic_node_properties = dict(topic_nodes[0])    # Extract properties from the Neo4j Node
    logging.pedantic(f"Topic node properties: {topic_node_properties}")    

    topic_lesson_node_id = learning_statement_node['helper']['lesson_learning_statement_lesson_id']
    logging.pedantic(f"Processing topic lesson node ID: {topic_lesson_node_id}")
    topic_lesson_nodes = neo4j.find_nodes_by_label_and_properties(neo4j_driver, 'Lesson', {'topic_lesson_id': topic_lesson_node_id})
    if not topic_lesson_nodes:
        logging.error(f"No topic lesson node found for ID {topic_lesson_node_id}")
        continue
    logging.pedantic(f"Topic lesson nodes found: {topic_lesson_nodes}")
    lesson_node_properties = dict(topic_lesson_nodes[0])  # Extract properties from the Neo4j Node
    logging.pedantic(f"Lesson node properties: {lesson_node_properties}")
    
    # Create instances of TopicNode and TopicLessonNode using the extracted properties
    logging.pedantic(f"Creating instances of TopicNode and TopicLessonNode and LearningStatementNode")
    neontology_lesson_node = TopicLessonNode(**lesson_node_properties)
    logging.pedantic(f"Neontology lesson node: {neontology_lesson_node}")
    neontology_topic_node = TopicNode(**topic_node_properties)
    logging.pedantic(f"Neontology topic node: {neontology_topic_node}")
    neontology_learning_statement_node = LearningStatementNode(**learning_statement_node_properties)
    logging.pedantic(f"Neontology learning statement node: {neontology_learning_statement_node}")

    # Create the relationship between learning statement and lesson
    logging.pedantic(f"Creating relationship between {neontology_learning_statement_node} and {neontology_lesson_node}")
    statement_in_lesson_relationship = LearningStatementPartOfTopicLesson(source=neontology_learning_statement_node, target=neontology_lesson_node)
    logging.pedantic(f"Relationship created: {statement_in_lesson_relationship}")

    # Create the relationship between learning statement and topic
    logging.pedantic(f"Creating relationship between {neontology_learning_statement_node} and {neontology_topic_node}")
    topic_has_learning_statement_relationship = TopicIncludesLearningStatement(source=neontology_topic_node, target=neontology_learning_statement_node)
    logging.pedantic(f"Relationship created: {topic_has_learning_statement_relationship}")

    # Merge or create relationships in the database
    logging.pedantic(f"Merging or creating relationship: {statement_in_lesson_relationship}")
    neon.create_or_merge_neontology_relationship(statement_in_lesson_relationship, operation='merge')
    logging.pedantic(f"Relationship merged or created: {statement_in_lesson_relationship}")
    logging.pedantic(f"Merging or creating relationship: {topic_has_learning_statement_relationship}")
    neon.create_or_merge_neontology_relationship(topic_has_learning_statement_relationship, operation='merge')
    logging.pedantic(f"Relationship merged or created: {topic_has_learning_statement_relationship}")
    logging.pedantic(f"Relationships created between {neontology_learning_statement_node} and {neontology_lesson_node} and {neontology_topic_node}")
    
    
