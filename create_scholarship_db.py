import sqlite3

conn = sqlite3.connect("college.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scholarships(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    eligibility TEXT,
    benefit TEXT,
    last_date TEXT
)
""")

conn.commit()

print("Scholarship Table Created!")

conn.close()