#!/usr/bin/env python3
import os
from mapping_db import DATABASE_FILE, create_table as create_mapping_table
from comment_mapping_db import create_comment_table

def reset_database():
    # Check if the database file exists and remove it.
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)
        print(f"Removed database file: {DATABASE_FILE}")
    else:
        print(f"Database file {DATABASE_FILE} does not exist. Nothing to remove.")

    # Recreate the tables by calling the table creation functions.
    create_mapping_table()
    create_comment_table()
    print("Database reset complete.")

if __name__ == "__main__":
    reset_database()
