from flask import Flask, render_template, request

app = Flask(__name__)

colleges = [
    {
        "name": "JECRC Jaipur",
        "course": "BTech",
        "branch": "CSE",
        "fees": 220000
    },
    {
        "name": "LNMIIT Jaipur",
        "course": "BTech",
        "branch": "CSE",
        "fees": 450000
    },
    {
        "name": "SKIT Jaipur",
        "course": "BTech",
        "branch": "IT",
        "fees": 180000
    }
]

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

    result = []

    for college in colleges:

        if (
            college["course"] == course
            and college["branch"] == branch
            and college["fees"] <= budget
        ):
            result.append(college)

    return render_template(
        "results.html",
        colleges=result
    )


if __name__ == "__main__":
    app.run(debug=True)