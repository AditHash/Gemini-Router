# dockerfile for general chat server
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the ports for the servers
EXPOSE 8000

CMD ["uvicorn", "0_mcp_router_true:app", "--host", "0.0.0.0", "--port", "8000"]
