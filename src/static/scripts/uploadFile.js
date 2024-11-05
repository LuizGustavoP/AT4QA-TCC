document.addEventListener('DOMContentLoaded', function() {

    const uploadedFilesList = document.getElementById('uploadedFilesList');
    const customFileButton = document.getElementById('customFileButton');
    const fileList = document.getElementById('fileList');
    const fileInput = document.getElementById('file');

    let filesUploaded = 0;

    customFileButton.addEventListener('click', function(event) 
    {
        event.preventDefault();
        fileInput.click();
    });

    fileInput.addEventListener('change', function(event) 
    {
        fileList.innerHTML = '';
        const files = event.target.files;

        if (files.length > 0)
            customFileButton.textContent = `${files.length} file(s) selected`;
        else
            customFileButton.textContent = 'Select Files';

        for (let i = 0; i < files.length; i++) 
        {

            const file = files[i];
            const fileItem = document.createElement('div');
            const fileName = document.createElement('span');

            fileItem.classList.add('file-item');

            fileName.classList.add('file-name');
            fileName.textContent = file.name;
            fileItem.appendChild(fileName);

            const loadingIcon = document.createElement('div');
            loadingIcon.classList.add('loading-icon');
            fileItem.appendChild(loadingIcon);

            fileList.appendChild(fileItem);
        }

        if (files.length > 0)
            uploadFiles(files);
    });

    function uploadFiles(files) 
    {
        filesUploaded = 0;

        for (let i = 0; i < files.length; i++) 
        {
            const file = files[i];
            const formData = new FormData();
            
            formData.append('file', file);
            uploadFile(formData, i, files.length);
        }
    }

    function uploadFile(formData, index)
    {
        const xhr = new XMLHttpRequest();
        const fileItem = document.getElementsByClassName('file-item')[index];
        const loadingIcon = fileItem.querySelector('.loading-icon');

        xhr.open('POST', '/upload_test', true);

        xhr.upload.onprogress = function(event) 
        {
            if (event.lengthComputable) 
            {
                const percentComplete = (event.loaded / event.total) * 100;
                console.log(`File ${index + 1}: ${percentComplete}% uploaded`);
            }
        };

        xhr.onload = function()
        {
            if (xhr.status === 200)
            {
                console.log(`File ${index + 1} uploaded successfully`);

                loadingIcon.innerHTML = '✔️';
                loadingIcon.classList.add('checkmark');
                loadingIcon.classList.remove('loading-icon');
                filesUploaded++;

                fetchUploadedFiles();
            }
            else
            {
                console.error(`Error uploading file ${index + 1}: ${xhr.statusText}`);
                alert(`Error uploading file ${index + 1}`);
                loadingIcon.innerHTML = '❌';
            }
        };

        xhr.onerror = function()
        {
            console.error(`Network error while uploading file ${index + 1}`);
            alert(`Network error while uploading file ${index + 1}`);
            loadingIcon.innerHTML = '❌';
        };

        xhr.send(formData);
    }

    function fetchUploadedFiles() 
    {
        fetch('/list_uploaded_files')
            .then(response => response.json())
            .then(data => {

                if (data.files) 
                {
                    uploadedFilesList.innerHTML = '';
                    data.files.forEach(file => {

                        const listItem = document.createElement('li');
                        listItem.classList.add('uploaded-file-item');

                        const fileNameSpan = document.createElement('span');
                        fileNameSpan.textContent = file;
                        listItem.appendChild(fileNameSpan);

                        const deleteButton = document.createElement('button');
                        
                        deleteButton.textContent = 'X';
                        deleteButton.classList.add('delete-button');
                        deleteButton.addEventListener('click', function(){
                            deleteFile(file);
                        });

                        listItem.appendChild(deleteButton);
                        uploadedFilesList.appendChild(listItem);
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching uploaded files:', error);
            });
    }

    function deleteFile(fileName)
    {
        fetch('/delete_file', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ file_name: fileName }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message)
            {
                console.log(data.message);
                fetchUploadedFiles();
            }
            else if (data.error)
            {
                console.error(data.error);
                alert(`Error deleting file: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error deleting file:', error);
        });
    }

    fetchUploadedFiles();
});