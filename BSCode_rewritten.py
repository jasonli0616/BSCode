from tkinter import *
from tkinter import ttk as ttk
from tkinter.filedialog import askopenfilename, askopenfile
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
        winTitleLab = ttk.Label(newWin, text=title, style="NewWin.TLabel")
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


def openFileBtnDo():
    '''
    Opens file dialog, user chooses file
    '''
    global fileName, filePath, filePathName, fileExt, fileChosen

    openFileDialog = askopenfilename(title='Select file to open', initialdir='/', filetypes=[('Python', '*.py'), ('Node.js', '*.js'), ('Swift', '*.swift'), ('HTML', '*.html')])
    fileName = str(os.path.split(openFileDialog)[1])
    filePath = str(os.path.split(openFileDialog)[0])
    filePathName = str(openFileDialog)
    fileExt = str(os.path.splitext(fileName)[1])
    root.title(root_title + ' - ' + fileName)
    fileChosen = True

    with open(filePathName) as f:
        content = f.read()
        textInput.delete('1.0', 'end')
        textInput.insert('1.0', content)


def runBtnDo():
    '''
    Button to run script
    '''
    global fileName, filePath, filePathName, fileExt, compilers, fileChosen

    noRun = False
    errorReason = ''
    runList = []

    if fileChosen == False:
        newWin(
            title='Error:',
            content1='No file chosen',
        )
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
    global fileName, filePath, filePathName, fileExt, fileChosen

    if fileChosen == False:
        newWin(
            title='Error:',
            content1='No file chosen'
        )
    else:
        saveContent = textInput.get(1.0, 'end-1c')
        with open(filePathName, 'w') as f:
            f.write(saveContent)


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
textInput = Text(textInputFrame, bg='#666666', fg='#F7F7F7', width=180, height=40)
textInput.configure(font=("Courier", 12))
textInput.pack()

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

'''
------------------------------
'''



if __name__ == '__main__':
    root.mainloop()
