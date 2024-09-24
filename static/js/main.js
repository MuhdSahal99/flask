document.addEventListener('DOMContentLoaded', () => {
    const candidateForm = document.getElementById('candidateForm');
    const employerForm = document.getElementById('employerForm');
    const addResumeButton = document.getElementById('addResume');

    if (candidateForm) {
        candidateForm.addEventListener('submit', handleCandidateSubmit);
    }

    if (employerForm) {
        employerForm.addEventListener('submit', handleEmployerSubmit);
    }

    if (addResumeButton) {
        addResumeButton.addEventListener('click', addResumeInput);
    }
});

async function handleCandidateSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const recommendationsDiv = document.getElementById('recommendations');
    recommendationsDiv.innerHTML = '<p>Processing your resume...</p>';

    try {
        const response = await fetch('/candidate', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        if (response.ok) {
            displayRecommendations(data.recommendations);
        } else {
            throw new Error(data.error || 'An error occurred while processing your resume.');
        }
    } catch (error) {
        recommendationsDiv.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
    }
}

async function handleEmployerSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const matchesDiv = document.getElementById('matches');
    matchesDiv.innerHTML = '<p>Processing candidates...</p>';

    try {
        const response = await fetch('/employer', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        if (response.ok) {
            displayMatches(data.matches);
        } else {
            throw new Error(data.error || 'An error occurred while processing candidates.');
        }
    } catch (error) {
        matchesDiv.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
    }
}

function addResumeInput() {
    const resumeInputs = document.getElementById('resumeInputs');
    const newIndex = resumeInputs.children.length + 1;
    const newInput = document.createElement('div');
    newInput.className = 'mb-3';
    newInput.innerHTML = `
        <label for="resume${newIndex}" class="form-label">Resume ${newIndex}</label>
        <textarea class="form-control" id="resume${newIndex}" name="resumes" rows="4" required></textarea>
    `;
    resumeInputs.appendChild(newInput);
}

function displayRecommendations(recommendations) {
    const recommendationsDiv = document.getElementById('recommendations');
    recommendationsDiv.innerHTML = '<h2>Top Job Recommendations:</h2>';
    recommendations.forEach((rec, index) => {
        const [jobTitle, similarity, description] = rec;
        const recDiv = document.createElement('div');
        recDiv.className = 'recommendation';
        recDiv.innerHTML = `
            <h3>${index + 1}. ${jobTitle}</h3>
            <p>Similarity: ${(similarity * 100).toFixed(2)}%</p>
            <p>${description}</p>
        `;
        recommendationsDiv.appendChild(recDiv);
    });
}

function displayMatches(matches) {
    const matchesDiv = document.getElementById('matches');
    matchesDiv.innerHTML = '<h2>Top Candidate Matches:</h2>';
    matches.forEach((match, index) => {
        const [resume, similarity, summary] = match;
        const matchDiv = document.createElement('div');
        matchDiv.className = 'match';
        matchDiv.innerHTML = `
            <h3>Candidate ${index + 1}</h3>
            <p>Similarity: ${(similarity * 100).toFixed(2)}%</p>
            <p>${summary}</p>
        `;
        matchesDiv.appendChild(matchDiv);
    });
}