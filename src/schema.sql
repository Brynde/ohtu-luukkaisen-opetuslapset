CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    ref_type TEXT,
    author TEXT,
    title TEXT,
    year INTEGER,
    journal TEXT,
    publisher TEXT,
    doi TEXT,
    bibtex TEXT
);
