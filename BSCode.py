from tkinter import *
import subprocess
from platform import system

root = Tk()
root.geometry("350x150")
root.title("BSCode")

if str(system()) == "Darwin" or str(system()) == "Linux":
    python = "python3"
elif str(system()) == "Windows":
    python = "python"

def run_dark():
    subprocess.call([python, "BSCode_dark.py"])


def run_light():
    subprocess.call([python, "BSCode_light.py"])


Label(text="").pack()
Label(text="Welcome to BSCode").pack()
Label(text="").pack()

buttonsFrame = Frame(root)
buttonsFrame.pack()

darkButton = Button(buttonsFrame, text="Dark Mode", command=run_dark)
lightButton = Button(buttonsFrame, text="Light Mode", command=run_light)
darkButton.pack(side=LEFT)
lightButton.pack(side=LEFT)

root.mainloop()