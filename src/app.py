import re
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.book_repository import get_books, create_book, get_info, edit_book, delete_book, find_books
from config import app, db
from util import validate_book, UserInputError, get_random_gif
from repositories.tag_repository import get_tags, find_tags, create_tag, attach_tag

app.jinja_env.globals.update(get_random_gif=get_random_gif)

def _row_to_dict(row):
    if isinstance(row, dict):
        return row
    try:
        return dict(row._mapping)
    except Exception:
        try:
            return dict(row)
        except Exception:
            return {}

@app.route("/")
def index():
    doi_query = request.args.get("doi_query", "").strip()
    selected_tag = request.args.get("tag", "").strip() or None

    if doi_query:
        raw_sources = find_books("", doi_query=doi_query)
    else:
        criteria = request.args.get("sort")
        raw_sources = get_books(criteria)

    sources = [_row_to_dict(s) for s in raw_sources]

    tags_map = find_tags(sources)
    for s in sources:
        s_tags = []
        if "id" in s and s["id"] is not None and s["id"] in tags_map:
            s_tags = tags_map.get(s["id"], [])
        elif "key" in s and s.get("key") in tags_map:
            s_tags = tags_map.get(s.get("key"), [])
        s["tags"] = s_tags

    if selected_tag:
        sources = [s for s in sources if selected_tag in s.get("tags", [])]

    all_tags = get_tags()

    return render_template("source_pages/index.html", sources=sources, doi_query=doi_query, tags=all_tags, selected_tag=selected_tag)


@app.route("/sources")
def sources():
    return redirect("/")


@app.route("/sources/new", methods=["GET", "POST"])
def new_source():
    tags = get_tags()
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
            book_id = create_book(key, ref_type, author, title, year, journal, publisher, doi)

            selected_tags = request.form.getlist('tags')
            new_tags_raw = request.form.get('new_tags', '')
            new_tags = [p.strip() for p in re.split(r'[,\\n]+', new_tags_raw) if p.strip()]
            all_tag_names = []
            for tag in selected_tags + new_tags:
                if tag and tag not in all_tag_names:
                    all_tag_names.append(tag)
            for tag_name in all_tag_names:
                try:
                    tag_id = create_tag(tag_name)
                    attach_tag(book_id, tag_id)
                except UserInputError as error:
                    flash(str(error))
                    return render_template("forms/new_reference.html", tags=tags)
            db.session.commit()
            return redirect("/")
        except IntegrityError:
            flash("Viiteavain on jo käytössä. Anna jokaiselle lähteelle yksilöllinen avain.")
            return render_template("forms/new_reference.html", tags=tags)
        except Exception as error:
            flash(str(error))
            return render_template("forms/new_reference.html", tags=tags)
    return render_template("forms/new_reference.html", tags=tags)

