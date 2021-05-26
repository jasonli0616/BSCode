const { app, BrowserWindow, screen, dialog, ipcMain } = require('electron');
require('electron-reload')(__dirname);

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
    if (process.platform !== 'darwin') {app.quit()};
});


ipcMain.on('get-file', async (event) => {
    funcReturn = await openFile();
    event.reply('post-file', funcReturn)
})


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