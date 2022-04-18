"""import module"""
from tkinter import Tk, Frame, Label, Entry, Button, StringVar, Canvas, NW, TOP, BOTH
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk

ui = Tk()
ui.title("PUSPA - Pusat Penyewaan Tanaman")
ui.geometry("1920x1080")
ui.configure(background='white')
ui.state('zoomed')

data = sqlite3.connect("user.db")
crsr = data.cursor()
crsr.execute("CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL, password TEXT NOT NULL,\
        name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL, address TEXT NOT NULL,\
        role DEFAULT 'USER');")
data.close()

class Login:
    """class Login"""
    def __init__(self):
        """constructor"""
        self.frame = Frame(ui, bg='white')
        self.frame.pack(side=TOP, expand=True, fill=BOTH)

        self.login_username = StringVar()
        self.login_password = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.name = StringVar()
        self.email = StringVar()
        self.phone = StringVar()
        self.address = StringVar()

    def clear_screen(self):
        """clear ui"""
        for widget in self.frame.winfo_children():
            widget.destroy()

    def login(self):
        """login function"""
        database = sqlite3.connect("user.db")
        cursor = database.cursor()

        find_user = 'SELECT * FROM user WHERE username = ? and password = ?'
        cursor.execute(find_user, [(self.login_username.get()), (self.login_password.get())])

        if self.login_username.get() == "" or self.login_password.get() == "":
            ms.showerror("Login Failed", "Username or Password is empty")
        else:
            result = cursor.fetchall()
            if result:
                role = result[0][6]
                ms.showinfo("Login Success", "Login Successful" + "\n" + "Role: " + role)
                self.clear_screen()
            else:
                ms.showerror("Login Failed", "Username or Password is incorrect")

    def register(self):
        """register function"""
        database = sqlite3.connect("user.db")
        cursor = database.cursor()

        find_user = 'SELECT * FROM user WHERE username = ?'
        cursor.execute(find_user, [(self.username.get())])

        if self.username.get() == "":
            ms.showerror("Register Failed", "Username is empty")
        elif self.password.get() == "":
            ms.showerror("Register Failed", "Password is empty")
        elif self.name.get() == "":
            ms.showerror("Register Failed", "Name is empty")
        elif self.email.get() == "":
            ms.showerror("Register Failed", "Email is empty")
        elif self.phone.get() == "":
            ms.showerror("Register Failed", "Phone is empty")
        elif self.address.get() == "":
            ms.showerror("Register Failed", "Address is empty")
        else:
            result = cursor.fetchall()
            if result:
                ms.showerror("Register Failed", "Username already exists")
            else:
                cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?)",\
                            (self.username.get(), self.password.get(), self.name.get(), \
                            self.email.get(), self.phone.get(), self.address.get(), "USER"))
                ms.showinfo("Register Success", "Register Successful")
                database.commit()
                database.close()
                self.clear_screen()
                self.login_ui()

    def login_ui(self):
        """login ui"""

        self.clear_screen()

        self.login_username = StringVar()
        self.login_password = StringVar()

        background = ImageTk.PhotoImage(Image.open("background.png"))
        canvas = Canvas(self.frame, height=1080, width=1160)
        canvas.create_image(0, 0, anchor=NW, image=background)
        canvas.place(x=760, y=0)

        label1 = Label(self.frame, text="Login to your account", font=("", 27), pady=10, bg='white')
        label1.place(x=200, y=290)
        label2 = Label(self.frame, text="Username", font=("", 17), pady=7, bg='white')
        label2.place(x=200, y=360)
        label3 = Label(self.frame, text="Password", font=("", 17), pady=7, bg='white')
        label3.place(x=200, y=440)

        entry2 = Entry(self.frame, textvariable=self.login_username, bd=5, font=("", 17), width=25)
        entry2.place(x=200, y=400)
        entry3 = Entry(self.frame, textvariable=self.login_password,\
                        bd=5, font=("", 17), width=25, show="*")
        entry3.place(x=200, y=480)

        button1 = Button(self.frame, text="Login", command=self.login,\
                         font=("", 16), width=27)
        button1.place(x=200, y=540)

        label4 = Label(self.frame, text="Don't have an account?", font=("", 16),\
                        pady=10, bg='white')
        label4.place(x=200, y=590)
        label5 = Label(self.frame, text="Register", font=("", 16), pady=10,\
                        fg="#668cff", bg='white')
        label5.place(x=430, y=590)
        label5.bind("<Button-1>", lambda e:self.register_ui())

        self.frame.mainloop()

    def register_ui(self):
        """register ui"""
        self.clear_screen()

        self.username = StringVar()
        self.password = StringVar()
        self.name = StringVar()
        self.email = StringVar()
        self.phone = StringVar()
        self.address = StringVar()

        background = ImageTk.PhotoImage(Image.open("background.png"))
        canvas = Canvas(self.frame, height=1080, width=1160)
        canvas.create_image(0, 0, anchor=NW, image=background)
        canvas.place(x=760, y=0)

        label1 = Label(self.frame, text="Create new account", font=("", 27), pady=10, bg='white')
        label1.place(x=200, y=150)
        label2 = Label(self.frame, text="Username", font=("", 17), pady=7, bg='white')
        label2.place(x=200, y=220)
        label3 = Label(self.frame, text="Password", font=("", 17), pady=7, bg='white')
        label3.place(x=200, y=300)
        label4 = Label(self.frame, text="Name", font=("", 17), pady=7, bg='white')
        label4.place(x=200, y=380)
        label4 = Label(self.frame, text="Email", font=("", 17), pady=7, bg='white')
        label4.place(x=200, y=460)
        label5 = Label(self.frame, text="Phone", font=("", 17), pady=7, bg='white')
        label5.place(x=200, y=540)
        label6 = Label(self.frame, text="Address", font=("", 17), pady=7, bg='white')
        label6.place(x=200, y=620)

        entry2 = Entry(self.frame, textvariable=self.username, bd=5, font=("", 17), width=25)
        entry2.place(x=200, y=260)
        entry3 = Entry(self.frame, textvariable=self.password, bd=5, font=("", 17), width=25,\
                        show="*")
        entry3.place(x=200, y=340)
        entry4 = Entry(self.frame, textvariable=self.name, bd=5, font=("", 17), width=25)
        entry4.place(x=200, y=420)
        entry4 = Entry(self.frame, textvariable=self.email, bd=5, font=("", 17), width=25)
        entry4.place(x=200, y=500)
        entry5 = Entry(self.frame, textvariable=self.phone, bd=5, font=("", 17), width=25)
        entry5.place(x=200, y=580)
        entry6 = Entry(self.frame, textvariable=self.address, bd=5, font=("", 17), width=25)
        entry6.place(x=200, y=660)

        button1 = Button(self.frame, text="Register", command=self.register, font=("", 16),\
                         width=27)
        button1.place(x=200, y=720)

        label7 = Label(self.frame, text="Already have an account?", font=("", 16), pady=10,\
                     bg='white')
        label7.place(x=200, y=770)
        label8 = Label(self.frame, text="Login", font=("", 16), pady=10, fg="#668cff", bg='white')
        label8.place(x=450, y=770)
        label8.bind("<Button-1>", lambda e:self.login_ui())

        self.frame.mainloop()

if __name__ == "__main__":
    ui = Login()
    ui.login_ui()
