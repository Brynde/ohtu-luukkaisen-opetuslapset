from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.book_repository import get_books, create_book, get_info, edit_book
from config import app, test_env
from util import validate_book



@app.route("/")
def index():
    all_sources = get_books()  # fetch all sources from the DB
    return render_template("index.html", sources=all_sources)


@app.route("/sources")
def sources():
    return redirect("/")


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
        
        try:
            validate_book(key, ref_type, author, title, year, journal, publisher)
            create_book(key, ref_type, author, title, year, journal, publisher)
            return redirect("/")
        except Exception as error:
            flash(str(error))
            print(key, ref_type, author, title, year, journal, publisher)
            return render_template("new_reference.html")
        
    return render_template("new_reference.html")

@app.route("/sources/edit/<string:source_key>")
def edit_source(source_key):
    source = get_info(source_key)
    return render_template("edit_reference.html", key=source_key, source=source)

@app.route("/sources/update_item", methods=["POST"])
def update_source():
    source_key = request.form.get("key")
    ref_type = request.form.get("ref_type")
    author = request.form.get("author")
    title = request.form.get("title")
    year = request.form.get("year")
    journal = request.form.get("journal")
    publisher = request.form.get("publisher")
    edit_book(source_key, [source_key, ref_type, author, title, year, journal, publisher])
    return redirect("/")

@app.route("/")
def delete_source():
    return redirect("/")

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
