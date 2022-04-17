"""Halaman detail tanaman beserta pemesanannya"""

import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox
from random import randint
from PIL import Image, ImageTk

class TanamanInfo:
    """Berisi informasi hasil query tabel tanaman"""
    def __init__(self, db_name, item_id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tanaman WHERE item_id=?", [item_id])
        result_fetch = cursor.fetchall()
        if len(result_fetch) == 0:
            return
        result_one = result_fetch[0]
        self.item_id = result_one[0]
        self.item_name = result_one[1]
        self.current_price = result_one[2]
        self.description = result_one[3]
        self.stock = result_one[4]
        self.image_path = result_one[5]
        conn.close()

class DetailTanaman(tk.Frame):
    """Halaman detail tanaman"""
    def __init__(self, master, username, item_id):
        tk.Frame.__init__(self, master, bg="#FFFFFF", padx=100)
        self.username = username
        self.item_id = item_id
        self.tanaman_info = TanamanInfo("puspa.db", item_id)
        tanaman_info = self.tanaman_info

        item_name_label = tk.Label(self, text=tanaman_info.item_name,
                                   font=("Helvetica", 30, "bold"), bg="#FFFFFF")
        item_name_label.grid(row=0, column=0, columnspan=4, sticky="w", pady=(50,0))

        description_title_label = tk.Label(self, text="Deskripsi Tanaman:",
                                           font=("Helvetica", 11, "bold"), bg="#FFFFFF")
        description_title_label.grid(row=1, column=0, columnspan=4, sticky="w", pady=(10,0))

        description_label = tk.Label(self, text=tanaman_info.description,
                                     bg="#FFFFFF", wraplength=400, justify="left")
        description_label.grid(row=2, column=0, columnspan=4, sticky="w", pady=(0,0))

        self.stock_var = tk.StringVar()
        self.stock_var.set("Stok: " + str(tanaman_info.stock))
        stock_label = tk.Label(self, textvariable=self.stock_var,
                               bg="#FFFFFF", font=("Helvetica", 9, "bold"))
        stock_label.grid(row=3, column=0, columnspan=4, sticky="w", pady=(10,0))

        harga_text = "Harga: " + str(tanaman_info.current_price) + " / tanaman / hari"
        harga_label = tk.Label(self, text=harga_text, font=("Helvetica", 9, "bold"), bg="#FFFFFF")
        harga_label.grid(row=4, column=0, columnspan=4, sticky="w", pady=(0,50))

        atur_jumlah_label = tk.Label(self, text="Atur Jumlah: ",
                                     font=("Helvetica", 9, "bold"), bg="#FFFFFF")
        atur_jumlah_label.grid(row=5, column=0, sticky="w")
        atur_durasi_label = tk.Label(self, text="Durasi (hari): ",
                                     font=("Helvetica", 9, "bold"), bg="#FFFFFF")
        atur_durasi_label.grid(row=6, column=0, sticky="w")

        self.jumlah = tk.StringVar()
        self.durasi = tk.StringVar()
        self.jumlah.set("5")
        self.durasi.set("5")

        jumlah_label = tk.Label(self, textvariable=self.jumlah, bg="#FFFFFF")
        durasi_label = tk.Label(self, textvariable=self.durasi, bg="#FFFFFF")
        tambah_jumlah = tk.Button(self, text="+", font=("Helvetica", "9", "bold"),
                                  bg="#FFFFFF", command=lambda: self.update_jumlah(True))
        kurang_jumlah = tk.Button(self, text="-", font=("Helvetica", "9", "bold"),
                                  bg="#FFFFFF", command=lambda: self.update_jumlah(False))
        tambah_durasi = tk.Button(self, text="+", font=("Helvetica", "9", "bold"),
                                  bg="#FFFFFF", command=lambda: self.update_durasi(True))
        kurang_durasi = tk.Button(self, text="-", font=("Helvetica", "9", "bold"),
                                  bg="#FFFFFF", command=lambda: self.update_durasi(False))

        kurang_jumlah.grid(row=5, column=1, sticky="e")
        jumlah_label.grid(row=5, column=2)
        tambah_jumlah.grid(row=5, column=3, sticky="w")
        kurang_durasi.grid(row=6, column=1, sticky="e")
        durasi_label.grid(row=6, column=2)
        tambah_durasi.grid(row=6, column=3, sticky="w")


        pesan_button = tk.Button(self, text="Pesan", bg='#55A361', fg='#FFFFFF',
                            bd=0, font=("Arial", "12", "bold"), padx=10, pady=7,
                            command=self.pesan)
        back_button = tk.Button(self, text="Kembali", fg='#000000',
                            bd=0, font=("Arial", "11", "bold"), padx=10, pady=7,
                            command=self.kembali)
        pesan_button.grid(row=7, column=0, pady=(20,0), sticky="we")
        back_button.grid(row=8, column=0, pady=(10,0), sticky="we")

        self.plant_image = ImageTk.PhotoImage(Image.open(tanaman_info.image_path).resize(size=(500, 500), resample=Image.NEAREST))
        plant_image_label = tk.Label(self, image=self.plant_image, bg="#FFFFFF")
        plant_image_label.grid(row=0, column=4, rowspan=9, sticky="news")
        self.grid_columnconfigure(4, weight=1)

    def update_jumlah(self, istambah):
        """Mengupdate label jumlah"""
        if istambah:
            self.jumlah.set(str(max(1, int(self.jumlah.get()) + 1)))
        else:
            self.jumlah.set(str(max(1, int(self.jumlah.get()) - 1)))
    def update_durasi(self, istambah):
        """Mengupdate label durasi"""
        if istambah:
            self.durasi.set(str(max(1, int(self.durasi.get()) + 1)))
        else:
            self.durasi.set(str(max(1, int(self.durasi.get()) - 1)))

    def pesan(self):
        """Melakukan pemesanan dan menambahkannya ke database"""
        conn = sqlite3.connect("puspa.db")
        success = False
        while not success:
            try:
                sekarang = datetime.datetime.now()
                id_pesanan = generate_id_pesanan(sekarang)
                conn.execute("INSERT INTO pesanan VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [
                    id_pesanan,
                    self.username,
                    self.item_id,
                    "ONGOING",
                    sekarang.strftime("%Y-%m-%d"),
                    int(self.durasi.get()),
                    int(self.jumlah.get()),
                    self.tanaman_info.current_price
                ])
                success = True
            except sqlite3.OperationalError:
                pass
        conn.execute("UPDATE tanaman SET stock=? WHERE item_id=?;", [
            self.tanaman_info.stock - int(self.jumlah.get()),
            self.item_id
        ])
        self.tanaman_info.stock -= int(self.jumlah.get())
        self.stock_var.set("Stok: " + str(self.tanaman_info.stock))
        info = (f"Pemesanan {self.jumlah.get()} {self.tanaman_info.item_name}" +
                f" selama {self.durasi.get()} hari berhasil!")
        messagebox.showinfo("Pemesanan Berhasil", info)

        conn.commit()
        conn.close()


    def kembali(self):
        """Kembali ke menu sebelumnya/menu utama"""
        # agar pylint tidak marah, kalkulasi hanya placeholder
        # Belum diimplementasikan
        hasil = self.tanaman_info.current_price
        hasil += 10
        return hasil

def generate_id_pesanan(waktu):
    """Menghasilkan id pesanan, memiliki struktur tertentu berdasarkan waktu"""
    idwaktu = waktu.strftime("%M%H%d%m%y")
    angkarandom = randint(100, 999)
    return idwaktu + str(angkarandom)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PUSPA - Pusat Penyewaan Tanaman")
    root.geometry("1280x720")
    root.state("zoomed")
    root.configure(bg="white")
    detail_tanaman_frame = DetailTanaman(root, "bryanahusna", 1)
    detail_tanaman_frame.pack(expand=True, fill="both")
    root.mainloop()
