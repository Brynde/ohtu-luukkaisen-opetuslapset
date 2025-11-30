from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.book_repository import get_books, create_book, get_info, edit_book, delete_book, find_books
from config import app, test_env
from util import validate_book
from sqlalchemy.exc import IntegrityError


@app.route("/")
def index():
    doi_query = request.args.get("doi_query", "").strip()
    if doi_query:
        sources = find_books("", doi_query=doi_query)
    else:
        sources = get_books()
    return render_template("index.html", sources=sources, doi_query=doi_query)


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
        doi = request.form.get("doi")

        try:
            validate_book(key, ref_type, author, title, year, journal, publisher, doi)
            create_book(key, ref_type, author, title, year, journal, publisher, doi)
            return redirect("/")
        except IntegrityError:
            flash("Viiteavain on jo käytössä. Anna jokaiselle lähteelle yksilöllinen avain.")
            return render_template("new_reference.html")
        except Exception as error:
            flash(str(error))
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
    doi = request.form.get("doi")

    try:
        validate_book(source_key, ref_type, author, title, year, journal, publisher)
        edit_book(source_key, [source_key, ref_type, author, title, year, journal, publisher, doi])
        return redirect("/")
    except Exception as error:
        flash(str(error))
        print(source_key, ref_type, author, title, year, journal, publisher, doi)
        source = get_info(source_key)
        return render_template("edit_reference.html", key=source_key, source=source)


@app.route("/sources/delete/<string:source_key>", methods=["POST"])
def delete_source(source_key):
    if delete_book(source_key):
        flash("Poisto onnistui!")
    else:
        flash("Poisto epäonnistui!")
    return redirect("/")


@app.route("/sources/find_source")
def find_source():
    query = request.args.get("query", "")
    ref_type = request.args.get("ref_type", "")
    doi_query = request.args.get("doi_query", "")

    print("find_source args:", dict(request.args))

    results = find_books(query, ref_type=ref_type or None, doi_query=doi_query or None)
    print(results)

    return render_template(
        "index.html",
        query=query,
        ref_type=ref_type,
        doi_query=doi_query,
        sources=results,
    )
