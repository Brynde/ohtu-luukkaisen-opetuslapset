from pathlib import Path
from config import app, db

def reset_db():
    schema_path = Path(__file__).resolve().parent / "schema.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")
    conn = db.engine.raw_connection()
    try:
        cursor = conn.cursor()
        cursor.executescript("DROP TABLE IF EXISTS books;")
        cursor.executescript(schema_sql)
        conn.commit()
        print("Database recreated from schema.sql")
    finally:
        conn.close()

if __name__ == "__main__":
    with app.app_context():
        reset_db()
