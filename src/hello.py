"""test a tkinter window"""
import tkinter as tk


def add(a, b):
    """adds a and b together"""
    return a + b


def main():
    """main function"""
    window = tk.Tk()
    greeting = tk.Label(text="Hello, I'm Tkinter.\nNice to meet you!")
    greeting.pack()
    window.mainloop()


if __name__ == "__main__":
    main()
