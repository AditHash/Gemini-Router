import React, { useState } from "react";
import { FaPaperPlane, FaFileUpload } from "react-icons/fa";
import "./ChatFooter.css";

function ChatFooter({ onSendMessage, onFileUpload, loading }) {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (message.trim()) {
      onSendMessage(message);
      setMessage("");
    }
  };

  return (
    <div className="chat-footer">
      <input
        type="file"
        accept="application/pdf"
        onChange={onFileUpload}
        className="upload-icon"
        style={{ display: "none" }}
        id="file-upload"
      />
      <label htmlFor="file-upload" className="upload-icon-label">
        <FaFileUpload />
      </label>
      <input
        type="text"
        className="message-input"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message here..."
      />
      <button
        className="send-icon"
        onClick={handleSend}
        disabled={loading}
      >
        <FaPaperPlane />
      </button>
    </div>
  );
}

export default ChatFooter;