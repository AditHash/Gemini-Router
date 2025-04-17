import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import { v4 as uuidv4 } from "uuid";

function App() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(uuidv4()); // Initialize with a unique session ID

  const handleNewChat = () => {
    setSessionId(uuidv4()); // Generate a new unique session ID
    setChatHistory([]); // Clear chat history for the new session
  };

  const handleSendMessage = async () => {
    if (!message.trim()) {
      alert("Please enter a message.");
      return;
    }

    const newMessage = { role: "user", content: message };
    setChatHistory((prev) => [...prev, newMessage]);
    setMessage("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId, // Use the current session ID
          message: message,
        }),
      });
      const data = await res.json();
      const botResponse = {
        role: "bot",
        content: JSON.stringify(data, null, 2), // Return raw response
      };
      setChatHistory((prev) => [...prev, botResponse]);
    } catch (error) {
      const errorMessage = { role: "bot", content: `Error: ${error.message}` };
      setChatHistory((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      await fetch("http://localhost:8004/upload", {
        method: "POST",
        body: formData,
      });
      alert("PDF uploaded successfully.");
    } catch (error) {
      alert(`Error uploading PDF: ${error.message}`);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        MCP Chatbot
        <button className="new-chat-button" onClick={handleNewChat}>
          New Chat
        </button>
      </div>
      <div className="chat-body">
        {chatHistory.map((chat, index) => (
          <div
            key={index}
            className={`chat-message ${chat.role === "user" ? "user-message" : "bot-message"}`}
          >
            {chat.content}
          </div>
        ))}
      </div>
      <div className="chat-footer">
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileUpload}
          className="upload-button"
        />
        <input
          type="text"
          className="message-input"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message here..."
        />
        <button
          className="send-button"
          onClick={handleSendMessage}
          disabled={loading}
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;
