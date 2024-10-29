document.getElementById('file').addEventListener('change', handleFileSelect);
document.getElementById('uploadForm').addEventListener('submit', handleFormSubmit);

function handleFileSelect(event) {
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';  // Clear previous file list

    const files = event.target.files;
    for (let i = 0; i < files.length; i++) {
        const file = files[i];

        const fileItem = document.createElement('section');
        fileItem.classList.add('file-item');

        const fileName = document.createElement('span');
        fileName.classList.add('file-name');
        fileName.textContent = file.name;
        fileItem.appendChild(fileName);

        const loadingIcon = document.createElement('section');
        loadingIcon.classList.add('loading-icon');
        fileItem.appendChild(loadingIcon);

        fileList.appendChild(fileItem);
    }
}

function handleFormSubmit(event) {
    event.preventDefault();

    const form = event.target;
    const files = document.getElementById('file').files;
    const fileList = document.getElementById('fileList');

    if (files.length === 0) {
        alert('Please select at least one file.');
        return;
    }

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const formData = new FormData();
        formData.append('file', file);

        uploadFile(formData, i);
    }
}

function uploadFile(formData, index) {
    const xhr = new XMLHttpRequest();
    const fileItem = document.getElementsByClassName('file-item')[index];
    const loadingIcon = fileItem.querySelector('.loading-icon');

    xhr.open('POST', '{{url_for("upload_test")}}', true);

    // Track upload progress
    xhr.upload.onprogress = function(event) {
        if (event.lengthComputable) {
            const percentComplete = (event.loaded / event.total) * 100;
            console.log(`File ${index + 1}: ${percentComplete}% uploaded`);
        }
    };

    // On upload complete
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Replace loading icon with checkmark
            loadingIcon.classList.remove('loading-icon');
            loadingIcon.innerHTML = '&#10004;';  // Checkmark symbol
            loadingIcon.classList.add('checkmark');
        } else {
            alert('Error uploading file ' + (index + 1));
        }
    };

    xhr.send(formData);
}