document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('paulo-chat-toggle');
    const window_ = document.getElementById('paulo-chat-window');
    const closeBtn = document.getElementById('paulo-chat-close');
    const input = document.getElementById('paulo-chat-input');
    const sendBtn = document.getElementById('paulo-chat-send');
    const messages = document.getElementById('paulo-chat-messages');
    const iconOpen = document.getElementById('paulo-toggle-icon-open');
    const iconClose = document.getElementById('paulo-toggle-icon-close');

    let chatHistory = [];
    let isOpen = false;
    let greeted = false;

    // Suggested questions
    const suggestions = [
        "What are Paulo's skills?",
        "What's his work experience?",
        "Can he build WordPress sites?",
        "How can I hire Paulo?"
    ];

    function openChat() {
        isOpen = true;
        window_.classList.add('open');
        iconOpen.style.display = 'none';
        iconClose.style.display = 'block';
        if (!greeted) {
            greeted = true;
            setTimeout(() => {
                appendMessage('bot', "Hi there! 👋 I'm Paulo's AI assistant. I can answer any questions about his skills, experience, and portfolio.");
                setTimeout(() => appendSuggestions(), 600);
            }, 300);
        }
        setTimeout(() => input.focus(), 400);
    }

    function closeChat() {
        isOpen = false;
        window_.classList.remove('open');
        iconOpen.style.display = 'block';
        iconClose.style.display = 'none';
    }

    toggle.addEventListener('click', () => isOpen ? closeChat() : openChat());
    closeBtn.addEventListener('click', closeChat);
    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keydown', (e) => { if (e.key === 'Enter') sendMessage(); });

    function appendSuggestions() {
        const wrapper = document.createElement('div');
        wrapper.className = 'suggestion-chips';
        suggestions.forEach(text => {
            const chip = document.createElement('button');
            chip.className = 'suggestion-chip';
            chip.textContent = text;
            chip.addEventListener('click', () => {
                wrapper.remove();
                input.value = text;
                sendMessage();
            });
            wrapper.appendChild(chip);
        });
        messages.appendChild(wrapper);
        scrollToBottom();
    }

    function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        // Remove suggestion chips
        const chips = messages.querySelector('.suggestion-chips');
        if (chips) chips.remove();

        appendMessage('user', text);
        input.value = '';
        input.disabled = true;
        sendBtn.disabled = true;

        const typingId = appendTyping();
        chatHistory.push({ role: 'user', text });

        fetch(pauloChatbot.server_url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: text,
                history: chatHistory.slice(-10)
            })
        })
        .then(res => res.json())
        .then(data => {
            removeTyping(typingId);
            if (data.reply) {
                appendMessage('bot', data.reply);
                chatHistory.push({ role: 'model', text: data.reply });
            } else {
                appendMessage('bot', 'Sorry, I ran into an issue. Please try again!');
            }
        })
        .catch(() => {
            removeTyping(typingId);
            appendMessage('bot', 'Connection error. Make sure the server is running.');
        })
        .finally(() => {
            input.disabled = false;
            sendBtn.disabled = false;
            input.focus();
        });
    }

    function appendMessage(sender, text) {
        const div = document.createElement('div');
        div.className = `chat-msg ${sender}-msg`;

        if (sender === 'bot') {
            const avatar = document.createElement('div');
            avatar.className = 'bot-avatar';
            avatar.textContent = 'P';
            div.appendChild(avatar);
        }

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = text;
        div.appendChild(bubble);

        messages.appendChild(div);
        scrollToBottom();
        return div;
    }

    function appendTyping() {
        const id = 'typing-' + Date.now();
        const div = document.createElement('div');
        div.className = 'chat-msg bot-msg';
        div.id = id;

        const avatar = document.createElement('div');
        avatar.className = 'bot-avatar';
        avatar.textContent = 'P';

        const bubble = document.createElement('div');
        bubble.className = 'bubble typing-bubble';
        bubble.innerHTML = '<span></span><span></span><span></span>';

        div.appendChild(avatar);
        div.appendChild(bubble);
        messages.appendChild(div);
        scrollToBottom();
        return id;
    }

    function removeTyping(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        messages.scrollTop = messages.scrollHeight;
    }
});
