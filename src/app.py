from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.book_repository import get_books, create_book
from config import app, test_env
from util import validate_book
from source_service import add_source, get_sources


@app.route("/")
def index():
    return redirect("/sources")


@app.route("/sources")
def sources():
    all_sources = get_sources()  # fetch all sources from the DB
    return render_template("sources.html", sources=all_sources)


@app.route("/sources/new", methods=["GET", "POST"])
def new_source():
    if request.method == "POST":
        key = request.form.get("key")
        ref_type = request.form.get("ref_type")
        author = request.form.get("author")
        title = request.form.get("title")
        year = request.form.get("year")
        journal = request.form.get("journal")
        publisher = request.form.get("publisher")
        create_book(author, title, year)
        return redirect("/sources")

    return render_template("new_reference.html")

@app.route("/sources/edit/<string:source_key>")
def edit_source(source_key):
    key = sources.get_key(source_key)

    return render_template("edit_source.html", key=key)

@app.route("/sources/update", methods=["POST"])
def update_source():
    source_key = request.form["source_key"]
    ref_type = request.form("ref_type")
    author = request.form("author")
    title = request.form("title")
    year = request.form("year")
    journal = request.form("journal")
    publisher = request.form("publisher")

    sources.update_source(source_key, ref_type, author, title, year, journal, publisher)

    return redirect("source/" + str(source_key))


@app.route("/new_todo")
def new():
    return render_template("new_todo.html")


@app.route("/create_todo", methods=["POST"])
def todo_creation():
    content = request.form.get("content")
    try:
        validate_book(content)
        create_book(content)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_todo")


@app.route("/toggle_todo/<todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    return redirect("/")


if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
