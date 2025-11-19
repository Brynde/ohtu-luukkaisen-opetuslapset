from sqlalchemy import text
from config import db

def add_source(key, ref_type, author, title, year, journal, publisher):
    sql = text("""
        INSERT INTO books (key, ref_type, author, title, year, journal, publisher)
        VALUES (:key, :ref_type, :author, :title, :year, :journal, :publisher)
    """)
    db.session.execute(sql, {
        "key": key,
        "ref_type": ref_type,
        "author": author,
        "title": title,
        "year": year,
        "journal": journal,
        "publisher": publisher
    })
    db.session.commit()

def get_sources():
    sql = text("SELECT * FROM books")
    result = db.session.execute(sql)
    return result.fetchall() 