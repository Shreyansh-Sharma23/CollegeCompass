import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM colleges")

rows = cursor.fetchall()

print("Total Colleges:", len(rows))

for row in rows:
    print(row)

conn.close()