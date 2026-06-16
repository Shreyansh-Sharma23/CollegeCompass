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


if __name__ == "__main__":
    app.run(debug=True)