import sqlite3

conn = sqlite3.connect("college.db")

cursor = conn.cursor()

colleges = [

("JECRC Jaipur","Jaipur","BTech","CSE",220000,"6.5 LPA","44 LPA","88%"),

("LNMIIT Jaipur","Jaipur","BTech","CSE",450000,"14 LPA","85 LPA","97%"),

("SKIT Jaipur","Jaipur","BTech","IT",180000,"5.2 LPA","18 LPA","82%"),

("Graphic Era","Dehradun","BTech","CSE",320000,"8 LPA","51 LPA","90%"),

("UPES","Dehradun","BTech","CSE",450000,"8.6 LPA","50 LPA","92%")

]

cursor.executemany("""
INSERT INTO colleges
(name,city,course,branch,fees,avg_package,highest_package,placement)

VALUES(?,?,?,?,?,?,?,?)
""", colleges)

conn.commit()

print("Data Inserted!")

conn.close()