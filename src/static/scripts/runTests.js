document.addEventListener('DOMContentLoaded', function() {

    const reportLinks = document.getElementById('reportLinks');
    const consoleOutput = document.getElementById('outputText');
    const consoleScreen = document.getElementById('consoleOutput');
    const runTestsButton = document.getElementById('runTestsButton');
    const stopTestsButton = document.getElementById('stopTestsButton');
    
    const reportHTMLButton = document.querySelector('.reportHTMLButton');
    const reportJSONButton = document.querySelector('.reportJSONButton');

    let eventSource = null;

    runTestsButton.addEventListener('click', function(event) 
    {

        event.preventDefault();

        consoleScreen.style.display = 'block';
        consoleOutput.textContent = '';
        reportLinks.style.display = 'none';

        const tags = document.getElementById('tags').value;

        runTestsButton.disabled = true;
        runTestsButton.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Running tests...';

        stopTestsButton.style.display = 'inline-block';

        eventSource = new EventSource(`/run_test?tags=${encodeURIComponent(tags)}`);

        eventSource.onmessage = function(event) 
        {
            consoleOutput.textContent += event.data + '\n';
            consoleOutput.scrollTop = consoleOutput.scrollHeight;

            if (event.data.includes('Report available:'))
            {

                const reportUrl = event.data.split('Report available: ')[1].trim();

                if (reportUrl.endsWith('.html')) 
                {
                    reportHTMLButton.href = reportUrl;
                    reportHTMLButton.style.display = 'inline-block';
                }
                else if (reportUrl.endsWith('.json')) 
                {
                    reportJSONButton.href = reportUrl;
                    reportJSONButton.style.display = 'inline-block';
                }
            }
        };

        eventSource.onerror = function() 
        {
            consoleOutput.textContent += '\nError: Could not connect to the server.\n';

            eventSource.close();

            runTestsButton.disabled = false;
            runTestsButton.innerHTML = 'Run Tests!';
            stopTestsButton.style.display = 'none';
        };

        eventSource.addEventListener('end', function() 
        {
            runTestsButton.disabled = false;
            runTestsButton.innerHTML = 'Run Tests!';
            stopTestsButton.style.display = 'none';
            reportLinks.style.display = 'block';
            eventSource.close();
        });
    });

    stopTestsButton.addEventListener('click', function() 
    {
        fetch('/stop_test', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                
                if (data.success)
                    consoleOutput.textContent += '\nTests stopped by user.\n';
                else
                    consoleOutput.textContent += '\nError: Could not stop the tests.\n';

                if (eventSource)
                    eventSource.close();

                runTestsButton.disabled = false;
                runTestsButton.innerHTML = 'Run Tests!';
                stopTestsButton.style.display = 'none';
            })
            .catch(error => {
                consoleOutput.textContent += '\nError: Could not stop the tests.\n';
                consoleOutput.textContent += error;
                runTestsButton.disabled = false;
                runTestsButton.innerHTML = 'Run Tests!';
                stopTestsButton.style.display = 'none';
            });
    });
});