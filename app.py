from flask import Flask, render_template, request
from flask import redirect
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

    city = request.form["city"]
    sort = request.form["sort"]

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM colleges
    WHERE course = ?
    AND branch = ?
    AND fees <= ?
    """

    params = [course, branch, budget]

    if city != "":
        query += " AND city = ?"
        params.append(city)

    if sort == "roi":
        query += " ORDER BY roi DESC"

    elif sort == "fees":
        query += " ORDER BY fees ASC"

    elif sort == "package":
        query += " ORDER BY avg_package DESC"

    elif sort == "placement":
        query += " ORDER BY placement DESC"

    cursor.execute(query, params)

    colleges = cursor.fetchall()

    if city == "":
        cursor.execute("""
        SELECT id, name
        FROM colleges
        WHERE course = ?
        AND branch = ?
        """, (course, branch))

    else:
        cursor.execute("""
        SELECT id, name
        FROM colleges
        WHERE course = ?
        AND branch = ?
        AND city = ?
        """, (course, branch, city))

    college_names = cursor.fetchall()

    conn.close()

    return render_template(
        "results.html",
        colleges=colleges,
        college_names=college_names,
        course=course,
        branch=branch,
        city=city,
        budget=budget,
        sort=sort
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

    print("College ID:", college_id)
    print("College Data:", college)

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
@app.route("/predictor")
def predictor():
    return render_template("predictor.html")
@app.route("/predict-result", methods=["POST"])
def predict_result():

    rank = int(request.form["rank"])
    branch = request.form["branch"]

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM cutoffs WHERE branch=?",
        (branch,)
    )

    colleges = cursor.fetchall()

    conn.close()

    results = []

    for college in colleges:

        if rank <= college[5]:
            status = "🔴 Ambitious"

        elif rank <= college[4]:
            status = "🟡 Moderate"

        elif rank <= college[3]:
            status = "🟢 Safe"

        else:
            status = "❌ Low Chance"

        results.append(
            (college[1], status)
        )

    return render_template(
        "predict_result.html",
        results=results
    )
@app.route("/fit-score")
def fit_score():
    return render_template("fit_score.html")
@app.route("/fit-score-result", methods=["POST"])
def fit_score_result():

    rank = int(request.form["rank"])
    budget = int(request.form["budget"])
    branch = request.form["branch"]

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM colleges
        WHERE branch=?
    """,(branch,))

    colleges = cursor.fetchall()

    conn.close()

    scores=[]

    for college in colleges:

        score = 0

        # Budget
        if budget >= college[5]:
            score += 30

        # Placement
        placement = int(college[8].replace("%",""))

        if placement >= 90:
            score += 30

        elif placement >= 80:
            score += 20

        # ROI

        if college[9] >= 3:
            score += 25

        elif college[9] >=2:
            score +=20

        else:
            score +=10

        # Rank

        if rank <=50000:
            score +=15

        elif rank<=100000:
            score+=10

        else:
            score+=5

        scores.append((college,score))

    scores.sort(
        key=lambda x:x[1],
        reverse=True
    )

    return render_template(
        "fit_score_result.html",
        scores=scores
    )
@app.route("/favorite/<int:college_id>")
def favorite(college_id):

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO favorites(college_id) VALUES(?)",
        (college_id,)
    )

    conn.commit()
    conn.close()
@app.route("/favorites")
def favorites():

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT colleges.*
    FROM favorites
    JOIN colleges
    ON favorites.college_id = colleges.id
    """)

    colleges = cursor.fetchall()

    conn.close()

    return render_template(
        "favorites.html",
        colleges=colleges
    )
    return redirect("/favorites")
if __name__ == "__main__":
    app.run(debug=True)