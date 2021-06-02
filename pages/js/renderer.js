const { ipcRenderer } = require("electron");
const fs = require('fs')
const path = require('path')

var fileDataList = ''
var filePathGlobal = ''
var fileNameGlobal = ''


// When Open button pressed
document.getElementById("open-file-btn").addEventListener('click', function() {
    // Tell main.js to get file
    ipcGetFile();
})

function ipcGetFile() {
    ipcRenderer.send('get-file');
}


// When main.js sends file
ipcRenderer.on('post-file', (event, funcReturn) => {
    let filePath = String(funcReturn[0]);
    let canceled = funcReturn[1];
    
    if (!canceled) {
        fs.readFile(filePath, 'utf8', function(err, data) {
            if (err) throw err;
            fileDataList = data.split('\n');
            showOnScreen(filePath, fileDataList);
        })
    } else {
        ipcRenderer.send('show-error', 'No file selected', 'Please select a file');
    }
})

// Add text to screen
function showOnScreen(filePath, fileContentAsList) {
    const lineLen = fileContentAsList.length;
    
    // Get file names
    fileName = path.basename(filePath);
    fileDir = path.dirname(filePath);
    filePathGlobal = filePath;
    fileNameGlobal = fileName;

    // Change title
    document.title = `BSCode - ${filePath}`;
    document.getElementById("title").innerHTML = `<h5>${fileDir}/</h5><h3>${fileName}</h3>`;

    document.getElementById("btns").innerHTML = document.getElementById("btns").innerHTML + '<button id="save-file-btn">Save file</button>'
    document.getElementById('save-file-btn').addEventListener('click', saveFile)

    const textarea_div = document.getElementById("textarea-div");

    textarea_div.style.border = '1px solid white';

    textarea_div.innerHTML = ''

    for (i = 0; i<lineLen; i++) {
        textarea_div.innerHTML = textarea_div.innerHTML + `
            <div class="textarea-item">
                <p>${i+1}</p>
                <textarea name="" id="textarea${i}" rows="1"></textarea>
            </div>
        `
    }

    for (i = 0; i<lineLen; i++) {
        document.getElementById(`textarea${i}`).value = fileContentAsList[i];
    }

}


// Save button
function saveFile() {
    let fileSaveContent = ''
    lineTotalNum = document.getElementsByTagName('textarea').length
    for (lineNum = 0; lineNum < lineTotalNum; lineNum++) {
        try {
            // If last line, don't add new empty line at end
            if (lineNum == lineTotalNum-1) {
                fileSaveContent = fileSaveContent + (document.getElementById(`textarea${lineNum}`).value)
            } else {
                fileSaveContent = fileSaveContent + (document.getElementById(`textarea${lineNum}`).value) + '\n'
            }
        } catch (error) {
            break
        }
    }
    fs.writeFile(filePathGlobal, fileSaveContent, function(err) {
        if (err) throw err;
    })
    ipcRenderer.send('show-msg', 'Saved', `${fileNameGlobal} has been saved successfully.`);
}
