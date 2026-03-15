FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && \
    uv pip install --system -e .

# Copy application code
COPY . .

# Expose port
ENV MCP_SERVER_PORT=8000
EXPOSE ${MCP_SERVER_PORT}

# Run the application in HTTP mode with OAuth
CMD ["python", "main.py", "--transport", "http"]