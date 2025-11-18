import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage, getWeather, getMarketPrice } from '../services/api';
import ChatMessage from '../components/ChatMessage';
import InputBox from '../components/InputBox';
import '../styles/ChatPage.css';

function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: 'Dumela! Welcome to the Agriculture Extension Chatbot.\n\nI\'m here to help with:\n• Crop advice\n• Weather alerts\n• Market prices\n• Pest information\n\nWhat can I help you with today?',
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState('english');
  const [farmerId, setFarmerId] = useState(1);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      sender: 'user',
      text: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await sendChatMessage(
        farmerId,
        inputValue,
        'web',
        language
      );

      const botMessage = {
        id: messages.length + 2,
        sender: 'bot',
        text: response.data.response,
        timestamp: new Date(),
        tokensUsed: response.data.tokens_used,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: messages.length + 2,
        sender: 'bot',
        text: 'Sorry, there was an error processing your request. Please try again.',
        timestamp: new Date(),
        isError: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-page">
      <div className="chat-header">
        <div className="header-content">
          <h1>🌾 Agriculture Extension Chatbot</h1>
          <p>Supporting Sustainable Farming in Lesotho</p>
        </div>
        <div className="header-controls">
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="language-select"
          >
            <option value="english">English</option>
            <option value="sesotho">Sesotho</option>
          </select>
        </div>
      </div>

      <div className="chat-container">
        <div className="messages-container">
          {messages.map((msg) => (
            <ChatMessage key={msg.id} message={msg} />
          ))}
          {loading && <div className="typing-indicator">Bot is typing...</div>}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSendMessage} className="input-form">
          <InputBox
            value={inputValue}
            onChange={setInputValue}
            disabled={loading}
            placeholder="Ask about crops, weather, prices, or pests..."
          />
          <button
            type="submit"
            disabled={loading || !inputValue.trim()}
            className="send-button"
          >
            {loading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default ChatPage;
