# INF601 - Advanced Programming in Python
# Oumar Mballo
# Mini Project 5

"""SQLite database helpers.

Handles opening a per-request connection, closing it automatically, and
the `flask --app app init-db` command that builds the tables from schema.sql.
"""

import sqlite3

import click
from flask import current_app, g


def get_db():
    """Return a SQLite connection for the current request, opening one if needed."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        # Rows behave like dicts, so templates can use book["title"].
        g.db.row_factory = sqlite3.Row
        # Make SQLite actually enforce the foreign key constraint.
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    """Close the connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the database tables from schema.sql (drops any existing data)."""
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """CLI command: `flask --app app init-db`."""
    init_db()
    click.echo("Database initialized.")


def init_app(app):
    """Register database hooks and commands with the Flask app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
