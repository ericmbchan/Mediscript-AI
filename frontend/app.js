// MediScript AI Frontend JavaScript
class MediScriptApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.checkApiHealth();
        this.generateDocumentation = this.generateDocumentation.bind(this);
        this.clearAll = this.clearAll.bind(this);
        this.copyToClipboard = this.copyToClipboard.bind(this);
    }

    initializeElements() {
        this.notesInput = document.getElementById('medical-notes');
        this.generateBtn = document.getElementById('generate-btn');
        this.clearBtn = document.getElementById('clear-btn');
        this.copyBtn = document.getElementById('copy-btn');
        this.outputContent = document.getElementById('output-content');
        this.loading = document.getElementById('loading');
    }

    bindEvents() {
        this.generateBtn.addEventListener('click', () => this.generateDocumentation());
        this.clearBtn.addEventListener('click', () => this.clearAll());
        this.copyBtn.addEventListener('click', () => this.copyToClipboard());
        
        // Auto-resize textarea
        this.notesInput.addEventListener('input', () => {
            this.notesInput.style.height = 'auto';
            this.notesInput.style.height = this.notesInput.scrollHeight + 'px';
        });

        // Enable/disable generate button based on input
        this.notesInput.addEventListener('input', () => {
            this.generateBtn.disabled = !this.notesInput.value.trim();
        });

        // Initial state
        this.generateBtn.disabled = true;
    }

    async checkApiHealth() {
        try {
            const response = await fetch('https://mediscript-ai.onrender.com/api/health');
            if (response.ok) {
                console.log('✅ API is healthy');
            } else {
                this.showError('API health check failed');
            }
        } catch (error) {
            console.warn('⚠️ API health check failed:', error);
            this.showError('Unable to connect to the API. Please check if the server is running.');
        }
    }

    async generateDocumentation() {
        const notes = this.notesInput.value.trim();
        
        if (!notes) {
            this.showError('Please enter some medical notes first.');
            return;
        }

        this.showLoading(true);
        this.generateBtn.disabled = true;
        this.copyBtn.disabled = true;

        try {
            const response = await fetch('https://mediscript-ai.onrender.com/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: notes })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.ok) {
                this.displayResult(data.message);
            } else {
                throw new Error(data.error || 'Unknown error occurred');
            }

        } catch (error) {
            console.error('Error generating documentation:', error);
            this.showError(`Failed to generate documentation: ${error.message}`);
        } finally {
            this.showLoading(false);
            this.generateBtn.disabled = false;
        }
    }

    displayResult(content) {
        this.outputContent.innerHTML = `<div class="fade-in">${this.formatContent(content)}</div>`;
        this.copyBtn.disabled = false;
        this.outputContent.classList.add('success');
        
        // Remove success styling after a few seconds
        setTimeout(() => {
            this.outputContent.classList.remove('success');
        }, 3000);
    }

    formatContent(content) {
        // Basic formatting for medical documentation
        return content
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/^# (.*$)/gm, '<h3>$1</h3>')
            .replace(/^## (.*$)/gm, '<h4>$1</h4>')
            .replace(/^### (.*$)/gm, '<h5>$1</h5>');
    }

    showError(message) {
        this.outputContent.innerHTML = `
            <div class="error-message fade-in">
                <i class="fas fa-exclamation-triangle" style="color: #ef4444; margin-right: 10px;"></i>
                ${message}
            </div>
        `;
        this.outputContent.classList.add('error');
        this.copyBtn.disabled = true;
        
        // Remove error styling after a few seconds
        setTimeout(() => {
            this.outputContent.classList.remove('error');
        }, 5000);
    }

    showLoading(show) {
        if (show) {
            this.loading.classList.remove('hidden');
        } else {
            this.loading.classList.add('hidden');
        }
    }

    clearAll() {
        this.notesInput.value = '';
        this.notesInput.style.height = 'auto';
        this.outputContent.innerHTML = `
            <div class="placeholder">
                <i class="fas fa-robot"></i>
                <p>Your professional medical documentation will appear here...</p>
            </div>
        `;
        this.copyBtn.disabled = true;
        this.generateBtn.disabled = true;
        this.outputContent.classList.remove('success', 'error');
    }

    async copyToClipboard() {
        const content = this.outputContent.textContent;
        
        if (!content || content.includes('Your professional medical documentation will appear here')) {
            this.showError('Nothing to copy. Generate documentation first.');
            return;
        }

        try {
            await navigator.clipboard.writeText(content);
            
            // Visual feedback
            const originalText = this.copyBtn.innerHTML;
            this.copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
            this.copyBtn.style.background = '#10b981';
            
            setTimeout(() => {
                this.copyBtn.innerHTML = originalText;
                this.copyBtn.style.background = '';
            }, 2000);
            
        } catch (error) {
            console.error('Failed to copy to clipboard:', error);
            this.showError('Failed to copy to clipboard. Please try selecting and copying manually.');
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MediScriptApp();
});

// Add some helpful keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to generate
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const generateBtn = document.getElementById('generate-btn');
        if (!generateBtn.disabled) {
            generateBtn.click();
        }
    }
    
    // Escape to clear
    if (e.key === 'Escape') {
        document.getElementById('clear-btn').click();
    }
});

// Add some sample data for demo purposes
function loadSampleData() {
    const sampleNotes = `Patient: 45-year-old male
Chief Complaint: Chest pain and shortness of breath
History: Patient reports sudden onset of chest pain 2 hours ago, described as crushing, radiating to left arm. Associated with diaphoresis and nausea.
Vital Signs: BP 150/95, HR 110, RR 24, Temp 98.6°F, O2 Sat 94% on room air
Physical Exam: Patient appears anxious, diaphoretic. Heart rate regular, no murmurs. Lungs clear bilaterally. No peripheral edema.
Assessment: Possible acute coronary syndrome
Plan: EKG, cardiac enzymes, chest X-ray, cardiology consult`;

    const notesInput = document.getElementById('medical-notes');
    if (notesInput && !notesInput.value.trim()) {
        notesInput.value = sampleNotes;
        notesInput.style.height = 'auto';
        notesInput.style.height = notesInput.scrollHeight + 'px';
        document.getElementById('generate-btn').disabled = false;
    }
}

// Uncomment the line below to load sample data on page load
// document.addEventListener('DOMContentLoaded', loadSampleData);
