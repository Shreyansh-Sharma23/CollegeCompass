import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

scholarships = [

("Merit Scholarship", "90% Boards", "50% Fee Waiver", "31 Dec 2026"),

("JEE Excellence Scholarship", "95 Percentile JEE", "₹1,00,000", "15 Jan 2027"),

("CUET Merit Scholarship", "85 Percentile CUET", "₹50,000", "10 Feb 2027"),

("Academic Excellence Award", "98% Boards", "100% Tuition Fee", "20 Dec 2026")

]

cursor.executemany("""
INSERT INTO scholarships
(name, eligibility, benefit, last_date)
VALUES (?, ?, ?, ?)
""", scholarships)

conn.commit()

print("Scholarships Added!")

conn.close()