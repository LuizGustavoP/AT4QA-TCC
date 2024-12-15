document.addEventListener('DOMContentLoaded', function () {
    const generateButton = document.getElementById('generateTestsButton');
    const messageContainer = document.createElement('p');
    messageContainer.style.marginTop = '10px';
    generateButton.parentNode.appendChild(messageContainer);

    generateButton.addEventListener('click', function (event) {
        event.preventDefault();

        const selectedFile = document.querySelector('.uploadedFilesList input[type="radio"]:checked').value;
        const paths = document.getElementById('endpointList').value;

        if (selectedFile === '') {
            alert('Please select at least one file to generate.');
            return;
        }

        let dots = 0;
        generateButton.disabled = true;
        const originalText = generateButton.textContent;
        const animationInterval = setInterval(() => {
            dots = (dots + 1) % 4; 
            generateButton.textContent = `Translating${'.'.repeat(dots)}`;
        }, 500);

        fetch('/generate_feature', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ file: selectedFile, paths: paths}),
        })
            .then(response => response.json())
            .then(data => {
                clearInterval(animationInterval); 
                generateButton.textContent = originalText;
                generateButton.disabled = false;

                if (data.message) {
                    messageContainer.textContent = 'Feature Generation started successfully! Your generated file will be saved in the features folder, and should be visible in the Tester page!';
                    messageContainer.style.color = 'green';
                } else if (data.error) {
                    messageContainer.textContent = `Error: ${data.error}`;
                    messageContainer.style.color = 'red';
                }
            })
            .catch(error => {
                clearInterval(animationInterval);
                generateButton.textContent = originalText; 
                generateButton.disabled = false;

                messageContainer.textContent = 'Error generating files. Please try again.';
                messageContainer.style.color = 'red';
                console.error('Error translating files:', error);
            });
    });
});