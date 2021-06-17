'''
------------------------------

BSCode

Made by:
Jason Li

------------------------------
'''



from tkinter import *
from tkinter import ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from ttkthemes import ThemedTk #pip install ttkthemes
import subprocess
import os
import platform
import webbrowser
import threading



'''
Initialize
------------------------------
'''

root = ThemedTk(theme='equilux')
s = ttk.Style()
root_title = 'BSCode Rewritten Edition'
root.title(root_title)
root.winfo_screenheight()
root.winfo_screenwidth()

root.configure(bg='#464646')
s.configure("Title.TLabel", font=('*', 25), padding=10)
s.configure("Subtitle.TLabel", font=('*', 17), padding=10)

menubar = Menu(root)

compilers = {
    '.py': 'python3',
    '.js': 'node',
    '.swift': 'swift',
}

if str(platform.system()) == 'Windows':
    compilers['.py'] = 'python'

'''
------------------------------
'''



'''
Functions
------------------------------
'''

def addToTree(path, parentiid=''):
    '''
    Creates file tree
    '''
    pathFiles = os.listdir(path)
    for file in pathFiles:
        values = []
        for i in tree.item(parentiid)['values']:
            values.append(i)
        values.append(tree.item(parentiid)['text'])
        tree.insert(parentiid, pathFiles.index(file), f'{parentiid}id{pathFiles.index(file)}', text=file, values=values)
    for file in pathFiles:
        if os.path.isdir(f'{path}/{file}'):
            iid = f'{parentiid}id{pathFiles.index(file)}'
            newDir = f'{path}/{file}'
            threading.Thread(target=lambda:addToTree(newDir, iid)).start()
    tree.bind("<Double-1>", treeClickEvent)


def putToScreen():
    with open(filePathFull) as f:
            content = f.read()
            textInput.delete('1.0', 'end')
            textInput.insert('1.0', content)


def openFileBtnDo():
    '''
    Opens file dialog, user chooses file
    '''
    global filePathName

    openFileDialog = filedialog.askdirectory()
    if str(openFileDialog) != '':
        filePathName = str(openFileDialog)
        root.title(root_title + ' - ' + filePathName)

        # Check if file tree is empty
        if len(tree.get_children()) > 0:
            tree.delete(*tree.get_children())
        addToTree(filePathName)
    
    else:
        messagebox.showerror(title='Error', message='No file opened')


def treeClickEvent(event):
    '''
    Open file when clicked on tree
    '''
    global filePathName, filePathFull

    item = tree.selection()[0]
    clickedFilePath = str(tree.item(item)['text'])
    if tree.item(item)['values']:
        parentDir = ''
        for i in tree.item(item)['values']:
            parentDir = parentDir + i + '/'
        clickedFilePath = str(parentDir + clickedFilePath)
    filePathFull = filePathName + clickedFilePath
    putToScreen()


def runBtnDo():
    '''
    Button to run script
    '''
    global filePathName

    # Clear terminal
    if str(platform.system()) == 'Darwin' or str(platform.system()) == 'Linux':
        os.system('clear')
    elif str(platform.system()) == 'Windows':
        os.system('cls')

    try:
        if filePathFull:
            fileExt = os.path.splitext(filePathFull)[1]
            print(fileExt)
            if fileExt == '.html':
                webbrowser.open_new_tab(f'file://{filePathFull}')
            else:
                subprocess.call([compilers[fileExt], filePathFull])

    except NameError:
        messagebox.showerror(title='Error', message='No file chosen')


def saveBtnDo():
    '''
    Button to save changes to file
    '''
    global filePathName, filePathFull

    if filePathName and filePathFull:
        saveContent = textInput.get(1.0, 'end-1c')
        with open(filePathFull, 'w') as f:
            f.write(saveContent)
        with open(filePathFull) as f:
            content = f.read()
            textInput.delete('1.0', 'end')
            textInput.insert('1.0', content)
        root.title(root_title + ' - ' + filePathFull)
    else:
        messagebox.showerror('Error', 'File not chosen')


