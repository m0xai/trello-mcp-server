FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir \
    "mcp[cli]>=1.6.0" \
    "httpx>=0.28.1" \
    "uvicorn>=0.30.0" \
    "starlette>=0.37.0" \
    "python-dotenv>=1.0.0"

# Copy application code
COPY . .

# Run the application in HTTP mode with OAuth
CMD ["python", "main.py", "--transport", "http"]
