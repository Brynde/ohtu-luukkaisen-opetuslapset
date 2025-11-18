from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.book_repository import get_books, create_book
from config import app, test_env
from util import validate_book

@app.route("/")
def index():
    books = get_books()
    return render_template("index.html", books=books) 

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
        return  redirect("/new_todo")

@app.route("/toggle_todo/<todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
