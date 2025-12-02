from sqlalchemy import text
from config import db
from util import UserInputError

def create_tag(name):
    name = (name or "").strip()
    if not name:
        raise UserInputError("Tunnisteen nimi ei voi olla tyhjä")
    if len(name) > 25:
        raise UserInputError("Tunnisteen nimi ei voi olla yli 25 merkkiä")
    # check existing
    existing = get_tag_by_name(name)
    if existing:
        return existing["id"]
    db.session.execute(text("INSERT INTO tags (name) VALUES (:name)"), {"name": name})
    db.session.commit()
    row = db.session.execute(text("SELECT id FROM tags WHERE name = :name LIMIT 1"), {"name": name}).fetchone()
    return row[0] if row else None

def get_tag_by_name(name):
    row = db.session.execute(text("SELECT id, name FROM tags WHERE lower(name)=:n LIMIT 1"), {"n": (name or "").strip().lower()}).fetchone()
    if not row:
        return None
    return {"id": row[0], "name": row[1]}

def attach_tag(book_id, tag_id):
    sql = text("INSERT OR IGNORE INTO book_tags (book_id, tag_id) ""VALUES (:book_id, :tag_id)")
    db.session.execute(sql, {"book_id": book_id, "tag_id": tag_id})

def get_tags():
    result = db.session.execute(
        text(f"SELECT name FROM tags ORDER BY name")
    )
    rows = result.fetchall()
    tags = [r[0] for r in rows]
    return tags

def get_books_with_tag(tag_id):
    result = db.session.execute(
        text(f"SELECT book_id FROM book_tags WHERE tag_id like :tag_id"), tag_id
    )
    books = result.fetchall()
    return books

def validate_tag(tag):
    name = (tag or "").strip()
    if not name:
        raise UserInputError("Tunniste ei voi olla tyhjä")
    
    if len(name) >= 25:
        raise UserInputError("Tunnisteen pituus ei saa ylittää yli 25 merkkiä")

    existing = db.session.execute(
        text("SELECT 1 FROM tags WHERE lower(name) = :name LIMIT 1"),
        {"name": name.lower()}
    ).fetchone()

    if existing:
        raise UserInputError(f"Tunniste '{name}' on jo olemassa")

    return True

def find_tags(sources):
    if not sources:
        return {}

    ids = []
    keys = []
    for s in sources:
        if "id" in s and s["id"] is not None:
            try:
                ids.append(int(s["id"]))
            except Exception:
                pass
        if "key" in s and s["key"]:
            keys.append(str(s["key"]))

    where_clauses = []
    params = {}

    if ids:
        id_placeholders = []
        for i, val in enumerate(ids):
            name = f"id{i}"
            id_placeholders.append(f":{name}")
            params[name] = val
        where_clauses.append(f"books.id IN ({', '.join(id_placeholders)})")

    if keys:
        key_placeholders = []
        for i, val in enumerate(keys):
            name = f"k{i}"
            key_placeholders.append(f":{name}")
            params[name] = val
        where_clauses.append(f"books.key IN ({', '.join(key_placeholders)})")

    if not where_clauses:
        return {}

    sql = (
        "SELECT books.id AS book_id, books.key AS book_key, tags.name AS tag_name "
        "FROM books "
        "JOIN book_tags ON book_tags.book_id = books.id "
        "JOIN tags ON tags.id = book_tags.tag_id "
        "WHERE " + " OR ".join(where_clauses) + " "
        "ORDER BY books.id, tags.name"
    )

    res = db.session.execute(text(sql), params)
    rows = res.fetchall()
    try:
        res.close()
    except Exception:
        pass

    mapping = {}
    for book_id, book_key, tag_name in rows:
        if book_id is not None:
            mapping.setdefault(book_id, []).append(tag_name)
        if book_key:
            mapping.setdefault(book_key, []).append(tag_name)

    for s in sources:
        if "id" in s and s["id"] is not None:
            mapping.setdefault(int(s["id"]), [])
        if "key" in s and s["key"]:
            mapping.setdefault(s["key"], [])

    return mapping