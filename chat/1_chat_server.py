# ✅ MCP Server 1 – Chat + Memory (Gemini Flash 1.5)

from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# Configure the API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()
memory_store = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    history = memory_store.get(req.session_id, [])
    history.append({"role": "user", "parts": [req.message]})

    response = model.generate_content(history)
    reply = response.text
    history.append({"role": "model", "parts": [reply]})

    memory_store[req.session_id] = history
    return {"reply": reply}
