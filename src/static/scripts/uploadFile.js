document.addEventListener('DOMContentLoaded', function () {
    const customFileButton = document.getElementById('customFileButton');
    const fileList = document.getElementById('fileList');
    const fileInput = document.getElementById('file');

    let filesUploaded = 0;

    customFileButton.addEventListener('click', function (event) {
        event.preventDefault();
        fileInput.click();
    });

    fileInput.addEventListener('change', function (event) {
        fileList.innerHTML = '';
        const files = event.target.files;

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

            const loadingIcon = document.createElement('div');
            loadingIcon.classList.add('loading-icon');
            fileItem.appendChild(loadingIcon);

            fileList.appendChild(fileItem);
        }

        if (files.length > 0)
            uploadFiles(files);
    });

    function uploadFiles(files) {
        filesUploaded = 0;

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const formData = new FormData();

            formData.append('file', file);
            uploadFile(formData, i, files.length);
        }
    }

    function uploadFile(formData, index) {
        const xhr = new XMLHttpRequest();
        const fileItem = document.getElementsByClassName('fileItem')[index];
        const loadingIcon = fileItem.querySelector('.loading-icon');

        const fileName = formData.get('file').name;
        const fileExtension = fileName.split('.').pop().toLowerCase();

        let typeSelect;
        if (['feature'].includes(fileExtension))
            typeSelect = 'features';
        else if (['yaml', 'json'].includes(fileExtension))
            typeSelect = 'documentation';
        else if (['mask'].includes(fileExtension))
            typeSelect = 'masks';
        else
            typeSelect = 'dictionaries';

        xhr.open('POST', `/upload_file?type=${typeSelect}`, true);

        xhr.upload.onprogress = function (event) {
            if (event.lengthComputable) {
                const percentComplete = (event.loaded / event.total) * 100;
                console.log(`File ${index + 1}: ${percentComplete}% uploaded`);
            }
        };

        xhr.onload = function () {
            if (xhr.status === 200) {
                console.log(`File ${index + 1} uploaded successfully`);

                loadingIcon.innerHTML = '✔️';
                loadingIcon.classList.add('checkmark');
                loadingIcon.classList.remove('loading-icon');
                filesUploaded++;

                fetchAllUploadedFiles();
            } else {
                console.error(`Error uploading file ${index + 1}: ${xhr.statusText}`);
                alert(`Error uploading file ${index + 1}`);
                loadingIcon.innerHTML = '❌';
            }
        };

        xhr.onerror = function () {
            console.error(`Network error while uploading file ${index + 1}`);
            alert(`Network error while uploading file ${index + 1}`);
            loadingIcon.innerHTML = '❌';
        };

        xhr.send(formData);
    }

    function fetchAllUploadedFiles() {
        const uploadedFilesLists = document.querySelectorAll('.uploadedFilesList');

        uploadedFilesLists.forEach(list => {
            const listId = list.id;
            let typeSelect;

            if (listId.includes('feature'))
                typeSelect = 'features';
            else if (listId.includes('documentation'))
                typeSelect = 'documentation';
            else if (listId.includes('mask'))
                typeSelect = 'masks';
            else
                typeSelect = 'dictionaries';
            

            fetch(`/list_uploaded_files?type=${typeSelect}`)
                .then(response => response.json())
                .then(data => {
                    if (data.files) {
                        list.innerHTML = '';
                        data.files.forEach(file => {
                            const listItem = document.createElement('li');
                            listItem.classList.add('uploaded-fileItem');

                            const fileInfoSection = document.createElement('section');
                            fileInfoSection.classList.add('fileInfo');
                            
                            const checkbox = document.createElement('input');
                            checkbox.type = 'checkbox';
                            checkbox.value = file;
                            checkbox.classList.add('file-checkbox');
                            fileInfoSection.appendChild(checkbox);
                            
                            const fileNameSpan = document.createElement('span');
                            fileNameSpan.textContent = file;
                            fileInfoSection.appendChild(fileNameSpan);


                            const deleteButton = document.createElement('button');
                            deleteButton.textContent = 'X';
                            deleteButton.classList.add('delete-button');
                            deleteButton.addEventListener('click', function () {
                                deleteFile(file, typeSelect, list);
                            });

                            listItem.appendChild(fileInfoSection);
                            listItem.appendChild(deleteButton);
                            list.appendChild(listItem);
                        });
                    }
                })
                .catch(error => {
                    console.error(`Error fetching uploaded files for ${typeSelect}:`, error);
                });
        });
    }

    function deleteFile(fileName, typeSelect, list) {
        fetch(`/delete_file?type=${typeSelect}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ file_name: fileName }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    console.log(data.message);
                    fetchAllUploadedFiles(); // Refresh all lists after deletion
                } else if (data.error) {
                    console.error(data.error);
                    alert(`Error deleting file: ${data.error}`);
                }
            })
            .catch(error => {
                console.error('Error deleting file:', error);
            });
    }

    fetchAllUploadedFiles();
});