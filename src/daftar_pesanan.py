"""Menu Daftar Pesanan"""

import sqlite3
import tkinter as tk
import datetime
from PIL import Image, ImageTk

class PesananInfo:
    """Berisi informasi lengkap dari Pesanan, beserta detail user dan tanamannya"""
    def __init__(self, single_query_result):
        self.order_id = single_query_result[0]
        self.username = single_query_result[1]
        self.item_id = single_query_result[2]
        self.status = single_query_result[3]
        self.order_date = single_query_result[4]
        self.duration = single_query_result[5]
        self.quantity = single_query_result[6]
        self.unit_price = single_query_result[7]
        self.name = single_query_result[8]
        self.email = single_query_result[9]
        self.password = single_query_result[10]
        self.address = single_query_result[11]
        self.phone_number = single_query_result[12]
        self.role = single_query_result[13]
        self.item_name = single_query_result[14]
        self.current_price = single_query_result[15]
        self.description = single_query_result[16]
        self.stock = single_query_result[17]
        self.image_path = single_query_result[18]

class PesananGuiEntry(tk.LabelFrame):
    """Berisi Suatu Entri Pesanan"""
    def __init__(self, master, bg = "#FFFFFF", padx = 0, pady = 0) -> None:
        super().__init__(master=master, padx=padx, pady=pady, bg=bg)

    def set_pesanan(self, pesanan):
        """Mengeset pesanan pada entri GUI ini"""
        self.pesanan = pesanan

    @staticmethod
    def generate(master, pesanan):
        """Menghasilkan PesananGuiEntry baru"""
        pge = PesananGuiEntry(master, padx=10, pady=10)
        pge.set_pesanan(pesanan)
        # row 1
        username_label = tk.Label(pge, text=pesanan.username, bg="#FFFFFF")
        username_label.grid(row=0, column=0, sticky="w")
        name_label = tk.Label(pge, text=pesanan.name, bg="#FFFFFF")
        name_label.grid(row=0, column=1, sticky="w")
        order_id_label = tk.Label(pge, text="#"+str(pesanan.order_id), bg="#FFFFFF")
        order_id_label.grid(row=0, column=2, sticky="w")

        # row 2
        status_label = tk.Label(pge, text=pesanan.status.upper(), bg="#FFFFFF")
        status_label.grid(row=1, column=0, sticky="w")

        item_name_label = tk.Label(pge, text=pesanan.item_name, bg="#FFFFFF")
        item_name_label.grid(row=2, column=0, sticky="w", pady=(10,0))

        # row 3
        jumlah_label = tk.Label(pge, text="Jumlah: " + str(pesanan.quantity), bg="#FFFFFF")
        jumlah_label.grid(row=3, column=0, sticky="w")

        # row 4
        start_date = datetime.datetime.strptime(pesanan.order_date, "%Y-%m-%d")
        end_date = start_date + datetime.timedelta(days=pesanan.duration)
        start_end_date_text = (start_date.strftime("%d/%m/%Y") + " - "
                               + end_date.strftime("%d/%m/%Y")
                               + " (" + str(pesanan.duration) + " hari)")
        order_date_label = tk.Label(pge, text=start_end_date_text, bg="#FFFFFF")
        order_date_label.grid(row=4, column=0, columnspan=2, sticky="w")

        # row 5
        price_calculation_text = ("Rp" + str(pesanan.unit_price) + " x "  + str(pesanan.quantity)
                                 + " x " + str(pesanan.duration) + " hari")
        price_calculation_label = tk.Label(pge, text=price_calculation_text, bg="#FFFFFF")
        price_calculation_label.grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))

        # row 6
        total_price_text = "Rp" + str(pesanan.unit_price * pesanan.quantity * pesanan.duration)
        total_price_label = tk.Label(pge, text=total_price_text, bg="#FFFFFF",
                                     font=("Helvetica", 9, "bold"))
        total_price_label.grid(row=6, column=0, sticky="w")

        # Gambar
        pge.plant_image = ImageTk.PhotoImage(Image.open(pesanan.image_path).resize((125, 125)))
        plant_image_label = tk.Label(pge, image=pge.plant_image, bg="#FFFFFF")
        plant_image_label.grid(row=0, column=3, rowspan=7, sticky="nwes")

        pge.grid_columnconfigure(0, minsize=100)
        pge.grid_columnconfigure(1, minsize=100)
        pge.grid_columnconfigure(2, minsize=100)
        pge.grid_columnconfigure(3, weight=1)
        return pge

