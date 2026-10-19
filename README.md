# BookNook — INF601 Mini Project 5

**Oumar Mballo · INF601 – Advanced Programming in Python**

BookNook is a small Flask web application for keeping track of the books you read.
Each user registers an account, logs in, and manages a private bookshelf: add a book
with its title, author, reading status, an optional 1–5 star rating, and notes, then
remove books with a confirmation dialog.

## Features

- Five+ pages built on a shared Jinja template (Home, About, Register, Log In, My Shelf, Add Book).
- Register / log in / log out with session-based authentication and **hashed passwords** (Werkzeug).
- A **SQLite database with two tables linked by a foreign key** — `users` (one) → `books` (many), via `books.user_id`.
- An **Add Book** page with a form served over `GET` and saved over `POST`.
- **Bootstrap 5** styling, including a **modal** that confirms before a book is deleted.
- Each user only ever sees and edits their own books.

## Project structure

```
miniproject5OumarMballo/
├── app.py              # main app: factory, routes, auth (header comment here)
├── db.py               # SQLite helpers + the `init-db` command
├── schema.sql          # the two tables and their foreign key
├── requirements.txt
├── README.md
├── static/
│   └── css/style.css
└── templates/
    ├── base.html       # shared layout: navbar, flash messages, Bootstrap
    ├── index.html
    ├── about.html
    ├── register.html
    ├── login.html
    ├── books.html      # shelf table + delete-confirmation modal
    └── add_book.html   # the GET/POST form
```

(The SQLite file is created at runtime in an `instance/` folder, which is git-ignored.)

## Setup and running

You need Python 3.8+.

**1. (Optional) create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

**2. Install the requirements**

```bash
pip install -r requirements.txt
```

**3. Initialize the database** (creates the tables — run once)

```bash
flask --app app init-db
```

**4. Run the development server**

```bash
flask --app app run --debug
```

Then open <http://127.0.0.1:5000> in your browser.

> Shortcut: you can also just run `python app.py`. It builds the database on its
> first run and then starts the server.

## How to use it

1. Click **Register** and create an account.
2. **Log in** with that account.
3. Go to **Add Book**, fill in the form, and submit — the book appears on **My Shelf**.
4. Use the **Delete** button on a book to open the confirmation modal and remove it.

## AI Usage

I used an AI assistant (Claude) as a helper while building this project, in line
with the course AI Use Policy. Specifically, AI was used to:

- Scaffold the Flask application-factory structure and the `sqlite3` database
  helpers (`db.py` / `schema.sql`), following the standard Flask tutorial pattern.
- Draft the Jinja templates and wire up Bootstrap 5, including the delete-confirmation modal.
- Help write this README and suggest edge-case handling (duplicate usernames,
  mismatched passwords, restricting deletes to the owning user).

I reviewed, tested, and verified all of the generated code myself, made sure I
understand how each part works, and confirmed the app meets the project
requirements before submitting. All final decisions and the submitted work are my own.
