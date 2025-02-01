# mapping_db.py

import sqlite3
import os

# The database file will be created in the same directory as this file.
DATABASE_FILE = os.path.join(os.path.dirname(__file__), "mapping.db")

def create_connection():
    """
    Create and return a database connection to the SQLite database.
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except sqlite3.Error as e:
        print(f"[ERROR] mapping_db: {e}")
    return None

def create_table():
    """
    Create the mapping table if it doesn't exist.
    The table stores:
      - reddit_submission_id: the ID of the Reddit submission (or thread)
      - reddit_trigger_comment_id: the ID of the comment that triggered the bridge
      - lemmy_post_id: the ID of the corresponding Lemmy post
      - created_at: timestamp when the mapping was created
    """
    conn = create_connection()
    if conn is not None:
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS mapping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reddit_submission_id TEXT NOT NULL,
            reddit_trigger_comment_id TEXT,
            lemmy_post_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"[ERROR] mapping_db (create_table): {e}")
    else:
        print("[ERROR] mapping_db: Cannot create database connection.")

def insert_mapping(reddit_submission_id, reddit_trigger_comment_id, lemmy_post_id):
    """
    Insert a new mapping record and return the row ID.
    """
    conn = create_connection()
    if conn is None:
        print("[ERROR] mapping_db: No connection available for inserting mapping.")
        return None

    sql = ''' 
        INSERT INTO mapping(reddit_submission_id, reddit_trigger_comment_id, lemmy_post_id)
        VALUES(?,?,?) 
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (reddit_submission_id, reddit_trigger_comment_id, lemmy_post_id))
        conn.commit()
        last_id = cur.lastrowid
        conn.close()
        return last_id
    except sqlite3.Error as e:
        print(f"[ERROR] mapping_db (insert_mapping): {e}")
        conn.close()
        return None

def get_mapping_by_reddit_submission(reddit_submission_id):
    """
    Retrieve mapping records for a given Reddit submission ID.
    """
    conn = create_connection()
    if conn is None:
        return []
    sql = "SELECT * FROM mapping WHERE reddit_submission_id = ?"
    cur = conn.cursor()
    cur.execute(sql, (reddit_submission_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_mappings():
    """
    Retrieve all mapping records.
    """
    conn = create_connection()
    if conn is None:
        return []
    sql = "SELECT * FROM mapping"
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":

    # Create the mapping table if run as a standalone script.
    create_table()
    print(f"Mapping table created or verified in {DATABASE_FILE}")