class DaftarPesananPage(tk.Frame):
    """Halaman daftar pesanan"""
    def __init__(self, master, username, isadmin, bg="#FFFFFF", padx=100):
        tk.Frame.__init__(self, master, bg=bg, padx=padx)
        self.username = username
        self.isadmin = isadmin

        # Konfigurasi Scrollbar
        pesanan_canvas = tk.Canvas(self)
        pesanan_scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=pesanan_canvas.yview)
        pesanan_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        pesanan_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(20, 0))

        def _on_mouse_wheel(event):
            pesanan_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
        pesanan_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        # Membuat frame pesanan dan memasukkannya ke scrollbar canvas
        pesanan_frame = tk.LabelFrame(pesanan_canvas, text="Daftar Pesanan", bg="#FFFFFF")
        pesanan_frame.bind(
            "<Configure>",
            lambda e: pesanan_canvas.configure(scrollregion=pesanan_canvas.bbox("all"))
        )
        pesanan_frame_id = pesanan_canvas.create_window((0, 0), window=pesanan_frame, anchor="nw")
        pesanan_canvas.configure(yscrollcommand=pesanan_scrollbar.set)
        pesanan_canvas.bind(
            "<Configure>",
            lambda e: pesanan_canvas.itemconfig(pesanan_frame_id, width=e.width)
        )

        # Mengambil data dari database dan memasukkannya ke frame
        results = get_all_pesanan(self.isadmin, username)
        for pesanan in results:
            pge = PesananGuiEntry.generate(pesanan_frame, pesanan)
            pge.pack(fill='x', padx=10, pady=(10,0))

def is_expired(tanggal_selesai):
    """Mengecek apakah suatu tanggal telah kadaluarsa"""
    nowliteral = datetime.datetime.now().strftime("%Y-%m-%d")
    sekarang = datetime.datetime.strptime(nowliteral, "%Y-%m-%d") # menghilangkan komponen jam dan menit
    return tanggal_selesai < sekarang


def get_all_pesanan(isadmin: bool, username:str = None) -> 'list[PesananInfo]':
    """Mendapatkan semua Pesanan yang ada di database dan mengupdatenya jika ada yang expired"""
    ret = []
    conn = sqlite3.connect('puspa.db')
    cur = conn.cursor()
    if isadmin:
        cur.execute('SELECT * FROM pesanan NATURAL INNER JOIN user NATURAL INNER JOIN tanaman'
                    + ' ORDER BY order_date DESC;')
    else:
        cur.execute(
            'SELECT * FROM pesanan NATURAL INNER JOIN user NATURAL INNER JOIN tanaman' +
            ' WHERE username=? ORDER BY order_date DESC;',
        (username,))
    results_fetch = cur.fetchall()

    for result in results_fetch:
        pinfo = PesananInfo(result)
        start_date = datetime.datetime.strptime(pinfo.order_date, "%Y-%m-%d")
        end_date = start_date + datetime.timedelta(days=pinfo.duration)
        if pinfo.status.upper() == "ONGOING" and is_expired(end_date):
            cur.execute('UPDATE pesanan SET status="FINISHED" WHERE order_id=?;', [
                pinfo.order_id
            ])
            cur.execute('UPDATE tanaman SET stock=stock + ? WHERE item_id=?;', [
                pinfo.quantity,
                pinfo.item_id
            ])
            pinfo.status = "FINISHED"
        ret.append(pinfo)

    conn.commit()
    conn.close()
    return ret

def calculate_cost(pesanannow):
    """Menghitung total biaya dari suatu pesanan"""
    return pesanannow.unit_price * pesanannow.duration * pesanannow.quantity

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PUSPA - Pusat Penyewaan Tanaman")
    root.geometry("1920x1080")
    root.state('zoomed')
    root.configure(bg='white')
    root.configure(padx=100, pady=10)

    dpp = DaftarPesananPage(root, "bryanahusna", False)
    dpp.pack(expand=True, fill="both")

    root.mainloop()