def settingsBtnDo():
    '''
    Opens settings
    '''

    def pyInterpreterSaveDo():
        # Overwrite Python interpreter/compiler
        compilers['.py'] = str(pyInterpreterEntry.get())

    def nodeInterpreterSaveDo():
        # Overwrite Node.js interpreter/compiler
        compilers['.js'] = str(nodeInterpreterEntry.get())

    def swiftInterpreterSaveDo():
        # Overwrite Swift interpreter/compiler
        compilers['.swift'] = str(swiftInterpreterEntry.get())

    def fontNameSizeOverwriteDo():
        # Overwrite font name
        global textInput, textInputFont
        textInputFont = [str(fontNameOverwriteEntry.get()), int(fontSizeVar.get())]
        textInput.config(font=(str(fontNameOverwriteEntry.get()), int(fontSizeVar.get())))

    # Initialize settings
    settingsWin = Toplevel()
    settingsWin.title(root_title + ' - Settings')
    settingsWin.configure(bg='#464646')
    settingsTitle = ttk.Label(settingsWin, text='Settings', style='Title.TLabel')
    settingsTitle.pack()

    # Create section to overwrite compiler
    compilerOverwriteFrame = ttk.Frame(settingsWin)
    compilerOverwriteFrame.pack()
    compilerOverwriteTitle = ttk.Label(compilerOverwriteFrame, text='Overwrite default compiler/interpreter', style='Subtitle.TLabel')
    compilerOverwriteTitle.pack()

    # Python overwrite
    pyInterpreterFrame = ttk.Frame(compilerOverwriteFrame)
    pyInterpreterFrame.pack()
    pyInterpreterTitle = ttk.Label(pyInterpreterFrame, text='Python: ')
    pyInterpreterTitle.pack(side=LEFT)
    pyInterpreterEntry = ttk.Entry(pyInterpreterFrame)
    pyInterpreterEntry.insert(1, compilers['.py'])
    pyInterpreterEntry.pack(side=LEFT)
    pyInterpreterSave = ttk.Button(pyInterpreterFrame, text='Save', command=pyInterpreterSaveDo)
    pyInterpreterSave.pack()

    # Node.js overwrite
    nodeInterpreterFrame = ttk.Frame(compilerOverwriteFrame)
    nodeInterpreterFrame.pack()
    nodeInterpreterTitle = ttk.Label(nodeInterpreterFrame, text='Node.js: ')
    nodeInterpreterTitle.pack(side=LEFT)
    nodeInterpreterEntry = ttk.Entry(nodeInterpreterFrame)
    nodeInterpreterEntry.insert(1, compilers['.js'])
    nodeInterpreterEntry.pack(side=LEFT)
    nodeInterpreterSave = ttk.Button(nodeInterpreterFrame, text='Save', command=nodeInterpreterSaveDo)
    nodeInterpreterSave.pack()

    # Swift overwrite
    swiftInterpreterFrame = ttk.Frame(compilerOverwriteFrame)
    swiftInterpreterFrame.pack()
    swiftInterpreterTitle = ttk.Label(swiftInterpreterFrame, text='Swift: ')
    swiftInterpreterTitle.pack(side=LEFT)
    swiftInterpreterEntry = ttk.Entry(swiftInterpreterFrame)
    swiftInterpreterEntry.insert(1, compilers['.swift'])
    swiftInterpreterEntry.pack(side=LEFT)
    swiftInterpreterSave = ttk.Button(swiftInterpreterFrame, text='Save', command=swiftInterpreterSaveDo)
    swiftInterpreterSave.pack()



    # Create section to overwrite font
    fontOverwriteFrame = ttk.Frame(settingsWin)
    fontOverwriteFrame.pack()
    fontOverwriteTitle = ttk.Label(fontOverwriteFrame, text='Overwrite default font', style='Subtitle.TLabel')
    fontOverwriteTitle.pack()

    # Font name + size overwrite
    fontNameSizeOverwriteFrame = ttk.Frame(fontOverwriteFrame)
    fontNameSizeOverwriteFrame.pack()
    fontNameOverwriteEntry = ttk.Entry(fontNameSizeOverwriteFrame)
    fontNameOverwriteEntry.insert(1, textInputFont[0])
    fontNameOverwriteEntry.pack(side=LEFT)
    fontSizeVar = StringVar()
    fontSizeOverwriteOptions = [str(textInputFont[1])]
    for i in range(1, 1001):
        fontSizeOverwriteOptions.append(str(i))
    fontSizeVar.set(str(textInputFont[1]))
    fontSizeOverwriteEntry = ttk.OptionMenu(fontNameSizeOverwriteFrame, fontSizeVar, *fontSizeOverwriteOptions)
    fontSizeOverwriteEntry.pack(side=LEFT)
    fontNameSizeOverwriteSave = ttk.Button(fontNameSizeOverwriteFrame, text='Save', command=fontNameSizeOverwriteDo)
    fontNameSizeOverwriteSave.pack(side=LEFT)


