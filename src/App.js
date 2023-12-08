import React, { useState, useEffect, useRef } from 'react';
import './App.css'; // Make sure your CSS matches the provided styles

function App() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async () => {
    if (message.trim() === '') return;
    const newMessage = { text: message, sender: 'user' };
    setMessages([...messages, newMessage]);

    // Send message to Flask backend
    const response = await fetch('http://127.0.0.1:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: message }),
    });
    const data = await response.json();

    // Add response from Flask to messages
    const botMessage = { text: "Received audio", sender: 'bot', audioUrl: data.audioUrl };
    setMessages(messages => [...messages, botMessage]);

    setMessage('');
  };

  return (
    <div className="chat">
      <div className="chat-title">
        <h1>Samantha Ruth prabhu</h1>
        <h2>🥵</h2>
        <figure className="avatar">
          <img src="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwallpapers.com%2Fsamantha-hd&psig=AOvVaw2TMesz3p6tnE-U1uYHMkBc&ust=1701926830046000&source=images&cd=vfe&ved=0CBIQjRxqFwoTCID09NKJ-oIDFQAAAAAdAAAAABAE.jpg" alt="avatar" />
        </figure>
      </div>
      <div className="messages">
        <div className="messages-content">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender === 'user' ? 'message-personal' : ''}`}>
              {msg.sender === 'bot' && <audio controls src={msg.audioUrl} />}
              {msg.text}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <div className="message-box">
        <textarea 
          className="message-input" 
          placeholder="Type message..." 
          value={message}
          onChange={e => setMessage(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && sendMessage()}
        ></textarea>
        <button className="message-submit" onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
