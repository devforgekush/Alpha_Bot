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

# Create downloads directory
RUN mkdir -p downloads

# Expose port
EXPOSE 8000

# Start the application
CMD ["bash", "start"]
