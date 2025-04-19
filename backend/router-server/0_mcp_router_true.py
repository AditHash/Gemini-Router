# # ✅ MCP router server – (Gemini Flash 1.5)

# === Imports ===
import json
import requests
import os
import hashlib
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

# === Configure Gemini ===
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
router_model = genai.GenerativeModel("gemini-1.5-flash")
chat_model = genai.GenerativeModel("gemini-1.5-flash")  # Use the same model for chat

# === Load Tool Endpoint Config ===
with open("config.json") as f:
    endpoint_config = json.load(f)

# === FastAPI App ===
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Tool Definitions (Descriptions + Dynamic Endpoints) ===
TOOLS = [
    {
        "name": "chat",
        "description": "General-purpose conversation with memory and prior context.",
        "endpoint": endpoint_config["chat"],
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
                "message": {"type": "string"}
            },
            "required": ["session_id", "message"]
        }
    },
    {
        "name": "search",
        "description": "Real-time web search using DuckDuckGo.",
        "endpoint": endpoint_config["search"],
        "parameters": {
            "type": "object",
            "properties": {
                "q": {"type": "string"}
            },
            "required": ["q"]
        }
    },
    {
        "name": "think",
        "description": "For deep thinking and reasoning about complex tasks.",
        "endpoint": endpoint_config["think"],
        "parameters": {
            "type": "object",
            "properties": {
                "task": {"type": "string"}
            },
            "required": ["task"]
        }
    },
    {
        "name": "query",
        "description": "Question answering over user-uploaded documents (RAG).",
        "endpoint": endpoint_config["query"],
        "parameters": {
            "type": "object",
            "properties": {
                "question": {"type": "string"}
            },
            "required": ["question"]
        }
    },
    {
        "name": "weather",
        "description": "Get current weather information for a specified location.",
        "endpoint": endpoint_config["weather"],
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "rag",
        "description": "Retrieve answers from uploaded documents.",
        "endpoint": endpoint_config["rag"],
        "parameters": {
            "type": "object",
            "properties": {
                "question": {"type": "string"}
            },
            "required": ["question"]
        }
    }
]

# === Session and Cache Stores ===
session_memory: Dict[str, list] = {}
tool_cache: Dict[str, Any] = {}

# === Input Model ===
class UserQuery(BaseModel):
    session_id: str
    message: str

# === Prompt Builder ===
def build_router_prompt(session_id: str, user_query: str):
    history = session_memory.get(session_id, [])
    history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history])

    tool_descriptions = "\n\n".join([
        f"Tool: {tool['name']}\nDescription: {tool['description']}\nParams: {json.dumps(tool['parameters']['properties'])}"
        for tool in TOOLS
    ])

    return f"""
You are an intelligent tool router for an AI system.

Available tools:
{tool_descriptions}

Conversation history:
{history_text}

User query: "{user_query}"

Respond in JSON only:
{{
  "tool": "tool_name",
  "parameters": {{...}} | null,
  "confidence": "high | medium | low"
}}
"""

# === POST /ask ===
@app.post("/ask")
def ask_router(req: UserQuery):
    history = session_memory.setdefault(req.session_id, [])
    history.append({"role": "user", "content": req.message})

    # Caching
    cache_key = hashlib.sha256(f"{req.session_id}:{req.message}".encode()).hexdigest()
    if cache_key in tool_cache:
        return {
            "status": "success",
            "cached": True,
            "data": tool_cache[cache_key]
        }

    # Ask the router model
    prompt = build_router_prompt(req.session_id, req.message)
    response = router_model.generate_content(prompt)

    # === Clean LLM output from markdown-style triple backticks ===
    raw_response = response.text.strip()
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw_response, flags=re.IGNORECASE | re.MULTILINE).strip()

    try:
        tool_call = json.loads(cleaned)
    except Exception:
        return {
            "status": "error",
            "message": "Failed to parse LLM output.",
            "raw_response": raw_response
        }

    tool_name = tool_call.get("tool")
    params = tool_call.get("parameters", {})
    confidence = tool_call.get("confidence", "unknown")

    # Handle general chat internally
    if tool_name == "chat" or tool_name is None:
        chat_response = handle_general_chat(req.session_id, req.message)
        return {
            "status": "success",
            "cached": False,
            "data": {
                "tool_used": "chat",
                "confidence": "high",
                "reply": chat_response
            }
        }

    # Handle external tool calls
    tool = next((t for t in TOOLS if t["name"] == tool_name), None)
    if not tool:
        return {
            "status": "error",
            "message": f"Tool '{tool_name}' not found."
        }

    if "session_id" in tool["parameters"]["properties"]:
        params["session_id"] = req.session_id

    # Tool Call
    try:
        res = requests.post(tool["endpoint"], json=params)
        res.raise_for_status()
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to call tool '{tool_name}'",
            "details": str(e)
        }

    reply = res.json()
    history.append({"role": "tool", "content": str(reply)})

    tool_cache[cache_key] = {
        "tool_used": tool_name,
        "parameters": params,
        "confidence": confidence,
        "reply": reply
    }

    return {
        "status": "success",
        "cached": False,
        "data": {
            "tool_used": tool_name,
            "confidence": confidence,
            "parameters": params,
            "reply": reply
        }
    }

def handle_general_chat(session_id: str, message: str):
    """
    Handle general chat internally using the chat model.
    """
    history = session_memory.get(session_id, [])
    history.append({"role": "user", "content": message})

    response = chat_model.generate_content(history)
    reply = response.text
    history.append({"role": "model", "content": reply})

    session_memory[session_id] = history
    return reply
