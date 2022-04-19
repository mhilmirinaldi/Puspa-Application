"""Test untuk daftar_pesanan.py"""

import datetime
import daftar_pesanan

def test_calculate_cost():
    """Testing calculate_cost()"""
    single_query_result = [0 for i in range(19)]
    pesanan = daftar_pesanan.PesananInfo(single_query_result)
    pesanan.unit_price = 10000
    pesanan.quantity = 5
    pesanan.duration = 5
    assert daftar_pesanan.calculate_cost(pesanan) == 250000
    
def test_is_expired():
    """Testing pengecekan expired"""
    waktu_now = datetime.datetime.now().strftime("%Y-%m-%d")
    waktu_now = datetime.datetime.strptime(waktu_now, "%Y-%m-%d")
    waktu_tomorrow = waktu_now + datetime.timedelta(days=1)
    waktu_yesterday = waktu_now + datetime.timedelta(days=-1)

    assert daftar_pesanan.is_expired(waktu_now) == False
    assert daftar_pesanan.is_expired(waktu_tomorrow) == False
    assert daftar_pesanan.is_expired(waktu_yesterday) == True
    