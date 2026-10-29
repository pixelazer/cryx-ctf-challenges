'''
This file is part of a challenge for CRYX CTF [SPHINX 2026]
Written by Aryan Takalkar.
'''

import sqlite3
from pathlib import Path
from flask import Flask, request, render_template, g

app = Flask(__name__)
HOME_DIR = Path(__file__).resolve().parent
DB_PATH = HOME_DIR / "dbs" / "database.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS secrets;

        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            price REAL
        );

        CREATE TABLE secrets (
            id INTEGER PRIMARY KEY,
            flag TEXT
        );
    """)
    cur.executemany(
        "INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
        [
            ("Vulcan RTX 4080", "GPU", 1599.99),
            ("Vulcan RTX 4060", "GPU", 1399.99),
            ("Vulcan RTX 4040", "GPU", 1099.99),
            ("Magnum GTR 119", "GPU", 1099.99),
            ("Magnum GTR 118", "GPU", 899.99),
            ("Magnum GTR 117", "GPU", 599.99),
            ("Ferrox i9-14900K", "CPU", 589.00),
            ("Magma DDR5 32GB", "RAM", 129.99),
            ("Cinder X870 Motherboard", "Motherboard", 349.50),
            ("Ember 1000W PSU", "PSU", 189.00),
        ],
    )
    cur.execute("INSERT INTO secrets (flag) VALUES (?)", ("CRYX{placeholder_flag}",))
    db.commit()
    db.close()


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    error = None

    if request.method == "POST":
        query_term = request.form.get("q", "").strip()
        db = get_db()
        cur = db.cursor()
        sql = f"SELECT name, category FROM products WHERE category LIKE '%{query_term}%'"

        try:
            cur.execute(sql)
            results = cur.fetchall()
        except sqlite3.Error as e:
            error = str(e)

    return render_template("index.html", results=results, error=error)


if __name__ == "__main__":
    if not DB_PATH.exists():
        init_db()
    app.run(host="0.0.0.0", port=5000)