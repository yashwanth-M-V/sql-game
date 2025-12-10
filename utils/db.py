import sqlite3
import pandas as pd

DB_PATH = "databases/supermarket.db"


# -----------------------------------
#  CONNECTION HANDLING
# -----------------------------------
def get_connection():
    """Create and return a new SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # allows column name access
    return conn


# -----------------------------------
#  QUERY EXECUTION FUNCTIONS
# -----------------------------------
def run_user_query(sql: str) -> pd.DataFrame:
    """
    Execute a user's SQL query and return a DataFrame.
    Errors will be displayed in Streamlit.
    """
    conn = get_connection()
    try:
        df = pd.read_sql_query(sql, conn)
        return df
    finally:
        conn.close()


def run_correct_query(sql: str) -> pd.DataFrame:
    """
    Execute the golden/correct SQL query from JSON.
    """
    conn = get_connection()
    try:
        df = pd.read_sql_query(sql, conn)
        return df
    finally:
        conn.close()


# -----------------------------------
#  TABLE DISCOVERY FUNCTIONS
# -----------------------------------
def get_all_tables() -> list:
    """
    Returns a list of all tables in the supermarket database.
    """
    conn = get_connection()
    try:
        tables_df = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;", conn
        )
        return tables_df["name"].tolist()
    finally:
        conn.close()


# -----------------------------------
#  TABLE PREVIEW
# -----------------------------------
def get_table_preview(table_name: str, limit: int = 5) -> pd.DataFrame:
    """
    Returns a preview of the specified table.
    """
    conn = get_connection()
    try:
        query = f"SELECT * FROM {table_name} LIMIT {limit};"
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()


# -----------------------------------
#  GET TABLE SCHEMA / COLUMN NAMES
# -----------------------------------
def get_table_schema(table_name: str) -> pd.DataFrame:
    """
    Returns schema information (column names & types) for a given table.
    """
    conn = get_connection()
    try:
        schema_df = pd.read_sql_query(f"PRAGMA table_info({table_name});", conn)
        return schema_df
    finally:
        conn.close()


# -----------------------------------
#  UTILITY: SAFELY VALIDATE SELECTION
# -----------------------------------
def table_exists(table_name: str) -> bool:
    """Check whether a given table exists in the DB."""
    tables = get_all_tables()
    return table_name in tables
