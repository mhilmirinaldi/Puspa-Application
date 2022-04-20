"""Tanaman Entity"""

import sqlite3

class TanamanInfo:
    """Berisi informasi lengkap dari Tanaman"""
    def __init__(self, single_query_result):
        self.item_id = single_query_result[0]
        self.name = single_query_result[1]
        self.current_price = single_query_result[2]
        self.description = single_query_result[3]
        self.stock = single_query_result[4]
        self.image_path = single_query_result[5]

def get_all_tanaman() -> 'list[TanamanInfo]':
    """Mendapatkan semua Tanaman yang ada di database"""
    ret = []
    conn = sqlite3.connect('puspa.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM tanaman;')
    results_fetch = cur.fetchall()

    for result in results_fetch:
        tanaman = TanamanInfo(result)
        ret.append(tanaman)

    return ret
    