from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from config import app, test_env
from util import validate_todo


@app.route("/")
def index():
    return redirect("/sources")


@app.route("/sources")
def sources():
    return render_template("sources.html")


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
        return redirect("/sources")

    return render_template("new_reference.html")


@app.route("/new_todo")
def new():
    return render_template("new_todo.html")


@app.route("/create_todo", methods=["POST"])
def todo_creation():
    content = request.form.get("content")
    try:
        validate_todo(content)
        create_todo(content)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_todo")


@app.route("/toggle_todo/<todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    set_done(todo_id)
    return redirect("/")


if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
