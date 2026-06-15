import sqlite3

conn = sqlite3.connect("college.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS colleges(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    city TEXT,
    course TEXT,
    branch TEXT,
    fees INTEGER,
    avg_package TEXT,
    highest_package TEXT,
    placement TEXT
)
""")

conn.commit()

print("Database Created Successfully!")

conn.close()