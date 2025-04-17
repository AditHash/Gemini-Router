import React from "react";
import { FaPlus } from "react-icons/fa";
import "./ChatHeader.css";

function ChatHeader({ onNewChat }) {
  return (
    <div className="chat-header">
      MCP Chatbot
      <button className="new-chat-icon" onClick={onNewChat}>
        <FaPlus />
      </button>
    </div>
  );
}

export default ChatHeader;