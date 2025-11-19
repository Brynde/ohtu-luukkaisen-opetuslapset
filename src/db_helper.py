from config import app, db
import os

def reset_db():
  print(f"Clearing contents from table books")
  sql = text(f"DELETE FROM books")
  db.session.execute(sql)
  db.session.commit()

    conn = db.engine.raw_connection()
    try:
        cursor = conn.cursor()
        cursor.executescript(schema_sql)
        conn.commit()
        print("Database recreated from schema.sql")
    finally:
        conn.close()


if __name__ == "__main__":
    with app.app_context():
        reset_db()
