"""Menu Catalog"""

import tkinter as tk
from PIL import Image, ImageTk
from Tanaman import *
from edit import *
from pemesanan import *


def edit_tanaman(frm, id_item):
    """edit tanaman function"""
    for widgets in frm.winfo_children():
        widgets.destroy()
    edit = Edit(frm)
    edit.edit_plant_ui(id_item)


def selengkapnya(frm, item_id, username):
    """Menampilkan halaman selengkapnya"""
    for widgets in frm.winfo_children():
        widgets.destroy()
    detail_tanaman_frame = DetailTanaman(frm, username, item_id)
    detail_tanaman_frame.pack(expand=True, fill="both")


class TanamanGuiEntry(tk.LabelFrame):
    """Berisi Suatu Entri Tanaman"""

    def __init__(self, master, bg="#FFFFFF", padx=0, pady=0) -> None:
        super().__init__(master=master, padx=padx, pady=pady, bg=bg)
        self.tanaman = None
        self.plant_image = None

    def set_tanaman(self, tanaman):
        """Mengeset tanaman pada entri GUI ini"""
        self.tanaman = tanaman

    @staticmethod
    def generate(master, tanaman, is_admin, prev_frame, username):
        """Menghasilkan tanamanGuiEntry baru"""
        pge = TanamanGuiEntry(master, padx=10, pady=10)
        pge.set_tanaman(tanaman)

        # row image
        pge.plant_image = ImageTk.PhotoImage(
            Image.open(tanaman.image_path).resize((125, 125)))
        plant_image_label = tk.Label(pge, image=pge.plant_image, bg="#FFFFFF")
        plant_image_label.grid(row=0, column=0, columnspan=2, sticky="nwes")

        # nama tanaman bold
        plant_name_label = tk.Label(
            pge, text=tanaman.name, bg="#FFFFFF", font=(None, 12, "bold"))
        plant_name_label.grid(row=1, column=0, sticky="w", pady=(10, 0))

        # harga
        tk.Label(pge, text="Harga:", bg="#FFFFFF").grid(
            row=2, column=0, sticky="w")
        tk.Label(pge, text=tanaman.current_price, bg="#FFFFFF").grid(
            row=3, column=0, sticky="w")

        # stok
        tk.Label(pge, text="Stok:", bg="#FFFFFF").grid(
            row=2, column=1, sticky="w")
        tk.Label(pge, text=tanaman.stock, bg="#FFFFFF").grid(
            row=3, column=1, sticky="w")

        if not is_admin:
            # selengkapnya
            btn_selengkapnya = tk.Button(pge, text="Selengkapnya", bg="green", fg="white",
                                        command=lambda: selengkapnya(prev_frame, tanaman.item_id, username))
            btn_selengkapnya.grid(row=4, column=0, columnspan=2, sticky="ew")

        if is_admin:
            # edit
            btn_edit = tk.Button(pge, text="Edit", bg="blue", fg="white",
                                 command=lambda: edit_tanaman(prev_frame, tanaman.item_id))
            btn_edit.grid(row=5, column=0, columnspan=2, sticky="ew")

        return pge


class Catalog():
    """catalog UI"""

    def __init__(self, master, is_admin, username):
        """Inisialisasi catalog"""
        self.username = username
        self.master = master
        self.is_admin = is_admin
        self.create_widgets()

    def create_widgets(self):
        """membuat widget"""
        # Konfigurasi Scrollbar
        catalog_canvas = tk.Canvas(self.master)
        catalog_scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL,
                                         command=catalog_canvas.yview)
        catalog_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        catalog_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        def _on_mouse_wheel(event):
            catalog_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
        catalog_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        # Membuat frame catalog dan memasukkannya ke scrollbar canvas
        catalog_frame = tk.LabelFrame(
            catalog_canvas, text="Daftar catalog", bg="#FFFFFF")
        catalog_frame.bind(
            "<Configure>",
            lambda e: catalog_canvas.configure(
                scrollregion=catalog_canvas.bbox("all"))
        )
        catalog_frame_id = catalog_canvas.create_window(
            (0, 0), window=catalog_frame, anchor="nw")
        catalog_canvas.configure(yscrollcommand=catalog_scrollbar.set)
        catalog_canvas.bind(
            "<Configure>",
            lambda e: catalog_canvas.itemconfig(
                catalog_frame_id, width=e.width)
        )

       #  Mengambil data dari database dan memasukkannya ke frame
        results = get_all_tanaman()
        total_column = 7
        i = 0
        j = 0
        for tanaman in results:
            pge = TanamanGuiEntry.generate(
                catalog_frame, tanaman, self.is_admin, self.master, self.username)
            pge.grid(row=i, column=j,  padx=10, pady=10, sticky="ew")
            if j == total_column - 1:
                i += 1
            j = (j + 1) % total_column
