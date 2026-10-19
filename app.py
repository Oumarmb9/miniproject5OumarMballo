# INF601 - Advanced Programming in Python
# Oumar Mballo
# Mini Project 5

"""BookNook - a small Flask web app for tracking the books you read.

Set up and run:
    flask --app app init-db      # create the database (first time only)
    flask --app app run --debug  # start the development server
or simply:
    python app.py                # creates the DB on first run, then serves
"""

import os
import functools

from flask import (
    Flask, render_template, redirect, url_for, request, flash, session, g
)
from werkzeug.security import generate_password_hash, check_password_hash

import db


def create_app():
    """Application factory: build and configure the Flask app."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-change-me"),
        DATABASE=os.path.join(app.instance_path, "booknook.sqlite"),
    )

    # The instance folder holds the SQLite file; make sure it exists.
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    register_routes(app)
    return app


def login_required(view):
    """Decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please log in to view that page.", "warning")
            return redirect(url_for("login", next=request.path))
        return view(**kwargs)
    return wrapped_view


def register_routes(app):
    """Attach all URL routes and the before-request user loader."""

    @app.before_request
    def load_logged_in_user():
        """Load the logged-in user (if any) into g.user for every request."""
        user_id = session.get("user_id")
        if user_id is None:
            g.user = None
        else:
            g.user = db.get_db().execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            ).fetchone()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if g.user:
            return redirect(url_for("books"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            confirm = request.form.get("confirm", "")
            conn = db.get_db()

            if not username or not password:
                flash("Username and password are required.", "danger")
            elif password != confirm:
                flash("Passwords do not match.", "danger")
            elif conn.execute(
                "SELECT id FROM users WHERE username = ?", (username,)
            ).fetchone():
                flash("That username is already taken.", "danger")
            else:
                conn.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                conn.commit()
                flash("Account created! You can log in now.", "success")
                return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if g.user:
            return redirect(url_for("books"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            conn = db.get_db()
            user = conn.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()

            if user and check_password_hash(user["password_hash"], password):
                session.clear()
                session["user_id"] = user["id"]
                flash(f"Welcome back, {user['username']}!", "success")
                next_page = request.args.get("next")
                return redirect(next_page or url_for("books"))

            flash("Invalid username or password.", "danger")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for("index"))

    @app.route("/books")
    @login_required
    def books():
        conn = db.get_db()
        my_books = conn.execute(
            "SELECT * FROM books WHERE user_id = ? ORDER BY date_added DESC",
            (g.user["id"],),
        ).fetchall()
        return render_template("books.html", books=my_books)

    @app.route("/books/add", methods=["GET", "POST"])
    @login_required
    def add_book():
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            author = request.form.get("author", "").strip()
            status = request.form.get("status", "To Read")
            rating = request.form.get("rating") or None
            notes = request.form.get("notes", "").strip()

            if not title or not author:
                flash("Title and author are both required.", "danger")
            else:
                conn = db.get_db()
                conn.execute(
                    "INSERT INTO books (title, author, status, rating, notes, user_id) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (title, author, status,
                     int(rating) if rating else None, notes, g.user["id"]),
                )
                conn.commit()
                flash(f'"{title}" was added to your shelf.', "success")
                return redirect(url_for("books"))

        return render_template("add_book.html")

    @app.route("/books/<int:book_id>/delete", methods=["POST"])
    @login_required
    def delete_book(book_id):
        conn = db.get_db()
        book = conn.execute(
            "SELECT * FROM books WHERE id = ?", (book_id,)
        ).fetchone()

        if book is None:
            flash("Book not found.", "danger")
        elif book["user_id"] != g.user["id"]:
            # Only the owner may delete a book.
            flash("You can only delete your own books.", "danger")
        else:
            conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
            conn.commit()
            flash(f'"{book["title"]}" was removed from your shelf.', "info")

        return redirect(url_for("books"))


app = create_app()


if __name__ == "__main__":
    # On first run, build the database automatically for convenience.
    if not os.path.exists(app.config["DATABASE"]):
        with app.app_context():
            db.init_db()
        print("Created new database at", app.config["DATABASE"])
    app.run(debug=True)
