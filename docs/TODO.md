# TODO List for Neo4j Database Creation Tools Development

## General Database Tools

- [ ] **Setup Project Structure for Neo4j Tools**
  - [X] Initialize project directories and files.
  - [ ] Set up version control branches.
- [ ] **Develop Database Connection Utilities**
  - [ ] Implement function to connect to Neo4j database.

    ```python
    neo4j_driver = driver.get_neo4j_driver()
    neon.init_neo4j_connection()
    ```
    *Reference: backend/app/modules/database/cc_init_db_curriculum.ipynb*
    ```python

    neo4j_driver = driver.get_neo4j_driver()
    neon.init_neo4j_connection()
    ```
  - [ ] Create utility functions for database operations (create, read, update, delete).

### Schema-Specific Tools
- [ ] **Node Creation Tools**
  - [ ] Develop functions to create and merge nodes for different types:
    - Schools
    - Departments
    - Key Stages
    - Subjects
    ```python
    for school in schools:
        neon.create_or_merge_neontology_node(school, operation='create')
    for department in departments:
        neon.create_or_merge_neontology_node(department, operation='create')
    for key_stage in key_stages:
        neon.create_or_merge_neontology_node(key_stage, operation='create')
    for subject in subjects:
        neon.create_or_merge_neontology_node(subject, operation='create')
    ```
    *Reference: backend/app/modules/database/cc_init_db_curriculum.ipynb*
    ```python
    for school in schools:
        neon.create_or_merge_neontology_node(school, operation='create')
    for department in departments:
        neon.create_or_merge_neontology_node(department, operation='create')
    for key_stage in key_stages:
        neon.create_or_merge_neontology_node(key_stage, operation='create')
    for subject in subjects:
        neon.create_or_merge_neontology
```

```markdown
_node(subject, operation='create')
    ```

### Spreadsheet Import Functionality
- [ ] **Develop Spreadsheet Parsing Tools**
  - [ ] Implement functions to read and parse Excel files for different data types:
    - Topics
    - Lessons
    - Learning Statements
    ```python
    planner = planner.get_excel_sheets('planner.xlsx ')
    topic_df = planner['topiclookup_df']
    lesson_df = planner['lessonlookup_df']
    statement_df = planner['statementlookup_df']
    ```
    *Reference: backend/app/modules/database/cc_init_db_curriculum.ipynb*
    ```python
    planner = planner.get_excel_sheets('planner.xlsx ')
    topic_df = planner['topiclookup_df']
    lesson_df = planner['lessonlookup_df']
    statement_df = planner['statementlookup_df']
    ```
  - [ ] Map spreadsheet data to database schema and create nodes.
    ```python
    for node_data in topic_excel_node_list:
        neon.create_or_merge_neontology_node(node_data['node'], operation='merge')
    for node_data in topic_lesson_excel_node_list:
        neon.create_or_merge_neontology_node(node_data['node'], operation='create')
    for node_data in learning_statement_excel_node_list:
        neon.create_or_merge_neontology_node(node_data['node'], operation='create')
    ```
    *Reference: backend/app/modules/database/cc_init_db_curriculum.ipynb*
    ```python
    for node_data in topic_excel_node_list:
        neon.create_or_merge_neontology_node(node_data['node'], operation='merge')
    for node_data in topic_lesson_excel_node_list:
        neon.create_or_merge_neontology_node(node_data['node'], operation='create')
    for node_data in learning_statement_excel_node_list:
        neon.create_or_merge_neontology_node(node_data['node'], operation='create')
    ```

### Integration and Testing
- [ ] **Write Integration Tests**
  - [ ] Ensure that all database tools work together seamlessly.
  - [ ] Validate data integrity and consistency after operations.

### Documentation
- [ ] **Document the Development Process and Tools**
  - [ ] Write comprehensive README files.
  - [ ] Provide examples and usage guidelines for future developers.
```

This updated TODO list now includes the actual code snippets directly referenced from the provided code blocks, ensuring clarity and ease of access to the relevant code for each task.