#!/bin/bash

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python is not installed. Installing Python 3.12..."
    # Adjust the following commands based on your OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update
        sudo apt install -y python3.12 python3.12-venv python3.12-distutils
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python@3.12
    else
        echo "Unsupported OS. Please install Python 3.12 manually."
        exit 1
    fi
fi

# Ensure python3-venv is installed
if ! dpkg -l | grep -q python3.12-venv; then
    echo "python3-venv is not installed. Installing python3.12-venv..."
    sudo apt install -y python3.12-venv
fi

# Create and activate a virtual environment
echo "Setting up virtual environment..."
python3.12 -m venv venv
if [ ! -d "venv" ]; then
    echo "Failed to create virtual environment. Exiting..."
    exit 1
fi
source venv/bin/activate

# Ensure pip is installed
if ! command -v pip &>/dev/null; then
    echo "pip is not installed. Installing pip..."
    python3.12 -m ensurepip --upgrade
    pip install --upgrade pip
fi

# Install dependencies
echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

# Load environment variables from .env file
if [ -f ".env" ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found. Please create one with the required environment variables."
    exit 1
fi

# Start the servers
echo "Starting servers..."
uvicorn chat.1_chat_server:app --host 0.0.0.0 --port 8001 &
uvicorn rag.4_rag_server:app --host 0.0.0.0 --port 8004 &
uvicorn search.2_search_server:app --host 0.0.0.0 --port 8002 &
uvicorn think.3_thinking_server:app --host 0.0.0.0 --port 8003 &
uvicorn router.0_mcp_router_true:app --host 0.0.0.0 --port 8000
