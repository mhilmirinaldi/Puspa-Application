"""Pengetesan pemesanan"""
import datetime
import pemesanan

def test_generate_id_pesanan():
    """Testing generate_id_pesanan(waktu)"""
    waktu = datetime.datetime.strptime("22-04-08 00:45", "%y-%m-%d %H:%M")
    angkarandom = str(123)
    hasil_id = pemesanan.generate_id_pesanan(waktu)[:-3]
    assert (hasil_id + angkarandom) == "4500080422123"
