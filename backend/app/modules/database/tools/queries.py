def create_database(db_name):
        return f"CREATE DATABASE `{db_name}` IF NOT EXISTS"
        
        
def delete_database(db_name):
        f":USE system"
        f"STOP DATABASE {db_name}"
        f"DROP DATABASE {db_name}"

show_constraints = "SHOW CONSTRAINTS"

show_indexes = "SHOW INDEXES"

def drop_index(index_name):
        f"DROP INDEX {index_name}"

def drop_constraint(constraint_name):
        f"DROP CONSTRAINT {constraint_name}"

delete_batch = """
        MATCH (n)
        WITH n LIMIT $batch_size
        DETACH DELETE n
        RETURN count(*)
        """