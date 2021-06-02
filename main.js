/*
------------------------------

BSCode Electron Edition

Author: Jason Li

------------------------------

npm install electron
npm install electron-reload

------------------------------
*/


const { app, BrowserWindow, screen, dialog, ipcMain, Menu } = require('electron');
require('electron-reload')(__dirname);
const isMac = process.platform === 'darwin';


// Boilerplate Electron code
//------------------------------

function createWindow() {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize
    const win = new BrowserWindow({
        width: width,
        height: height,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });
    win.loadFile('pages/index.html');
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', function() {
        if (BrowserWindow.getAllWindows.length === 0) {createWindow()};
    });

});

app.on('window-all-closed', function() {
    if (!isMac) {app.quit()};
});

//------------------------------



// Menubar
//------------------------------

// If is mac, change Ctrl to Cmd
/*
let Ctrl = '';
if (isMac) ctrl = 'Cmd'
else ctrl = 'Ctrl'
const menubar = Menu.buildFromTemplate(
    
    [
    // If is mac, show app menu
    ...(isMac ? [{ role: 'appMenu' }] : []),

    // File menu
    {
        label: 'File',
        submenu: [
            {
                label: 'Open file',
                accelerator: `${ctrl}+O`,
                click: async () => {
                    // Show file dialog
                    funcReturn = await openFile();
                    // Return file dialog to renderer js
                }
            }
        ]
    }
]);
Menu.setApplicationMenu(menubar);
*/

//------------------------------



// When open file button pressed
ipcMain.on('get-file', async (event) => {
    // Show file dialog
    funcReturn = await openFile();
    // Return file dialog to renderer js
    event.reply('post-file', funcReturn);
})

// Show file dialog
async function openFile() {
    let fileName = '';
    let canceled = false;
    await dialog.showOpenDialog({
        properties: ['openFile'],
        filters: [
            { name: 'Python', extensions: ['py'] },
            { name: 'JavaScript', extensions: ['js'] },
            { name: 'HTML', extensions: ['html'] },
        ]
    }).then(result => {
        if (!result.canceled) {
            fileName = result.filePaths;
        } else {
            canceled = true;
        }
    })
    return [fileName, canceled]
}

ipcMain.on('show-error', (event, errorTitle, errorMsg) => {
    dialog.showErrorBox(errorTitle, errorMsg);
});

ipcMain.on('show-msg', (event, msgContent, msgDetail) => {
    dialog.showMessageBoxSync({
        type: 'info',
        message: msgContent,
        detail: msgDetail
    });
});