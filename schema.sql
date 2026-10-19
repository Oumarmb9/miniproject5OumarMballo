-- INF601 - Advanced Programming in Python
-- Oumar Mballo
-- Mini Project 5
--
-- Two tables linked by a foreign key:
--   users (one)  ->  books (many)

DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE books (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT NOT NULL,
    author     TEXT NOT NULL,
    status     TEXT NOT NULL DEFAULT 'To Read',
    rating     INTEGER,
    notes      TEXT,
    date_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id    INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
