from config import db
from sqlalchemy import text

from entities.todo import Todo
from entities.book import Book

def get_books():
    result = db.session.execute(text("SELECT author, title, year FROM books"))
    books = result.fetchall()
    return [Book(book[0], book[1], book[2]) for book in books] 

def get_info(book_id):
    sql = text("SELECT author, title, year FROM books WHERE id = :id")
    result = db.session.execute(sql, {"id": book_id})
    book_info = result.fetchone()
    if book_info is None:
        return None
    return book_info

def create_book(author, title, year):
    sql = text("INSERT INTO books (author, title, year) VALUES (:author, :title, :year)")
    db.session.execute(sql, {"author": author, "title": title, "year": year})
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
        sql = text(f"UPDATE books SET author = :author, title = :title, year = :year WHERE id = :id")
        db.session.execute(sql, {"author": current_info[0], "title": current_info[1], "year": current_info[2], "id": book_id})
        db.session.commit()