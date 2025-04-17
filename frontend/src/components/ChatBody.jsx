import React from "react";
import "./ChatBody.css";

function ChatBody({ chatHistory = [] }) {
  return (
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
  );
}

export default ChatBody;