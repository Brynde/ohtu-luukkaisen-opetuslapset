from sqlalchemy import text
from config import db

def build_bibtex(key, ref_type, author, title, year, journal, publisher):
    ref_type = (ref_type or "").strip()
    key = (key or "").strip()
    parts = []
    if author:
        parts.append(f"  author = {{{author}}}")
    if year is not None and year != "":
        parts.append(f"  year = {{{year}}}")
    if title:
        parts.append(f"  title = {{{title}}}")
    if journal:
        parts.append(f"  journal = {{{journal}}}")
    if publisher:
        parts.append(f"  publisher = {{{publisher}}}")

    body = ",\n".join(parts)
    bib = f"@{ref_type}{{{key},\n{body}\n}}\n"
    return bib

def get_books(criteria):
    if criteria == None:
        criteria = "title DESC"
    
    types = ["title DESC", "title", "year DESC", "year", "author"]
    if criteria not in types:
        raise ValueError("Lajittelutyyppiä ei löydy")

    result = db.session.execute(
        text(f"SELECT * FROM books ORDER BY {criteria}")
    )
    books = result.fetchall()
    return books

def get_info(source_key):
    sql = text("SELECT key, ref_type, author, title, year, journal, publisher, doi, bibtex FROM books WHERE key = :key")
    result = db.session.execute(sql, {"key": source_key})
    book_info = result.fetchone()
    if book_info is None:
        return None
    return {
        "key": book_info[0],
        "ref_type": book_info[1],
        "author": book_info[2],
        "title": book_info[3],
        "year": book_info[4],
        "journal": book_info[5],
        "publisher": book_info[6],
        "doi": book_info[7],
        "bibtex": book_info[8]
    }

def update_bibtex(key):
    sql = text("SELECT key, ref_type, author, title, year, journal, publisher FROM books WHERE key = :key")
    row = db.session.execute(sql, {"key": key}).fetchone()
    if row is None:
        return None

    bib = build_bibtex(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    update_sql = text("UPDATE books SET bibtex = :bib WHERE key = :key")
    db.session.execute(update_sql, {"bib": bib, "key": key})
    db.session.commit()
    return bib

def create_book(key, ref_type, author, title, year, journal, publisher, doi):
    bibtex = build_bibtex(key, ref_type, author, title, year, journal, publisher)
    sql = text(
        "INSERT INTO books (key, ref_type, author, title, year, journal, publisher, doi, bibtex) "
        "VALUES (:key, :ref_type, :author, :title, :year, :journal, :publisher, :doi, :bibtex) "
        "RETURNING id"
    )
    result = db.session.execute(sql, {
        "key": key,
        "ref_type": ref_type,
        "author": author,
        "title": title,
        "year": year,
        "journal": journal,
        "publisher": publisher,
        "doi": doi,
        "bibtex": bibtex
    })
    row = result.fetchone()
    try:
        result.close()
    except Exception:
        pass
    if row:
        db.session.commit()
        return row[0]
    else:
        db.session.rollback()
        return None

def edit_book(source_key, content):
    fields = ["key", "ref_type", "author", "title", "year", "journal", "publisher", "doi"]

    current = get_info(source_key)
    if current is None:
        return False

    if isinstance(content, (list, tuple)):
        if len(content) != len(fields):
            raise ValueError("content list must have 8 elements")
        new = dict(zip(fields, content))

    elif isinstance(content, dict):
        new = content.copy()
    else:
        raise TypeError("content must be dict or list/tuple")

    def normalize(value, field):
        if value is None:
            return None
        if isinstance(value, str):
            v = value.strip()
            if v == "":
                return None
            if field == "year":
                try:
                    return int(v)
                except ValueError:
                    return v
            return v
        return value

    set_clauses = []
    params = {}
    for f in fields:
        if f == "key":
            continue
        if f in new:
            new_val = normalize(new[f], f)
            cur_val = normalize(current.get(f), f)
            if new_val != cur_val:
                set_clauses.append(f + " = :" + f)
                params[f] = new_val

    if not set_clauses:
        return False

    params["source_key"] = source_key
    sql = text(f"UPDATE books SET {', '.join(set_clauses)} WHERE key = :source_key")
    db.session.execute(sql, params)
    db.session.commit()
    update_bibtex(source_key)
    return True

def delete_book(source_key):
    if get_info(source_key) is None:
        return False
    sql = text("DELETE FROM books WHERE key = :key")
    db.session.execute(sql, {"key": source_key})
    db.session.commit()
    return True

def find_books(query, ref_type=None, doi_query=None):
    query = (query or "").strip()
    q = "%" if query == "" else f"%{query}%"

    sql = (
        "SELECT key, ref_type, author, title, year, journal, publisher, doi, bibtex "
        "FROM books "
        "WHERE (COALESCE(key,'') LIKE :q OR COALESCE(ref_type,'') LIKE :q "
        "OR COALESCE(author,'') LIKE :q OR COALESCE(title,'') LIKE :q "
        "OR COALESCE(CAST(year AS TEXT),'') LIKE :q OR COALESCE(journal,'') LIKE :q "
        "OR COALESCE(publisher,'') LIKE :q)"
    )
    params = {"q": q}

    if ref_type:
        sql += " AND lower(COALESCE(ref_type,'')) = :ref_type"
        params["ref_type"] = ref_type.strip().lower()

    if doi_query:
        sql += " AND COALESCE(doi,'') = :doi_query"
        params["doi_query"] = doi_query.strip()

    sql += " ORDER BY key COLLATE NOCASE"

    result = db.session.execute(text(sql), params)
    rows = result.fetchall()
    return [
        {
            "key": r[0],
            "ref_type": r[1],
            "author": r[2],
            "title": r[3],
            "year": r[4],
            "journal": r[5],
            "publisher": r[6],
            "doi": r[7],
            "bibtex": r[8],
        }
        for r in rows
    ]
