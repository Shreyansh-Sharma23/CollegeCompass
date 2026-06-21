from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/colleges")
def college_page():
    return render_template("colleges.html")


@app.route("/search", methods=["POST"])
def search():

    course = request.form["course"]
    branch = request.form["branch"]
    budget = int(request.form["budget"])

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM colleges
    WHERE course = ?
    AND branch = ?
    AND fees <= ?
    """, (course, branch, budget))

    colleges = cursor.fetchall()

    conn.close()

    return render_template(
        "results.html",
        colleges=colleges
    )


@app.route("/college/<int:college_id>")
def college_profile(college_id):

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM colleges WHERE id = ?",
        (college_id,)
    )

    college = cursor.fetchone()

    conn.close()

    return render_template(
        "college_profile.html",
        college=college
    )
@app.route("/compare")
def compare():

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM colleges")

    colleges = cursor.fetchall()

    conn.close()

    return render_template(
        "compare.html",
        colleges=colleges
    )
@app.route("/compare-result", methods=["POST"])
def compare_result():

    college1_id = request.form["college1"]
    college2_id = request.form["college2"]

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM colleges WHERE id=?",
        (college1_id,)
    )

    college1 = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM colleges WHERE id=?",
        (college2_id,)
    )

    college2 = cursor.fetchone()

    conn.close()

    return render_template(
        "compare_result.html",
        college1=college1,
        college2=college2
    )
@app.route("/scholarships")
def scholarships():

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scholarships")

    scholarships = cursor.fetchall()

    conn.close()

    return render_template(
        "scholarships.html",
        scholarships=scholarships
    )

@app.route("/scholarship-result", methods=["POST"])
def scholarship_result():

    boards = int(request.form["boards"])
    jee = int(request.form["jee"])
    cuet = int(request.form["cuet"])

    eligible = []

    if boards >= 90:
        eligible.append(
            ("Merit Scholarship", "50% Fee Waiver")
        )

    if jee >= 95:
        eligible.append(
            ("JEE Excellence Scholarship", "₹1,00,000")
        )

    if cuet >= 85:
        eligible.append(
            ("CUET Merit Scholarship", "₹50,000")
        )

    return render_template(
        "scholarship_result.html",
        scholarships=eligible
    )
if __name__ == "__main__":
    app.run(debug=True)