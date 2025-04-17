import React, { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import ChatHeader from "./components/ChatHeader";
import ChatBody from "./components/ChatBody";
import ChatFooter from "./components/ChatFooter";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(uuidv4());

  const handleSendMessage = async (message) => {
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
          session_id: sessionId,
          message: message,
        }),
      });
      const data = await res.json();
      const botResponse = {
        role: "bot",
        content: JSON.stringify(data, null, 2),
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
    if (!file) {
      alert("No file selected.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8004/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        alert("PDF uploaded successfully.");
      } else {
        const errorData = await response.json();
        alert(`Error uploading PDF: ${errorData.message || response.statusText}`);
      }
    } catch (error) {
      alert(`Error uploading PDF: ${error.message}`);
    }
  };

  return (
    <div className="chat-container">
      <ChatHeader onNewChat={() => {
        setSessionId(uuidv4());
        setChatHistory([]);
      }} />
      <ChatBody chatHistory={chatHistory} />
      <ChatFooter
        onSendMessage={handleSendMessage}
        onFileUpload={handleFileUpload}
        loading={loading}
      />
    </div>
  );
}

export default App;