@app.route("/sources/edit/<string:source_key>")
def edit_source(source_key):
    source = get_info(source_key)
    if source is None:
        flash("Viitettä ei löytynyt")
        return redirect("/")
    sdict = _row_to_dict(source)
    tags = get_tags()
    tags_map = find_tags([sdict])
    selected = []
    if "id" in sdict and sdict["id"] is not None and sdict["id"] in tags_map:
        selected = tags_map.get(sdict["id"], [])
    elif "key" in sdict and sdict.get("key") in tags_map:
        selected = tags_map.get(sdict.get("key"), [])
    return render_template("forms/edit_reference.html", key=source_key, source=sdict, tags=tags, selected_tags=selected)

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

        row = db.session.execute(text("SELECT id FROM books WHERE key = :key LIMIT 1"), {"key": source_key}).fetchone()
        book_id = row[0] if row else None
        db.session.execute(text("DELETE FROM book_tags WHERE book_id = :b"), {"b": book_id})
        selected_tags = request.form.getlist('tags')
        new_tags_raw = request.form.get('new_tags', '')
        new_tags = [p.strip() for p in re.split(r'[,\\n]+', new_tags_raw) if p.strip()]
        all_tag_names = []
        for tag in selected_tags + new_tags:
            if tag and tag not in all_tag_names:
                all_tag_names.append(tag)
        for tag_name in all_tag_names:
            try:
                tag_id = create_tag(tag_name)
                attach_tag(book_id, tag_id)
            except UserInputError as error:
                flash(str(error))
                source = get_info(source_key)
                sdict = _row_to_dict(source)
                tags = get_tags()
                tags_map = find_tags([sdict])
                selected = []
                if "id" in sdict and sdict["id"] is not None and sdict["id"] in tags_map:
                    selected = tags_map.get(sdict["id"], [])
                elif "key" in sdict and sdict.get("key") in tags_map:
                    selected = tags_map.get(sdict.get("key"), [])
                return render_template("forms/edit_reference.html", key=source_key, source=source, tags=tags, selected_tags=selected)
        db.session.commit()
        return redirect("/")
    except Exception as error:
        flash(str(error))
        source = get_info(source_key)
        sdict = _row_to_dict(source)
        tags = get_tags()
        tags_map = find_tags([sdict])
        selected = []
        if "id" in sdict and sdict["id"] is not None and sdict["id"] in tags_map:
            selected = tags_map.get(sdict["id"], [])
        elif "key" in sdict and sdict.get("key") in tags_map:
            selected = tags_map.get(sdict.get("key"), [])
        return render_template("forms/edit_reference.html", key=source_key, source=source, tags=tags, selected_tags=selected)


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
    selected_tag = request.args.get("tag", "").strip() or None

    # get raw results and normalize to dicts so we can attach tags
    raw_results = find_books(query, ref_type=ref_type or None, doi_query=doi_query or None)
    results = [_row_to_dict(r) for r in raw_results]

    # attach tags to each source
    tags_map = find_tags(results)
    for s in results:
        s_tags = []
        if "id" in s and s["id"] is not None and s["id"] in tags_map:
            s_tags = tags_map.get(s["id"], [])
        elif "key" in s and s.get("key") in tags_map:
            s_tags = tags_map.get(s.get("key"), [])
        s["tags"] = s_tags

    # filter by tag if requested
    if selected_tag:
        results = [s for s in results if selected_tag in s.get("tags", [])]

    # pass available tags for the UI
    all_tags = get_tags()

    return render_template(
        "source_pages/find_reference.html",
        query=query,
        ref_type=ref_type,
        doi_query=doi_query,
        sources=results,
        tags=all_tags,
        selected_tag=selected_tag,
    )

@app.route("/reset_db")

def reset_database():

    reset_db()

    # create_book(key, ref_type, author, title, year, journal, publisher)
    book_id = create_book("LuukProjekti", "article", "Luukkaisen opetuslapset", "Miten saada miniprojektista täydet pisteet", 2025, "Helsingin Sanomat", "", "13371337")
    book_id2 = create_book("Mullet", "article", "Gary the Gadget Guy", "Guide to catching Mullet", 1999, "", "The Ski Lodge", "1010104843A")
    book_id3 = create_book("PuffleHistory", "book", "Puffle jr.", "How Puffle the great conquered the world", 1597, "", "", "67420069")
    book_id4 = create_book("Dojoguifr", "inproceedings", "Sensei", "Why you can't get black belt", 2020, "Dojo Conference", "", "")
    book_id5 = create_book("Igloos", "article", "Igloo fanatic", "How to make your igloo prettier than your neighbors", 2001, "", "", "978-3-16-148410-0")
    tag_id = create_tag("tärkeä")
    tag_id2 = create_tag("fiktio")
    tag_id3 = create_tag("2000-luvulla kirjoitettu")
    attach_tag(book_id, tag_id)
    attach_tag(book_id, tag_id3)
    attach_tag(book_id2, tag_id2)
    attach_tag(book_id3, tag_id2)
    attach_tag(book_id4, tag_id3)
    attach_tag(book_id5, tag_id3)
    db.session.commit()

    return jsonify({"message": "db reset"})

@app.route("/kiitos_demosta")
def kiitos_demosta():
    return render_template("source_pages/kiitos_demosta.html")