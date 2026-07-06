from flask import Flask, render_template, request, session
import pandas as pd

app = Flask(__name__)
app.secret_key = "movieproject"

# Read movie data
movies = pd.read_csv("movies.csv")

@app.route("/")
def home():
    return render_template("name.html")

@app.route("/language", methods=["POST"])
def language():
    session["name"] = request.form["name"]
    return render_template("language.html")

@app.route("/genre", methods=["POST"])
def genre():
    session["language"] = request.form["language"]
    return render_template("genre.html")

@app.route("/rating", methods=["POST"])
def rating():
    session["genre"] = request.form["genre"]
    return render_template("rating.html")

@app.route("/result", methods=["POST"])
def result():
    session["rating"] = float(request.form["rating"])

    language = session["language"]
    genre = session["genre"]
    rating = session["rating"]

    filtered = movies[
        (movies["Language"] == language) &
        (movies["Genre"] == genre) &
        (movies["Rating"] >= rating)
    ]

    movie_list = filtered["Movie"].tolist()

    if len(movie_list) == 0:
        return render_template(
            "result.html",
            name=session["name"],
            movies=[],
            message="Sorry! No movies found. Please try again."
        )

    return render_template(
        "result.html",
        name=session["name"],
        movies=movie_list,
        message=""
    )

if __name__ == "__main__":
    app.run(debug=True)