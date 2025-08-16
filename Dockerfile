FROM python:3.11-slim

# Install only essential system dependencies (avoid ffmpeg here to prevent OOM in limited builders)
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUTF8=1
ENV PYTHONUNBUFFERED=1
ARG ENABLE_VOICE=false
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# If voice support is requested, install additional build tools needed by
# native extensions used by voice packages (this keeps default images small).
RUN if [ "$ENABLE_VOICE" = "true" ] ; then \
        apt-get update && apt-get install -y --no-install-recommends \
            build-essential \
            libffi-dev \
            libsndfile1 \
            pkg-config \
            ffmpeg \
        && apt-get clean && rm -rf /var/lib/apt/lists/* ; fi

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
COPY requirements-voice.txt .


# Ensure compatible motor and pymongo versions are installed first
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel
RUN pip3 uninstall -y motor pymongo || true
RUN pip3 install --no-cache-dir motor==3.1.2 pymongo==4.3.3

# Install a lightweight ffmpeg runtime via pip (imageio-ffmpeg provides a static ffmpeg binary)
RUN pip3 install --no-cache-dir imageio-ffmpeg

# Install Python requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Install optional voice requirements when ENABLE_VOICE is true
RUN if [ "$ENABLE_VOICE" = "true" ] && [ -f requirements-voice.txt ] ; then pip3 install --no-cache-dir -r requirements-voice.txt ; fi

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
