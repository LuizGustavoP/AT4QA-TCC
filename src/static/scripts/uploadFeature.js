function handleFileSelect(event) {
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';  // Clear previous file list

    const files = event.target.files;
    console.log('Files selected:', files);  // Debugging: Check if files are selected

    for (let i = 0; i < files.length; i++) {
        const file = files[i];

        // Create a file item container
        const fileItem = document.createElement('div');
        fileItem.classList.add('file-item');

        // Display file name
        const fileName = document.createElement('span');
        fileName.classList.add('file-name');
        fileName.textContent = file.name;
        fileItem.appendChild(fileName);

        // Add loading icon
        const loadingIcon = document.createElement('div');
        loadingIcon.classList.add('loading-icon');
        fileItem.appendChild(loadingIcon);

        fileList.appendChild(fileItem);
    }
}

function handleFormSubmit(event) {
    event.preventDefault();  // Prevent the default form submission

    const form = event.target;
    const files = document.getElementById('file').files;
    const fileList = document.getElementById('fileList');

    if (files.length === 0) {
        alert('Please select at least one file.');
        return;
    }

    console.log('Submitting form with files:', files);  // Debugging: Check if form is submitted

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const formData = new FormData();
        formData.append('file', file);

        // Upload each file individually
        uploadFile(formData, i);
    }
}

function uploadFile(formData, index) {
    const xhr = new XMLHttpRequest();
    const fileItem = document.getElementsByClassName('file-item')[index];
    const loadingIcon = fileItem.querySelector('.loading-icon');

    xhr.open('POST', '/upload_test', true);

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
            console.log(`File ${index + 1} uploaded successfully`);  // Debugging: Check if file upload is successful
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