import React from 'react';
import '../styles/ChatMessage.css';

function ChatMessage({ message }) {
  const isBot = message.sender === 'bot';

  return (
    <div className={`message-wrapper ${isBot ? 'bot' : 'user'}`}>
      <div className={`message ${isBot ? 'bot-message' : 'user-message'} ${message.isError ? 'error' : ''}`}>
        <p>{message.text}</p>
        {message.tokensUsed && (
          <small className="tokens-info">Tokens used: {message.tokensUsed}</small>
        )}
        <small className="timestamp">
          {message.timestamp.toLocaleTimeString()}
        </small>
      </div>
    </div>
  );
}

export default ChatMessage;
