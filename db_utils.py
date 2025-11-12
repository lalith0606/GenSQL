# db_utils.py
from sqlalchemy import create_engine, inspect, text
import sqlite3, re
from typing import List, Dict, Any

def get_engine(db_url: str = "sqlite:///sample.db"):
    return create_engine(db_url, connect_args={"check_same_thread": False})

# ----- DATABASE CREATION -----
def ensure_sample_db():
    """Create customer/order demo tables if not exist."""
    conn = sqlite3.connect("sample.db")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY,
        name TEXT,
        country TEXT,
        signup_date TEXT
    );
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        amount REAL,
        order_date TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    );
    """)
    conn.commit()
    conn.close()

def ensure_hospital_db():
    """Create hospital-related tables for testing."""
    conn = sqlite3.connect("sample.db")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        disease TEXT,
        admitted_date TEXT
    );
    CREATE TABLE IF NOT EXISTS doctor(
        id INTEGER PRIMARY KEY,
        name TEXT,
        specialization TEXT,
        experience_years INTEGER
    );
    """)
    conn.commit()
    conn.close()

# ----- SCHEMA + VALIDATION -----
def get_schema_snippet(db_url: str = "sqlite:///sample.db") -> str:
    """Return compact schema info for Gemini prompt."""
    engine = get_engine(db_url)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    parts = []
    for t in tables:
        cols = inspector.get_columns(t)
        col_names = ", ".join([c['name'] for c in cols])
        parts.append(f"{t}({col_names})")
    return " | ".join(parts) if parts else "No tables found."

def is_safe_select(sql: str) -> bool:
    """
    Allow plain SELECTs only.
    Reject anything that has INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
    TRUNCATE, EXEC, or multiple statements.
    """
    s = sql.strip().lower()
    if s.endswith(";"):
        s = s[:-1].strip()
    if ";" in s:
        return False
    if not s.startswith("select"):
        return False
    forbidden = re.compile(r"\b(insert|update|delete|drop|alter|create|truncate|exec)\b")
    return not bool(forbidden.search(s))

def run_select(db_url: str, sql: str) -> List[Dict[str, Any]]:
    """Execute safe SELECT queries."""
    engine = get_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        return [dict(r) for r in result.fetchall()]
