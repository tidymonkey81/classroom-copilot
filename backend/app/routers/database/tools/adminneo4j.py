

# Function to delete nodes in Neo4j based on given criteria
def delete_nodes(session, criteria, delete_related=False):
    """
    Function to delete nodes in Neo4j based on given criteria.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        criteria (dict): A dictionary containing the properties to match for deletion.
        delete_related (bool): If True, deletes related nodes and relationships; otherwise, deletes only the matched nodes.

    Example usage:
        # Delete only the nodes matching the criteria
        delete_nodes(neo4j_driver, {'TopicID': 'AP.PAG10'})

        # Delete the nodes and their related relationships
        delete_nodes(neo4j_driver, {'TopicID': 'AP.PAG10'}, delete_related=True)
    """
    session.write_transaction(_delete_nodes, criteria, delete_related)

def _delete_nodes(tx, criteria, delete_related=False):
    """
    Internal function to execute a Cypher query to delete nodes based on criteria.

    Args:
        tx (neo4j.Transaction): The Neo4j transaction.
        criteria (dict): A dictionary containing the properties to match for deletion.
        delete_related (bool): Specifies whether to delete related nodes and relationships.
    """
    condition_str = " AND ".join([f"n.{key} = ${key}" for key in criteria])
    if delete_related:
        query = f"""
        MATCH (n)-[r]-()
        WHERE {condition_str}
        DELETE n, r
        """
    else:
        query = f"""
        MATCH (n)
        WHERE {condition_str}
        DELETE n
        """
    # logging.query(f"Running query: {query}")
    tx.run(query, **criteria)

# Function to delete all nodes and relationships in the Neo4j database in batches
def delete_lots_of_nodes_and_relationships(session):
    """
    Function to delete all nodes and relationships in the Neo4j database in batches.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        session (str): The Neo4j session.
    """
    total_deleted = 0
    while True:
        deleted_count = session.write_transaction(_delete_batch)
        total_deleted += deleted_count
        if deleted_count == 0:
            break  # Exit the loop if no more nodes are deleted
    # logging.prod(f"All nodes and relationships have been deleted. Total deleted: {total_deleted}")
    print(f"All nodes and relationships have been deleted. Total deleted: {total_deleted}")

def _delete_batch(tx):
    """
    Function to execute a Cypher query to delete a batch of nodes and relationships.

    Args:
        tx (neo4j.Transaction): The Neo4j transaction.
    """
    batch_size = 10000  # Adjust the batch size according to your needs
    query = """
    MATCH (n)
    WITH n LIMIT $batch_size
    DETACH DELETE n
    RETURN count(*)
    """
    # logging.query(f"Running query: {query}")
    result = tx.run(query, batch_size=batch_size)
    result_data = result.single()
    
    if result_data is None:
        return 0
    deleted_count = result_data[0]
    if deleted_count is None:  # This check might be redundant, but kept for clarity
        return 0
    if deleted_count > 0:
        # logging.database(f"Deleted {deleted_count} nodes.")
        print(f"Deleted {deleted_count} nodes.")
    return deleted_count

def delete_all_constraints(session):
    # Correct command to fetch all constraints for Neo4j 4.x and later
    constraints_query = "SHOW CONSTRAINTS"
    # logging.query(f"Running query: {constraints_query}")
    if constraints_query_result := session.run(constraints_query).data():
        for constraint in constraints_query_result:
            # Ensure correct key is used to extract constraint name
            constraint_name = constraint['name']  # Adjust this if necessary
            drop_query = f"DROP CONSTRAINT {constraint_name}"
            # logging.query(f"Running query: {drop_query}")
            session.run(drop_query)
            # logging.database(f"Dropped constraint: {constraint_name}")
            print(f"Dropped constraint: {constraint_name}")
    else:
        # logging.warning("No constraints found to delete.")
        print("No constraints found to delete.")
        
def reset_all_indexes(session):
    indexes = session.run("SHOW INDEXES").data()
    for index in indexes:
        index_name = index['name']
        session.run(f"DROP INDEX {index_name}")
        # logging.info(f"Deleted index: {index_name}")
        print(f"Deleted index: {index_name}")

def reset_database(session):
    delete_lots_of_nodes_and_relationships(session)
    delete_all_constraints(session)
    reset_all_indexes(session)

def create_database(session, db_name):
    """
    Creates a new database in Neo4j if it does not already exist.

    Args:
        session (neo4j.Session): The Neo4j session.
        db_name (str): The name of the database to create.
    """
    query = f"CREATE DATABASE `{db_name}` IF NOT EXISTS"
    try:
        session.run(query)
        print(f"Database {db_name} created successfully.")
    except Exception as e:
        print(f"Failed to create database {db_name}: {str(e)}")