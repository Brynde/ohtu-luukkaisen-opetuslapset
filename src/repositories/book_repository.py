from config import db
from sqlalchemy import text

from entities.book import Book

def get_books():
    result = db.session.execute(text("SELECT * FROM books"))
    books = result.fetchall()
    return books

def get_info(source_key):
    sql = text("SELECT key, ref_type, author, title, year, journal, publisher FROM books WHERE key = :key")
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
    }

def create_book(key, ref_type, author, title, year, journal, publisher):
    sql = text("INSERT INTO books (key, ref_type, author, title, year, journal, publisher) VALUES (:key, :ref_type, :author, :title, :year, :journal, :publisher)")
    db.session.execute(sql, {"key": key, "ref_type": ref_type, "author": author, "title": title, "year": year, "journal": journal, "publisher": publisher})
    db.session.commit()

def edit_book(source_key, content):
    """Update book identified by source_key.
    `content` can be a dict or a list/tuple in order:
    [key, ref_type, author, title, year, journal, publisher]
    Returns True if a row was updated.
    """
    fields = ["key", "ref_type", "author", "title", "year", "journal", "publisher"]

    current = get_info(source_key)
    if current is None:
        return False

    if isinstance(content, (list, tuple)):
        if len(content) != len(fields):
            raise ValueError("content list must have 7 elements")
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
    return True