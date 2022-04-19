""" Menginisialisasi database dengan membuat tabel baru"""

import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect('puspa.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS user(username TEXT PRIMARY KEY, name TEXT, email TEXT,'
                + 'password TEXT, address TEXT, phone_number TEXT, role TEXT);')
    cur.execute('CREATE TABLE IF NOT EXISTS tanaman(item_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                + 'item_name TEXT, current_price INTEGER, description TEXT, stock INTEGER, '
                + 'image_path TEXT);')
    cur.execute('CREATE TABLE IF NOT EXISTS pesanan(order_id TEXT PRIMARY KEY, '
                + 'username TEXT REFERENCES user(username), '
                + 'item_id INTEGER REFERENCES tanaman(item_id), status TEXT, order_date TEXT, '
                + 'duration INTEGER, quantity INTEGER, unit_price INTEGER);')
    conn.commit()
    conn.close()
