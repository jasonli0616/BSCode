from tkinter import *
from tkinter import ttk as ttk
from tkinter.filedialog import askopenfilename, askopenfile, askdirectory, asksaveasfile
from ttkthemes import ThemedTk
import subprocess
import os
import platform
import webbrowser



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

compilers = {
    '.py': 'python3',
    '.js': 'node',
    '.swift': 'swift',
}

fileChosen = False
fileSaved = False
fileLastSave = ''

'''
------------------------------
'''



'''
Functions
------------------------------
'''

def newWin(
        winSize='350x200',
        title='', content1='', content2='', content3='', content4='',
        button1txt='', button1cmd='',
        button2txt='', button2cmd=''
    ):
    '''
    Creates popup window with error/success message
    This takes arguments for window size + title + content (text) + buttons
    '''
    newWin = Toplevel()
    newWin.configure(bg='#464646')
    newWin.geometry(winSize)
    if title != '':
        winTitleLab = ttk.Label(newWin, text=title, style="Subtitle.TLabel")
        winTitleLab.pack()
    if content1 != '':
        winLab1 = ttk.Label(newWin, text=content1, padding=5)
        winLab1.pack()
    if content2 != '':
        winLab2 = ttk.Label(newWin, text=content2, padding=5)
        winLab2.pack()
    if content3 != '':
        winLab3 = ttk.Label(newWin, text=content3, padding=5)
        winLab3.pack()
    if content4 != '':
        winLab4 = ttk.Label(newWin, text=content4, padding=5)
        winLab4.pack()
    if button1txt != '' and button1cmd != '':
        winBtn1 = ttk.Button(newWin, text=button1txt, command=button1cmd)
        winBtn1.pack()
    if button2txt != '' and button1cmd != '':
        winBtn2 = ttk.Button(newWin, text=button2txt, command=button2cmd)
        winBtn2.pack()


def key_press(event):
    '''
    On key press event

    '''
    if str(platform.system()) == 'Darwin':
        if str(event.state) == '8' and str(event.char) == 's':
            saveBtnDo()

        if str(event.state) == '8' and str(event.char) == 'r':
            runBtnDo()

    elif str(platform.system()) == 'Linux' or str(platform.system()) == 'Windows':
        if str(event.state) == 'Control' and str(event.keysym) == 's':
            saveBtnDo()

        if str(event.state) == 'Control' and str(event.keysym) == 'c':
            runBtnDo()

    if str(event.char) == '(':
        textInput.insert(INSERT, ')')

    if str(event.char) == '[':
        textInput.insert(INSERT, ']')

    if str(event.char) == '{':
        textInput.insert(INSERT, '}')

    if str(event.char) == '\'':
        textInput.insert(INSERT, '\'')

    if str(event.char) == '"':
        textInput.insert(INSERT, '"')

    checkIsSaved()


def checkIsSaved():
    '''
    Check if file is saved
    '''
    global fileSaved, fileLastSave

    try:
        if fileLastSave != textInput.get(1.0, 'end-1c'):
            root.title(root_title + ' - ' + fileName + '*')
        else:
            root.title(root_title + ' - ' + fileName)
    except NameError:
        saveNewFileDo()


def saveNewFileDo():
    '''
    Saves new file
    '''
    global fileName, filePath, filePathName, fileExt, fileChosen, fileSaved

    savefileDialog = asksaveasfile(title='Save this file', initialdir='/', initialfile='Untitled.txt', defaultextension='.txt', filetypes=[('Text file', '*.txt'), ('Python', '*.py'), ('Node.js', '*.js'), ('Swift', '*.swift'), ('HTML', '*.html'), ('CSS', '*.css')])
    fileName = str(os.path.split(savefileDialog)[1])
    filePath = str(os.path.split(savefileDialog)[0])
    filePathName = str(savefileDialog)
    fileExt = str(os.path.splitext(fileName)[1])


def openFileBtnDo():
    '''
    Opens file dialog, user chooses file
    '''
    global fileName, filePath, filePathName, fileExt, fileChosen, fileSaved, fileLastSave

    openFileDialog = askopenfilename(title='Select file to open', initialdir='/', filetypes=[('Text file', '*.txt'), ('Python', '*.py'), ('Node.js', '*.js'), ('Swift', '*.swift'), ('HTML', '*.html'), ('CSS', '*.css')])
    fileName = str(os.path.split(openFileDialog)[1])
    filePath = str(os.path.split(openFileDialog)[0])
    filePathName = str(openFileDialog)
    fileExt = str(os.path.splitext(fileName)[1])
    root.title(root_title + ' - ' + fileName)
    fileChosen = True
    fileSaved = True

    with open(filePathName) as f:
        content = f.read()
        textInput.delete('1.0', 'end')
        textInput.insert('1.0', content)
        fileLastSave = content


