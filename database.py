import sqlite3
import random
import string

def connect_db():
    return sqlite3.connect("campus.db")

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS schools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        school_name TEXT,
        username TEXT UNIQUE,
        password TEXT,
        school_code TEXT UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        username TEXT UNIQUE,
        password TEXT,
        school_code TEXT
    )
    """)

    conn.commit()
    conn.close()

create_tables()
print("Database Ready")