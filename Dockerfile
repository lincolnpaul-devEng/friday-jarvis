# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agent.py .
COPY tools.py .
COPY prompts.py .

# Set environment variables (will be overridden by Cloud Run)
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Run the agent
CMD ["python", "-m", "livekit.agents", "agent"]
