// Sample emails for quick testing
const sampleEmails = {
    spam: "🎉 CONGRATULATIONS! You've WON $1,000,000 in our exclusive lottery! Click HERE NOW to claim your prize before it expires! This is a LIMITED TIME OFFER! Act fast and get your FREE money today! No purchase necessary!",
    ham: "Hi Team,\n\nJust wanted to remind everyone about our project meeting scheduled for tomorrow at 3:00 PM in Conference Room B. Please review the attached documents before the meeting.\n\nLooking forward to discussing the Q4 roadmap with you all.\n\nBest regards,\nJohn"
};

// DOM Elements
const emailInput = document.getElementById('emailInput');
const classifyBtn = document.getElementById('classifyBtn');
const clearBtn = document.getElementById('clearBtn');
const resultSection = document.getElementById('resultSection');
const resultCard = document.getElementById('resultCard');
const resultTitle = document.getElementById('resultTitle');
const resultDescription = document.getElementById('resultDescription');
const resultIcon = document.querySelector('.result-icon');
const confidenceSection = document.getElementById('confidenceSection');
const hamBar = document.getElementById('hamBar');
const spamBar = document.getElementById('spamBar');
const hamPercent = document.getElementById('hamPercent');
const spamPercent = document.getElementById('spamPercent');

// Example buttons
const exampleButtons = document.querySelectorAll('.example-btn');
exampleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const type = btn.getAttribute('data-type');
        emailInput.value = sampleEmails[type];
        emailInput.focus();
    });
});

// Clear button
clearBtn.addEventListener('click', () => {
    emailInput.value = '';
    resultSection.classList.add('hidden');
    emailInput.focus();
});

// Classify button
classifyBtn.addEventListener('click', async () => {
    const emailText = emailInput.value.trim();
    
    if (!emailText) {
        alert('Please enter some email content to classify!');
        return;
    }
    
    // Show loading state
    resultSection.classList.remove('hidden');
    resultCard.className = 'result-card analyzing';
    resultIcon.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    resultTitle.textContent = 'Analyzing...';
    resultDescription.textContent = 'Please wait while we classify your email';
    confidenceSection.classList.add('hidden');
    classifyBtn.disabled = true;
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: emailText })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResult(data);
        } else {
            showError(data.error || 'An error occurred');
        }
    } catch (error) {
        showError('Failed to connect to the server. Make sure the Flask app is running.');
    } finally {
        classifyBtn.disabled = false;
    }
});

// Display classification result
function displayResult(data) {
    const isSpam = data.is_spam;
    
    // Update card styling
    resultCard.className = `result-card ${isSpam ? 'spam' : 'ham'}`;
    
    // Update icon
    resultIcon.innerHTML = isSpam 
        ? '<i class="fas fa-exclamation-triangle"></i>'
        : '<i class="fas fa-check-circle"></i>';
    
    // Update title and description
    resultTitle.textContent = isSpam ? '🚨 SPAM DETECTED!' : '✅ LEGITIMATE EMAIL';
    resultDescription.textContent = isSpam
        ? 'This email appears to be spam. Be cautious and do not click any links.'
        : 'This email appears to be legitimate and safe.';
    
    // Show and update confidence bars
    confidenceSection.classList.remove('hidden');
    
    const hamConfidence = data.ham_confidence;
    const spamConfidence = data.spam_confidence;
    
    // Animate bars
    setTimeout(() => {
        hamBar.style.width = `${hamConfidence}%`;
        spamBar.style.width = `${spamConfidence}%`;
        hamPercent.textContent = `${hamConfidence.toFixed(1)}%`;
        spamPercent.textContent = `${spamConfidence.toFixed(1)}%`;
    }, 100);
}

// Show error message
function showError(message) {
    resultCard.className = 'result-card analyzing';
    resultIcon.innerHTML = '<i class="fas fa-exclamation-circle"></i>';
    resultTitle.textContent = 'Error';
    resultDescription.textContent = message;
    confidenceSection.classList.add('hidden');
}

// Allow Enter key to submit (with Shift+Enter for new line)
emailInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        classifyBtn.click();
    }
});
