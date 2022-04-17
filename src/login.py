from tkinter import *
from tkinter import messagebox as ms
from PIL import Image, ImageTk
import sqlite3

ui = Tk()
ui.title("PUSPA")
ui.geometry("1200x800")
ui.configure(background='white')

db = sqlite3.connect("user.db")
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL, password TEXT NOT NULL, name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL, address TEXT NOT NULL, role DEFAULT 'USER');")
db.commit()
db.close()


class Login:
    def __init__(self):
        global frame
        frame = Frame(ui, bg='white')
        frame.pack(side=TOP, expand=True, fill=BOTH)

    def clear_screen(self):
        for widget in frame.winfo_children():
            widget.destroy()
    
    def login(self):
        db = sqlite3.connect("user.db")
        c = db.cursor()

        find_user = 'SELECT * FROM user WHERE username = ? and password = ?'
        c.execute(find_user, [(login_username.get()), (login_password.get())])

        if login_username.get() == "" or login_password.get() == "":
            ms.showerror("Login Failed", "Username or Password is empty")
        else:
            result = c.fetchall()
            if result:
                role = result[0][6]
                ms.showinfo("Login Success", "Login Successful" + "\n" + "Role: " + role)
                
            else:
                ms.showerror("Login Failed", "Username or Password is incorrect")

    def register(self):
        db = sqlite3.connect("user.db")
        c = db.cursor()

        find_user = 'SELECT * FROM user WHERE username = ?'
        c.execute(find_user, [(username.get())])

        if username.get() == "":
            ms.showerror("Register Failed", "Username is empty")
        elif password.get() == "":
            ms.showerror("Register Failed", "Password is empty")
        elif name.get() == "":
            ms.showerror("Register Failed", "Name is empty")
        elif email.get() == "":
            ms.showerror("Register Failed", "Email is empty")
        elif phone.get() == "":
            ms.showerror("Register Failed", "Phone is empty")
        elif address.get() == "":
            ms.showerror("Register Failed", "Address is empty")
        else:
            result = c.fetchall()
            if result:
                ms.showerror("Register Failed", "Username already exists")
            else:
                c.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?)", (username.get(), password.get(), name.get(), email.get(), phone.get(), address.get(), "USER"))
                ms.showinfo("Register Success", "Register Successful")            
                db.commit()
                db.close()
                self.clear_screen()
                self.login_ui()

    def login_ui(self):
        global login_username
        global login_password

        self.clear_screen()

        login_username = StringVar()
        login_password = StringVar()

        background = ImageTk.PhotoImage(Image.open("background.png"))
        canvas = Canvas(frame, height=800, width=600)
        canvas.create_image(0, 0, anchor=NW, image=background)
        canvas.place(x=600, y=0)

        label1 = Label(frame, text="Login to your account", font=("", 17), pady=10, bg='white')
        label1.place(x=130, y=100)
        label2 = Label(frame, text="Username", font=("", 14), pady=7, bg='white')
        label2.place(x=130, y=150)
        label3 = Label(frame, text="Password", font=("", 14), pady=7, bg='white')
        label3.place(x=130, y=230)

        entry2 = Entry(frame, textvariable=login_username, bd=5, font=("", 14), width=25)
        entry2.place(x=130, y=190)
        entry3 = Entry(frame, textvariable=login_password, bd=5, font=("", 14), width=25, show="*")
        entry3.place(x=130, y=270)

        button1 = Button(frame, text="Login", command=self.login, font=("", 14), width=25)
        button1.place(x=130, y=320)

        label4 = Label(frame, text="Don't have an account?", font=("", 14), pady=10, bg='white')
        label4.place(x=130, y=360)
        label5 = Label(frame, text="Register", font=("", 14), pady=10, fg="#668cff", bg='white')
        label5.place(x=335, y=360)
        label5.bind("<Button-1>", lambda e:self.register_ui())

        frame.mainloop()

    def register_ui(self):
        global username
        global password
        global name
        global email
        global phone
        global address

        self.clear_screen()

        username = StringVar()
        password = StringVar()
        name = StringVar()
        email = StringVar()
        phone = StringVar()
        address = StringVar()

        background = ImageTk.PhotoImage(Image.open("background.png"))
        canvas = Canvas(frame, height=800, width=600)
        canvas.create_image(0, 0, anchor=NW, image=background)
        canvas.place(x=600, y=0)

        label1 = Label(frame, text="Create new account", font=("", 17), pady=10, bg='white')
        label1.place(x=130, y=100)
        label2 = Label(frame, text="Username", font=("", 14), pady=7, bg='white')
        label2.place(x=130, y=150)
        label3 = Label(frame, text="Password", font=("", 14), pady=7, bg='white')
        label3.place(x=130, y=230)
        label4 = Label(frame, text="Name", font=("", 14), pady=7, bg='white')
        label4.place(x=130, y=310)
        label4 = Label(frame, text="Email", font=("", 14), pady=7, bg='white')
        label4.place(x=130, y=390)
        label5 = Label(frame, text="Phone", font=("", 14), pady=7, bg='white')
        label5.place(x=130, y=470)
        label6 = Label(frame, text="Address", font=("", 14), pady=7, bg='white')
        label6.place(x=130, y=550)

        entry2 = Entry(frame, textvariable=username, bd=5, font=("", 14), width=25)
        entry2.place(x=130, y=190)
        entry3 = Entry(frame, textvariable=password, bd=5, font=("", 14), width=25, show="*")
        entry3.place(x=130, y=270)
        entry4 = Entry(frame, textvariable=name, bd=5, font=("", 14), width=25)
        entry4.place(x=130, y=350)
        entry4 = Entry(frame, textvariable=email, bd=5, font=("", 14), width=25)
        entry4.place(x=130, y=430)
        entry5 = Entry(frame, textvariable=phone, bd=5, font=("", 14), width=25)
        entry5.place(x=130, y=510)
        entry6 = Entry(frame, textvariable=address, bd=5, font=("", 14), width=25)
        entry6.place(x=130, y=590)

        button1 = Button(frame, text="Register", command=self.register, font=("", 14), width=25)
        button1.place(x=130, y=640)

        label7 = Label(frame, text="Already have an account?", font=("", 14), pady=10, bg='white')
        label7.place(x=130, y=680)
        label8 = Label(frame, text="Login", font=("", 14), pady=10, fg="#668cff", bg='white')
        label8.place(x=350, y=680)
        label8.bind("<Button-1>", lambda e:self.login_ui())

        frame.mainloop()

if __name__ == "__main__":
    ui = Login()
    ui.login_ui()
