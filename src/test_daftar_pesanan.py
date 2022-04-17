import daftar_pesanan

def test_calculate_cost():
    single_query_result = [0 for i in range(19)]
    pesanan = daftar_pesanan.PesananInfo(single_query_result)
    pesanan.unit_price = 10000
    pesanan.quantity = 5
    pesanan.duration = 5
    assert daftar_pesanan.calculate_cost(pesanan) == 250000
    