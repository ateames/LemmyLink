# DELETES ALL DATA! Delete and recreate both databases
import os
# from mapping_db import DATABASE_FILE, create_table as create_mapping_table
from comment_mapping_db import create_comment_table
from mapping_db import create_table as create_mapping_table, DATABASE_FILE

def reset_database():
    confirmation = input("This will delete all database data. Confirm by typing [Y] to continue or [N] to cancel: ")
    if confirmation.lower() != "y":
        print("Cancelled. No changes made.")
        return
    
    # Check if the database file exists and remove it.
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)
        print(f"Removed database file: {DATABASE_FILE}")
    else:
        print(f"Database file {DATABASE_FILE} does not exist. Nothing to remove.")

    # Recreate the tables by calling the table creation functions.
def setup_database():
    # Create the mapping table (for post mappings)
    create_mapping_table()
    print(f"Mapping table created or verified in {DATABASE_FILE}")

    # Create the comment mapping table (for comment mappings)
    create_comment_table()
    print("Comment mapping table created or verified.")

if __name__ == "__main__":
    reset_database()
