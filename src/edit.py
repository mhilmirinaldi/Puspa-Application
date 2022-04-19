""" Module for editing plants and its UI"""
from tkinter import Tk, Frame, Label, Entry, Button, StringVar, IntVar, messagebox, filedialog, TOP, BOTH, WORD, END, INSERT
from tkinter.scrolledtext import ScrolledText
import sqlite3
from PIL import Image, ImageTk


class Edit:
    """class Edit"""

    def __init__(self, frm_parent):
        """constructor"""
        self.frm_parent = frm_parent
        self.frame = Frame(self.frm_parent, bg="#f6f9fc")
        self.frame.pack(side=TOP, expand=True, fill=BOTH)

        self.item_id = IntVar()
        self.item_name = StringVar()
        self.current_price = IntVar()
        self.description = StringVar()
        self.stock = IntVar()
        self.image_path = StringVar()
        self.desc_box = ScrolledText()
        self.img_box = Label()

    def clear_screen(self):
        """clear ui"""
        for widget in self.frame.winfo_children():
            widget.destroy()

    def open_file(self):
        """file open function"""
        self.image_path.set(filedialog.askopenfilename(title='Select Image', filetypes=(
            ("jpeg files", "*.jpg"), ("png files", "*.png"))))

        plant_img = ImageTk.PhotoImage(Image.open(self.image_path.get()))
        self.img_box.configure(image=plant_img)
        self.img_box.image = plant_img

    def edit_plant(self):
        """edit plant function"""
        self.description.set(self.desc_box.get("1.0", END))
        database = sqlite3.connect("puspa.db")
        cursor = database.cursor()

        find_plant = 'SELECT * FROM tanaman WHERE item_id = ?'
        cursor.execute(find_plant, [(self.item_id.get())])

        if self.item_name.get() == "":
            messagebox.showerror("Add Failed", "Name is empty")
        elif self.current_price.get() == "":
            messagebox.showerror("Add Failed", "Price is empty")
        elif self.stock.get() == "":
            messagebox.showerror("Add Failed", "Stock is empty")
        elif self.image_path == "":
            messagebox.showerror("Add Failed", "Image is empty")
        else:
            cursor.execute("UPDATE tanaman SET item_name = ?, current_price = ?, description = ?, stock = ?, image_path = ? WHERE item_id = ?", (
                self.item_name.get(), self.current_price.get(), self.description.get(), self.stock.get(), self.image_path.get(), self.item_id.get()))
            messagebox.showinfo("Add Success", "Add Successful")
            database.commit()
            database.close()

    def delete_plant(self):
        """delete current plant from database"""
        database = sqlite3.connect("puspa.db")
        cursor = database.cursor()

        find_plant = 'SELECT * FROM tanaman WHERE item_id = ?'
        cursor.execute(find_plant, [(self.item_id.get())])

        result = cursor.fetchall()
        if result:
            cursor.execute("DELETE FROM tanaman WHERE item_id = ?", [
                           (self.item_id.get())])
            messagebox.showinfo("Delete Success", "Delete Successful")
            database.commit()
            database.close()
        else:
            messagebox.showerror("Delete Failed", "Plant not found")

    def add_plant(self):
        """add plant function"""
        self.description.set(self.desc_box.get("1.0", END))
        database = sqlite3.connect("puspa.db")
        cursor = database.cursor()

        find_plant = 'SELECT * FROM tanaman WHERE item_id = ?'
        cursor.execute(find_plant, [(self.item_id.get())])

        if self.item_name.get() == "":
            messagebox.showerror("Add Failed", "Name is empty")
        elif self.current_price.get() == "":
            messagebox.showerror("Add Failed", "Price is empty")
        elif self.stock.get() == "":
            messagebox.showerror("Add Failed", "Stock is empty")
        elif self.image_path.get() == "":
            messagebox.showerror("Add Failed", "Image is empty")
        else:
            result = cursor.fetchall()
            if result:
                messagebox.showerror("Add Failed", "Plant already exists")
            else:
                cursor.execute("INSERT INTO tanaman (item_name, current_price, description, stock, image_path) VALUES (?, ?, ?, ?, ?)", (
                    self.item_name.get(), self.current_price.get(), self.description.get(), self.stock.get(), self.image_path.get()))
                messagebox.showinfo("Add Success", "Add Successful")
                database.commit()
                database.close()

    def edit_plant_ui(self, item_id):
        """edit plant ui"""
        self.clear_screen()
        self.item_id.set(item_id)

        database = sqlite3.connect("puspa.db")
        cursor = database.cursor()
        find_plant = 'SELECT * FROM tanaman WHERE item_id = ?'
        cursor.execute(find_plant, [(self.item_id.get())])
        result = cursor.fetchall()
        self.item_name.set(result[0][1])
        self.current_price.set(result[0][2])
        self.description.set(result[0][3])
        self.stock.set(result[0][4])
        self.image_path.set(result[0][5])
        database.close()

        plant_img = ImageTk.PhotoImage(Image.open(self.image_path.get()))
        self.img_box.configure(image=plant_img)
        self.img_box.image = plant_img

        label_title = Label(self.frame, text="Edit Tanaman",
                            font=("", 18), pady=7, bg='#f6f9fc')
        label_title.place(x=130, y=20)

        label2 = Label(self.frame, text="File Gambar:",
                       font=("", 14), pady=7, bg='#f6f9fc')
        label2.place(x=130, y=110)
        button0 = Button(self.frame, text='Select Image',
                         command=self.open_file)
        button0.place(x=240, y=115)

        label2 = Label(self.frame, text="Nama Tanaman:",
                       font=("", 14), pady=7, bg='#f6f9fc')
        label2.place(x=130, y=150)
        entry2 = Entry(self.frame, textvariable=self.item_name,
                       bd=5, font=("", 14), width=25)
        entry2.place(x=130, y=190)

        label3 = Label(self.frame, text="Deskripsi:",
                       font=("", 14), pady=7, bg='#f6f9fc')
        label3.place(x=130, y=230)
        self.desc_box = ScrolledText(
            self.frame, wrap=WORD, width=50, height=100, )
        self.desc_box.place(x=130, y=270, height=100)
        self.desc_box.insert(INSERT, chars=self.description.get())

        label4 = Label(self.frame, text="Stock:",
                       font=("", 14), pady=7, bg='#f6f9fc')
        label4.place(x=130, y=400)
        entry4 = Entry(self.frame, textvariable=self.stock,
                       bd=5, font=("", 14), width=5)
        entry4.place(x=200, y=400)

        label5 = Label(self.frame, text="Harga:              /Tanaman/Hari",
                       font=("", 14), pady=7, bg='#f6f9fc')
        label5.place(x=130, y=450)
        entry5 = Entry(self.frame, textvariable=self.current_price,
                       bd=5, font=("", 14), width=5)
        entry5.place(x=200, y=450)

        label5 = Label(self.frame, text="Gambar akan muncul disini",
                       font=("", 14), pady=7, bg='#f6f9fc')
        label5.place(x=550, y=50)

        self.img_box = Label(self.frame, bg='#f6f9fc')
        self.img_box.place(x=550, y=50)

        button1 = Button(self.frame, text="Edit", command=self.edit_plant, font=("", 14),
                         width=25, bg='green', fg='#f6f9fc')
        button1.place(x=130, y=600)

        button1 = Button(self.frame, text="Delete", command=self.delete_plant, font=("", 14),
                         width=25, bg='red', fg='#f6f9fc')
        button1.place(x=130, y=650)

        self.frame.mainloop()

    def add_plant_ui(self):
        """ui for adding plants"""
        self.clear_screen()
        label_title = Label(self.frame, text="Tambah Tanaman",
                            font=("", 20), pady=7, bg='#f6f9fc')
        label_title.place(x=130, y=50)

        label2 = Label(self.frame, text="File Gambar:",
                       font=("", 14), pady=7, bg='#f6f9fc')
        label2.place(x=130, y=110)
        button0 = Button(self.frame, text='Select Image',
                         command=self.open_file)
        button0.place(x=240, y=115)

        label2 = Label(self.frame, text="Nama Tanaman:",
                       font=("", 14), pady=7, bg='#f6f9fc')
        label2.place(x=130, y=150)
        entry2 = Entry(self.frame, textvariable=self.item_name,
                       bd=5, font=("", 14), width=25)
        entry2.place(x=130, y=190)

        label3 = Label(self.frame, text="Deskripsi:",
                       font=("", 14), pady=7, bg='#f6f9fc')
        label3.place(x=130, y=230)
        self.desc_box = ScrolledText(
            self.frame, wrap=WORD, width=50, height=100)
        self.desc_box.place(x=130, y=270, height=100)

        label4 = Label(self.frame, text="Stock:",
                       font=("", 14), pady=7, bg='#f6f9fc')
        label4.place(x=130, y=400)
        entry4 = Entry(self.frame, textvariable=self.stock,
                       bd=5, font=("", 14), width=5)
        entry4.place(x=200, y=400)

        label5 = Label(self.frame, text="Harga:              /Tanaman/Hari",
                       font=("", 14), pady=7, bg='#f6f9fc')
        label5.place(x=130, y=450)
        entry5 = Entry(self.frame, textvariable=self.current_price,
                       bd=5, font=("", 14), width=5)
        entry5.place(x=200, y=450)

        label5 = Label(self.frame, text="Gambar akan muncul disini",
                       font=("", 14), pady=7, bg='#f6f9fc')
        label5.place(x=550, y=50)

        self.img_box = Label(self.frame, bg='#f6f9fc')
        self.img_box.place(x=550, y=50)

        button1 = Button(self.frame, text="Tambah", command=self.add_plant, font=("", 14),
                         width=25, bg='green', fg='#f6f9fc')
        button1.place(x=130, y=600)

        self.frame.mainloop()


if __name__ == "__main__":
    edit = Edit(ui)
    edit.add_plant_ui()
    # edit.edit_plant_ui(14)