def runBtnDo():
    '''
    Button to run script
    '''
    global fileName, filePath, filePathName, fileExt, compilers, fileChosen, fileSaved

    # Clear terminal
    if str(platform.system()) == 'Darwin' or str(platform.system()) == 'Linux':
        subprocess.call(['clear'])
    elif str(platform.system()) == 'Windows':
        subprocess.call(['cls'])

    # Initialize
    noRun = False
    errorReason = ''
    runList = []

    # Catches errors
    if fileChosen == False:
        newWin(
            title='Error:',
            content1='No file chosen',
        )
    elif fileSaved == False:
        saveBtnDo()
        runBtnDo()

    elif fileExt == '.css' or fileExt == '.txt':
        noRun = True
        errorReason = f'This is a {fileExt} file'

    # Run file in terminal (or web browser for .html)
    else:
        if str(platform.system()) == 'Windows':
            compilers['.py'] = 'python'

        if fileExt != '.html':
            runList.append(compilers[fileExt])

        runList.append(fileName)

        if noRun == False and fileExt != '.html':
            subprocess.call(runList, cwd=filePath)
        elif noRun == False and fileExt == '.html':
            webbrowser.open_new_tab('file://' + filePathName)
        else:
            newWin(
                title='Error:',
                content1=errorReason,
            )


def saveBtnDo():
    '''
    Button to save changes to file
    '''
    global fileName, filePath, filePathName, fileExt, fileChosen, fileSaved, fileLastSave

    if fileChosen == False:
        saveNewFileDo()
    else:
        saveContent = textInput.get(1.0, 'end-1c')
        with open(filePathName, 'w') as f:
            f.write(saveContent)
        with open(filePathName) as f:
            content = f.read()
            textInput.delete('1.0', 'end')
            textInput.insert('1.0', content)
        root.title(root_title + ' - ' + fileName)
        fileLastSave = saveContent
        fileSaved = True


def settingsBtnDo():
    '''
    Opens settings
    '''
    global compilers

    def pyInterpreterSaveDo():
        compilers['.py'] = str(pyInterpreterEntry.get())

    def nodeInterpreterSaveDo():
        compilers['.js'] = str(nodeInterpreterEntry.get())

    def swiftInterpreterSaveDo():
        compilers['.swift'] = str(swiftInterpreterEntry.get())

    # Initialize settings
    settingsWin = Toplevel()
    settingsWin.title(root_title + ' - Settings')
    settingsWin.configure(bg='#464646')
    settingsTitle = ttk.Label(settingsWin, text='Settings', style='Title.TLabel')
    settingsTitle.pack()

    # Create section to overwrite compiler
    compilerOverwriteFrame = ttk.Frame(settingsWin)
    compilerOverwriteFrame.pack()
    compilerOverwriteTitle = ttk.Label(compilerOverwriteFrame, text='Overwrite default compiler/interpreter path', style='Subtitle.TLabel')
    compilerOverwriteTitle.pack()

    # Python overwrite
    pyInterpreterFrame = ttk.Frame(compilerOverwriteFrame)
    pyInterpreterFrame.pack()
    pyInterpreterTitle = ttk.Label(pyInterpreterFrame, text='Python:')
    pyInterpreterTitle.pack(side=LEFT)
    pyInterpreterEntry = ttk.Entry(pyInterpreterFrame)
    pyInterpreterEntry.pack(side=LEFT)
    pyInterpreterSave = ttk.Button(pyInterpreterFrame, text='Save', command=pyInterpreterSaveDo)
    pyInterpreterSave.pack()

    # Node.js overwrite
    nodeInterpreterFrame = ttk.Frame(compilerOverwriteFrame)
    nodeInterpreterFrame.pack()
    nodeInterpreterTitle = ttk.Label(nodeInterpreterFrame, text='Node.js:')
    nodeInterpreterTitle.pack(side=LEFT)
    nodeInterpreterEntry = ttk.Entry(nodeInterpreterFrame)
    nodeInterpreterEntry.pack(side=LEFT)
    nodeInterpreterSave = ttk.Button(nodeInterpreterFrame, text='Save', command=nodeInterpreterSaveDo)
    nodeInterpreterSave.pack()

    # Swift overwrite
    swiftInterpreterFrame = ttk.Frame(compilerOverwriteFrame)
    swiftInterpreterFrame.pack()
    swiftInterpreterTitle = ttk.Label(swiftInterpreterFrame, text='Swift:')
    swiftInterpreterTitle.pack(side=LEFT)
    swiftInterpreterEntry = ttk.Entry(swiftInterpreterFrame)
    swiftInterpreterEntry.pack(side=LEFT)
    swiftInterpreterSave = ttk.Button(swiftInterpreterFrame, text='Save', command=swiftInterpreterSaveDo)
    swiftInterpreterSave.pack()


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

# Text editor part
textInputFrame = ttk.Frame(root)
textInputFrame.pack()
if str(platform.system()) == 'Windows':
    textInputWidth = 120
    textInputHeight = 30
else:
    textInputWidth = 180
    textInputHeight = 40
scrollbar = Scrollbar(textInputFrame)
scrollbar.pack(side=RIGHT, fill=Y)
textInput = Text(textInputFrame, bg='#666666', fg='#F7F7F7', width=textInputWidth, height=textInputHeight, yscrollcommand=scrollbar.set)
textInput.configure(font=("Courier", 12))
textInput.pack(side=LEFT)
scrollbar.config(command=textInput.yview)

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

root.bind("<Key>", key_press)

'''
------------------------------
'''



if __name__ == '__main__':
    root.mainloop()
