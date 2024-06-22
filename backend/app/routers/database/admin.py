from fastapi import APIRouter, Depends, File, UploadFile
from ...dependencies import admin_dependency
from app.modules.driver_tools import send_neo4j_request

router = APIRouter()

def _delete_batch(tx):
    batch_size = 10000
    query = """
    MATCH (n)
    WITH n LIMIT $batch_size
    DETACH DELETE n
    RETURN count(*)
    """
    result = tx.run(query, batch_size=batch_size)
    result_data = result.single()
    if result_data is None:
        return 0
    deleted_count = result_data[0]
    if deleted_count is None:  # This check might be redundant, but kept for clarity
        return 0
    if deleted_count > 0:
        print(f"Deleted {deleted_count} nodes.")
    return deleted_count

@router.post("/create-global-school-db")
async def create_global_school_db():
    query = "CREATE DATABASE `GlobalSchools` IF NOT EXISTS"
    return send_neo4j_request(query)

@router.post("/create-database")
async def create_database(db_name: str):
    query = f"CREATE DATABASE `{db_name}` IF NOT EXISTS"
    return send_neo4j_request(query)

@router.post("/reset-database")
async def reset_database(db_name: str):
    total_deleted = 0
    while True:
        deleted_count = session.write_transaction(_delete_batch)
        total_deleted += deleted_count
        if deleted_count == 0:
            break

def reset_databases(session):
    delete_all_constraints(session)
    reset_all_indexes(session)
    
    



def delete_all_constraints(session):
    constraints_query = "SHOW CONSTRAINTS"
    if constraints_query_result := session.run(constraints_query).data():
        for constraint in constraints_query_result:
            constraint_name = constraint['name']
            drop_query = f"DROP CONSTRAINT {constraint_name}"
            session.run(drop_query)
            print(f"Dropped constraint: {constraint_name}")
    else:
        print("No constraints found to delete.")
        
def reset_all_indexes(session):
    indexes = session.run("SHOW INDEXES").data()
    for index in indexes:
        index_name = index['name']
        session.run(f"DROP INDEX {index_name}")
        print(f"Deleted index: {index_name}")
