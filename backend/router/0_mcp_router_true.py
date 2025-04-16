# # ✅ MCP router server – (Gemini Flash 1.5)

# === Imports ===
import json
import requests
import os
import hashlib
import re
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import google.generativeai as genai

# === Configure Gemini ===
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
router_model = genai.GenerativeModel("gemini-1.5-flash")

# === Load Tool Endpoint Config ===
with open("config.json") as f:
    endpoint_config = json.load(f)

# === FastAPI App ===
app = FastAPI()

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
  "parameters": {{...}},
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
            "tool_used": tool_cache[cache_key]["tool"],
            "cached": True,
            "confidence": tool_cache[cache_key]["confidence"],
            "reply": tool_cache[cache_key]["reply"]
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
        return {"error": "Failed to parse LLM output.", "raw": raw_response}

    tool_name = tool_call.get("tool")
    params = tool_call.get("parameters", {})
    confidence = tool_call.get("confidence", "unknown")

    tool = next((t for t in TOOLS if t["name"] == tool_name), None)
    if not tool:
        return {"error": f"Tool '{tool_name}' not found."}

    if "session_id" in tool["parameters"]["properties"]:
        params["session_id"] = req.session_id

    # Tool Call
    try:
        res = requests.post(tool["endpoint"], json=params)
        res.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to call tool '{tool_name}'", "details": str(e)}

    reply = res.json()
    history.append({"role": "tool", "content": str(reply)})

    tool_cache[cache_key] = {
        "tool": tool_name,
        "parameters": params,
        "confidence": confidence,
        "reply": reply
    }

    return {
        "tool_used": tool_name,
        "confidence": confidence,
        "parameters": params,
        "reply": reply
    }
