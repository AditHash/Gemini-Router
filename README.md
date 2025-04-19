# 🚀 MCP Server using Gemini - `GeminiRouter`

## 🔍 About

This project is a working implementation of the **Model Context Protocol (MCP)** integrated with **Google's Gemini Flash 1.5 API**, designed to demonstrate how modular AI services can collaborate through a centralized router.

### 🧐 **What is MCP and How Does It Work Here?**

**Model Context Protocol (MCP)** is an architectural pattern designed to enable modular and context-aware communication between multiple specialized AI agents or services. This project applies MCP principles to build a scalable, intelligent AI system with dedicated microservices, all coordinated through a central router.

Each service (or "context")—whether for chat, web search, weather info, deep reasoning, or retrieval-augmented generation (RAG)—performs a distinct function and communicates via lightweight requests routed intelligently through a **Router/Client**.

---

### ↺ **Workflow Overview**

Here's how the system works from input to response:

1. **User Input**: The user sends a query from the frontend UI.

2. **Routing Logic**:
   - The **Router/Client** receives the query and analyzes the intent.
   - Based on keywords, context, or past interactions, it selects the appropriate server (chat, search, RAG, think, etc.) to handle the query.

3. **Service Handling**:
   - **Chat Server**: If the query is conversational or casual, it’s routed here for quick responses.
   - **Search Server**: For queries that need real-time or factual data (e.g., “What’s the capital of Sweden?”), the router invokes Gemini APIs via this module.
   - **RAG Server**: For complex questions needing document-based or external knowledge synthesis, the RAG module uses a retrieval layer + Gemini for answer generation.
   - **Thinking Server**: For logical reasoning or multi-step problem solving, the query is handed over here for deep thought processing.
   - **Weather (via Search)**: The Search server also integrates with the OpenWeather API to handle natural language weather queries like "What's the weather in Tokyo?"

4. **Response Aggregation**:
   - The chosen module processes the request and sends a response back to the **Router**.
   - The Router can optionally combine responses from multiple modules if the query requires it (e.g., a response that includes weather + a suggestion).

5. **Frontend Output**: The final response is returned to the user interface and presented in a clean, conversational format.

---

## 🚀 Features

- **Modular AI Services**: Each function (chat, search, RAG, think) runs independently as a microservice.
- **Centralized Context Router**: Handles request dispatching, context management, and coordination between services.
- **Gemini Flash 1.5**: High-performance model for reasoning, generation, and information retrieval.
- **OpenWeather Integration**: Real-time weather data included in the search context.
- **Dockerized Backend**: Easily deploy all services in isolation or as a single stack using Docker.

---

## ⚙️ Prerequisites

- Python 3.12+
- Node.js & npm
- Docker & Docker Compose
- Environment variables configured in `.env`

```dotenv
GEMINI_API_KEY=<your_gemini_api_key>
OPENWEATHER_API_KEY=<your_openweather_api_key>
```

---

## 🧱 Architecture
![MCP Architecture](mcp2transparent.drawio.svg)

---

## 🛠️ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/AditHash/gemini-mcp-router.git
cd gemini-mcp-router
```

### 2. Start the Backend
```bash
cd backend
docker-compose up --build
```

### 3. Start the Frontend
```bash
npm install
npm run dev
```

---

## 🗂️ Project Structure

```plaintext
backend/
│
├── chat/           # Chat server (basic conversation handling)
├── search/         # Web search & weather functionality
├── rag/            # Retrieval-Augmented Generation logic
├── think/          # Deep reasoning and logic module
├── router/         # Central request dispatcher and router
│
├── requirements.txt
└── .env            # API keys for Gemini and OpenWeather

```

---

## 📈 Future Plans

- ⚙️ Integrate frontend into Docker-compose setup
- 🎨 Improve UI with modern components and chat UX
- 📊 Add real-time monitoring & logs for each service
- 🤖 Extend MCP with dynamic memory and agent-based reasoning
- ↺ Build support for auto-scaling and horizontal load distribution

---

## 📝 Notes

- Ensure valid API keys in `.env` for Gemini and OpenWeather services.
- Use `docker logs <container_name>` to debug any backend issues.

