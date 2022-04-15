"""test a tkinter window"""
import tkinter as tk

window = tk.Tk()

greeting = tk.Label(text="Hello, I'm Tkinter.\nNice to meet you!")

greeting.pack()

window.mainloop()


def add(a, b):
    """adds a and b together"""
    return a + b
