const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const userNameInput = document.getElementById('userName');

// Auto-resize textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Send message on Enter (Shift+Enter for new line)
messageInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Send button click
sendButton.addEventListener('click', sendMessage);

function sendMessage() {
    const message = messageInput.value.trim();
    const userName = userNameInput.value.trim() || 'anonymous';
    
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Disable input while processing
    setInputState(false);
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    // Send to API
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            question: message,
            user: userName
        })
    })
    .then(response => response.json())
    .then(data => {
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        if (data.error) {
            addMessage(`Error: ${data.error}${data.details ? '\n' + data.details : ''}`, 'error');
        } else if (data.response) {
            addMessage(data.response, 'bot');
        } else {
            addMessage('Respuesta recibida pero sin contenido', 'error');
        }
        
        // Re-enable input
        setInputState(true);
    })
    .catch(error => {
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        addMessage(`Error de conexión: ${error.message}`, 'error');
        
        // Re-enable input
        setInputState(true);
    });
}

function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Format text with proper line breaks and structure
    const formattedText = formatMessageText(text);
    contentDiv.innerHTML = formattedText;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = formatTime(new Date());
    
    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timeDiv);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function formatMessageText(text) {
    // Escape HTML to prevent XSS
    const escapeHtml = (str) => {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    };
    
    let escaped = escapeHtml(text);
    
    // Convert numbered lists (1. 2. 3. etc.)
    escaped = escaped.replace(/(\d+)\.\s+\*\*([^*]+)\*\*:/g, '<strong>$1. $2:</strong>');
    
    // Convert bold text (**text**)
    escaped = escaped.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Convert italic text (*text* or _text_)
    escaped = escaped.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    escaped = escaped.replace(/_([^_]+)_/g, '<em>$1</em>');
    
    // Convert line breaks to <br>
    escaped = escaped.replace(/\n/g, '<br>');
    
    // Convert bullet points (- item)
    escaped = escaped.replace(/^- (.+)(<br>|$)/gm, '• $1$2');
    
    return escaped;
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typing-indicator-' + Date.now();
    
    const indicatorDiv = document.createElement('div');
    indicatorDiv.className = 'typing-indicator';
    indicatorDiv.innerHTML = '<span></span><span></span><span></span>';
    
    typingDiv.appendChild(indicatorDiv);
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
    
    return typingDiv.id;
}

function removeTypingIndicator(id) {
    const indicator = document.getElementById(id);
    if (indicator) {
        indicator.remove();
    }
}

function setInputState(enabled) {
    messageInput.disabled = !enabled;
    sendButton.disabled = !enabled;
    userNameInput.disabled = !enabled;
    
    if (enabled) {
        messageInput.focus();
    }
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatTime(date) {
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

// Focus on input on load
messageInput.focus();
