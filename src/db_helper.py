from config import app, db
from sqlalchemy import text
from pathlib import Path
import os

def reset_db():
  print(f"Clearing contents from table books")
  sql = text(f"DELETE FROM books")
  db.session.execute(sql)
  db.session.commit()
  schema_path = Path(__file__).resolve().parent / "schema.sql"
  schema_sql = schema_path.read_text(encoding="utf-8")

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
