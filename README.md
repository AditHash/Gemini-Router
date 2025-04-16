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
- A valid `GEMINI_API_KEY` is required and should be set in the `.env` file.

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/AditHash/gemini-mcp-server-chatbot.git
   cd MCP-prod2
   ```

2. Set up the `.env` file with your Gemini API key:
   ```properties
   GEMINI_API_KEY=your_gemini_api_key
   ```

3. Run the `install.sh` script to set up the environment and start the servers:
   ```bash
   ./install.sh
   ```

   This script will:
   - Check if Python 3.12 is installed and install it if necessary.
   - Create and activate a virtual environment.
   - Install the required dependencies from `requirements.txt`.
   - Start all the servers:
     - Chat Server: `http://0.0.0.0:8001`
     - RAG Server: `http://0.0.0.0:8004`
     - Search Server: `http://0.0.0.0:8002`
     - Thinking Server: `http://0.0.0.0:8003`
     - Router: `http://0.0.0.0:8000`

## Project Structure
- **chat/**: Contains the chat server implementation.
- **search/**: Contains the search server implementation.
- **rag/**: Contains the RAG server implementation.
- **think/**: Contains the thinking server implementation.
- **router/**: Contains the router server implementation.
- **install.sh**: Script to set up the environment and start the servers.
- **requirements.txt**: Lists the Python dependencies for the project.
- **.env**: Stores environment variables, including the `GEMINI_API_KEY`.

## Future Plans
- Develop a `docker-compose.yaml` template to simplify deployment using Docker.
- Add more advanced features to the MCP framework, such as dynamic scaling and monitoring.
- Enhance the integration with Gemini APIs for improved performance and reliability.

## Notes
- Ensure that the `GEMINI_API_KEY` is valid and has the necessary permissions for the Gemini APIs.
- If you encounter any issues, check the logs for each server to debug the problem.
