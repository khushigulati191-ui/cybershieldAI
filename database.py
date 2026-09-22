import sqlite3
from datetime import datetime
import uuid

DATABASE_NAME = "cybershield.db"


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """
    Create the analyses table if it does not already exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id UUID NOT NULL,
            target TEXT NOT NULL,
            target_type TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_analysis(
    target,
    target_type
):
    """
    Save one analysis result into the database.
    """

    conn = get_connection()
    cursor = conn.cursor()
    import uuid

    visitor_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO analyses (
            visitor_id,
            target,
            target_type,
            timestamp
        )
        VALUES (?, ?, ?, ?)
    """, (
        visitor_id,
        target,
        target_type,
        timestamp
    ))

    conn.commit()

    analysis_id = cursor.lastrowid
    conn.close()
    return analysis_id

def get_all_analyses():
    """
    Return all previous analyses.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM analyses
        ORDER BY timestamp DESC
    """)

    results = cursor.fetchall()

    conn.close()

    return results


def get_analysis_by_id(analysis_id):
    """
    Return a specific analysis using its ID.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM analyses
        WHERE id = ?
    """, (analysis_id,))

    result = cursor.fetchone()

    conn.close()

    return result


get_connection()
init_database()