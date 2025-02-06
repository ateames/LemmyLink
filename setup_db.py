# This script sets up the database by creating the necessary tables.

from LemmyLink.mapping_db import create_table as create_mapping_table, DATABASE_FILE
from LemmyLink.comment_mapping_db import create_comment_table

def setup_database():
    # Create the mapping table (for post mappings)
    create_mapping_table()
    print(f"Mapping table created or verified in {DATABASE_FILE}")

    # Create the comment mapping table (for comment mappings)
    create_comment_table()
    print("Comment mapping table created or verified.")

if __name__ == "__main__":
    setup_database()
