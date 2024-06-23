from contextlib import suppress
import query_library as query

def delete_all_nodes_and_relationships(session):
    total_deleted = 0
    while True:
        deleted_count = session.write_transaction(_delete_batch)
        total_deleted += deleted_count
        if deleted_count == 0:
            break

def _delete_batch(tx):
    result_data = tx.run(query.delete_batch, batch_size=10000).single()
    return 0 if result_data is None else result_data[0]

def delete_all_constraints(session):
    if show_constraints_result := session.run(query.show_constraints).data():
        for constraint in show_constraints_result:
            constraint_name = constraint['name']
            session.run(query.drop_constraint(constraint_name))
        
def reset_all_indexes(session):
    indexes = session.run(query.show_indexes).data()
    for index in indexes:
        index_name = index['name']
        session.run(query.drop_index(index_name))
        
def reset_databases(session):
    delete_all_nodes_and_relationships(session)
    delete_all_constraints(session)
    reset_all_indexes(session)
    
def close_session(session):
    if session:
        with suppress(Exception):
            session.close()

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
    tx.run(query, **criteria)