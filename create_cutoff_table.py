import sqlite3

conn = sqlite3.connect("college.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cutoffs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    college_name TEXT,
    branch TEXT,
    safe_rank INTEGER,
    moderate_rank INTEGER,
    ambitious_rank INTEGER
)
""")

conn.commit()

print("Cutoff Table Created!")

conn.close()