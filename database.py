import sqlite3
from datetime import datetime

DB_NAME = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount INTEGER,
        category TEXT,
        location TEXT,
        date_shamsi TEXT,
        date_miladi TEXT,
        note TEXT,
        created_at TEXT
    )''')
    conn.commit()
    conn.close()

def add_expense(user_id, amount, category, location, date_shamsi, date_miladi, note):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO expenses 
        (user_id, amount, category, location, date_shamsi, date_miladi, note, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, amount, category, location, date_shamsi, date_miladi, note, datetime.now()))
    conn.commit()
    conn.close()

def get_user_expenses(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM expenses WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    data = c.fetchall()
    conn.close()
    return data
