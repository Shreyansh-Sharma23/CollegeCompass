import sqlite3

conn = sqlite3.connect("college.db")

cursor = conn.cursor()

colleges = [

("JECRC Jaipur","Jaipur","BTech","CSE",220000,6.5,"44 LPA","88%",2.95),

("LNMIIT Jaipur","Jaipur","BTech","CSE",450000,14.0,"85 LPA","97%",3.11),

("Graphic Era","Dehradun","BTech","CSE",320000,8.0,"51 LPA","90%",2.50),

("UPES","Dehradun","BTech","CSE",450000,8.6,"50 LPA","92%",1.91),

("SKIT Jaipur","Jaipur","BTech","IT",180000,5.2,"18 LPA","82%",2.89),

("Poornima University","Jaipur","BTech","CSE",210000,4.8,"15 LPA","80%",2.29),

("Manipal University Jaipur","Jaipur","BTech","CSE",430000,8.5,"54 LPA","93%",1.98),

("Bennett University","Greater Noida","BTech","CSE",500000,7.5,"44 LPA","89%",1.50),

("SRM University","Chennai","BTech","CSE",400000,7.8,"57 LPA","91%",1.95),

("VIT Vellore","Vellore","BTech","CSE",350000,9.2,"88 LPA","94%",2.63),

("Chandigarh University","Mohali","BTech","CSE",250000,6.8,"54 LPA","90%",2.72),

("Amity University","Noida","BTech","CSE",450000,6.5,"61 LPA","88%",1.44),

("Lovely Professional University","Jalandhar","BTech","CSE",300000,7.0,"64 LPA","92%",2.33),

("Jaypee Noida","Noida","BTech","CSE",350000,8.2,"58 LPA","91%",2.34),

("Thapar Institute","Patiala","BTech","CSE",480000,11.0,"55 LPA","95%",2.29)

]

cursor.executemany("""
INSERT INTO colleges
(name,city,course,branch,fees,avg_package,highest_package,placement,roi)

VALUES(?,?,?,?,?,?,?,?,?)
""", colleges)

conn.commit()

print("Data Inserted!")

conn.close()