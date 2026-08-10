const API_BASE_URL = 'http://localhost:5000/api';
const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const resetBtn = document.getElementById('resetBtn');
const statusMessage = document.getElementById('statusMessage');

let isLoading = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkBotStatus();
    userInput.focus();
});

// Event listeners
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
        sendMessage();
    }
});
resetBtn.addEventListener('click', resetConversation);

async function checkBotStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) {
            throw new Error('Bot service unavailable');
        }
        const data = await response.json();
        showStatus(`✅ ${data.botName} is online`, 'success');
    } catch (error) {
        showStatus('⚠️ Bot service unavailable. Make sure the Flask server is running!', 'error');
        console.error('Health check failed:', error);
    }
}

async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message || isLoading) return;
    
    isLoading = true;
    sendBtn.disabled = true;
    userInput.disabled = true;
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    userInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    clearStatus();
    
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to get response');
        }
        
        const data = await response.json();
        removeTypingIndicator();
        addMessageToChat(data.message, 'assistant');
        
    } catch (error) {
        removeTypingIndicator();
        const errorMsg = error.message || 'An error occurred. Please try again.';
        showStatus(`❌ Error: ${errorMsg}`, 'error');
        console.error('Chat error:', error);
    } finally {
        isLoading = false;
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

function addMessageToChat(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = message;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timeDiv);
    
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTypingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.id = 'typing-indicator';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.className = 'typing-dot';
        contentDiv.appendChild(dot);
    }
    
    messageDiv.appendChild(contentDiv);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

async function resetConversation() {
    if (!confirm('Reset conversation history?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/reset`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('Failed to reset conversation');
        }
        
        // Clear chat box and show welcome message
        chatBox.innerHTML = `
            <div class="welcome-message">
                <h2>Welcome! 👋</h2>
                <p>Hi there! I'm Don's AI recruiter assistant. Ask me anything about:</p>
                <ul>
                    <li>💻 Technical Skills & Expertise</li>
                    <li>🚀 Featured Projects & Experience</li>
                    <li>🎯 Career Focus & Goals</li>
                    <li>📧 Contact Information</li>
                    <li>🌐 Portfolio & Links</li>
                </ul>
                <p style="margin-top: 15px; font-size: 12px; color: #666;">Try asking: "What are Don's main technical skills?" or "Tell me about the BC WildWatch project"</p>
            </div>
        `;
        
        showStatus('✅ Conversation reset', 'success');
        userInput.focus();
        
    } catch (error) {
        showStatus(`❌ Error: ${error.message}`, 'error');
        console.error('Reset error:', error);
    }
}

function showStatus(message, type = 'info') {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
}

function clearStatus() {
    statusMessage.textContent = '';
    statusMessage.className = 'status-message';
}
