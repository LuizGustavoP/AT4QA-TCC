document.getElementById('file').addEventListener('change', function(event) {

    const files = event.target.files;
    const fileList = document.getElementById('fileList');
    const customFileButton = document.getElementById('customFileButton');
    
    fileList.innerHTML = '';

    if (files.length > 0)
        customFileButton.textContent = `${files.length} file(s) selected`;
    else
        customFileButton.textContent = 'Select Files';
    

    for (let i = 0; i < files.length; i++) {

        const file = files[i];
        const fileItem = document.createElement('div');
        const fileName = document.createElement('span');
        
        fileItem.classList.add('fileItem');
        fileName.classList.add('fileName');
        fileName.textContent = file.name;
        
        fileItem.appendChild(fileName);
        fileList.appendChild(fileItem);
    }
});