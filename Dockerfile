FROM python:3.11-slim

# Install only essential system dependencies (avoid ffmpeg here to prevent OOM in limited builders)
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .


# Ensure compatible motor and pymongo versions are installed first
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel
RUN pip3 uninstall -y motor pymongo || true
RUN pip3 install --no-cache-dir motor==3.1.2 pymongo==4.3.3

# Install a lightweight ffmpeg runtime via pip (imageio-ffmpeg provides a static ffmpeg binary)
RUN pip3 install --no-cache-dir imageio-ffmpeg

# Install Python requirements
RUN pip3 install --no-cache-dir -r requirements.txt

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

# Make start scripts executable
RUN chmod +x start start_simple.py

# Expose port
EXPOSE 8000

# Start the application using the simple start wrapper
CMD ["bash", "start"]