'''
------------------------------
'''



'''
Main Layout
------------------------------
'''

# Title
titleFrame = ttk.Frame(root)
titleFrame.pack()
titleLab = ttk.Label(titleFrame, text="BSCode", style='Title.TLabel')
titleLab.pack()



# Create section for buttons
btnFrame = ttk.Frame(root, padding=(30, 10))
btnFrame.pack()

# Open file button
openFileBtn = ttk.Button(btnFrame, text='Open', command=openFileBtnDo)
openFileBtn.pack(side=LEFT)

# Run button
runBtn = ttk.Button(btnFrame, text='Run in terminal', command=runBtnDo)
runBtn.pack(side=LEFT)

# Save button
saveBtn = ttk.Button(btnFrame, text='Save', command=saveBtnDo)
saveBtn.pack(side=LEFT)

# Settings button
settingsBtn = ttk.Button(btnFrame, text='Settings', command=settingsBtnDo)
settingsBtn.pack(side=LEFT)


# File tree
tree = ttk.Treeview(root, height=30)
tree.pack(side=LEFT)



# Text editor + Scroll bar
textInputFrame = ttk.Frame(root)
textInputFrame.pack(side=LEFT)
if str(platform.system()) == 'Windows':
    textInputWidth = 120
    textInputHeight = 30
else:
    textInputWidth = 180
    textInputHeight = 40
scrollbar = Scrollbar(textInputFrame)
scrollbar.pack(side=RIGHT, fill=Y)
textInput = Text(textInputFrame, bg='#555555', fg='#F7F7F7', width=textInputWidth, height=textInputHeight, yscrollcommand=scrollbar.set)
if str(platform.system()) == 'Darwin':
    textInputFont = ('Monaco', 12)
elif str(platform.system()) == 'Windows' or str(platform.system()) == 'Linux':
    textInputFont = ('Courier New', 12)
textInput.insert(1.0, 'Welcome to the new version of BSCode!\n\nTo open a file, click "Open"\nTo change settings, click "Settings"\nTo run your file, click "Run in terminal"')
textInput.configure(font=textInputFont)
textInput.pack(side=LEFT)
scrollbar.config(command=textInput.yview)

'''
------------------------------
'''



'''
Menubar
------------------------------
'''

# Menubar shrortcuts
if str(platform.system()) == 'Darwin':
    openShortcut = 'Cmd+O'
    newShortcut = 'Cmd+N'
    saveShortcut = 'Cmd+S'
    runShortcut = 'Cmd+R'
elif str(platform.system()) == 'Windows' or str(platform.system()) == 'Linux':
    openShortcut = 'Ctrl+O'
    newShortcut = 'Ctrl+N'
    saveShortcut = 'Ctrl+S'
    runShortcut = 'Ctrl+R'

# Add File menubar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Open', command=openFileBtnDo, accelerator=openShortcut)
filemenu.add_command(label='Save', command=saveBtnDo, accelerator=saveShortcut)
menubar.add_cascade(label='File', menu=filemenu)

# Add Run menubar
runmenu = Menu(menubar, tearoff=0)
runmenu.add_command(label='Run', command=runBtnDo, accelerator=runShortcut)
menubar.add_cascade(label='Run', menu=runmenu)

'''
------------------------------
'''



# Run
if __name__ == '__main__':
    root.config(menu=menubar)
    root.mainloop()
