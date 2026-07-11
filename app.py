from flask import Flask, render_template, request, redirect, session
from flask import redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "collegecompass123"
@app.context_processor
def inject_session():
    return dict(session=session)

@app.route("/")
def home():

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    # Total Colleges
    cursor.execute("SELECT COUNT(*) FROM colleges")
    total_colleges = cursor.fetchone()[0]

    # Total Scholarships
    cursor.execute("SELECT COUNT(*) FROM scholarships")
    total_scholarships = cursor.fetchone()[0]

    # Total Cities
    cursor.execute("SELECT COUNT(DISTINCT city) FROM colleges")
    total_cities = cursor.fetchone()[0]
        # Top 3 Colleges by ROI
    cursor.execute("""
    SELECT id, name, roi
    FROM colleges
    ORDER BY roi DESC
    LIMIT 3
    """)

    top_colleges = cursor.fetchall()

    conn.close()

    return render_template(
    "index.html",
    total_colleges=total_colleges,
    total_scholarships=total_scholarships,
    total_cities=total_cities,
    top_colleges=top_colleges
)


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
    category = request.form["category"]
    state = request.form["state"]
    budget = int(request.form["budget"])

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM colleges

        WHERE branch=?
        AND fees<=?

    """,(branch,budget))

    colleges = cursor.fetchall()

    conn.close()

    predictions=[]

    for college in colleges:

        if rank <= 20000:

            chance="🟢 Safe"

        elif rank <= 50000:

            chance="🟡 Moderate"

        else:

            chance="🔴 Ambitious"

        predictions.append((college,chance))

    return render_template(

        "predict_result.html",

        predictions=predictions,

        rank=rank,

        category=category,

        state=state

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
@app.route("/placement")
def placement():

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, city, avg_package, highest_package, placement
    FROM colleges
    ORDER BY avg_package DESC
    """)

    colleges = cursor.fetchall()

    conn.close()

    return render_template(
        "placement.html",
        colleges=colleges
    )
@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/add-college")
def add_college():
    return render_template("add_college.html")


@app.route("/save-college", methods=["POST"])
def save_college():

    name = request.form["name"]
    city = request.form["city"]
    course = request.form["course"]
    branch = request.form["branch"]
    fees = int(request.form["fees"])
    avg_package = float(request.form["avg_package"])
    highest_package = request.form["highest_package"]
    placement = request.form["placement"]
    roi = float(request.form["roi"])

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO colleges
        (name, city, course, branch, fees,
         avg_package, highest_package, placement, roi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        city,
        course,
        branch,
        fees,
        avg_package,
        highest_package,
        placement,
        roi
    ))

    conn.commit()
    conn.close()

    return redirect("/admin")
@app.route("/manage-colleges")
def manage_colleges():

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM colleges ORDER BY name")

    colleges = cursor.fetchall()

    conn.close()

    return render_template(
        "manage_colleges.html",
        colleges=colleges
    )
@app.route("/edit-college/<int:college_id>")
def edit_college(college_id):

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM colleges WHERE id=?",
        (college_id,)
    )

    college = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_college.html",
        college=college
    )
@app.route("/update-college/<int:college_id>", methods=["POST"])
def update_college(college_id):

    name = request.form["name"]
    city = request.form["city"]
    course = request.form["course"]
    branch = request.form["branch"]
    fees = int(request.form["fees"])
    avg_package = float(request.form["avg_package"])
    highest_package = request.form["highest_package"]
    placement = request.form["placement"]
    roi = float(request.form["roi"])

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE colleges
        SET
            name=?,
            city=?,
            course=?,
            branch=?,
            fees=?,
            avg_package=?,
            highest_package=?,
            placement=?,
            roi=?
        WHERE id=?
    """, (
        name,
        city,
        course,
        branch,
        fees,
        avg_package,
        highest_package,
        placement,
        roi,
        college_id
    ))

    conn.commit()
    conn.close()

    return redirect("/manage-colleges")
@app.route("/delete-college/<int:college_id>")
def delete_college(college_id):

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM colleges WHERE id=?",
        (college_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/manage-colleges")
@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/save-user", methods=["POST"])
def save_user():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users(name, email, password)
        VALUES (?, ?, ?)
        """, (name, email, password))

        conn.commit()

    except sqlite3.IntegrityError:
        conn.close()
        return "Email already exists!"

    conn.close()

    return redirect("/login")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/login-user", methods=["POST"])
def login_user():

    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE email=? AND password=?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()

    if user:

        session["user_id"] = user[0]
        session["user_name"] = user[1]
        session["user_email"] = user[2]

        return redirect("/profile")

    return "Invalid Email or Password!"
@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM favorites")

    favorite_count = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "profile.html",
        name=session["user_name"],
        email=session["user_email"],
        favorite_count=favorite_count
    )
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")        

if __name__ == "__main__":
    app.run(debug=True)