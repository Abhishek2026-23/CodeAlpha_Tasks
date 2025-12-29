class ChatBot {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.typingIndicator = document.getElementById('typingIndicator');
        
        this.initializeEventListeners();
        this.updateTimestamp('botTimestamp');
    }

    initializeEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter key press
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Input validation
        this.userInput.addEventListener('input', () => {
            const message = this.userInput.value.trim();
            this.sendButton.disabled = message.length === 0;
        });
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        
        if (!message) return;

        // Disable input while processing
        this.setInputState(false);
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.userInput.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send request to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add bot response
            this.addMessage(data.response, 'bot', data.confidence);
            
        } catch (error) {
            console.error('Error:', error);
            this.hideTypingIndicator();
            this.addMessage('Sorry, something went wrong. Please try again.', 'bot');
        } finally {
            // Re-enable input
            this.setInputState(true);
            this.userInput.focus();
        }
    }

    addMessage(text, sender, confidence = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('p');
        messageText.textContent = text;
        messageContent.appendChild(messageText);
        
        // Add timestamp
        const timestamp = document.createElement('span');
        timestamp.className = 'timestamp';
        timestamp.textContent = this.getCurrentTime();
        messageContent.appendChild(timestamp);
        
        // Add confidence score for bot messages
        if (sender === 'bot' && confidence !== null && confidence > 0) {
            const confidenceSpan = document.createElement('span');
            confidenceSpan.className = 'confidence-score';
            confidenceSpan.textContent = `Confidence: ${(confidence * 100).toFixed(0)}%`;
            messageContent.appendChild(confidenceSpan);
        }
        
        messageDiv.appendChild(messageContent);
        this.chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        this.scrollToBottom();
    }

    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }

    setInputState(enabled) {
        this.userInput.disabled = !enabled;
        this.sendButton.disabled = !enabled || this.userInput.value.trim().length === 0;
        
        if (enabled) {
            this.userInput.focus();
        }
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }

    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }

    updateTimestamp(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = this.getCurrentTime();
        }
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatBot();
});

// Add some sample questions for user guidance
document.addEventListener('DOMContentLoaded', () => {
    const sampleQuestions = [
        "What is CodeAlpha?",
        "How long is the internship?",
        "What are the requirements?",
        "Is it paid or unpaid?",
        "Can I work remotely?"
    ];

    // You can add these as quick suggestion buttons if desired
    // This is just a placeholder for potential enhancement
});