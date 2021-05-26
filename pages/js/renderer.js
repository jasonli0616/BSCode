const { fips } = require("crypto");
const { ipcRenderer } = require("electron");
const fs = require('fs')


document.getElementById("open-file-btn").addEventListener('click', function() {

    ipcRenderer.send('get-file')

})

ipcRenderer.on('post-file', (event, funcReturn) => {
    let filePath = String(funcReturn[0]);
    let canceled = funcReturn[1];

    
    if (!canceled) {
        fs.readFile(filePath, 'utf8', function(err, data) {
            if (err) {
                console.log(err);
            }
            showOnScreen(data)
        })
    }
})

function showOnScreen(textContent) {
    const perLine = textContent.split("\n");
    const lineLen = perLine.length;

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
        document.getElementById(`textarea${i}`).value = perLine[i];
    }
}