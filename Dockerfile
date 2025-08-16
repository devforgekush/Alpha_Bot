FROM python:3.11-slim

# Install only essential system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install requirements (try basic if working fails)
COPY requirements-working.txt .
COPY requirements-basic.txt .

# Try to install requirements, fallback to basic if needed
RUN pip3 install --no-cache-dir -r requirements-working.txt || \
    pip3 install --no-cache-dir -r requirements-basic.txt

# Copy app
COPY . .

# Ensure config.py is in the right place and accessible
RUN ls -la /app/ && \
    echo "Checking if config.py exists:" && \
    ls -la /app/config.py || echo "config.py not found in /app/"

# Create downloads directory
RUN mkdir -p downloads

# Set Python path explicitly
ENV PYTHONPATH=/app

# Make start script executable
RUN chmod +x start_simple.py

# Expose port
EXPOSE 8000

# Start the application
CMD ["python3", "start_simple.py"]
