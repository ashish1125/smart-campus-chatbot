import sqlite3
import random
import string

# -----------------------------------
# Connect Database
# -----------------------------------
def connect_db():
    return sqlite3.connect("campus.db")


# -----------------------------------
# Generate Unique Institute Code
# -----------------------------------
def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


# -----------------------------------
# Create Tables
# -----------------------------------
def create_tables():

    conn = connect_db()
    cur = conn.cursor()

    # Institutes Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS institutes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        institute_name TEXT,
        institute_type TEXT,
        username TEXT UNIQUE,
        password TEXT,
        institute_code TEXT UNIQUE,
        logo_path TEXT,
        address TEXT,
        email TEXT,
        phone TEXT,
        instagram TEXT,
        facebook TEXT,
        website TEXT,
        description TEXT
    )
    """)

    # Students Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        username TEXT UNIQUE,
        password TEXT,
        institute_code TEXT
    )
    """)

    # Documents Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        filename TEXT,
        content TEXT
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------------
# Run Automatically
# -----------------------------------
create_tables()
print("Database Ready Successfully")