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