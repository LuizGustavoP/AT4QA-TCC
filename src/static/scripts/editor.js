document.addEventListener('DOMContentLoaded', function () {
    const customFileButton = document.getElementById('customFileButton');
    const fileInput = document.getElementById('file');
    const editorContainer = document.getElementById('editor');
    const saveButton = document.getElementById('saveButton');
    const saveAsButton = document.getElementById('saveAsButton');
    let editor;

    customFileButton.addEventListener('click', function (event) {
        event.preventDefault();
        fileInput.click();
    });

    fileInput.addEventListener('change', function (event) {
        const files = event.target.files;

        if (files.length > 0) {
            customFileButton.textContent = `${files.length} file(s) selected`;

            const file = files[0];
            const formData = new FormData();
            formData.append('file', file);

            fetch('/upload_file_for_editing', {
                method: 'POST',
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.content) {
                        if (!editor) {
                            editor = ace.edit('editor');
                            editor.setTheme('ace/theme/monokai');
                        }

                        const fileName = file.name.toLowerCase();
                        if (fileName.endsWith('.feature')) {
                            editor.session.setMode('ace/mode/gherkin');
                        } else {
                            editor.session.setMode('ace/mode/text');
                        }

                        editor.setValue(data.content, -1);
                        editorContainer.style.display = 'block';
                        saveButton.style.display = 'block';
                    } else if (data.error) {
                        alert(`Error: ${data.error}`);
                    }
                })
                .catch((error) => {
                    console.error('Error uploading file:', error);
                });
        } else {
            customFileButton.textContent = 'Select Files';
        }
    });

    saveButton.addEventListener('click', function () {
        if (editor) {
            const editedContent = editor.getValue();

            fetch('/save_edited_file?type=save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content: editedContent, name: fileInput.files[0].name }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.message) {
                        alert('File saved successfully!');
                    } else if (data.error) {
                        alert(`Error saving file: ${data.error}`);
                    }
                })
                .catch((error) => {
                    console.error('Error saving file:', error);
                });
        }
    });

    saveAsButton.addEventListener('click', async function () {
        if (editor) {
            const editedContent = editor.getValue();

            try {
                const fileHandle = await window.showSaveFilePicker({
                    suggestedName: fileInput.files[0]?.name || 'new_file.feature',
                    types: [
                        {
                            description: 'Text Files',
                            accept: { 'text/plain': ['.txt', '.feature'] },
                        },
                    ],
                });

                const writableStream = await fileHandle.createWritable();
                await writableStream.write(editedContent);
                await writableStream.close();

                alert('File saved successfully!');
            } catch (error) {
                if (error.name === 'AbortError') {
                    console.log('File save was canceled.');
                } else {
                    console.error('Error saving file:', error);
                }
            }
        }
    });
});