import sqlite3
import pandas as pd

# ✅ Database location
DB_PATH = "/content/project_files/phonepe_pulse.db"

def connect_db():
    """Create and return a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        print("✅ Database connected successfully!")
        return conn
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None

def run_query(conn, query):
    """Run a SQL query and return results as a pandas DataFrame."""
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print("⚠️ Query execution error:", e)
        return pd.DataFrame()
