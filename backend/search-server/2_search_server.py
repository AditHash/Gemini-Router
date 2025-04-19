# # ✅ MCP Server 2 – DuckDuckGo Search + Gemini Flash 1.5

from fastapi import FastAPI
from pydantic import BaseModel
from duckduckgo_search import DDGS
import google.generativeai as genai  # Gemini SDK
import os

app = FastAPI()

# Set your Gemini API Key here (use environment variable ideally)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class Query(BaseModel):
    q: str

@app.post("/search")
def grounded_response(query: Query):
    # Step 1: Get search results from DuckDuckGo
    with DDGS() as ddgs:
        raw_results = ddgs.text(query.q, max_results=5)

    # Format sources for grounding
    sources = []
    context_chunks = []
    for result in raw_results:
        title = result.get("title", "")
        snippet = result.get("body", "")
        url = result.get("href", "")
        context_chunks.append(f"{title}\n{snippet}\nSource: {url}")
        sources.append(url)

    # Prepare context for Gemini
    context = "\n\n---\n\n".join(context_chunks)

    # Step 2: Ask Gemini to generate a grounded answer
    prompt = (
        f"Based on the following search results, answer the question: \"{query.q}\".\n\n"
        f"Use the information provided, and cite the sources in your response using the URLs.\n\n"
        f"{context}"
    )

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return {
        "question": query.q,
        "answer": response.text,
        "sources": sources
    }
