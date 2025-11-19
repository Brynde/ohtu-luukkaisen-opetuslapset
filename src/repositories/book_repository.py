from config import db
from sqlalchemy import text

from entities.todo import Todo
from entities.book import Book

def get_books():
    result = db.session.execute(text("SELECT author, title, year FROM books"))
    books = result.fetchall()
    return [Book(book[0], book[1], book[2]) for book in books] 

def get_info(book_id):
    sql = text("SELECT key, ref_type, author, title, year, journal, publisher FROM books WHERE id = :id")
    result = db.session.execute(sql, {"id": book_id})
    book_info = result.fetchone()
    if book_info is None:
        return None
    return book_info

def create_book(key, ref_type, author, title, year, journal, publisher):
    sql = text("INSERT INTO books (key, ref_type, author, title, year, journal, publisher) VALUES (:key, :ref_type, :author, :title, :year, :journal, :publisher)")
    db.session.execute(sql, {"key": key, "ref_type": ref_type, "author": author, "title": title, "year": year, "journal": journal, "publisher": publisher})
    db.session.commit()

def edit_book(book_id, content):
    current_info = get_info(book_id)
    i=0
    new_info = False
    for info in content:
        if info != current_info[i]:
            new_info = True
            current_info[i] = info
        i+=1
    if new_info:
        sql = text(f"UPDATE books SET key = :key, ref_type = :ref_type, author = :author, title = :title, year = :year, journal = :journal, publisher = :publisher WHERE id = :id")
        db.session.execute(sql, {"key": current_info[0], "ref_type": current_info[1], "author": current_info[2], "title": current_info[3], "year": current_info[4], "journal": current_info[5], "publisher": current_info[6],"id": book_id})
        db.session.commit()