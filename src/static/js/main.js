document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('analyzeForm');
    const resultsDiv = document.getElementById('results');
    const resultsList = document.getElementById('resultsList');
    const improvedResumeDiv = document.getElementById('improvedResume');
    const improvedResumeContent = document.getElementById('improvedResumeContent');
    let improvedResumeText = '';

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            resultsDiv.classList.add('hidden');
            resultsList.innerHTML = '';
            improvedResumeDiv.classList.add('hidden');
            improvedResumeContent.textContent = '';
            improvedResumeText = '';

            const formData = new FormData(form);

            fetch('/analyze', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultsList.innerHTML = `<p style="color:red;">${data.error}</p>`;
                    resultsDiv.classList.remove('hidden');
                    return;
                }
                let html = '';
                data.results.forEach(result => {
                    html += `<div class="result-item">
                        <strong>${result.filename}</strong>: <span>${result.status}</span> (Score: ${result.score})
                    </div>`;
                    if (result.improved_resume) {
                        improvedResumeText = result.improved_resume;
                        improvedResumeContent.textContent = improvedResumeText;
                        improvedResumeDiv.classList.remove('hidden');
                    }
                });
                resultsList.innerHTML = html;
                resultsDiv.classList.remove('hidden');
            })
            .catch(err => {
                resultsList.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
                resultsDiv.classList.remove('hidden');
            });
        });
    }

    window.downloadImprovedResume = function () {
        if (!improvedResumeText) return;
        const blob = new Blob([improvedResumeText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'improved_resume.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };
});