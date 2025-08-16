FROM python:3.11-slim

# Install only essential system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install requirements (try working, then basic, then flexible)
COPY requirements-working.txt .
COPY requirements-basic.txt .
COPY requirements-flexible.txt .


# Ensure compatible motor and pymongo versions are installed first
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel
RUN pip3 uninstall -y motor pymongo || true
RUN pip3 install --no-cache-dir motor==3.1.2 pymongo==3.12.3

# Then install requirements with multiple fallbacks
RUN pip3 install --no-cache-dir -r requirements-working.txt || \
    pip3 install --no-cache-dir -r requirements-basic.txt || \
    pip3 install --no-cache-dir -r requirements-flexible.txt

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
