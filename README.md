# MCP-server-using-Gemini

## About
This project is a working implementation of the **Model Context Protocol (MCP)**, showcasing its integration with **Gemini APIs**. The architecture consists of multiple servers, each handling specific functionalities such as chat, search, retrieval-augmented generation (RAG), and more. The project demonstrates how different services can work together seamlessly using the MCP framework.

## Features
- **Chat Server**: Handles conversational interactions.
- **Search Server**: Provides search capabilities using Gemini APIs.
- **RAG Server**: Implements retrieval-augmented generation for enhanced responses.
- **Thinking Server**: Processes complex logic and reasoning tasks.
- **Router**: Acts as the central hub, routing requests to the appropriate servers.

## Prerequisites
- Python 3.12 or higher must be installed on your system.
- Ensure the `pip` package manager is available.
- A valid `.env` file must be created in the `backend` directory with the following content:
  ```properties
  GEMINI_API_KEY=<your_gemini_api_key>
  OPENWEATHER_API_KEY=<your_openweather_api_key>
  ```
  Replace `<your_gemini_api_key>` and `<your_openweather_api_key>` with your actual API keys.

## How to Run

### Clone the Repository
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/AditHash/gemini-mcp-router.git
   cd gemini-mcp-router
   ```

### Backend
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```

3. Start the backend services using Docker:
   ```bash
   docker-compose up --build
   ```

### Frontend
4. Install the required dependencies:
   ```bash
   npm install
   ```

5. Start the frontend in development mode:
   ```bash
   npm run dev
   ```

## Project Structure
- **chat/**: Contains the chat server implementation.
- **search/**: Contains the search server implementation.
- **rag/**: Contains the RAG server implementation.
- **think/**: Contains the thinking server implementation.
- **router/**: Contains the router server implementation.

- **requirements.txt**: Lists the Python dependencies for the project.
- **.env**: Stores environment variables, including the `GEMINI_API_KEY`.

## Future Plans
- Frontend integration
- Develop a `docker-compose.yaml` template to simplify deployment using Docker.
- Add more advanced features to the MCP framework, such as dynamic scaling and monitoring.
- Enhance the integration with Gemini APIs for improved performance and reliability.

## Notes
- Ensure that the `GEMINI_API_KEY` is valid and has the necessary permissions for the Gemini APIs.
- If you encounter any issues, check the logs for each server to debug the problem.

## Diagram
![MCP Architecture](mcp.drawio.svg)