from sqlalchemy import text
from config import db

def create_tag(name):
    sql = text("INSERT INTO tags (name) ""VALUES (:name)")
    db.session.execute(sql, {"name": name})
    db.session.commit()

def attach_tag(book_id, tag_id):
    sql = text("INSERT INTO book_tags (book_id, tag_id) ""VALUES (:book_id, :tag_id)")
    db.session.execute(sql, {"book_id": book_id, "tag_id": tag_id})
    db.session.commit()

def get_tags():
    result = db.session.execute(
        text(f"SELECT * FROM tags ORDER BY name")
    )
    tags = result.fetchall()
    return tags

def get_books_with_tag(tag_id):
    result = db.session.execute(
        text(f"SELECT book_id FROM book_tags WHERE tag_id like :tag_id"), tag_id
    )
    books = result.fetchall()
    return books