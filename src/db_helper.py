from config import app, db
import os

def reset_db():
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r") as f:
        schema_sql = f.read()

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
