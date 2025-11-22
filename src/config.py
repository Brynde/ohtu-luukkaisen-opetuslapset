from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import getenv

load_dotenv()

test_env = getenv("TEST_ENV") == "true"
print(f"Test environment: {test_env}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///local.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

#Väliaikainen robot-testejä varten
sources = []


@app.route("/")
def index():
    return render_template("index.html", sources=sources)


@app.route("/sources/new", methods=["GET", "POST"])
def new_reference():
    if request.method == "POST":
        key = request.form.get("key", "").strip()
        ref_type = request.form.get("ref_type", "").strip()
        author = request.form.get("author", "").strip()
        title = request.form.get("title", "").strip()
        year = request.form.get("year", "").strip()
        journal = request.form.get("journal", "").strip()
        publisher = request.form.get("publisher", "").strip()

        if not key or not author or not title or not year:
            return render_template("new_reference.html")

        sources.append(
            {
                "key": key,
                "ref_type": ref_type,
                "author": author,
                "title": title,
                "year": year,
                "journal": journal,
                "publisher": publisher,
            }
        )
        return redirect(url_for("index"))

    return render_template("new_reference.html")


@app.route("/reset_db")
def reset_db():
    sources.clear()
    return redirect(url_for("index"))


@app.route("/sources/<string:source_key>/edit")
def edit_source(source_key):
    return redirect(url_for("index"))


@app.route("/sources/<string:source_key>/delete", methods=["POST"])
def delete_source(source_key):
    global sources
    sources = [s for s in sources if s["key"] != source_key]
    return redirect(url_for("index"))
