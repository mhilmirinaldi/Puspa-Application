"""User Entity"""

import sqlite3

class User:
    """Berisi informasi lengkap dari User"""
    def __init__(self, username):
        self.username = username

    def get_info(self, single_query_result):
        """Mendapatkan informasi lengkap dari user"""
        self.username = single_query_result[0]
        self.name = single_query_result[1]
        self.email = single_query_result[2]
        self.password = single_query_result[3]
        self.address = single_query_result[4]
        self.phone = single_query_result[5]
        self.role = single_query_result[6]

    def get_user(self):
        """Mendapatkan user yang ada di database"""
        conn = sqlite3.connect('puspa.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM user WHERE username=?;', (self.username,))
        results_fetch = cur.fetchall()
        return results_fetch
        