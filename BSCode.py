from tkinter import *
import subprocess
import platform

root = Tk()
root.geometry("350x150")
root.title("BSCode")

def run_dark():
    if str(platform.system()) == "Darwin" or str(platform.system()) == "Linux":
        try:
            subprocess.call(["python3", "BSCode_dark.py"])
            print('1')
        except:
            subprocess.call(["python3", "BSCode_dark.py"])
            print('2')
    elif str(platform.system()) == "Windows":
        subprocess.call(["python", "BSCode_dark.py"])


def run_light():
    if str(platform.system()) == "Darwin" or str(platform.system()) == "Linux":
        try:
            subprocess.call(["python3", "BSCode_light.py"])
        except:
            subprocess.call(["python", "BSCode_light.py"])
    elif str(platform.system()) == "Windows":
        subprocess.call(["python", "BSCode_light.py"])


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