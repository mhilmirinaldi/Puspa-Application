""" Main program """
from tkinter import Tk
import login
import initialize_db as init_db


def main():
    """ Main program function"""
    ui = Tk()
    ui.title("PUSPA - Pusat Penyewaan Tanaman")
    ui.geometry("1920x1080")
    ui.configure(background='white')
    ui.state('zoomed')

    init_db.init_db()
    login_ui = login.Login(ui)
    login_ui.login_ui()


if __name__ == "__main__":
    main()
