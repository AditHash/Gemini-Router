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

### Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start the backend services using Docker:
   ```bash
   docker-compose up --build
   ```

### Frontend
1. Install the required dependencies:
   ```bash
   npm i
   ```

2. Start the frontend in development mode:
   ```bash
   npm run dev
   ```

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
- Frontend integration
- Develop a `docker-compose.yaml` template to simplify deployment using Docker.
- Add more advanced features to the MCP framework, such as dynamic scaling and monitoring.
- Enhance the integration with Gemini APIs for improved performance and reliability.

## Notes
- Ensure that the `GEMINI_API_KEY` is valid and has the necessary permissions for the Gemini APIs.
- If you encounter any issues, check the logs for each server to debug the problem.

## Diagram
![MCP Architecture](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=mcp.drawio&dark=auto#R%3Cmxfile%3E%3Cdiagram%20name%3D%22Page-1%22%20id%3D%22XMl6Z2Mjh__lQdjCvQym%22%3E7Vpdc6I6GP41zpy9sEOI%2BHHpR9vTnXbWWWc%2FzmWEFHKKhAmx6v76k0iCBNDSLerqnJuWvCExPG%2BeJ08gLTherO8ZioMn6uGwZVveugUnLdu2O1ZH%2FJORTRoBDuimEZ8RT8V2gRn5hVXQUtEl8XBi3MgpDTmJzaBLowi73IghxujKvO2ZhuavxsjHpcDMRWE5%2BoN4PFBRYFm7ir8x8QP1031HVSyQvlkFkgB5dJULwdsWHDNKeXq1WI9xKNHTuKTt7vbUZgNjOOJ1Ggz5SxTB6ez%2B8%2BTz4%2BLbzxGZhW3opN28onCpnliNlm80BIwuIw%2FLXqwWHK0CwvEsRq6sXYmsi1jAF6EoAXGpusOM4%2FXegYLs8cXEwXSBOduIW1SDtq3BVZOmnaG9yqXA0lMkyMHfgyqIVN79rPsdNOJCofMOpOymkfJQEmzv1YUp4hyzSEZkv%2BJPI3DCApp2GcsM8DyUcHAsKPsl4LAnSKeKlPGA%2BjRC4e0uOjKh3d3zSGmsMPwXc75RCoKWnJpwC7TY5qdqvy38Iws3ji5O1vnKyUaV3CV7zdKUcMT4UMqKCLghShLi6vAdCStT%2BxzS1TAiQg8IjQyWyKc%2BnFQBEl0yFx8AU4siYj7mB%2B5zqicJw6EY2Ks5jsYzrlmZI8%2FTeFo5DR7RXKwhRupQSHyJnCvAwUwEJB%2BI0OihqlgQz0tnCU7ILzTf9ieTF1MS8e3DOKOWMzlEKLWAqMY72c7nZP9s3ss%2B68YaWAODgGpJrI286nsqn2XXsd01OoUdswP6%2FJyI%2BVBMXDbADwihVZm3I9PXoOEfQqneBym1bSrUBG1yN6gpuzfv7b4p507HKmQ57bHZnIMSf7%2FFIUXedVA458eqOQycgcnhdrcRErd7HbNbzerj07ic0XFI8HZwMyy4xj7mbhowLm3QKTqXChtoV1iX7rGcy%2BCsziUrHM%2B5VCmr4WYalFm7pszumSWncS5273qdy%2BAw%2FYTswY7pMvqNqF7HNkUPnk704LV7l9qkss%2FJKtApsWrEkPhVufgg5gbiYjh9uA6apZPuEM%2BsQd%2FkWdtphGiO2atzKprZpey27G7I5VpCXsWlLy%2B1y7CGulL8Vq6%2Boslf6eT4tK%2FBmQ0LLPiV7rntCjj%2FVu0PfGMCL8J39K%2FXd4DD2y0hiHbPAQaVQDOCWHQep5NE%2Fdnjep1HbVqd9U0kKPv5LzGOROQHRjxIF6SrcR7dg0QTxsMqGPxuMzxrQ2jS1zoZ0eC7vMeovvdQ8%2BNSzEf28uR87gOUQPn%2Fbclvy2vnIlzL4IpdyxtvK60b2O84pr8AH1NTTeVCi%2BOJZ3lbfkg8x%2FXF8ytOLmrrVvWV%2FMTqeZav5DWF75S%2B0qkpfI18jSs5mewUhP54WzwVkY5LtTrCvqGsqN%2BFfFGWf1Umf9W27oYPs9mVaO3hj%2BpSa0HhyxlsxriaG8R%2B71TKW3W6aL%2FyTt6hvMP7SxFdCM4tuuXN4SMVnJCIIzGNUYI1lHOWW9s8kmQsfKKRTyejrDz1U75%2BKsGdBCiWl%2B4mJAJ3Bt8GfZ5m6HGeBZD74m%2Fz9mXJRTdY63gq8MBpJlNda48K5jMFKzIFwNHWR7uUqwcpZZHiZxXSAV4jX65RoxgzIsYhlU9Hpzpkv52HZ7LG%2BrAqMNbdhqjRtU3A204F4FUHIPtHw7uWQmUvUWrK01cc04QIemxqatQFprJXsJZnT6U%2BZFLcpamDH0kJdPHw%2FHj2QbrQZJeAhDP6gsc0pDKjEZWaJrIUhoVQEwuQU9ivwXJqBhWZ%2BY1DxqK4O%2BqdmobdiXl4%2Bx8%3D%3C%2Fdiagram%3E%3C%2Fmxfile%3E)