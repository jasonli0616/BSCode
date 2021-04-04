from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pynput.keyboard import Key, Controller
import subprocess
from platform import system

# initialize
root = Tk()
keyboard = Controller()
root.winfo_screenheight()
root.winfo_screenwidth()
root.title("BSCode")
style = ttk.Style(root)
root.tk.call('source', 'files/lightmode/azure.tcl')
style.theme_use('azure')

if str(system()) == "Darwin" or str(system()) == "Linux":
    python = "python3"
elif str(system()) == "Windows":
    python = "python"

bgColorStr = "#EFEFEF"
fileChosen = False

# clears shell output txt file
f = open("output.txt", "w")
f.write("")
f.close()

credit = ttk.Label(root, text="BSCode   © Bot Master 2021")
credit.config(font=('*', 15))
credit.pack()

text_input = Text(root, bg=bgColorStr, fg='#F7F7F7', width=200, height=30)
text_input.configure(font=("Courier", 12))
text_input.pack()

buttonFrame = Frame(root)
buttonFrame.pack()

output = Label()

OutputLabel = Label()

# autocomplete bracket, colon
def on_press(key):
    if key.keysym == 'parenleft':
        keyboard.press(')')
        keyboard.press(Key.left)
        keyboard.release(')')
        keyboard.release(Key.left)
    if key.keysym == 'colon':
        keyboard.press(Key.enter)
        keyboard.press(' ')
        keyboard.press(' ')
        keyboard.press(' ')
        keyboard.press(' ')
        keyboard.release(Key.enter)
        keyboard.release(' ')
        keyboard.release(' ')
        keyboard.release(' ')
        keyboard.release(' ')

def open_file():
    global pyFile
    pyFile = filedialog.askopenfilename(filetypes=[("Python files", ".py")])
    return pyFile

def new_file():
    def new_file_save_func():
        global pyFile, fileChosen
        newFileName.destroy()
        pyExtensionLabel.destroy()
        newFileSave.destroy()
        FileName = str(fileName.get() + ".py")
        fileWrite = open(FileName, "w")
        fileChosen = True
        pyFile = FileName
    fileName = StringVar()
    newFileName = ttk.Entry(buttonFrame, textvariable=fileName)
    newFileName.pack(side=LEFT)
    pyExtensionLabel = Label(buttonFrame, text=".py")
    pyExtensionLabel.pack(side=LEFT)
    newFileSave = ttk.Button(buttonFrame, text="Save", command=new_file_save_func)
    newFileSave.pack(side=LEFT)


def runfunc(pyFile):
    clearshell()
    global OutputLabel
    text_input_text = text_input.get("1.0",END)
    f = open(pyFile, "w")
    f.write(text_input_text)
    f.close()
    subprocess.call([python, pyFile])
    #Get console output here
    with open("output.txt", "w") as output:
        subprocess.call([python, pyFile], stdout=output)
    output = open("output.txt", "r")
    outputstr = output.read()
    OutputLabel.destroy()
    OutputLabel = Label(consoleFrame, text=outputstr, bg="#666666")
    OutputLabel.config(font=("Courier", 12))
    OutputLabel.pack(side=LEFT)

def run_button_func():
    global pyFile, fileChosen
    if fileChosen == False:
        runfunc(open_file())
        fileChosen = True
    elif fileChosen == True:
        runfunc(pyFile)

def clearshell():
    if fileChosen == False:
        def ok_button_func():
            errorWindow.destroy()
        errorWindow = Toplevel()
        errorWindow.geometry("270x100")
        errorLabel = Label(errorWindow, text="Error, no file selected")
        errorLabel.pack()
        okButton = ttk.Button(errorWindow, text="OK", command=ok_button_func)
        okButton.pack()
    else:
        global OutputLabel, pyFile
        OutputLabel.destroy()
        f = open(pyFile, "w")
        f.write("")
        f.close()

def cleartext():
    if fileChosen == False:
        def okButtonFunc():
            errorWindow.destroy()
        errorWindow = Toplevel()
        errorWindow.geometry("270x100")
        errorLabel = Label(errorWindow, text="Error, no file selected")
        errorLabel.pack()
        okButton = ttk.Button(errorWindow, text="OK", command=okButtonFunc)
        okButton.pack()
    else:
        text_input.delete(1.0, END)


printButton = ttk.Button(buttonFrame, text='Run', command=run_button_func)
printButton.pack(side=LEFT)
Label(buttonFrame).pack(side=LEFT)
cleartextButton = ttk.Button(buttonFrame, text='Clear text', command=cleartext)
cleartextButton.pack(side=LEFT)
Label(buttonFrame).pack(side=LEFT)
clearshellButton = ttk.Button(buttonFrame, text='Stop/Clear shell', command=clearshell)
clearshellButton.pack(side=LEFT)
Label(buttonFrame).pack(side=LEFT)
Label(buttonFrame).pack(side=LEFT)
newPyButton = ttk.Button(buttonFrame, text='New .py file', command=new_file)
newPyButton.pack(side=LEFT)

consoleFrame = Frame(root, highlightthickness=1, highlightbackground='black', height=300, width=1350, bg=bgColorStr)
consoleFrame.pack_propagate(FALSE)
consoleFrame.pack()
Label(root).pack()

root.bind('<KeyPress>', on_press)

def on_closing():
    f = open("output.txt", "w")
    f.write("")
    f.close()
    quit()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
