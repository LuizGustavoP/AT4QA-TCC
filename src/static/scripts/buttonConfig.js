document.getElementById('file').addEventListener('change', function(event) {
  const fileList = document.getElementById('fileList');
  const customFileButton = document.getElementById('customFileButton');
  fileList.innerHTML = '';  // Clear previous file list

  const files = event.target.files;
  if (files.length > 0) {
      customFileButton.textContent = `${files.length} file(s) selected`;
  } else {
      customFileButton.textContent = 'Select Files';
  }

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

      fileList.appendChild(fileItem);
  }
});