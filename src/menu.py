"""Menu App"""

from User import *
from catalog import *
from edit import Edit
from tkinter import Tk


class MenuApp():
    """Menu App"""

    def __init__(self, ui, username):
        """ Init """
        self.username = username
        self.frame = ui

        self.frame.configure(bg="#f6f9fc")

        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.user()
        self.create_widgets()

    def user(self):
        """ Get user info """
        self.user_info = User(self.username).get_user()

    def create_widgets(self):
        """ Create widgets """
        self.frm_left = tk.Frame(
            self.frame, bg="white", borderwidth=0.5, relief="solid")
        self.frm_left.grid(row=0, column=0, sticky="nsew")

        self.frm_user = tk.Frame(self.frm_left, bg="white")
        self.frm_user.pack(side="top", fill="x", pady=(10, 0))

        img_user = Image.open("item_images/user.png").resize((75, 75))
        photo_user = ImageTk.PhotoImage(img_user)
        img_lbl = tk.Label(self.frm_user, image=photo_user,
                           bg="white", width=75, height=75)
        img_lbl.image = photo_user
        img_lbl.grid(row=0, column=0, pady=(0, 10))

        lbl_username = tk.Label(self.frm_user, bg="white",
                                text=self.user_info[0][0], font=(None, 12))
        lbl_username.grid(row=1, column=0, pady=(0, 5), padx=5)

        lbl_name = tk.Label(self.frm_user, bg="white",
                            text=self.user_info[0][1], font=(None, 12))
        lbl_name.grid(row=2, column=0, pady=(0, 5), padx=5)

        self.frm_menu_button = tk.Frame(self.frm_left)
        self.frm_menu_button.pack()

        self.frm_right = tk.Frame(self.frame, bg="#f6f9fc")
        self.frm_right.grid(row=0, column=1, sticky="nsew")

        self.selected_menu = tk.StringVar(self.frm_menu_button, "1")

        self.menu_values = {
            "Menu and Order": "1",
            "History": "2",
            "Editor": "3",
            "About": "4"
        }

        for menu_name, menu_value in self.menu_values.items():
            btn_menu = tk.Radiobutton(self.frm_menu_button, text=menu_name,
                                      variable=self.selected_menu, value=menu_value, indicator=0,
                                      bg="white", font=(None, 12), activeforeground="#4ec197",
                                      command=self.menu_clicked)
            btn_menu.grid(row=int(menu_value), column=0, sticky="nsew")

        btn_logout = tk.Button(self.frm_left, text="Logout", font=(None, 12),
                               bg="white", command=self.frame.destroy)
        btn_logout.pack(side="bottom", pady=(0, 10))

        # default menu
        Catalog(self.frm_right, self.username)

    def menu_clicked(self):
        """ Menu button clicked """
        edit = None
        if (edit != None):
            edit.img_box.configure(image='')
        for widgets in self.frm_right.winfo_children():
            widgets.destroy()
        if self.selected_menu.get() == "1":
            Catalog(self.frm_right, self.username)
        elif self.selected_menu.get() == "2":
            # b = Riwayat(self.frm_right)
            lbl_dua = tk.Label(self.frm_right, text="riwayat",
                               font=("Arial", 20, "bold"))
            lbl_dua.grid(row=0, column=0)
        elif self.selected_menu.get() == "3":
            edit = Edit(self.frm_right)
            edit.add_plant_ui()
        elif self.selected_menu.get() == "4":
            lbl_empat = tk.Label(self.frm_right, text="About",
                                 font=("Arial", 20, "bold"))
            lbl_empat.grid(row=0, column=0)
        elif self.selected_menu.get() == "5":
            lbl_lima = tk.Label(self.frm_right, text="Logout",
                                font=("Arial", 20, "bold"))
            lbl_lima.grid(row=0, column=0)


if __name__ == "__main__":
    # pass username argument dari login
    ui = Tk()
    ui.title("PUSPA - Pusat Penyewaan Tanaman")
    ui.geometry("1920x1080")
    ui.configure(background='white')
    ui.state('zoomed')
    username = "bob"
    app = MenuApp(ui, username)
    app.frame.mainloop()
