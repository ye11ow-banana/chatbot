'use strict'

const chatName = JSON.parse(
    document.querySelector('#chat-pk').textContent
);
const senderUsername = JSON.parse(
    document.querySelector('#senderUsername').textContent
);
const chat = document.querySelector('.chat');
const input = document.querySelector('.message-sending input');
const button = document.querySelector('.message-sending button');

function getCurrentDateTime() {
    const now = new Date();
    const options = {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric',
      hour12: true
    };
    return now.toLocaleString('en-US', options);
}

function renderMessage(sender, message) {
    const p_class = sender === senderUsername ? 'msg-user': 'msg-ai';
    const currentDateTime = getCurrentDateTime();
    chat.innerHTML += `<p class="msg ${p_class}">
      <span class="sender">${sender}:</span>
      ${message}
      <span class="date">${currentDateTime}</span>
    </p>`;
}

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + chatName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    renderMessage('AI Assistant', data.message)
    const typingAIText = document.querySelector('#typing-ai');
    typingAIText.remove();
    input.disabled = false;
    button.disabled = false;
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

input.focus();
input.onkeyup = function(e) {
    if (e.keyCode === 13) {
        button.click();
    }
};

button.onclick = function(e) {
    const message = input.value;
    if (message) {
        renderMessage(senderUsername, message);
        chatSocket.send(JSON.stringify({
            'message': message,
        }));
        input.value = '';
        chat.innerHTML += '<p id="typing-ai">AI is typing...</p>';
        input.disabled = true;
        button.disabled = true;
    }
};
