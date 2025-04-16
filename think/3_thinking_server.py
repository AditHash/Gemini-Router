# ✅ MCP Server 3 – Deep Thinking / Agentic Reasoning using Gemini Flash 1.5
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai  # updated import
import os

# Correct way to configure the API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

class ThinkRequest(BaseModel):
    task: str

@app.post("/think")
def think(req: ThinkRequest):
    system_prompt = "You are an expert reasoning agent. Break down the task step-by-step."
    response = model.generate_content([{"role": "user", "parts": [system_prompt + "\n" + req.task]}])
    return {"thoughts": response.text}