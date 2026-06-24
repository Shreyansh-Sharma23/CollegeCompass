import sqlite3

conn = sqlite3.connect("college.db")

cursor = conn.cursor()

cutoffs = [

("JECRC Jaipur", "CSE", 120000, 90000, 70000),

("LNMIIT Jaipur", "CSE", 50000, 35000, 25000),

("Graphic Era", "CSE", 100000, 80000, 60000),

("UPES", "CSE", 90000, 70000, 50000),

("VIT Vellore", "CSE", 40000, 30000, 20000)

]

cursor.executemany("""
INSERT INTO cutoffs
(college_name, branch, safe_rank, moderate_rank, ambitious_rank)
VALUES (?, ?, ?, ?, ?)
""", cutoffs)

conn.commit()

print("Cutoff Data Added!")

conn.close()