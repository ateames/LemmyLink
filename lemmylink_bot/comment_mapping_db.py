# comment_mapping_db.py

import sqlite3
import os

DATABASE_FILE = os.path.join(os.path.dirname(__file__), "mapping.db")

def create_comment_table():
    """
    Create the comment mapping table if it doesn't exist.
    This table stores:
      - reddit_comment_id: ID of the Reddit comment.
      - lemmy_comment_id: ID of the corresponding Lemmy comment.
      - created_at: Timestamp when the mapping was created.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    sql = """
    CREATE TABLE IF NOT EXISTS comment_mapping (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reddit_comment_id TEXT NOT NULL,
        lemmy_comment_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn.execute(sql)
    conn.commit()
    conn.close()

def insert_comment_mapping(reddit_comment_id, lemmy_comment_id):
    """
    Insert a new comment mapping record.
    Returns the new row ID.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    sql = """
    INSERT INTO comment_mapping (reddit_comment_id, lemmy_comment_id)
    VALUES (?, ?)
    """
    cur = conn.cursor()
    cur.execute(sql, (reddit_comment_id, lemmy_comment_id))
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id

def get_comment_mapping_by_reddit_comment(reddit_comment_id):
    """
    Retrieve a mapping record by Reddit comment ID.
    Returns the record (or None if not found).
    """
    conn = sqlite3.connect(DATABASE_FILE)
    sql = "SELECT * FROM comment_mapping WHERE reddit_comment_id = ?"
    cur = conn.cursor()
    cur.execute(sql, (reddit_comment_id,))
    row = cur.fetchone()
    conn.close()
    return row

def get_comment_mapping_by_lemmy_comment(lemmy_comment_id):
    """
    Retrieve a mapping record by Lemmy comment ID.
    Returns the record (or None if not found).
    """
    conn = sqlite3.connect(DATABASE_FILE)
    sql = "SELECT * FROM comment_mapping WHERE lemmy_comment_id = ?"
    cur = conn.cursor()
    cur.execute(sql, (lemmy_comment_id,))
    row = cur.fetchone()
    conn.close()
    return row

if __name__ == "__main__":
    create_comment_table()
    print(f"Comment mapping table created or verified in {DATABASE_FILE}")
