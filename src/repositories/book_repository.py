from config import db
from sqlalchemy import text

from entities.todo import Todo
from entities.book import Book

def get_books():
    result = db.session.execute(text("SELECT author, title, year FROM books"))
    books = result.fetchall()
    return [Book(book[0], book[1], book[2]) for book in books] 

def create_book(content):
    sql = text("INSERT INTO books (content) VALUES (:content)")
    db.session.execute(sql, { "content": content })
    db.session.commit()
