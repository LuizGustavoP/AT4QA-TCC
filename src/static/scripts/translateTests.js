document.addEventListener('DOMContentLoaded', function () {
    const translateButton = document.getElementById('translateTestsButton');
    const messageContainer = document.createElement('p');
    messageContainer.style.marginTop = '10px';
    translateButton.parentNode.appendChild(messageContainer);

    translateButton.addEventListener('click', function (event) {
        event.preventDefault();

        const selectedFiles = [];
        const checkboxes = document.querySelectorAll('.uploadedFilesList input[type="checkbox"]:checked');

        checkboxes.forEach(checkbox => {
            selectedFiles.push(checkbox.value);
        });

        if (selectedFiles.length === 0) {
            alert('Please select at least one file to translate.');
            return;
        }

        let dots = 0;
        translateButton.disabled = true;
        const originalText = translateButton.textContent;
        const animationInterval = setInterval(() => {
            dots = (dots + 1) % 4; 
            translateButton.textContent = `Translating${'.'.repeat(dots)}`;
        }, 500);

        fetch('/translate_feature', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ files: selectedFiles }),
        })
            .then(response => response.json())
            .then(data => {
                clearInterval(animationInterval); 
                translateButton.textContent = originalText;
                translateButton.disabled = false;

                if (data.message) {
                    messageContainer.textContent = 'Translation started successfully! Your translated file will be saved in the features folder, and should be visible in the Tester page!';
                    messageContainer.style.color = 'green';
                } else if (data.error) {
                    messageContainer.textContent = `Error: ${data.error}`;
                    messageContainer.style.color = 'red';
                }
            })
            .catch(error => {
                clearInterval(animationInterval);
                translateButton.textContent = originalText; 
                translateButton.disabled = false;

                messageContainer.textContent = 'Error translating files. Please try again.';
                messageContainer.style.color = 'red';
                console.error('Error translating files:', error);
            });
    });
});