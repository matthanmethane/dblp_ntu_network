
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import project

class File:
    def __init__(self):
        self.filename = ""

    def get(self):
        return self.filename

    def set(self, arg):
        self.filename = arg


def openfile():
    file.set(askopenfilename())
    Label(root, text=file.get()).grid(row=1, column=2)


def no_file_alert():
    messagebox.showerror("Error", "No file selected")


def start():
    if file.get() == "":
        no_file_alert()
    else:
        project.main(file.filename)


root = Tk()
root.geometry("400x300")
root.title("DBLP Network Analysis")

file = File()

openfile_btn = Button(root, text ="Select File...", command=openfile).grid(row=1, column=1)
Label(root, text="No file selected!").grid(row=1, column=2)

start_btn = Button(root, text ="    Start    ", command=start).grid(row=2, column=1)


root.mainloop()
